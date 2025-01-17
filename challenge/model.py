import pandas as pd
from typing import Tuple, Union, List
from challenge.services.process_data import ProcessData
from challenge.errors.process_data import ProcessDataError
from challenge.errors.model import FitError, PredictError
import numpy as np
from challenge.storage.gcp_storage import GoogleCloudStorage
import xgboost as xgb
from io import BytesIO
import tempfile
from challenge.utils.logger import logger

class DelayModel:

    def __init__(
        self
    ):
        #self._model = None # Model should be saved in this attribute.
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01)
        self.storage_client = GoogleCloudStorage()

    def load_model(self, model_buffer) -> None:
        model_buffer.seek(0)
        #self._model.load_model(model_buffer)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(model_buffer.read())
            temp_file_path = temp_file.name
        self._model.load_model(temp_file_path)
    
    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        try:
            data_processor = ProcessData(data)
            
            if target_column is not None:
                features, target = data_processor.preprocess_for_training()
                return features, target
            else:
                features = data_processor.preprocess_for_serving()
                return features
        except ProcessDataError as e:
            raise ProcessDataError(f"Error durante el preprocesamiento de datos: {str(e)}") from e
        except Exception as e:
            raise ProcessDataError(f"Error inesperado durante el preprocesamiento de datos: {str(e)}") from e
        

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        target_values = target.iloc[:, 0]  # o target[target.columns[0]]
        
        n_y0 = np.sum(target_values == 0)
        n_y1 = np.sum(target_values == 1)
        scale = n_y0/n_y1

        try:
            self._model.set_params(scale_pos_weight=scale)
            self._model.fit(features, target)
            
            # Obtener el modelo en formato JSON o binario
            json_model = self._model.get_booster().save_raw()  # Esto devuelve bytes
            
            buffer = BytesIO(json_model)
        except Exception as e:
            raise FitError(f"Error al entrenar el modelo: {str(e)}") from e
        
        # Subir el buffer a GCS
        try:
            self.storage_client.upload(buffer)
        except Exception as e:
            logger.warning(f"Error al subir el modelo a GCS: {str(e)}")
        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        try:
            predictions = self._model.predict(features)
            return predictions.tolist()
        except Exception as e:
            raise PredictError(f"Error al predecir los retrasos: {str(e)}") from e