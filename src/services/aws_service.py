from typing import Annotated
import aioboto3
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings, get_settings
from src.database import get_async_session
from src.models.product import Product


class AwsService:
    def __init__(
        self, 
        session: Annotated[AsyncSession, Depends(get_async_session)], 
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        self._session = session
        self._s3 = aioboto3.Session(
            aws_access_key_id=settings.BUCKETEER_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.BUCKETEER_AWS_SECRET_ACCESS_KEY,
        )
        self._region = settings.BUCKETEER_AWS_REGION
        self._bucket_name = settings.BUCKETEER_BUCKET_NAME

    async def get_product_images(self, product: Product) -> list[str]:
        async with self._s3.resource(
            service_name="s3", region_name=self._region
        ) as resource:
            bucket = await resource.Bucket(self._bucket_name)
            images = bucket.objects.filter(
                Prefix=f"public/{product.formatted_title}/"
            )
            return [
                f"https://{self._bucket_name}.s3.amazonaws.com/{image.key}"
                async for image in images
                if not image.key.endswith("/")
            ]

    def get_product_thumbnail(self, product: Product) -> str:
        return f"https://{self._bucket_name}.s3.amazonaws.com/public/{product.formatted_title}/{product.thumbnail}"