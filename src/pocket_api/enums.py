from enum import Enum
from typing import NamedTuple


class CodeMsg(NamedTuple):
    code: int
    msg: str


class ResponseCode(Enum):
    """
    REST API 响应状态码枚举
    """

    # === 2xx 成功 ===
    SUCCESS = CodeMsg(200, "操作成功")
    CREATED = CodeMsg(201, "创建成功")
    ACCEPTED = CodeMsg(202, "请求已接受")
    NO_CONTENT = CodeMsg(204, "删除成功")

    # === 4xx 客户端错误 ===
    BAD_REQUEST = CodeMsg(400, "请求参数错误")
    UNAUTHORIZED = CodeMsg(401, "未授权，请先登录")
    FORBIDDEN = CodeMsg(403, "禁止访问")
    NOT_FOUND = CodeMsg(404, "资源不存在")
    METHOD_NOT_ALLOWED = CodeMsg(405, "请求方法不允许")
    CONFLICT = CodeMsg(409, "资源冲突")
    TOO_MANY_REQUESTS = CodeMsg(429, "请求过于频繁")

    # === 5xx 服务端错误 ===
    INTERNAL_SERVER_ERROR = CodeMsg(500, "服务器内部错误")
    SERVICE_UNAVAILABLE = CodeMsg(503, "服务暂不可用")

    # === 1xxx 业务自定义码 ===
    PARAM_ERROR = CodeMsg(1001, "参数校验失败")
    TOKEN_EXPIRED = CodeMsg(1002, "登录状态已过期")
    PERMISSION_DENIED = CodeMsg(1003, "权限不足")
    DATA_NOT_FOUND = CodeMsg(1004, "数据不存在")
    DUPLICATE_DATA = CodeMsg(1005, "数据已存在")

    @property
    def code(self) -> int:
        return self.value.code

    @property
    def msg(self) -> str:
        return self.value.msg

    def to_dict(self) -> dict:
        """转为字典"""
        return {"code": self.code, "msg": self.msg}

    def __str__(self) -> str:
        return f"[{self.code}] {self.msg}"
