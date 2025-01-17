import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import challenge.utils.settings as env
import challenge.utils.helpers as util
from challenge.errors.process_data import MissingColumnError, PreprocessingError
from challenge.utils.logger import logger

class ProcessData:
    def __init__(self, data: pd.DataFrame):
        required_columns = ['OPERA', 'MES', 'TIPOVUELO']
        missing_columns = set(required_columns) - set(data.columns)
        if missing_columns:
            raise MissingColumnError(f"Faltan las siguientes columnas en el DataFrame: {', '.join(missing_columns)}")
        self.data = data
        self.threshold = env.THRESHOLD_IN_MINUTES
        self.feature_cols = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
        
    def __process_period_day(self) -> None:
        self.data['period_day'] = self.data['Fecha-I'].apply(util.get_period_day)
        return
    
    def __process_high_season(self) -> None:
        self.data['high_season'] = self.data['Fecha-I'].apply(util.is_high_season)
        return
    
    def __process_min_diff(self) -> None:
        self.data['min_diff'] = self.data.apply(util.get_min_diff, axis = 1)
        return
    
    def __process_delay(self) -> None:
        self.data['delay'] = np.where(self.data['min_diff'] > self.threshold, 1, 0)
        return
    
    def preprocess_for_training(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        try:
            self.__process_period_day()
            self.__process_high_season()
            self.__process_min_diff()
            self.__process_delay()
        except KeyError as e:
            raise MissingColumnError(f"Falta la columna {str(e)} en el DataFrame")
        except Exception as e:
            raise PreprocessingError(f"Ocurrió un error durante el preprocesamiento: {str(e)}")
        
        training_data = shuffle(self.data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state = 111)
        
        features = pd.concat([
            pd.get_dummies(training_data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(training_data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(training_data['MES'], prefix = 'MES')], 
            axis = 1
        )
        target = training_data['delay']
        return features[self.feature_cols], pd.DataFrame(target)
    
    def preprocess_for_serving(self) -> pd.DataFrame:
        data_serving = self.data.copy()
        #data_serving = data_serving[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM']]
        data_serving = data_serving[['OPERA', 'MES', 'TIPOVUELO']]
        data_processed = pd.concat([
            pd.get_dummies(data_serving['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data_serving['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data_serving['MES'], prefix = 'MES')], 
            axis = 1
        )
        
        data_processed = data_processed.reindex(columns=self.feature_cols, fill_value=0)

        return data_processed
        