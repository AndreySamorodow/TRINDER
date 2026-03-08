from src.profile.S3.client import s3_client


class S3Service:
    def __init__(self):
        pass

    async def add_photo_to_s3(self, photo, name):
        url = await s3_client.upload_file(file=photo, object_name=name)
        return url
    