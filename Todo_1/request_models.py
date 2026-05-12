from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Workout",
                "description": "Workout in morning",
                "priority": 4,
                'complete': False
            }
        }
    }

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    password: str = Field(min_length=5)
    role: str = Field(min_length=1)

class Token(BaseModel):
    access_token: str
    token_type: str