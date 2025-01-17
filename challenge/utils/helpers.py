import pandas as pd
from datetime import datetime
from challenge.model import DelayModel
from challenge.storage.gcp_storage import GoogleCloudStorage
from challenge.errors.cloud_storage import GoogleStorageError
from challenge.utils.logger import logger

cloud_storage = GoogleCloudStorage()

def get_period_day(date: str) -> str:
    date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
    morning_min = datetime.strptime("05:00", '%H:%M').time()
    morning_max = datetime.strptime("11:59", '%H:%M').time()
    afternoon_min = datetime.strptime("12:00", '%H:%M').time()
    afternoon_max = datetime.strptime("18:59", '%H:%M').time()
    evening_min = datetime.strptime("19:00", '%H:%M').time()
    evening_max = datetime.strptime("23:59", '%H:%M').time()
    night_min = datetime.strptime("00:00", '%H:%M').time()
    night_max = datetime.strptime("4:59", '%H:%M').time()
    
    if(date_time > morning_min and date_time < morning_max):
        return 'mañana'
    elif(date_time > afternoon_min and date_time < afternoon_max):
        return 'tarde'
    elif(
        (date_time > evening_min and date_time < evening_max) or
        (date_time > night_min and date_time < night_max)
    ):
        return 'noche'
    
def is_high_season(fecha) -> int:
    fecha_año = int(fecha.split('-')[0])
    fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year = fecha_año)
    range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year = fecha_año)
    range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year = fecha_año)
    range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year = fecha_año)
    range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year = fecha_año)
    range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year = fecha_año)
    range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year = fecha_año)
    range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year = fecha_año)
    
    if ((fecha >= range1_min and fecha <= range1_max) or 
        (fecha >= range2_min and fecha <= range2_max) or 
        (fecha >= range3_min and fecha <= range3_max) or
        (fecha >= range4_min and fecha <= range4_max)):
        return 1
    else:
        return 0
    
def get_min_diff(data: pd.DataFrame) -> float:
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff

def init_model() -> DelayModel:
    logger.debug(f"Inicializando modelo")
    delay_model = DelayModel()
    try:
        model_buffer = cloud_storage.download_model()
        delay_model.load_model(model_buffer=model_buffer)
        logger.debug("Modelo cargado correctamente")
    except GoogleStorageError as e:
        logger.warning(f"Warning: No se pudo cargar la configuración del modelo desde GCS: {str(e)}")
    except Exception as e:
        logger.warning(f"Error inesperado al cargar el modelo: {str(e)}")
    return delay_model

def get_dataset() -> pd.DataFrame:
    try:
        dataset_buffer = cloud_storage.download_dataset()
        dataset = pd.read_csv(dataset_buffer)
        logger.debug("Dataset descargado correctamente")
        return dataset
    except GoogleStorageError as e:
        logger.warning(f"Error al descargar el dataset desde GCS: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        logger.warning(f"Error inesperado al descargar el dataset: {str(e)}")
        return pd.DataFrame()