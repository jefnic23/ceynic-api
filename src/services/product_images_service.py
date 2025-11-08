from typing import Annotated
import cloudinary.api
from cloudinary import config, uploader
from fastapi import Depends, UploadFile
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from PIL import Image
import hashlib
from io import BytesIO

from src.config import Settings, get_settings
from src.database import get_async_session
from src.models.product_image import ProductImage
from src.repositories.product_image_repository import ProductImageRepository


class ImageMetadata(BaseModel):
    file_bytes: bytes
    file_hash: str
    width: int
    height: int


class ProductImagesService:
    def __init__(
        self, 
        session: Annotated[AsyncSession, Depends(get_async_session)], 
        settings: Annotated[Settings, Depends(get_settings)],
        repository: Annotated[ProductImageRepository, Depends()]
    ):
        self._session = session
        self._settings = settings
        self._repository = repository

        config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    async def update(self, storefront_id: int, product_id: int, files: list[UploadFile]):
        # async with self._session.begin():  

        current_product_images = await self._repository.get_all(storefront_id, product_id)
        incoming_product_images = [await ProductImagesService.get_image_metadata(file) for file in files]

        images_to_delete, images_to_upload, image_order = ProductImagesService.get_image_operations(
            current_product_images, incoming_product_images
        )

        # delete images from cloudinary and db
        delete_response = cloudinary.api.delete_resources(images_to_delete)

        await self._repository.delete(storefront_id=storefront_id, product_id=product_id, public_ids=images_to_delete)
        
        product_images_to_add = []

        # upload new images to cloudinary
        for image in images_to_upload:
            response = uploader.upload(
                file=image.file_bytes, 
                public_id=image.file_hash, 
                public_id_prefix="", # storefront id/merchant name?
                unique_filename = False, 
                overwrite=True
            )
            # do anything with response?

            # add image to db but don't commit yet
            product_images_to_add.append(ProductImage(
                public_id=image.file_hash,
                position=image_order.get(image.file_hash),
                width=image.width,
                height=image.height,
                product_id=product_id
            ))

        await self._repository.add_all(product_images_to_add)

        # set order on existing images in db
        for image in current_product_images:
            if image.public_id in images_to_delete:
                continue
            self._repository.update(image, image_order.get(image.public_id))
        

    @staticmethod
    async def get_image_metadata(file: UploadFile) -> ImageMetadata:
        def hash_file(file_contents: bytes) -> str:
            sha256 = hashlib.sha256()
            sha256.update(file_contents)
            return sha256.hexdigest()
        
        def get_image_dimensions(file_contents: bytes) -> tuple[int, int]:
            image = Image.open(BytesIO(file_contents))
            return image.width, image.height 

        contents = await file.read()

        # get file hash for the public_id
        file_hash = hash_file(contents)

        # get width and height
        width, height = get_image_dimensions(contents)

        return ImageMetadata(file_bytes=contents, file_hash=file_hash, width=width, height=height)
    
    @staticmethod
    def get_image_operations(
        current: list[ProductImage], 
        incoming: list[ImageMetadata]
    ) -> tuple[list[str], list[ImageMetadata], dict[str, int]]:
        """
        Compare two ordered collections of image objects.

        Returns
        -------
        delete : list[str]
            Public-IDs present in `current` but absent in `incoming`.
        upload : list[Any]
            Incoming image objects that are new and must be uploaded.
        reorder : list[dict]
            Existing images whose position changed.  Each dict has
            {'public_id': str, 'from': int, 'to': int}.
        """
        current_ids = [product_image.public_id for product_image in current]
        incoming_ids = [product_image.file_hash for product_image in incoming]

        current_set = set(current_ids)
        incoming_set = set(incoming_ids)

        images_to_delete = list(current_set - incoming_set)

        images_to_upload = [product_image for product_image in incoming if product_image.file_hash not in current_set]

        image_order = {}
        for new_position, public_id in enumerate(incoming_ids, 1):
            if public_id in current_set:
                current_position = current_ids.index(public_id)
                if current_position != new_position:
                    image_order[public_id] = new_position
            else:
                image_order[public_id] = new_position

        return images_to_delete, images_to_upload, image_order