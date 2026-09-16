import re
from typing import Dict, List, Optional
from urllib.parse import urlparse


AI_BOT_USER_AGENTS = {
    "GPTBot": "OpenAI general training / web crawler",
    "OAI-SearchBot": "OpenAI search / SearchGPT retrieval crawler",
    "PerplexityBot": "Perplexity search retrieval crawler",
    "ClaudeBot": "Anthropic search / retrieval crawler",
    "anthropic-ai": "Anthropic training crawler",
    "Bytespider": "ByteDance / TikTok AI crawler",
    "CCBot": "Common Crawl dataset crawler",
    "Google-Extended": "Google Gemini training control token",
    "Applebot-Extended": "Apple Intelligence training control token",
}


class RobotsParser:
    """Parses robots.txt and analyzes crawler directives including AI bot permissions."""

    def __init__(self, content: str = ""):
        self.raw_content = content
        self.sitemaps: List[str] = []
        self.user_agent_rules: Dict[str, Dict[str, List[str]]] = {}
        self.parse()

    def parse(self) -> None:
        current_agents: List[str] = []
        for line in self.raw_content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip()

                if key == "user-agent":
                    agent = val
                    if not current_agents:
                        current_agents = [agent]
                    else:
                        current_agents.append(agent)
                    if agent not in self.user_agent_rules:
                        self.user_agent_rules[agent] = {"allow": [], "disallow": []}
                elif key == "sitemap":
                    if val and val not in self.sitemaps:
                        self.sitemaps.append(val)
                elif key == "disallow" and current_agents:
                    for ag in current_agents:
                        self.user_agent_rules[ag]["disallow"].append(val)
                elif key == "allow" and current_agents:
                    for ag in current_agents:
                        self.user_agent_rules[ag]["allow"].append(val)
            else:
                current_agents = []

    def is_allowed(self, user_agent: str, path: str) -> bool:
        """Check whether path is allowed for given user agent using longest matching rule."""
        if not path:
            path = "/"
        rules = self.user_agent_rules.get(user_agent)
        if not rules:
            # Fallback to wildcard '*'
            rules = self.user_agent_rules.get("*")
        if not rules:
            return True

        # Check disallow rules
        for dis in rules.get("disallow", []):
            if not dis:
                continue
            if dis == "/" or path.startswith(dis):
                # Check if there is a more specific allow
                for al in rules.get("allow", []):
                    if al and path.startswith(al) and len(al) >= len(dis):
                        return True
                return False
        return True

    def get_ai_crawler_status(self) -> Dict[str, Dict[str, any]]:
        """Evaluate access status for major AI search and training bots."""
        status = {}
        for bot, desc in AI_BOT_USER_AGENTS.items():
            has_specific_rule = bot in self.user_agent_rules
            allowed_root = self.is_allowed(bot, "/")
            status[bot] = {
                "description": desc,
                "explicit_rule": has_specific_rule,
                "allowed": allowed_root,
                "disallow_all": not allowed_root,
            }
        return status
