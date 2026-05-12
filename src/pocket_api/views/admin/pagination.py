from __future__ import annotations

from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request

from pocket_api.result import Result


def build_paginated_result(
    *,
    request: Request,
    queryset,
    serializer_class,
    msg: str = "查询成功",
):
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return Result.success(
            data={
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": serializer.data,
            },
            msg=msg,
        ).to_response()

    serializer = serializer_class(queryset, many=True)
    return Result.success(data=serializer.data, msg=msg).to_response()
