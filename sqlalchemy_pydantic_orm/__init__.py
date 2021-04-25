"""
This library makes it a lot easier to do nested database operation with
SQLAlchemy. With this library it is for example possible to validate, convert,
and upload a 100-level deep nested JSON (dict) to its corresponding tables in a
given database, within 3 lines of code.

[Pydantic](https://pydantic-docs.helpmanual.io/) is used for creating the
dataclass and validating it. Pydantic already has a function called
[`.from_orm()`](https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances)
that can do a nested get operation, but it only supports ORM -> Pydantic and
not Pydantic -> ORM. That's exactly where this library fills in, with 2
specific functions `.orm_create()` and `.orm_update()`, and one general
function `.to_orm()` that combines the functionality of the first 2, calling
one or the other, depending on if there is an id provided.
"""
from .main import ORMBaseSchema

__all__ = ["ORMBaseSchema"]
