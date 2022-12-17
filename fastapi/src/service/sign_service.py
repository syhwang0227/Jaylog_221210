
from datetime import datetime
import bcrypt
from dto import sign_dto
from sqlalchemy.orm import Session
from entity.user_entity import UserEntity
from util import functions
import time
from config import constants
import jwt
from fastapi.encoders import jsonable_encoder

USER_ID_EXIST_ERROR = {"code" : 1, "message" : "이미 존재하는 아이디 입니다."}
ID_NOT_EXIST_ERROR = {"code": 2, "message" : "가입되지 않은 아이디 입니다."}
DELETED_USER_ERROR = {"code": 3, "message" : "삭제된 유저입니다."}
PASSWORD_INCORRECT_ERROR = {"code": 4, "message" : "비밀번호가 틀립니다."}
INTERNAL_SERVER_ERROR = {"code" : 99, "message" : "서버 내부 에러입니다."}

def sign_in(reqDTO: sign_dto.ReqSignIn, db: Session):
    userEntity : UserEntity = db.query(UserEntity).filter(
        UserEntity.id == reqDTO.id).first()
    
    # 아이디가 없을 경우
    if userEntity == None:
        return functions.res_generator(status_code=400, error_dict=ID_NOT_EXIST_ERROR)
    
    # 아이디가 삭제된 경우 / 자주 있는 경우는 아님
    if userEntity.delete_date != None:
        return functions.res_generator(status_code=400, error_dict=DELETED_USER_ERROR)
        
    # 비밀번호가 틀릴 경우
    if not bcrypt.checkpw(reqDTO.password.encode("utf-8"), userEntity.password.encode("utf-8")):
        return functions.res_generator(status_code=400, error_dict=PASSWORD_INCORRECT_ERROR)
        
    # 정상
    accessJwtDTO = sign_dto.AccessJwt(
        idx=userEntity.idx,
        id=userEntity.id,
        simpleDesc=userEntity.simple_desc,
        profileImage=userEntity.profile_image,
        role=userEntity.role,
        exp=time.time() + constants.JWT_ACCESS_EXP_SECONDS
    )
    
    accessToken = jwt.encode(jsonable_encoder(accessJwtDTO), constants.JWT_SALT, algorithm="HS256")
    
    refreshJwtDTO = sign_dto.RefreshJwt(
        idx=userEntity.idx,
        exp=time.time() + constants.JWT_REFRESH_EXP_SECONDS
    )
    
    refreshToken = jwt.encode(jsonable_encoder(refreshJwtDTO), constants.JWT_SALT, algorithm="HS256")
    
    resSignInDTO = sign_dto.ResSignIn(
        accessToken=accessToken,
        refreshToken=refreshToken
    )
    
    return functions.res_generator(content=resSignInDTO) 


def sign_up(reqDTO: sign_dto.ReqSignUp, db: Session):
    # 유저가 있는지 없는지 부터 확인
    userEntity: UserEntity = db.query(UserEntity).filter(
        UserEntity.id == reqDTO.id).first()
    
    if (userEntity != None):
        return functions.res_generator(status_code=400, error_dict=USER_ID_EXIST_ERROR)
        # resDTO = res_dto.ResDTO(
        #     code=1,  # 문제가 생길 경우 1 / 정상일 경우 코드 0
        #     message="이미 존재하는 아이디입니다."
        # )
        # encodedResDTO = jsonable_encoder(resDTO)
        # return JSONResponse(status_code=400, content=encodedResDTO)
    
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
        return functions.res_generator(status_code=500, error_dict=INTERNAL_SERVER_ERROR)
        # resDTO = res_dto.ResDTO(
        #     code=99,
        #     message="서버 내부 에러입니다.",
        #     content=e
        # )
        
        # encodedError = jsonable_encoder(resDTO)
        # return JSONResponse(status_code=500, content=encodedError)
    
    finally:
        db.commit()
        
    db.refresh(db_user)
    
    return functions.res_generator(status_code=201, content=sign_dto.ReqSignUp(idx=db_user.idx))
    
    # 위 코드 (return ~) 한 줄로 코드가 간단해진 것을 볼 수 있다.
    # resDTO = res_dto.ResDTO(
    #     code=0,
    #     message="성공",
    #     content=sign_dto.ResSignUp(
    #         idx=db_user.idx
    #     )
    # )
    
    # encodedResDTO = jsonable_encoder(resDTO)
    # return JSONResponse(status_code=201, content=encodedResDTO)