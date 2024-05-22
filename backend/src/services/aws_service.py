from sqlmodel.ext.asyncio.session import AsyncSession
from boto3 import Session

from backend.src.config import Settings


class AwsService:
    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.bucket = (
            Session(
                aws_access_key_id=settings.BUCKETEER_AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.BUCKETEER_AWS_SECRET_ACCESS_KEY,
            )
            .resource(service_name="s3", region_name=settings.BUCKETEER_AWS_REGION)
            .Bucket(settings.BUCKETEER_BUCKET_NAME)
        )
