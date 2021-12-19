from collections import Counter
from typing import *
import joblib
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/api",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)

maxNormalNumbers = 50
maxStarNumbers = 12
minNumbers = 1
numberOfNormalNumber = 5
numberOfStarNumber = 2

def isListOfUniqueElement(listOfElement: List[int]):
    dictOfNumberOfOccurrencesByElement = Counter(listOfElement)
    return all(i == 1 for i in list(dictOfNumberOfOccurrencesByElement.values()))


def userInputNumbers(nOfNumbers: int, maxNumber: int, inputString: str):
    user_list = inputString.copy()

    checkElementIsUnique = isListOfUniqueElement(user_list)

    if checkElementIsUnique is True:
        if len(user_list) == nOfNumbers:
            for i in range(nOfNumbers):
                if type(user_list[i]) is str:
                    user_list[i] = int(user_list[i])
                else:
                    raise HTTPException(status_code=404, detail="Type error : one or more entries are not numbers")
                if not (user_list[i] <= maxNumber) or not (user_list[i] >= minNumbers):
                    raise HTTPException(status_code=404, detail="Limit reached : one or more numbers are greater than 50 or minor 1")
        else:
            raise HTTPException(status_code=404, detail="Count of number error : space between values is missing")
    else:
        raise HTTPException(status_code=404, detail="Not unique : one or more numbers are not unique")
    return user_list


def userTicket(ticket):
    user_list = ticket.split(" ")
    normalNumbersPart = user_list[0:5]
    starNumbersPart = user_list[5:7]

    normalNumberList = userInputNumbers(numberOfNormalNumber, maxNormalNumbers, normalNumbersPart)
    starNumberList = userInputNumbers(numberOfStarNumber, maxStarNumbers, starNumbersPart)

    combinationValues = normalNumberList + starNumberList

    return combinationValues


@router.post("/predict", tags=["predict"])
async def get_ml_stat(ticket):
    """
        Calculate the chance of winning for a given set of numbers and additional numbers (in ticket).
        Use machine learning model to calculate the chance of winning.
    """
    ticket = userTicket(ticket)
    # Load the model from the file
    model = joblib.load('./api/endpoints/model/random_forest.joblib')
    # Predict the result
    result = model.predict_proba([ticket])[0]
    # Return the result (chance to win)
    return result[1]