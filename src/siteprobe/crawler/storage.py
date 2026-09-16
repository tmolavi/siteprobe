import json
from pathlib import Path
from typing import List, Optional
import aiosqlite
from siteprobe.models.crawl import CrawlPage


class CrawlStorage:
    """SQLite-backed async storage for crawled pages to avoid high memory overhead."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._db: Optional[aiosqlite.Connection] = None

    async def initialize(self) -> None:
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(self.db_path)
        await self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS pages (
                url TEXT PRIMARY KEY,
                status_code INTEGER,
                content_type TEXT,
                headers_json TEXT,
                html TEXT,
                title TEXT,
                meta_description TEXT,
                canonical TEXT,
                robots_meta TEXT,
                lang TEXT,
                response_time_ms REAL,
                body_size_bytes INTEGER,
                depth INTEGER,
                is_indexable INTEGER,
                page_data_json TEXT
            )
            """
        )
        await self._db.commit()

    async def save_page(self, page: CrawlPage) -> None:
        if not self._db:
            await self.initialize()
        assert self._db is not None
        await self._db.execute(
            """
            INSERT OR REPLACE INTO pages (
                url, status_code, content_type, headers_json, html, title,
                meta_description, canonical, robots_meta, lang, response_time_ms,
                body_size_bytes, depth, is_indexable, page_data_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                page.url,
                page.status_code,
                page.content_type,
                json.dumps(page.headers),
                page.html,
                page.title,
                page.meta_description,
                page.canonical,
                page.robots_meta,
                page.lang,
                page.response_time_ms,
                page.body_size_bytes,
                page.depth,
                1 if page.is_indexable else 0,
                page.model_dump_json(),
            ),
        )
        await self._db.commit()

    async def get_page(self, url: str) -> Optional[CrawlPage]:
        if not self._db:
            return None
        cursor = await self._db.execute("SELECT page_data_json FROM pages WHERE url = ?", (url,))
        row = await cursor.fetchone()
        if row:
            return CrawlPage.model_validate_json(row[0])
        return None

    async def get_all_pages(self) -> List[CrawlPage]:
        if not self._db:
            return []
        cursor = await self._db.execute("SELECT page_data_json FROM pages ORDER BY depth ASC")
        rows = await cursor.fetchall()
        return [CrawlPage.model_validate_json(r[0]) for r in rows]

    async def count_pages(self) -> int:
        if not self._db:
            return 0
        cursor = await self._db.execute("SELECT COUNT(*) FROM pages")
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def close(self) -> None:
        if self._db:
            await self._db.close()
            self._db = None
