from typing import Any

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.file_storage import save_uploaded_file
from pocket_api.result import Result
from pocket_api.serializers import AdminFileUploadSerializer, FileUploadPayloadSerializer


class AdminFileUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        metadata = save_uploaded_file(serializer.validated_data["file"])
        payload = FileUploadPayloadSerializer(
            {
                "file_id": metadata["file_id"],
                "file_name": metadata["original_name"],
                "content_type": metadata.get("content_type"),
                "size": metadata["size"],
                "url": f"/files/{metadata['file_id']}/",
            }
        )
        return Result.created(data=payload.data, msg="上传成功").to_response()
