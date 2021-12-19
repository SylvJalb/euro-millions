from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)

@router.get("/predict", tags=["predict"])
async def generate_winning_ticket():
    return 1

