"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from scrapy import Request

from crawler.core.BaseQueue import BaseQueue


class PriorityQueue(BaseQueue):
    """priority queue."""

    @override
    def __len__(self) -> int:
        return self.client.zcard(self.key)

    @override
    def push(self, request: Request) -> None:
        data = self.encode_request(request)
        score = -request.priority
        self.client.execute_command("ZADD", self.key, score, data)

    @override
    def pop(self, timeout: int = 0) -> Request | None:
        pip = self.client.pipeline()
        pip.multi()
        pip.zrange(self.key, 0, 0)
        pip.zremrangebyrank(self.key, 0, 0)
        results, _ = pip.execute()  # type:ignore [no-untyped-call]
        return self.decode_request(results[0]) if results else None
