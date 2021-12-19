from collections import Counter
from typing import *
import joblib
import math
import pandas as pd
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


@router.post("/predict/stats", tags=["predict"])
async def get_stat(ticket):
    """
        Calculate the chance of winning for a given set of numbers and additional numbers (in ticket).
        Use combinations to calculate the chance of winning.
    """
    # Get chance to win
    def combination(n, k):
        return math.factorial(n) // (math.factorial(k) * math.factorial(n-k))

    # Separate the numbers
    numbers, additionalNumbers = ticket[:5], ticket[5:]

    # import datas
    df = pd.read_csv('../datasource/euromillions.csv', sep=";")
    # define types of numbers
    df['N1'] = df['N1'].astype(int)
    df['N2'] = df['N2'].astype(int)
    df['N3'] = df['N3'].astype(int)
    df['N4'] = df['N4'].astype(int)
    df['N5'] = df['N5'].astype(int)
    df['E1'] = df['E1'].astype(int)
    df['E2'] = df['E2'].astype(int)

    # Get apparitions times
    count_number = df['N1'].value_counts().add(df['N2'].value_counts(), fill_value=0).add(df['N3'].value_counts(), fill_value=0).add(df['N4'].value_counts(), fill_value=0).add(df['N5'].value_counts(), fill_value=0)
    count_additional_number = df['E1'].value_counts().add(df['E2'].value_counts(), fill_value=0)

    # calculate the chance of winning for the main numbers
    chanceOfWinningNumbers = 1 / combination(count_number.index.max(), len(numbers))
    averageChanceNumbers = 0
    for number in numbers:
        averageChanceNumbers += 1 - (count_number[number] - count_number.mean()) / count_number.sum()
    averageChanceNumbers /= len(numbers)
    chanceOfWinningNumbers *= averageChanceNumbers
    # calculate the chance of winning for the additional numbers
    chanceOfWinningAdditionalNumbers = 1 / combination(count_additional_number.index.max(), len(additionalNumbers))
    averageChanceAdditionalNumbers = 0
    for number in additionalNumbers:
        averageChanceAdditionalNumbers += 1 - (count_additional_number[number] - count_additional_number.mean()) / count_additional_number.sum()
    averageChanceAdditionalNumbers /= len(additionalNumbers)
    chanceOfWinningAdditionalNumbers *= averageChanceAdditionalNumbers
    # return the chance of winning for all numbers
    return chanceOfWinningNumbers * chanceOfWinningAdditionalNumbers