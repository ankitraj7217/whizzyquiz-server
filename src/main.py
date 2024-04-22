from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.bulk_data_insert_service import bulk_insert_data
from src.common_config import ALLOWED_CORS_ORIGIN, PORT
from src.services.qa_service import getRandomQuestions
from src.db.mongo_db import wq_mongo_db_client
from src.models.qa_model import AnswerRequestModel, AnswerResponseModel, QuestionResponseModel

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        wq_mongo_db_client.connect()

        yield

    finally:
        wq_mongo_db_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def test():
    bulk_insert_data()
    return {"status": "OK"}

#Ideally, should create a router folder with multiple distinct routers using APIRouter

@app.get("/api/v1/getQuestions", response_model=List[QuestionResponseModel])
async def getQuestions():
    return getRandomQuestions()

@app.post("/api/v1/getAnswer", response_model=List[AnswerResponseModel])
async def getAnswers(request: List[AnswerRequestModel]):
    return getAnswers(request)


if __name__ == "__main__":
    uvicorn.run(app, port=PORT)