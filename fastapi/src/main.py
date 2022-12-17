import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from controller import sign_controller, test_controller, post_controller
from entity.like_entity import LikeEntity
from entity.post_entity import PostEntity
from entity.user_entity import UserEntity
from fastapi import FastAPI


app = FastAPI()

# cors 설정 미들웨어
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(test_controller.router)
app.include_router(sign_controller.router)
app.include_router(post_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
