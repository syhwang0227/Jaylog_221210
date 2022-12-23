import time
from datetime import datetime

import bcrypt
import jwt
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import constants
from dto import post_dto, sign_dto
from entity.post_entity import PostEntity
from entity.user_entity import UserEntity
from fastapi import Request
from util import functions

AUTHORIZATION_ERROR = {"code":1, "message": "인증되지 않은 사용자입니다."}
ID_ERROR = {"code":2, "message": "계정에 문제가 있습니다."}
INTERNAL_SERVER_ERROR = {"code": 99, "message": "서버 내부 에러입니다."}


def get_posts(db: Session):
    post_entity_list : list[PostEntity] = db.query(
        PostEntity).filter(PostEntity.delete_date == None).order_by(
            PostEntity.create_date.desc()).all()
    
    res_main_post_list = list(map(post_dto.ResMainPost.toDTO, post_entity_list))
    
    return functions.res_generator(content=res_main_post_list)


def insert_post(request: Request, req_dto: post_dto.ReqInsertPost, db: Session) -> JSONResponse:
    if not request.state.user:
        return functions.res_generator(status_code=401, error_dict=AUTHORIZATION_ERROR)
    
    auth_user: sign_dto.AccessJwt = request.state.user
    
    user_entity : UserEntity = db.query(UserEntity).filter(
        UserEntity.idx == auth_user.idx).filter(
            UserEntity.delete_date == None).first()
        
    if(user_entity == None):
        return functions.res_generator(400, ID_ERROR)
    
    new_post = PostEntity(
        title=req_dto.title,
        content=req_dto.content,
        summary=req_dto.summary,
        thumbnail=req_dto.thumbnail,
        user_idx=user_entity.idx
    )
    
    try:
        db.add(new_post)
        db.flush()
    except Exception as e:
        db.rollback()
        print(e)
        return functions.res_generator(status_code=500, error_dict=INTERNAL_SERVER_ERROR, content=e)
    finally:
        db.commit()
    
    db.refresh(new_post)   
    
    return functions.res_generator(status_code=201, content=post_dto.ReqInsertPost(idx=new_post.idx))