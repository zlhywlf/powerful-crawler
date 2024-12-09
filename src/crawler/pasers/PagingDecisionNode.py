"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import math
import re
from typing import override

from scrapy import FormRequest

from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.models.MetaChecker import MetaChecker


class PagingDecisionNode(DecisionNode):
    """paging decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        t = 0
        if meta.config:
            if meta.config.get("needed"):
                t = 1
            text = ctx.response.text
            limit_match = re.search(meta.config.get("limit", ""), text)
            limit = limit_match.group(1) if limit_match else None
            count_match = re.search(meta.config.get("count", ""), text)
            count = count_match.group(1) if count_match else None
            url_match = re.search(meta.config.get("url", ""), text)
            url = url_match.group(1) if url_match else None
            pages = math.ceil(int(count) / int(limit))  # type:ignore  [arg-type]
            return MetaChecker(
                curr_meta=meta,
                type=t,
                result=[
                    FormRequest(
                        url=url,
                        formdata={"pageNumber": f"{page + 1}", "pageSize": limit},  # type:ignore  [dict-item]
                        meta={"decision": meta.meta[0]} if meta.meta else None,
                    )
                    for page in range(pages)
                    if page < 1
                ],
            )
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=[],
        )
