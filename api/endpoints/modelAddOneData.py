from collections import Counter
from typing import *
import joblib
import math
import pandas as pd
import random
from fastapi import HTTPException, Depends, APIRouter

nbrLostRows = 5000

maxNormalNumbers = 50
maxStarNumbers = 12
minNumbers = 1
numberOfNormalNumber = 5
numberOfStarNumber = 2

router = APIRouter(
    prefix="/api",
    tags=["model"],
    responses={404: {"description": "Not found"}},
)

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

@router.put("/model", tags=["model"])
async def add_data(date, ticket, winner, gain):
    """
        Add one more data to the data set. You should give : \n
        -- A date : yyyy-mm-dd\n
        -- A ticket should be like : N1 N2 N3 N4 N5 S1 S2\n
        With N(ormal) numbers between 1 and 50 and the S(tars) numbers between 1 and 12\n
        -- A winner : number of winners\n
        -- A gain : any number without any symbol\n
    """

    winner = int(winner)
    gain = int(gain)
    ticket = userTicket(ticket)

    # Build datas
    generations = [ticket]
    for i in range(nbrLostRows):
        # generate a list of random numbers
        set = sorted(random.sample(range(1, 51), 5)).__add__(sorted(random.sample(range(1, 13), 2)))
        # check if the set is different from the wining set or is not already generated
        while (set in generations):
            set = sorted(random.sample(range(1, 51), 5)).__add__(sorted(random.sample(range(1, 13), 2)))
        generations.append(set)
    # Load the data file
    finalFile = open('./datasource/euromillions_' + str(nbrLostRows+1) + '.csv', 'a+')
    # Write the winning ticket
    converted_ticket = [str(element) for element in ticket]
    print("converted_ticket", converted_ticket)
    finalFile.write(date + ';' + ';'.join(converted_ticket) + ';' + str(winner) + ';' + str(gain) + ';win\n')
    # Write all generated datas
    for generation in generations[1:]:
        converted_generation = [str(element) for element in generation]
        finalFile.write(date + ';' + ';'.join(converted_generation) + ';0;0;lose\n')
    finalFile.close()
    # Load the model from the file
    model = joblib.load('./api/endpoints/model/random_forest.joblib')
    # Fit the model with the wining ticket
    model.fit([ticket], ['win'])
    # Fit the model with all lose tickets
    model.fit(generations[1:], ['lose'] * (nbrLostRows))
    # Save the model to the file
    joblib.dump(model, './api/endpoints/model/random_forest.joblib')

