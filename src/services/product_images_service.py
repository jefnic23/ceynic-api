import hashlib
from io import BytesIO
from pathlib import Path
from typing import Annotated

from aiohttp import ClientResponseError
from fastapi import Depends, HTTPException, UploadFile, status
from PIL import Image

from src.dependencies import SETTINGS_DEPENDENCY
from src.http_client import HttpClient, get_http_client
from src.models.product import Product
from src.models.product_image import ProductImage
from src.schemas.image_metadata import ImageMetadata


class ProductImagesService:
    def __init__(self, http_client: Annotated[HttpClient, Depends(get_http_client)], settings: SETTINGS_DEPENDENCY):
        self._http_client = http_client
        self._settings = settings

    @property
    def bunny_storage_zone_endpoint(self) -> str:
        return f"https://{self._settings.BUNNY_STORAGE_ZONE_REGION}.storage.bunnycdn.com/{self._settings.BUNNY_STORAGE_ZONE_NAME}"

    async def create_and_upload(self, product: Product, file: UploadFile, position: int) -> ProductImage:
        image_metadata = await self.get_image_metadata(product, file)
        upload_response = await self.upload(image_metadata)
        if not upload_response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Mismatching product id.",
            )
        return ProductImage(
            url=image_metadata.download_url,
            position=position,
            width=image_metadata.width,
            height=image_metadata.height,
            product=product,
        )

    async def upload(self, image_metadata: ImageMetadata) -> bool:
        headers = {
            "AccessKey": self._settings.BUNNY_STORAGE_ZONE_PASSWORD,
            "Content-Type": "application/octet-stream",
        }

        try:
            await self._http_client.put_async(
                url=image_metadata.upload_url,
                headers=headers,
                data=image_metadata.file_bytes,
            )
        except ClientResponseError:
            return False

        return True

    async def delete(self, product: Product, image: ProductImage) -> bool:
        headers = {
            "AccessKey": self._settings.BUNNY_STORAGE_ZONE_PASSWORD,
        }

        try:
            await self._http_client.delete_async(
                url=f"{self.bunny_storage_zone_endpoint}/{product.storefront_id}/{product.id}/{Path(image.url).name}",
                headers=headers,
            )
        except ClientResponseError:
            return False

        return True

    async def get_image_metadata(self, product: Product, file: UploadFile) -> ImageMetadata:
        def hash_file(file_contents: bytes) -> str:
            return hashlib.sha256(file_contents, usedforsecurity=False).hexdigest()

        def get_image_dimensions(file_contents: bytes) -> tuple[int, int]:
            image = Image.open(BytesIO(file_contents))
            return image.width, image.height

        def get_image_urls(file_hash: str, filename: str) -> tuple[str, str]:
            return (
                f"{self.bunny_storage_zone_endpoint}/{product.storefront_id}/{product.id}/{file_hash}{Path(filename).suffix}",
                f"{self._settings.BUNNY_PULL_ZONE_HOSTNAME}/{product.storefront_id}/{product.id}/{file_hash}{Path(filename).suffix}",
            )

        contents = await file.read()

        file_hash = hash_file(contents)
        width, height = get_image_dimensions(contents)
        upload_url, download_url = get_image_urls(file_hash, file.filename)

        return ImageMetadata(
            file_bytes=contents,
            file_hash=file_hash,
            upload_url=upload_url,
            download_url=download_url,
            width=width,
            height=height,
        )

    # async def _authenticate(self) -> None:
    #     headers = {
    #         "AccessKey": self._settings.BUNNY_STORAGE_ZONE_PASSWORD,
    #     }

    #     await self._http_client.get_async(
    #         url=f"https://storage.bunnycdn.com/{self._settings.BUNNY_STORAGE_ZONE_NAME}/",
    #         headers=headers,
    #     )
