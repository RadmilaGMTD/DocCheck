from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible


@deconstructible
class DocumentValidator:
    """
    Валидатор документов для проверки размера и типа загружаемых файлов.
    """

    MAX_SIZE = 10 * 1024 * 1024
    ALLOWED_TYPES = [".gpg", ".doc", ".docx"]

    def __call__(self, value):
        file = value.get("file")
        if file.size > self.MAX_SIZE:
            raise ValidationError(f"Максимальный размер файла {filesizeformat(self.MAX_SIZE)}. ")

        ext = file.name.lower().rsplit(".", 1)[-1]
        if f".{ext}" not in self.ALLOWED_TYPES:
            raise ValidationError(f"Недопустимый тип файла. Разрешенные: {', '.join(self.ALLOWED_TYPES)}")
