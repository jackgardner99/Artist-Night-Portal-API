import cloudinary
import cloudinary.uploader
import cloudinary.utils
from cloudinary_storage.storage import MediaCloudinaryStorage

RAW_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt', 'zip'}


def get_resource_type(name):
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    return 'raw' if ext in RAW_EXTENSIONS else 'image'


class AutoTypeCloudinaryStorage(MediaCloudinaryStorage):
    def _save(self, name, content):
        resource_type = get_resource_type(name)
        content.seek(0)
        response = cloudinary.uploader.upload(
            content,
            public_id=name,
            resource_type=resource_type,
            type='upload',
            overwrite=True,
        )
        return response['public_id']

    def url(self, name):
        resource_type = get_resource_type(name)
        url, _ = cloudinary.utils.cloudinary_url(
            name,
            resource_type=resource_type,
            type='upload',
        )
        return url
