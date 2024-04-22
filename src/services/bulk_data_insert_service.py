import uuid
from fastapi import HTTPException
from pydantic import ValidationError
from src.models.qa_model import QuestionModel
from src.db.mongo_db import wq_mongo_db_client
from src.data.question_answer_data import questions

def bulk_insert_data():
    try:
        collection_name = "question_bank"

        validated_questions = []
        for question in questions:
            if "tags" not in question:
                question["tags"] = ["JavaScript"]

            question["id"] = str(uuid.uuid4())

            try:
                # print("question: ", question)
                validated_question = QuestionModel(**question)
                validated_questions.append(validated_question.model_dump())
            except ValidationError as e:
                # If validation fails, raise HTTPException with a 422 status code
                raise HTTPException(status_code=422, detail=f"Invalid question format: {e}")

        print("came till here")
        wq_mongo_db_client.bulk_insert(collection_name, validated_questions)
        
    except Exception as e:
        print("Exception occured due to: {}".format(e))