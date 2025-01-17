from pydantic import BaseModel, Field, model_validator
from typing import List, Annotated
from typing_extensions import Literal
from pydantic_core import PydanticCustomError

class Flight(BaseModel):
    OPERA: Annotated[
        str,
        Field(
            min_length=1,
            description="Operador del vuelo",
            json_schema_extra={
                "error_messages": {
                    "min_length": "El campo 'opera' debe ser un string no vacío."
                }
            }
        )
    ]
    TIPOVUELO: Literal["I", "N"] = Field(
        description="Tipo de vuelo: I (Internacional) o N (Nacional)",
        json_schema_extra={
            "error_messages": {
                "type": "El campo 'tipovuelo' debe ser 'I' o 'N'."
            }
        }
    )
    MES: Annotated[
        int,
        Field(
            ge=1, 
            le=12,
            description="Mes del vuelo (1-12)",
            json_schema_extra={
                "error_messages": {
                    "less_than_equal": "El campo 'mes' debe ser menor o igual a 12.",
                    "greater_than_equal": "El campo 'mes' debe ser mayor o igual a 1.",
                    "type": "El campo 'mes' debe ser un número entero."
                }
            }
        )
    ]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opera": "LATAM",
                    "tipovuelo": "I",
                    "mes": 6
                }
            ]
        }
    }

class FlightRequest(BaseModel):
    flights: Annotated[
        List[Flight],
        Field(
            min_length=1,
            description="Lista de vuelos a procesar",
            json_schema_extra={
                "error_messages": {
                    "min_length": "La lista 'flights' debe contener al menos un elemento.",
                    "type": "El campo 'flights' debe ser una lista de vuelos."
                }
            }
        )
    ]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "flights": [
                        {
                            "opera": "LATAM",
                            "tipovuelo": "I",
                            "mes": 6
                        }
                    ]
                }
            ]
        }
    }

    # Si necesitas validaciones más complejas, puedes usar model_validator
    @model_validator(mode='after')
    def validate_flights(self) -> 'FlightRequest':
        if not self.flights:
            raise PydanticCustomError(
                'custom_error',
                'La lista de vuelos no puede estar vacía'
            )
        return self