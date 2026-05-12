from __future__ import annotations

import json
import mimetypes
import secrets
from pathlib import Path
from typing import Any, BinaryIO

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile


def get_storage_root() -> Path:
    root = Path(getattr(settings, "FILE_STORAGE_ROOT"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def save_uploaded_file(uploaded_file: UploadedFile) -> dict[str, Any]:
    storage_root = get_storage_root()
    file_id = _generate_file_id(storage_root)
    suffix = Path(uploaded_file.name or "").suffix
    stored_name = f"{file_id}{suffix}"
    file_path = storage_root / stored_name

    with file_path.open("wb") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    content_type = uploaded_file.content_type or mimetypes.guess_type(uploaded_file.name)[0]
    metadata = {
        "file_id": file_id,
        "stored_name": stored_name,
        "original_name": uploaded_file.name,
        "content_type": content_type,
        "size": uploaded_file.size,
    }
    _write_metadata(storage_root / f"{file_id}.json", metadata)
    return metadata


def resolve_file(file_id: str) -> dict[str, Any] | None:
    storage_root = get_storage_root()
    metadata_path = storage_root / f"{file_id}.json"
    if not metadata_path.exists():
        return None

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    file_path = storage_root / metadata["stored_name"]
    if not file_path.exists():
        return None

    metadata["file_path"] = file_path
    if not metadata.get("content_type"):
        metadata["content_type"] = mimetypes.guess_type(file_path.name)[0]
    return metadata


def open_file_stream(file_id: str) -> tuple[dict[str, Any], BinaryIO] | tuple[None, None]:
    metadata = resolve_file(file_id)
    if metadata is None:
        return None, None
    file_handle = metadata["file_path"].open("rb")
    return metadata, file_handle


def _generate_file_id(storage_root: Path) -> str:
    while True:
        file_id = secrets.token_hex(16)
        if not (storage_root / f"{file_id}.json").exists():
            return file_id


def _write_metadata(path: Path, metadata: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
