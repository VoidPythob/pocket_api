from __future__ import annotations

from typing import Any

from django.http import FileResponse
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.file_storage import open_file_stream
from pocket_api.result import Result


class FileDownloadView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request: Request, file_id: str, *args: Any, **kwargs: Any):
        metadata, file_handle = open_file_stream(file_id)
        if metadata is None or file_handle is None:
            return Result.from_code(
                ResponseCode.NOT_FOUND,
                msg="文件不存在",
            ).to_response()

        response = FileResponse(
            file_handle,
            as_attachment=False,
            filename=metadata["original_name"],
            content_type=metadata.get("content_type") or "application/octet-stream",
        )
        response["X-File-Id"] = metadata["file_id"]
        return response
