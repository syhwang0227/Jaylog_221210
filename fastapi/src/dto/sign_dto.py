
from pydantic import BaseModel


class ReqSignUp(BaseModel):
    id: str
    password: str
    simpleDesc: str  # dto는 프론트엔드와 네이밍을 맞춰야 한다. / 주로 JS는 카멜케이스 사용
    
    
class ResSignUp(BaseModel):
    idx: int
    
    class Config:
        orm_mode = True