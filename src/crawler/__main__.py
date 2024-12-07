"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
import os

from scrapy.cmdline import execute
from scrapy.utils.project import ENVVAR, get_project_settings

from crawler.congfig import NAME
from crawler.spiders import init


def main() -> None:
    """The powerful crawler application."""
    asyncio.run(init())
    os.environ.setdefault(ENVVAR, __name__)
    settings = get_project_settings()
    settings.setdict({"SPIDER_MODULES": "crawler.spiders"}, priority="project")
    execute(["scrapy", "crawl", NAME], settings)


if __name__ == "__main__":
    main()
