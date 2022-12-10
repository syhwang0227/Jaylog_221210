
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from dto import sign_dto
from service import sign_service

router = APIRouter()


@router.post("/test")
async def test(reqDTO: sign_dto.ReqSignUp, db: Session = Depends(get_db)):
    return sign_service.sign_up(reqDTO, db)