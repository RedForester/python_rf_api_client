from pydantic import BaseModel


class ApiBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
