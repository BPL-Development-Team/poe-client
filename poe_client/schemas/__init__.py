from humps import camelize
from pydantic import BaseConfig, BaseModel, Extra


def to_camel(string):
    """Return a string as camel case."""
    return camelize(string)


class CamelModel(BaseModel):
    """Allow fields to be set as CamelCase."""

    class Config(BaseConfig):  # noqa: WPS431
        alias_generator = to_camel
        allow_population_by_field_name = True
        validate_assignment = True
        extra = Extra.forbid
