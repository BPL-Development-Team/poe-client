from humps import camelize
from pydantic import BaseConfig, BaseModel, Extra


def to_camel(string):
    """Return a string as camel case."""
    return camelize(string)


class Model(BaseModel):
    """Base model for data retrieved from the POE API.

    Fields on these models may be set as CamelCase.
    """

    class Config(BaseConfig):  # noqa: WPS431
        alias_generator = to_camel
        allow_population_by_field_name = True
        validate_assignment = True
        extra = Extra.forbid
