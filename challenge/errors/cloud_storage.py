class GoogleStorageError(Exception):
    """Excepción base para errores de Google Storage."""
    pass

class GoogleStorageUploadError(GoogleStorageError):
    """Excepción para errores durante la subida de archivos."""
    pass