import base64
import uuid
from datetime import datetime
from io import BytesIO

import boto3
from PIL import Image
from django.conf import settings


class UploadProfileService:
    def get_filekey(self, request):
        current_date = datetime.now().strftime("%Y%m%d")
        unique_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").rstrip("=")
        file_key = f"{request.user.id}/{current_date}_{unique_id}"

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_S3_SECRET_KEY,
        )

        file = request.FILES['file']
        image = Image.open(file)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        image_byte_array = BytesIO()
        image_resized = image.resize((110, 110))
        image_resized.save(image_byte_array, format='JPEG', quality=50, optimize=True)
        image_byte_array.seek(0)

        s3.upload_fileobj(image_byte_array, settings.AWS_S3_STORAGE_BUCKET_NAME, file_key,
                          ExtraArgs={"ContentType": file.content_type})

        return file_key
