from google.cloud import storage
from google.api_core import exceptions as google_exceptions
from io import BytesIO
import challenge.utils.settings as env
from challenge.errors.cloud_storage import GoogleStorageError, GoogleStorageUploadError
from challenge.utils.logger import logger

class GoogleCloudStorage:
    def __init__(self):
        self.bucket_name = env.BUCKET_NAME
        self.model_blob_name = env.MODEL_FILE
        self.dataset_blob_name = env.DATASET_FILE
        try:
            self.storage_client = storage.Client()
        except Exception as e:
            raise GoogleStorageError(f"Error al inicializar el cliente de Storage: {str(e)}")

    def upload(self, content: BytesIO) -> None:
        logger.info(f"Subiendo el archivo a {self.bucket_name}")
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.model_blob_name)

            content.seek(0)
            blob.upload_from_file(content)
            logger.debug("Se subio el archivo correctamente")
            return True
        except google_exceptions.NotFound:
            logger.error(f"No se encontró el bucket: {self.bucket_name}")
            raise GoogleStorageUploadError(f"No se encontró el bucket: {self.bucket_name}")
        except google_exceptions.Forbidden:
            logger.error("No tiene permisos suficientes para subir al bucket")
            raise GoogleStorageUploadError("No tiene permisos suficientes para subir al bucket")
        except Exception as e:
            logger.error(f"Error al subir el archivo: {str(e)}")
            raise GoogleStorageUploadError(f"Error al subir el archivo: {str(e)}")
        
    def download_dataset(self) -> BytesIO:
        logger.debug(f"Descargando archivo de {self.bucket_name}")
        return self.__download(self.dataset_blob_name)
        
    def download_model(self) -> BytesIO:
        logger.debug(f"Descargando archivo de {self.bucket_name}")
        return self.__download(self.model_blob_name)
    
    def __download(self, blob_name: str) -> BytesIO:
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)

            buffer = BytesIO()
            blob.download_to_file(buffer)
            buffer.seek(0)
            logger.debug(f"Se descargo el archivo correctamente")
            return buffer
        except google_exceptions.NotFound:
            logger.error(f"No se encontró el archivo: {blob_name} en el bucket: {self.bucket_name}")
            raise GoogleStorageError(f"No se encontró el archivo: {self.model_blob_name} en el bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Error al descargar el archivo: {str(e)}")
            raise GoogleStorageError(f"Error al descargar el archivo: {str(e)}")