from fastapi import Depends, FastAPI
from api.endpoints import predictWinningTicketML, predictWinningTicketStats, modelRetrain, generateWinningTicket, modelAddOneData, modelInformation
import joblib

description = """
Euromillion App API helps you to win (we hope). 🚀

## Prediction

You can :

* **Find the probabilities of a winning ticket**.
* **Generate an "high probability of winning" tiket**.

## Model

You can :

* **Add more data for the modele**.
* **Retrain the model**.
* **Get model's informations**.

"""

app = FastAPI(
    title="EuromillionApp",
    description=description,
    version="0.0.1",
    contact={
        "name": "Sylvain Jalbert & Romain Royer",
    },
)

app.include_router(predictWinningTicketML.router)
app.include_router(predictWinningTicketStats.router)
app.include_router(modelRetrain.router)
app.include_router(generateWinningTicket.router)
app.include_router(modelAddOneData.router)
app.include_router(modelInformation.router)




