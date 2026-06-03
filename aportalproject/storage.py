import cloudinary.uploader
from cloudinary_storage.storage import MediaCloudinaryStorage


class AutoTypeCloudinaryStorage(MediaCloudinaryStorage):
    def _save(self, name, content):
        response = cloudinary.uploader.upload(
            content,
            public_id=name,
            resource_type='auto',
            use_filename=True,
            unique_filename=True,
        )
        return response['public_id']
