from pydantic import BaseModel, validator
from pydantic.fields import Undefined


class ApiBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    @validator("*", pre=True)
    def default_if_null(cls, v, field):
        if v is None and field.default is not Undefined:
            return field.default
        return v
