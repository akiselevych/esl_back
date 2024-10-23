import shutil
import hashlib

from starlette.datastructures import UploadFile
from dataclasses import dataclass

from typing import Optional
from typing import NamedTuple

from .core.config import settings


class MediaFileUploadResponse(NamedTuple):
    file_path: Optional[str] = None
    error: Optional[str] = None


class MediaFilesUploadHelper:
    def __init__(self, upload_file: UploadFile) -> None:
        self.upload_file = upload_file
        self.upload_filename = self.upload_file.filename
        self.upload_file_format = self.upload_filename.split(".")[-1]

    @property
    def hashed_filename(self) -> str:
        return (
            hashlib.sha256(self.upload_filename.encode()).hexdigest()
            + "."
            + self.upload_file_format
        )

    async def get_file_link(self, hashed_name: str) -> str:
        return f"{settings.full_media_url}/{hashed_name}"

    async def save_upload_file(self) -> MediaFileUploadResponse:
        """Returns link to saved file"""
        print(self.upload_file_format)
        if self.upload_file_format in settings.media_allowed_formats:
            with open(f"{settings.media_root}/{self.hashed_filename}", "wb") as buffer:
                shutil.copyfileobj(self.upload_file.file, buffer)
            return MediaFileUploadResponse(
                file_path=await self.get_file_link(self.hashed_filename),
            )
        return MediaFileUploadResponse(
            error=f"File format is not allowed! Allowed formats: {settings.media_allowed_formats}"
        )
