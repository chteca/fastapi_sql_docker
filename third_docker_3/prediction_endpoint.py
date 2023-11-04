from fastapi import FastAPI, Depends
from fastapi import HTTPException
from pydantic import BaseModel
import contextlib
import pickle
from preprocess import DataPreprocessor
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class PredictionInput(BaseModel):
    ID: int
    A1_Score: int
    A2_Score: int
    A3_Score: int
    A4_Score: int
    A5_Score: int
    A6_Score: int
    A7_Score: int
    A8_Score: int
    A9_Score: int
    A10_Score: int
    age: float
    gender: str
    ethnicity: str
    jaundice: str
    austim: str
    contry_of_res: str
    used_app_before: str
    result: float
    age_desc: str
    relation: str
    ASD: int


class PredictionOutput(BaseModel):
    ASD: int

class RFModel:
    def __init__(self):
        self.model = None

    def load_model(self):
        model_file = "./model/best_model.sav"  
        self.model = pickle.load(open(model_file, 'rb'))
        

    def predict_output(self, input: PredictionInput) -> PredictionOutput:
        if not self.model:
            raise RuntimeError("Model files are not found!")
        data = pd.DataFrame({'ID': [input.ID],
                             'A1_Score': [input.A1_Score],
                             'A2_Score': [input.A2_Score],
                             'A3_Score': [input.A3_Score],
                             'A4_Score': [input.A4_Score],
                             'A5_Score': [input.A5_Score],
                             'A6_Score': [input.A6_Score],
                             'A7_Score': [input.A7_Score],
                             'A8_Score': [input.A8_Score],
                             'A9_Score': [input.A9_Score],
                             'A10_Score': [input.A10_Score],
                             'age': [input.age],
                             'gender': [input.gender],
                             'ethnicity': [input.ethnicity],
                             'jaundice': [input.jaundice],
                             'austim': [input.austim],
                             'contry_of_res': [input.contry_of_res],
                             'used_app_before': [input.used_app_before],
                             'result': [input.result],
                             'age_desc': [input.age_desc],
                             'relation': [input.relation],
                             'ASD': [input.ASD]})

        data = DataPreprocessor(dataset=data).preprocess_data()

        output = self.model.predict(data.drop(['ASD'], axis=1))
        ASD = output[0]
        return PredictionOutput(ASD=ASD)


rf_model = RFModel()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    rf_model.load_model()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/prediction", response_model=PredictionOutput)
async def get_prediction(input: PredictionInput):
    output = rf_model.predict_output(input)
    return output