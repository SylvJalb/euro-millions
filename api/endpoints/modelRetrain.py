from fastapi import APIRouter, Depends

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
    return 1