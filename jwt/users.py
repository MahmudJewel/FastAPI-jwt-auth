from fastapi import APIRouter, FastAPI

router = APIRouter(
    prefix="/jwt",
    tags=["jwt"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def home():
    return {"msg": "JWT page initialized successfully"}
