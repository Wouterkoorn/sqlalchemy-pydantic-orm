from abc import abstractmethod
from typing import Type, Any, Container, Optional

from pydantic import BaseModel, BaseConfig, create_model
from sqlalchemy import inspect
from sqlalchemy.orm import Session, ColumnProperty
from sqlalchemy.orm.decl_api import DeclarativeMeta


class _ORMBaseConfig(BaseConfig):
    orm_mode = True


class ORMBaseSchema(BaseModel):
    class Config:
        orm_mode = True

    def __init__(self, **data: Any):
        if not hasattr(config := self.Config, "orm_mode"):
            config.orm_mode = True
        elif not config.orm_mode:
            # Throwing an error instead of overwriting to prevent confusion
            raise ValueError(
                "sqlalchemy_pydantic: "
                "When adding your own 'Config' class, "
                "make sure you set 'orm_mode' to 'true'"
            )

        super().__init__(**data)  # needed before self._orm_model check

        if type(self._orm_model) != DeclarativeMeta:
            raise ValueError(
                "sqlalchemy_pydantic: "
                "Provided orm_model is not a valid SQLAlchemy model, "
                "make sure it inherits the declarative base"
            )
        elif "_orm_model" not in self.__private_attributes__:
            raise ValueError(
                "sqlalchemy_pydantic: "
                "Provided orm_model is not wrapped in a pydantic PrivateAttr"
            )

    @property
    @abstractmethod
    def _orm_model(self) -> Type[DeclarativeMeta]:
        pass

    def orm_create(self, **extra_fields: Any) -> DeclarativeMeta:
        current_level_fields = {}
        for field in self.__fields_set__:
            value = getattr(self, field)
            field = self.__fields__[field].alias
            if isinstance(value, ORMBaseSchema):
                current_level_fields[field] = value.orm_create()
            elif isinstance(value, (list, tuple, set)):
                models = []
                for schema in value:
                    if not isinstance(schema, ORMBaseSchema):
                        raise ValueError(
                            "sqlalchemy_pydantic: "
                            "Lists should only contain other schemas "
                            f"inherited from '{ORMBaseSchema.__name__}'"
                        )
                    models.append(schema.orm_create())

                current_level_fields[field] = models
            else:
                current_level_fields[field] = value

        return self._orm_model(**extra_fields, **current_level_fields)

    def orm_update(self, db: Session, db_model: DeclarativeMeta):
        for field in self.__fields_set__:
            update_value = getattr(self, field)
            field = self.__fields__[field].alias
            db_value = getattr(db_model, field)
            if isinstance(update_value, ORMBaseSchema):
                if db_value:
                    update_value.orm_update(db, db_value)
                else:
                    setattr(db_model, field, update_value.orm_create())
            elif isinstance(update_value, list):
                parsed_items = []
                for update_item in update_value:
                    item_id = getattr(update_item, "id", None)
                    if item_id:
                        try:
                            db_item = next(item for item in db_value if
                                           item.id == item_id)
                        except StopIteration:
                            raise ValueError("Wrong id provided")
                        update_item.update_orm(db, db_item)
                        parsed_items.append(db_item)
                    else:
                        new_item = update_item.create_orm()
                        parsed_items.append(new_item)
                        db_value.append(new_item)
                for db_item in db_value:
                    if db_item not in parsed_items:
                        db.delete(db_item)
            else:
                setattr(db_model, field, update_value)


# def sqlalchemy_to_pydantic(
#         db_model: Type, *,
#         config: Type[BaseConfig] = _ORMBaseConfig,
#         exclude: Container[str] = None
# ) -> Type[BaseModel]:
#     if exclude is None:
#         exclude = []
#
#     mapper = inspect(db_model)
#     fields = {}
#     for attr in mapper.attrs:
#         if isinstance(attr, ColumnProperty):
#             if attr.columns:
#                 name = attr.key
#                 if name in exclude:
#                     continue
#                 column = attr.columns[0]
#                 python_type: Optional[type] = None
#                 if hasattr(column.type, "impl"):
#                     if hasattr(column.type.impl, "python_type"):
#                         python_type = column.type.impl.python_type
#                 elif hasattr(column.type, "python_type"):
#                     python_type = column.type.python_type
#                 if not python_type:
#                     raise ValueError(
#                         f"Could not infer python_type for {column}"
#                     )
#                 default = None
#                 if column.default is None and not column.nullable:
#                     default = ...
#                 fields[name] = (python_type, default)
#     pydantic_model = create_model(
#         db_model.__name__,
#         __config__=config,
#         __base__=ORMBaseSchema,
#         **fields
#     )
#     return pydantic_model
