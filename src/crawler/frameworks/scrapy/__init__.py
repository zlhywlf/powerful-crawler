import os

from scrapy.cmdline import execute
from scrapy.utils.project import ENVVAR, get_project_settings

from crawler.congfig import NAME


def main() -> None:
    """The powerful crawler application."""
    os.environ.setdefault(ENVVAR, __name__)
    settings = get_project_settings()
    settings.setdict({"SPIDER_MODULES": "crawler.spiders"}, priority="project")
    execute(["scrapy", "crawl", NAME], settings)
