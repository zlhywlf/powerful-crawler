"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import os

from scrapy.cmdline import execute
from scrapy.utils.project import ENVVAR, get_project_settings


def main() -> None:
    """The powerful crawler application."""
    os.environ.setdefault(ENVVAR, __name__)
    settings = get_project_settings()
    settings.setdict({"SPIDER_MODULES": "crawler.spiders"}, priority="project")
    execute(["scrapy", "crawl", "Quotes"], settings)


if __name__ == "__main__":
    main()
