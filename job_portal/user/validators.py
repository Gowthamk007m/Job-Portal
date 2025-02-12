from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

def validate_video_file(value):
    

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']

    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Only .mp4, .avi, .mkv, .mov, .wmv are supported.'))