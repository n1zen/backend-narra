from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from models import SensorData, Soil, Parameter, SoilParameterList
import aiomysql
from datetime import datetime

app = FastAPI()

async def get_db():
    async with aiomysql.connect(
        host="localhost",
        user="pi",
        password="raspi",
        db="narra"
    ) as conn:
        yield conn

def formatID(ID, id_of):
    if (id_of == "Parameter"):
        return "P" + str(ID).zfill(4)
    elif (id_of == "Soil"):
        return "S" + str(ID).zfill(4)

def formatDate(iso_date):
    date = datetime.fromisoformat(str(iso_date))
    formatted = date.strftime("%b %d, %Y %I:%M %p")
    return formatted

@app.get("/")
def root():
    return {"Hello":"World"}

# Get all soils
@app.get("/soils", response_model=List[Soil])
async def get_soils(db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("SELECT Soil_ID, Soil_Name, ST_X(Soil_Location) as Loc_Longitude, ST_Y(Soil_Location) as Loc_Latitude FROM Soils")
        rows = await cur.fetchall()
        soils = []
        for row in rows:
            soil = Soil(
                Soil_ID=formatID(row[0], "Soil"),
                Soil_Name=row[1],
                Loc_Longitude=row[2],
                Loc_Latitude=row[3]
            )
            soils.append(soil)
        return soils

# Get parameters of a soil
@app.get("/soils/parameters/{Soil_ID}", response_model=SoilParameterList)
async def get_parameters(Soil_ID: int, db=Depends(get_db)) -> SoilParameterList:
    async with db.cursor() as cur:
        await cur.execute("SELECT Soil_ID, Soil_Name, ST_X(Soil_Location) as Loc_Longitude, ST_Y(Soil_Location) as Loc_Latitude FROM Soils WHERE Soil_ID = %s", (Soil_ID))
        row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Soil not found")
        soil = Soil(
            Soil_ID = formatID(row[0],"Soil"),
            Soil_Name = row[1],
            Loc_Longitude = row[2],
            Loc_Latitude = row[3],
        )
        await cur.execute("SELECT Parameters_ID, HUM, TEMP, EC, PH, Date_Recorded FROM Parameters WHERE Soil_ID = %s", (Soil_ID))
        rows = await cur.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="Soil Parameters not found")
        parameters = []
        for row in rows:
            parameter = Parameter(
                Parameter_ID=formatID(row[0],"Parameter"),
                Soil_ID=formatID(Soil_ID,"Soil"),
                Hum=row[1],
                Temp=row[2],
                Ec=row[3],
                Ph=row[4],
                Date_Recorded=formatDate(row[5])
            )
            parameters.append(parameter)
        soil_parameters = SoilParameterList(
            Soil = soil,
            Parameters = parameters
        )
        return soil_parameters

# Get a parameter of a soil
@app.get("/soils/parameters/{Soil_ID}/{Parameter_ID}", response_model=SoilParameterList )
async def get_specific_parameter(Soil_ID: int, Parameter_ID: int, db=Depends(get_db)) -> SoilParameterList:
    async with db.cursor() as cur:
        await cur.execute("SELECT Soil_ID, Soil_Name, ST_X(Soil_Location) as Loc_Longitude, ST_Y(Soil_Location) as Loc_Latitude FROM Soils WHERE Soil_ID = %s", (Soil_ID))
        row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Soil not found")
        soil = Soil(
            Soil_ID = formatID(row[0],"Soil"),
            Soil_Name = row[1],
            Loc_Longitude = row[2],
            Loc_Latitude = row[3],
        )
        await cur.execute("SELECT Parameters_ID, HUM, TEMP, EC, PH, Date_Recorded FROM Parameters WHERE Parameters_ID = %s AND Soil_ID = %s", (Parameter_ID, Soil_ID))
        row = await cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Soil Parameter not found")
        parameter = Parameter(
            Parameter_ID=formatID(row[0],"Parameter"),
            Soil_ID=formatID(Soil_ID,"Soil"),
            Hum=row[1],
            Temp=row[2],
            Ec=row[3],
            Ph=row[4],
            Date_Recorded=formatDate(row[5])
        )
        soil_parameter = SoilParameterList(
            Soil = soil,
            Parameters = [parameter]
        )
        return soil_parameter
