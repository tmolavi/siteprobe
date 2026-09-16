from pathlib import Path
from typing import Optional
import yaml
from siteprobe.models.config import SiteProbeConfig, SiteConfig, CrawlConfig, ChecksConfig, IntegrationsConfig


def load_config(config_path: Optional[str] = None) -> SiteProbeConfig:
    """Load configuration from YAML file or return defaults."""
    if config_path and Path(config_path).is_file():
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return SiteProbeConfig.model_validate(data)

    # Search for siteprobe.yml in current directory
    default_file = Path("siteprobe.yml")
    if default_file.is_file():
        with open(default_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return SiteProbeConfig.model_validate(data)

    # Default fallback
    return SiteProbeConfig(
        site=SiteConfig(url="https://example.com", language="en"),
        crawl=CrawlConfig(),
        checks=ChecksConfig(),
        integrations=IntegrationsConfig(),
    )
