from pydantic import BaseModel


class ImageMetadata(BaseModel):
    file_bytes: bytes
    file_hash: str
    upload_url: str
    download_url: str
    width: int
    height: int
