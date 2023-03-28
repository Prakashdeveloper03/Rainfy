from joblib import load  # for loading model pickle file
from datetime import datetime  # for data & time functions
import numpy as np  # for array conversion

# FastAPI is a modern, fast (high-performance), web framework for building APIs with Python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()  # instance of FastAPI class

# mount static folder files to /static route
app.mount("/static", StaticFiles(directory="static"), name="static")

# sets the templates folder for the app
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def load_model():
    app.model = load("./models/CatBoostClassifier.pkl")
    print("Model Loaded")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Function to render `index.html` at route '/' as a get request

    __Args__:
    - request (Request): request in path operation that will return a template

    __Returns__:
    - TemplateResponse: render `index.html`
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/predictor", response_class=HTMLResponse)
async def read_item(request: Request):
    """
    Function to render `predictor.html` at route '/predictor' as a get request

    __Args__:
    - request (Request): request in path operation that will return a template

    __Returns__:
    - TemplateResponse: render `predictor.html`
    """
    return templates.TemplateResponse("predictor.html", {"request": request})


@app.post("/predictor/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    date: str = Form(...),
    mintemp: float = Form(...),
    maxtemp: float = Form(...),
    rainfall: float = Form(...),
    evaporation: float = Form(...),
    sunshine: float = Form(...),
    windgustdir: float = Form(...),
    windgustspeed: float = Form(...),
    winddir9am: float = Form(...),
    winddir3pm: float = Form(...),
    windspeed9am: float = Form(...),
    windspeed3pm: float = Form(...),
    humidity9am: float = Form(...),
    humidity3pm: float = Form(...),
    pressure9am: float = Form(...),
    pressure3pm: float = Form(...),
    cloud9am: float = Form(...),
    cloud3pm: float = Form(...),
    temp9am: float = Form(...),
    temp3pm: float = Form(...),
    raintoday: float = Form(...),
    location: float = Form(...),
):
    """
    Function to predict tomorrow's rainfall and show the result by rendering `predictor.html` at route '/predictor/predict'

    __Args__:
    - request (Request): request in path operation that will return a template
    - date (str): the date for which rainfall is to be predicted (format: YYYY-MM-DD)
    - mintemp (float): minimum temperature in Celsius
    - maxtemp (float): maximum temperature in Celsius
    - rainfall (float): amount of rainfall in mm
    - evaporation (float): amount of evaporation in mm
    - sunshine (float): number of hours of sunshine
    - windgustdir (float): direction of the strongest gust in degrees
    - windgustspeed (float): speed of the strongest gust in km/h
    - winddir9am (float): direction of the wind at 9am in degrees
    - winddir3pm (float): direction of the wind at 3pm in degrees
    - windspeed9am (float): speed of the wind at 9am in km/h
    - windspeed3pm (float): speed of the wind at 3pm in km/h
    - humidity9am (float): relative humidity at 9am in percent
    - humidity3pm (float): relative humidity at 3pm in percent
    - pressure9am (float): atmospheric pressure at 9am in hPa
    - pressure3pm (float): atmospheric pressure at 3pm in hPa
    - cloud9am (float): fraction of sky obscured by cloud at 9am
    - cloud3pm (float): fraction of sky obscured by cloud at 3pm
    - temp9am (float): temperature in Celsius at 9am
    - temp3pm (float): temperature in Celsius at 3am
    - raintoday (float): amount of rainfall today in mm
    - location (float): location id number

    __Returns__:
    - Template: render `predictor.html`
    """
    day = float(datetime.strptime(date, "%Y-%m-%d").day)
    month = float(datetime.strptime(date, "%Y-%m-%d").month)
    input_list = [
        location,
        mintemp,
        maxtemp,
        rainfall,
        evaporation,
        sunshine,
        windgustdir,
        windgustspeed,
        winddir9am,
        winddir3pm,
        windspeed9am,
        windspeed3pm,
        humidity9am,
        humidity3pm,
        pressure9am,
        pressure3pm,
        cloud9am,
        cloud3pm,
        temp9am,
        temp3pm,
        raintoday,
        month,
        day,
    ]
    pred = app.model.predict([np.array(input_list)])[0]
    output = (
        "Tomorrow, No rainfall!" if (pred == 0) else "Tomorrow, We will have rainfall!"
    )
    return templates.TemplateResponse(
        "predictor.html", context={"request": request, "prediction": output}
    )
