from pydantic import BaseModel, ConfigDict


class RetainAIBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
