
from datetime import datetime
import bcrypt
from dto import sign_dto, res_dto
from sqlalchemy.orm import Session
from entity.user_entity import UserEntity

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def sign_up(reqDTO: sign_dto.ReqSignUp, db: Session):
    # 유저가 있는지 없는지 부터 확인
    userEntity: UserEntity = db.query(UserEntity).filter(
        UserEntity.id == reqDTO.id).first()
    
    if (userEntity != None):
        resDTO = res_dto.ResDTO(
            code=1,  # 문제가 생길 경우 1 / 정상일 경우 코드 0
            message="이미 존재하는 아이디입니다."
        )
        encodedResDTO = jsonable_encoder(resDTO)
        return JSONResponse(status_code=400, content=encodedResDTO)
    
    db_user = UserEntity(
        id=reqDTO.id,
        password=bcrypt.hashpw(
            reqDTO.password.encode("utf-8"), bcrypt.gensalt()),
        simple_desc=reqDTO.simpleDesc if reqDTO.simpleDesc else "한 줄 소개가 없습니다.",
        profile_image = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        role = "BLOGER", # 하드코딩
        create_date=datetime.now(),
    )
    
    try:
        db.add(db_user)
        db.flush()
    except Exception as e:
        db.rollback()
        print(e)
        resDTO = res_dto.ResDTO(
            code=99,
            message="서버 내부 에러입니다.",
            content=e
        )
        
        encodedError = jsonable_encoder(resDTO)
        return JSONResponse(status_code=500, content=encodedError)
    finally:
        db.commit()
        
    db.refresh(db_user)
    
    resDTO = res_dto.ResDTO(
        code=0,
        message="성공",
        content=sign_dto.ResSignUp(
            idx=db_user.idx
        )
    )
    
    encodedResDTO = jsonable_encoder(resDTO)
    return JSONResponse(status_code=201, content=encodedResDTO)