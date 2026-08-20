from fastapi import FastAPI , Path , HTTPException , Query # we just import the class fastapi 
import json
from pydantic import BaseModel , Field , computed_field
from typing import Literal , Annotated

class Patient(BaseModel):
    id : Annotated[str , Field(... , description="id of the patient" , example='P001')]
    name : Annotated[str , Field... , description="name of the patient" , example='ananthan' , max_length = 59)]
    city : Annotated[str , Field(... , description="city of the patient" , example='alappuzha')]
    age : Annotated[str , Field(... , description="age of the patient" , gt=0 )]
    gender : Annotated[Literal['male' , 'female'] , Field(... , description="gender of the patient")]
    height : Annotated[int , Field(... , gt = 0 , description = "The height of the patient")]
    weight : Annotated[int , Field(... , gt = 0 , description="The weight of the patient")]

    @computed_field
    @property
    def bmi(self) -> float :
        bmi = self.weight/(self.height**2)
        return bmi 

    @computed_field
    @property
    def verdit(self) -> str :
        

app = FastAPI()   # create an object of class fastapi 

def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)
    return data

@app.get("/")     # in order to create an endpoint we need to define a route , we used get method the request method will be a get request 
# in the above we have to define a path or route
def hello ():
    return {'message':'patient management system api'}

@app.get("/about")
def about():
    return{'message':'A fully functional website to handle patient records'}

@app.get("/view")
def view():
    data = load_data()
    return data 

@app.get("/patient/{patient_id}")
def view_patient(patient_id : str = Path(... , description = "the details of the patient from the given id" , example = "P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(
        status_code = 404 ,
        detail = "Patient not found"
    )

@app.get("/sort/")
def sort_patients(sort_by:str=Query(... , description="Sort on the basis of height , weight or bmi" , example="height") , order_by:str=Query('asc' , description="Sort in ascending or descending order ?")):
    if sort_by not in ['height' , 'weight' , 'bmi']:
        raise HTTPException(status_code = 400 , detail=f"Enter the correct sort by value")
    if order_by not in ['asc' , 'des']:
        raise HTTPException(status_code = 400 , detail=f"Enter the correct order by value")

    sort_order = True if order_by == 'des' else False

    data = load_data()

    sorted_dict = sorted(data.values() , key = lambda x:x.get(sort_by, 0) , reverse = sort_order)

    return sorted_dict

