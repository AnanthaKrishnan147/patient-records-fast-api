from fastapi import FastAPI , Path # we just import the class fastapi 
import json

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
def view_patient(patient_id : str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error':'patient is not found motherfucker'}