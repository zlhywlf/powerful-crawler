"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from scrapy.cmdline import execute


def main() -> None:
    """The powerful crawler application."""
    execute(["scrapy", "runspider", "QuotesSpider.py"])


if __name__ == "__main__":
    main()
