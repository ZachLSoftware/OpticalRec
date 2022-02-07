from django.core.exceptions import ValidationError

def validate_file_ext(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid=[".mp4", ".avi"]
    if not ext in valid:
        raise ValidationError(u'File Format not supported')