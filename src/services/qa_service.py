from typing import List
from pydantic import ValidationError
from src.models.qa_model import QuestionResponseModel, AnswerRequestModel, AnswerResponseModel
from src.db.mongo_db import wq_mongo_db_client
from fastapi import HTTPException

async def getRandomQuestions():
    try:
        collection_name = "question_bank"
        pipeline = [
            {"$sample":  {"size": 5}}
        ]
        projection = {
            "_id": False,
            "correctOption": False,
            "explanation": False,
            "tags": False
        }

        # Retrieve sample questions from MongoDB
        questions = wq_mongo_db_client.aggregate(collection_name, pipeline, projection)

        # Validate each question against QuestionResponseModel
        validated_questions = []
        for question in questions:
            try:
                # Try to parse the question into a GetQuestionResponseModel
                validated_question = QuestionResponseModel(**question)
                # model_dump is used as dict() is deprecated
                validated_questions.append(validated_question.model_dump()) 
            except ValidationError as e:
                # If validation fails, raise HTTPException with a 422 status code
                raise HTTPException(status_code=422, detail=f"Invalid question format: {e}")

        return validated_questions
    
    except KeyError as e:
        # Handle KeyError (e.g., if something went wrong with MongoDB aggregation)
        raise HTTPException(status_code=500, detail="Error retrieving questions")
    except Exception as e:
        # Handle any other unexpected exceptions
        raise HTTPException(status_code=500, detail="Internal server error")


async def getAnswers(questionIDs: List[AnswerRequestModel]):
    try:
        collection_name = "question_bank"

        ids = [dic["questionId"] for dic in questionIDs]
        query = {
                "id": {"$in": ids}
        }

        projection = {
            "_id": False,
            "options": False
        }

        answers = wq_mongo_db_client.find(collection_name, query, projection)
        validated_answers = []

        for answer in answers:
            try:
                # Try to parse the question into a AnswerResponseModel
                validated_answer = AnswerResponseModel(**answer)
                # model_dump is used as dict() is deprecated
                validated_answers.append(validated_answer.model_dump())
            except ValidationError as e:
                # If validation fails, raise HTTPException with a 422 status code
                raise HTTPException(status_code=422, detail=f"Invalid question format: {e}")
            
        return validated_answers

    except KeyError as e:
        # Handle KeyError (e.g., if something went wrong with MongoDB aggregation)
        raise HTTPException(status_code=500, detail="Error retrieving answers")
    except Exception as e:
        # Handle any other unexpected exceptions
        raise HTTPException(status_code=500, detail="Internal server error")

    