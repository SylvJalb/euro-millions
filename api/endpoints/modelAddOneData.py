from fastapi import APIRouter, Depends
import joblib
import random

nbrLostRows = 5000

router = APIRouter(
    prefix="/api",
    tags=["model"],
    responses={404: {"description": "Not found"}},
)

@router.put("/model", tags=["model"])
async def add_data(date, ticket, winner, gain):
    """
        Add one more data to the data set. You should give a date (yyyy-mm-dd), a ticket (N1 N2 N3 N4 N5 E1 E2), 
        if it's a winning one (1 for win and 0 for lose) and finally the gain (any number without any symbol)
    """
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
    finalFile = open('../../datasource/euromillions_' + str(nbrLostRows+1) + '.csv', 'a+')
    # Write the winning ticket
    converted_ticket = [str(element) for element in ticket]
    finalFile.write(date + ';' + ';'.join(converted_ticket) + ';' + str(winner) + ';' + str(gain) + ';win\n')
    # Write all generated datas
    for generation in generations[1:]:
        converted_generation = [str(element) for element in generation]
        finalFile.write(date + ';' + ';'.join(converted_generation) + ';0;0;lose\n')
    finalFile.close()
    # Load the model from the file
    model = joblib.load('./model/random_forest.joblib')
    # Fit the model with the wining ticket
    model.fit([ticket], ['win'])
    # Fit the model with all lose tickets
    model.fit(generations[1:], ['lose'] * (nbrLostRows))
    # Save the model to the file
    joblib.dump(model, './model/random_forest.joblib')
