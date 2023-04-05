from pydantic import BaseModel, Field


class StatusSchema(BaseModel):
    name: str = Field()
    category: str = Field()
