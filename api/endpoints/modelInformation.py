from fastapi import APIRouter, Depends
import joblib

router = APIRouter(
    prefix="/api",
    tags=["model"],
    responses={404: {"description": "Not found"}},
)

@router.get("/model", tags=["model"])
async def informations_model():
    """
        Return model's informations : n_estimators, random_state and verbose which are the parameter 
        of the RandomForestClassifier we used.
    """
    model = joblib.load('./api/endpoints/model/random_forest.joblib')
    
    return model.get_params()