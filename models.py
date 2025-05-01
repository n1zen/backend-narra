from pydantic import BaseModel
from typing import List

class SensorData(BaseModel):
    Moist: float
    Temp: float
    EC: float
    pH: float

class Soil(BaseModel):
    Soil_ID: str
    Soil_Name: str
    Loc_Longitude: float
    Loc_Latitude: float

class Parameter(BaseModel):
    Parameter_ID: str
    Soil_ID: str
    Hum: float
    Temp: float
    Ec: float
    Ph: float
    Date_Recorded: str

class SoilParameterList(BaseModel):
    Soil: Soil
    Parameters: List[Parameter]