from pydantic import BaseModel
from typing import List

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
    Comments: str
    Date_Recorded: str

class SoilParameterList(BaseModel):
    Soil: Soil
    Parameters: List[Parameter]

class ParameterCreate(BaseModel):
    Hum: float
    Temp: float
    Ec: float
    Ph: float
    Comments: str

class SoilCreate(BaseModel):
    Soil_Name: str
    Loc_Longitude: float
    Loc_Latitude: float    

class CreateItem(BaseModel):
    Soil: SoilCreate
    Parameters: ParameterCreate

class AddParameter(BaseModel):
    Soil_ID: int
    Parameters: ParameterCreate

class DeleteParameter(BaseModel):
    Parameter_ID: int

class DeleteSoil(BaseModel):
    Soil_ID: int

class DeleteResponse(BaseModel):
    message: str