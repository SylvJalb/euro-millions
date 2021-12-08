from collections import Counter
from typing import *

from fastapi import FastAPI

app = FastAPI()

maxNormalNumbers = 50
maxStarNumbers = 12
minNumbers = 1
numberOfNormalNumber = 5
numberOfStarNumber = 2
entreNormalNumberMessage = 'Enter 5 unique number between 1 and 50 separated by space : '
entreStarNumberMessage = 'Enter 2 unique number between 1 and 12 separated by space : '


def isListOfUniqueElement(listOfElement: List[int]):
    dictOfNumberOfOccurrencesByElement = Counter(listOfElement)
    return all(i == 1 for i in list(dictOfNumberOfOccurrencesByElement.values()))


def userInputNumbers(nOfNumbers: int, maxNumber: int, inputString: str):
    input_string = input(inputString)
    user_list = input_string.split()
    checkElementIsUnique = isListOfUniqueElement(user_list)

    if checkElementIsUnique is True:
        if len(user_list) == nOfNumbers:
            for i in range(nOfNumbers):
                if type(user_list[i]) is int:
                    user_list[i] = int(user_list[i])
                else:
                    exit("Type error : one or more entries are not numbers")
                if not (user_list[i] <= maxNumber) or not (user_list[i] >= minNumbers):
                    exit("Limit reached : one or more numbers are greater than 50 or minor 1 ")
        else:
            exit("Count of number error : space between values is missing")
    else:
        exit("Not unique : one or more numbers are not unique")
    return user_list


def userCombination():
    normalNumberList = userInputNumbers(numberOfNormalNumber, maxNormalNumbers, entreNormalNumberMessage)
    starNumberList = userInputNumbers(numberOfStarNumber, maxStarNumbers, entreStarNumberMessage)
    combinationValuesName = ["N1", "N2", "N3", "N4", "N5", "E1", "E2"]
    combinationValues = normalNumberList + starNumberList
    combinationDictFormat = {combinationValuesName[i]: combinationValues[i] for i in range(len(combinationValuesName))}

    print(combinationDictFormat)
    return combinationDictFormat


userCombination()


@app.post("/predict")
async def modelPrediction(combination):
    # return algo(combination)
    return 30, 70
