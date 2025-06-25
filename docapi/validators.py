from rest_framework.validators import ValidationError


class DocumentValidator:

    def __call__(self, value):
        size = ""
        file_size = value.get("file")
        if file_size > size:
            raise ValidationError("Недопустимый размер файла")
