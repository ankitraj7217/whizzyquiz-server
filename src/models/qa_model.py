from typing import List, Optional
from pydantic import BaseModel


class OptionModel(BaseModel):
    optionIdx: int  # Index of the option
    optionVal: str  # Value of the option

class QuestionModel(BaseModel):
    id: str  # Unique identifier for the question
    question: str  # The question itself
    code: Optional[str] = None
    options: List[OptionModel]  # List of options
    correctOption: OptionModel  # The correct option
    explanation: str  # Explanation for the correct answer
    tags: List[str]  # List of tags/categories for the question

class QuestionResponseModel(BaseModel):
    id: str  # Unique identifier for the question
    question: str  # The question itself
    code: Optional[str] = None
    options: List[OptionModel]  # List of option values

class AnswerRequestModel(BaseModel):
    questionId: str  # Unique identifier for the question

class AnswerResponseModel(BaseModel):
    id: str  # Unique identifier for the question
    question: str
    code: Optional[str] = None
    correctOption: OptionModel  # The correct option
    explanation: str  # Explanation for the correct answer
    tags: List[str]  # List of tags/categories for the question
