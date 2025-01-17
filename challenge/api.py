import fastapi
from challenge.dto.flight import FlightRequest
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from challenge.errors.process_data import ProcessDataError
from challenge.errors.model import FitError, PredictError
from fastapi import Request
import challenge.utils.helpers as util
import pandas as pd
from challenge.utils.logger import logger

app = fastapi.FastAPI()

delay_model = util.init_model()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(error.get("msg"))
    
    return JSONResponse(
        status_code=400,
        content={"detail": errors}
    )
        
@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: FlightRequest) -> dict:
    logger.debug(f"Inicio del metodo predict. Request: {request}")
    try:
        flights_data = [flight.model_dump() for flight in request.flights]
        flights_df = pd.DataFrame(flights_data)

        features = delay_model.preprocess(flights_df)
        logger.debug(f"features: {features}")

        # Realizar la predicción
        predictions = delay_model.predict(features)

        return {
            "predict": predictions
        }
    except ProcessDataError as e:
        logger.error(f"Error en el preprocesamiento de datos: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error en el preprocesamiento de datos"}
        )
    except PredictError as e:
        logger.error(f"Error en la prediccion de datos: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error en la prediccion de los datos"}
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error inesperado"}
        )
        
    
@app.post("/train", status_code=200)
async def post_train() -> dict:
    try:
        dataset = util.get_dataset()
        features, target = delay_model.preprocess(
            data=dataset,
            target_column="delay"
        )
        delay_model.fit(features=features, target=target)
        return {
            "status": "OK"
        }
    except ProcessDataError as e:
        logger.error(f"Error en el preprocesamiento de datos: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error en el preprocesamiento de datos"}
        )
    except FitError as e:
        logger.error(f"Error en el entrenamiento del modelo: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error en el entrenamiento del modelo"}
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error inesperado"}
        )