from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import random
import joblib

nbrLostRows = 5000

router = APIRouter(
    prefix="/api/model",
    tags=["model"],
    responses={404: {"description": "Not found"}},
)

@router.post("/retrain", tags=["model"])
async def retrain_model():
    """
        Retrain the previous model including the last data you added previously.
    """
    df = pd.read_csv('./datasource/euromillions_' + str(nbrLostRows+1) + '.csv', sep=";")
    dfTrain = df[:int(len(df) * 0.66)]
    model = RandomForestClassifier(n_estimators=1000, random_state=0, verbose=2)
    model.fit(dfTrain[['N1', 'N2', 'N3', 'N4', 'N5', 'E1', 'E2']].values, dfTrain['Result'].values)
    joblib.dump(model, './api/endpoints/model/random_forest.joblib')
    raise HTTPException(status_code=200, detail="Model successfully trained !")
