
import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


class CustomStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""

    location = os.path.join(settings.MEDIA_ROOT, "uploads/images/")
    base_url = urljoin(settings.MEDIA_URL, "uploads/images/")


#
# def get_filename(filename):
#     return filename.upper()
