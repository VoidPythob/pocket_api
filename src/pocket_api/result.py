from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from pocket_api.enums import ResponseCode

T = TypeVar("T")


@dataclass(slots=True)
class Result(Generic[T]):
    code: int
    msg: str
    data: T | None = None

    @classmethod
    def from_code(
        cls, code: ResponseCode, *, data: T | None = None, msg: str | None = None
    ) -> "Result[T]":
        return cls(code=code.code, msg=msg or code.msg, data=data)

    @classmethod
    def success(
        cls, *, data: T | None = None, msg: str | None = None
    ) -> "Result[T]":
        return cls.from_code(ResponseCode.SUCCESS, data=data, msg=msg)

    @classmethod
    def created(
        cls, *, data: T | None = None, msg: str | None = None
    ) -> "Result[T]":
        return cls.from_code(ResponseCode.CREATED, data=data, msg=msg)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"code": self.code, "msg": self.msg}
        if self.data is not None:
            payload["data"] = self.data
        return payload

    def to_response(self, *, headers: dict[str, str] | None = None) -> Response:
        return Response(self.to_dict(), status=self.code, headers=headers)


def result_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    response.data = Result(
        code=response.status_code,
        msg=_extract_error_message(response.data),
        data=response.data,
    ).to_dict()
    return response


def _extract_error_message(data: Any) -> str:
    if isinstance(data, dict):
        detail = data.get("detail")
        if detail is not None:
            return _extract_error_message(detail)

        for value in data.values():
            return _extract_error_message(value)

    if isinstance(data, list) and data:
        return _extract_error_message(data[0])

    return str(data)
