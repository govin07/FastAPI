from fastapi import FastAPI, Path, HTTPException , Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(..., description='ID of the patient',examples=['p001'])]
    name:Annotated[str,Field(...,description='name of the patient',examples='rahul')]
    city:Annotated[str, Field(..., description='city where patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=0,description='Age of the Patient')]
    gender:Annotated[Literal['Male','Female','Other'],Field(..., description='gender of the patient')]
    height:Annotated[float,Field(..., gt=0, description='Height of the Pateint ')]
    weight:Annotated[float,Field(..., description='Weight of the Patient')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'UnderWeight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'




def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {'message': 'Patient Management System'}


@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage Patients'}

@app.get("/view")
def viewData():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def viewPatient(patient_id:str = Path(..., description="ID of the patient in the DB",example='p001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.get('/sort')
def short_patients(sort_by:str = Query(..., description="sort on the basic of height weight or bmi"), order:str = Query('asc',description="sort in asc or desc order") ):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='invalid order select between asc and desc')
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient) 
