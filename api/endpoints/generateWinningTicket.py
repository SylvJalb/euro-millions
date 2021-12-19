from fastapi import APIRouter, Depends
import joblib
import random

router = APIRouter(
    prefix="/api",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)
    
@router.get("/predict", tags=["predict"])
async def generate_winning_ticket():
    # Load the model from the file
    model = joblib.load('./api/endpoints/model/random_forest.joblib')
    # initialize variables
    bestResult = 0.0
    bestTicket = []
    # generate random tickets and get the best one
    for i in range(200):
        # generate a random ticket
        set = sorted(random.sample(range(1, 51), 5)).__add__(sorted(random.sample(range(1, 13), 2)))
        # predict the proba to win
        result = model.predict_proba([set])[0]
        # compare best result
        if result[1] > bestResult:
            bestResult = result[1]
            bestTicket = set
    return bestTicket, bestResult
