
from pydantic import BaseModel


class AccessJwt(BaseModel):
    idx: int
    id: str
    simpleDesc: str
    profileImage: str
    role: str
    exp: int

    @staticmethod
    def toDTO(jwtDict: dict):
        return AccessJwt(
            idx=jwtDict["idx"],
            id=jwtDict["id"],
            simpleDesc=jwtDict["simpleDesc"],
            profileImage=jwtDict["profileImage"],
            role=jwtDict["role"],
            exp=jwtDict["exp"]
        )

    class Config:
        orm_mode = True


class RefreshJwt(BaseModel):
    idx: int
    exp: int

    @staticmethod
    def toDTO(jwtDict: dict):
        return RefreshJwt(
            idx=jwtDict["idx"],
            exp=jwtDict["exp"]
        )

    class Config:
        orm_mode = True


class ReqSignIn(BaseModel):
    id : str
    password : str
    
class ResSignIn(BaseModel):
    accessToken: str
    refreshToken: str
    

class ReqSignUp(BaseModel):
    id: str
    password: str
    simpleDesc: str  # dto는 프론트엔드와 네이밍을 맞춰야 한다. / 주로 JS는 카멜케이스 사용
    
    
class ResSignUp(BaseModel):
    idx: int
    
    class Config:
        orm_mode = True