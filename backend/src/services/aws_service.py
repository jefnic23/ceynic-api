import aioboto3
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.config import Settings


class AwsService:
    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.s3 = aioboto3.Session(
            aws_access_key_id=settings.BUCKETEER_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.BUCKETEER_AWS_SECRET_ACCESS_KEY,
        )
        self._region = settings.BUCKETEER_AWS_REGION
        self._bucket_name = settings.BUCKETEER_BUCKET_NAME

    async def get_product_images(self, product_name: str) -> list[str]:
        async with self.s3.resource(
            service_name="s3", region_name=self._region
        ) as resource:
            bucket = await resource.Bucket(self._bucket_name)
            images = bucket.objects.filter(
                Prefix=f"public/{product_name.replace(' ', '_')}/"
            )
            return [
                f"https://{self._bucket_name}.s3.amazonaws.com/{image.key}"
                async for image in images
            ]
