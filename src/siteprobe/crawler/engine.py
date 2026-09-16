import asyncio
import time
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, urljoin
import httpx
from siteprobe.crawler.extractors import extract_page_data
from siteprobe.crawler.robots import RobotsParser
from siteprobe.crawler.sitemap import SitemapParser
from siteprobe.crawler.storage import CrawlStorage
from siteprobe.models.config import CrawlConfig
from siteprobe.models.crawl import CrawlPage, CrawlSummary, RedirectHop
from siteprobe.utils.url_helper import is_same_domain, normalize_url, is_valid_http_url


class AsyncCrawler:
    """Async polite crawler with SQLite storage, rate limiting, and adaptive backoff."""

    def __init__(self, start_url: str, config: Optional[CrawlConfig] = None, storage: Optional[CrawlStorage] = None):
        self.start_url = normalize_url(start_url)
        self.config = config or CrawlConfig()
        self.storage = storage or CrawlStorage()
        self.robots: Optional[RobotsParser] = None
        self.sitemap_urls: List[str] = []
        self.visited_urls: Set[str] = set()
        self.redirect_map: Dict[str, List[RedirectHop]] = {}
        self._delay_seconds = self.config.crawl_delay_ms / 1000.0
        self._consecutive_errors = 0

    async def crawl(self) -> CrawlSummary:
        start_time = time.time()
        await self.storage.initialize()

        limits = httpx.Limits(max_keepalive_connections=self.config.concurrency, max_connections=self.config.concurrency * 2)
        headers = {"User-Agent": self.config.user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

        async with httpx.AsyncClient(headers=headers, limits=limits, timeout=self.config.timeout_seconds, follow_redirects=False) as client:
            # 1. Fetch robots.txt
            await self._fetch_robots(client)

            # 2. Fetch sitemap.xml
            await self._fetch_sitemaps(client)

            # 3. Setup queue
            queue: asyncio.Queue = asyncio.Queue()
            await queue.put((self.start_url, 0))
            self.visited_urls.add(self.start_url)

            # Enqueue discovered sitemap URLs
            for s_url in self.sitemap_urls:
                norm_s = normalize_url(s_url)
                if is_same_domain(self.start_url, norm_s) and norm_s not in self.visited_urls:
                    if len(self.visited_urls) < self.config.max_pages:
                        self.visited_urls.add(norm_s)
                        await queue.put((norm_s, 1))

            semaphore = asyncio.Semaphore(self.config.concurrency)
            active_tasks = set()
            pages_crawled = 0

            while (not queue.empty() or active_tasks) and pages_crawled < self.config.max_pages:
                while not queue.empty() and pages_crawled + len(active_tasks) < self.config.max_pages:
                    url, depth = await queue.get()

                    # Check robots.txt
                    parsed_path = urlparse(url).path or "/"
                    if self.config.respect_robots and self.robots and not self.robots.is_allowed("SiteProbe", parsed_path):
                        queue.task_done()
                        continue

                    task = asyncio.create_task(self._crawl_single(client, url, depth, semaphore, queue))
                    active_tasks.add(task)
                    task.add_done_callback(lambda t: queue.task_done())

                if not active_tasks:
                    break

                done, active_tasks = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)
                pages_crawled += len(done)

            # Wait for remaining active tasks
            if active_tasks:
                await asyncio.gather(*active_tasks, return_exceptions=True)

        duration = time.time() - start_time
        all_pages = await self.storage.get_all_pages()
        status_counts: Dict[str, int] = {}
        for p in all_pages:
            code_str = str(p.status_code)
            status_counts[code_str] = status_counts.get(code_str, 0) + 1

        return CrawlSummary(
            start_url=self.start_url,
            total_crawled=len(all_pages),
            total_internal_discovered=len(self.visited_urls),
            total_external_discovered=0,
            broken_links_count=sum(1 for p in all_pages if p.status_code >= 400),
            crawl_duration_seconds=round(duration, 2),
            status_codes_distribution=status_counts,
        )

    async def _fetch_robots(self, client: httpx.AsyncClient) -> None:
        parsed = urlparse(self.start_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            resp = await client.get(robots_url, timeout=5.0)
            if resp.status_code == 200:
                self.robots = RobotsParser(resp.text)
            else:
                self.robots = RobotsParser("")
        except Exception:
            self.robots = RobotsParser("")

    async def _fetch_sitemaps(self, client: httpx.AsyncClient) -> None:
        declared_sitemaps = self.robots.sitemaps if self.robots else []
        parsed = urlparse(self.start_url)
        default_sitemap = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        if default_sitemap not in declared_sitemaps:
            declared_sitemaps.append(default_sitemap)

        for sm_url in declared_sitemaps:
            found = await SitemapParser.fetch_sitemap_urls(sm_url, client)
            self.sitemap_urls.extend(found)
        self.sitemap_urls = list(dict.fromkeys(self.sitemap_urls))

    async def _crawl_single(self, client: httpx.AsyncClient, url: str, depth: int, semaphore: asyncio.Semaphore, queue: asyncio.Queue) -> None:
        async with semaphore:
            # Polite delay & adaptive backoff
            await asyncio.sleep(self._delay_seconds)

            current_url = url
            redirect_hops: List[RedirectHop] = []
            max_hops = 6
            response = None

            t0 = time.time()
            try:
                for _ in range(max_hops):
                    resp = await client.get(current_url)
                    redirect_hops.append(RedirectHop(url=current_url, status_code=resp.status_code))
                    if resp.is_redirect and "location" in resp.headers:
                        loc = resp.headers["location"]
                        next_url = normalize_url(urljoin(current_url, loc))
                        current_url = next_url
                    else:
                        response = resp
                        break
            except Exception as e:
                resp_time = (time.time() - t0) * 1000
                error_page = CrawlPage(
                    url=url,
                    status_code=0,
                    content_type="error/connection-failure",
                    html=f"<!-- Error: {str(e)} -->",
                    response_time_ms=resp_time,
                    depth=depth,
                    is_indexable=False,
                )
                await self.storage.save_page(error_page)
                self._consecutive_errors += 1
                if self._consecutive_errors > 3:
                    self._delay_seconds = min(self._delay_seconds * 1.5, 3.0)
                return

            resp_time = (time.time() - t0) * 1000

            if response is None:
                return

            if response.status_code in (429, 503):
                self._consecutive_errors += 1
                self._delay_seconds = min(self._delay_seconds * 2.0, 5.0)
            else:
                self._consecutive_errors = max(0, self._consecutive_errors - 1)

            html_text = response.text if "text/html" in response.headers.get("content-type", "") or response.text.startswith("<") else ""
            dict_headers = dict(response.headers.items())

            page_data = extract_page_data(
                url=current_url,
                html=html_text,
                status_code=response.status_code,
                headers=dict_headers,
                response_time_ms=resp_time,
                depth=depth,
            )
            page_data.redirect_chain = redirect_hops
            await self.storage.save_page(page_data)

            # Discover internal links for deeper crawling
            if depth < self.config.max_depth and page_data.html:
                for link in page_data.links:
                    if link.get("internal"):
                        target_url = link.get("href", "")
                        if target_url and target_url not in self.visited_urls and is_valid_http_url(target_url):
                            if len(self.visited_urls) < self.config.max_pages:
                                self.visited_urls.add(target_url)
                                await queue.put((target_url, depth + 1))
