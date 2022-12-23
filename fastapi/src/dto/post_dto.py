from datetime import datetime
from pydantic import BaseModel
# 클래스 안에 __init__ 없는 이유: pydantic을 사용하므로
from entity.user_entity import UserEntity
from entity.post_entity import PostEntity


class ReqInsertPost(BaseModel):
    title : str
    thumbnail: str | None = None
    content : str
    summary: str


class ResInsertPost(BaseModel):
    idx: int
    
    class Config:
        orm_mode = True    

class ResMainPost(BaseModel):
    
    # class 안의 클래스
    class _Writer(BaseModel):
        idx: int
        id: str
        profileImage: str
        
        class Config:
            orm_mode = True
            
        @staticmethod
        def toDTO(user_entity: UserEntity):
            return ResMainPost._Writer(
                idx=user_entity.idx,
                id=user_entity.id,
                profileImage=user_entity.profile_image
            )
    
    idx: int
    thumbnail: str | None
    title: str
    summary: str
    likeCount: int
    createDate: datetime
    writer: _Writer
    
    class Config:
        orm_mode = True
    
    @staticmethod
    def toDTO(post_entity: PostEntity):
        
        # "좋아요" 테이블에서 해당 post와 연관된 행 select
        # 그중에서 삭제 안 된 애들만 필터링
        # 개수 계산
        like_count = len(list(filter(lambda like_entity : like_entity.delete_date == None,
               post_entity.like_entity_list)))
        
        return ResMainPost(
            idx=post_entity.idx,
            thumbnail=post_entity.thumbnail,
            title=post_entity.title,
            summary=post_entity.summary,
            likeCount=like_count,
            createDate=post_entity.create_date,
            writer=ResMainPost._Writer.toDTO(post_entity.user_entity)
        )