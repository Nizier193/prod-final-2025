from typing import Any, List, Optional
from uuid import UUID, uuid4

from core.config import config
from .models import ImageModel


def generate_unique_filename(campaignId: UUID, filename: str):
    blank = "{campaignId}/{uuid}.{extension}"
    extension = filename.split(".")[-1]

    return blank.format(
        campaignId=str(campaignId),
        uuid=str(uuid4()),
        extension=extension
    )


class BotoRepository():
    def __init__(self, boto) -> None:
        self.boto = boto

    def get_images_by_campaign_id(self, campaignId: UUID, limit: int = 10, offset: int = 0) -> List[ImageModel]:
        image_url_template = f"http://{config.HOST.rstrip("/")}/images/?key=" 
        images: List[ImageModel] = []

        try:
            boto_images = self.boto.list_objects_v2(
                Bucket=config.BUCKET_NAME, 
                Prefix=f"{campaignId}/",
                MaxKeys=limit,
                StartAfter=str(offset)
            )
            for image in boto_images.get("Contents", []):
                image = ImageModel(
                    key=image.get("Key"),
                    url=image_url_template + image.get("Key", ""),
                    status=True
                )
                images.append(image)

            return images
        
        except Exception as err:
            print("Error while trying to retrieve image list:", str(err))
            return []


    def upload_image(self, campaignId: UUID, image, image_name: str) -> ImageModel:
        new_image_name = generate_unique_filename(campaignId, image_name)

        try:
            self.boto.upload_fileobj(
                image,
                config.BUCKET_NAME,
                new_image_name,
            )

            image_response = ImageModel(
                key=new_image_name,
                status=True
            )
            return image_response

        except Exception as err:
            print("Error while trying to upload image:", str(err))

            image_response = ImageModel(
                key=None,
                status=False
            )
            return image_response
        

    def get_image_by_key(self, key: str) -> Optional[Any]:
        try:
            object = self.boto.get_object(
                Bucket=config.BUCKET_NAME, 
                Key=key
            )
            if not object:
                return None
            
            return object['Body'], object.get('ContentType')  # Возвращаем тело и тип контента

        except Exception as err:
            print("Error while trying to get image by key:", str(err))
            return None