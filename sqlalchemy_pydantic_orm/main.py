from abc import abstractmethod
from typing import Type, Any

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

SUPPORTED_ITERABLES = (list, tuple, set)  # Could be extended


class ORMBaseSchema(BaseModel):
    class Config:
        orm_mode = True

    @property
    @abstractmethod
    def _orm_model(self) -> Type[DeclarativeMeta]:
        pass

    def __init__(self, **data: Any):
        if not hasattr(config := self.Config, "orm_mode"):
            config.orm_mode = True
        elif not config.orm_mode:
            # Throwing an error instead of overwriting to avoid confusion
            raise ValueError(
                "sqlalchemy-pydantic-orm: "
                "When adding your own 'Config' class, "
                "make sure you set 'orm_mode' to 'true'"
            )

        super().__init__(**data)  # needed before self._orm_model check

        if type(self._orm_model) != DeclarativeMeta:
            raise ValueError(
                "sqlalchemy-pydantic-orm: "
                "Provided orm_model is not a valid SQLAlchemy model, "
                "make sure it inherits the declarative base"
            )
        elif "_orm_model" not in self.__private_attributes__:
            raise ValueError(
                "sqlalchemy-pydantic-orm: "
                "Provided orm_model is not wrapped in a pydantic PrivateAttr"
            )

    def orm_create(self, **extra_fields: Any) -> DeclarativeMeta:
        current_level_fields = {}
        for field in self.__fields_set__:
            field_name = self.__fields__[field].alias
            value = getattr(self, field)
            if isinstance(value, ORMBaseSchema):
                current_level_fields[field_name] = value.orm_create()
            elif isinstance(value, SUPPORTED_ITERABLES):
                models = []
                for schema in value:
                    if not isinstance(schema, ORMBaseSchema):
                        raise ValueError(
                            "Lists should only contain other schemas "
                            f"inherited from '{ORMBaseSchema.__name__}' "
                            "(sqlalchemy-pydantic-orm)"
                        )
                    models.append(schema.orm_create())
                current_level_fields[field_name] = models
            else:
                current_level_fields[field_name] = value

        return self._orm_model(**extra_fields, **current_level_fields)

    def orm_update(self, db: Session, db_model: DeclarativeMeta):
        for field in self.__fields_set__:
            field_name = self.__fields__[field].alias
            db_value = getattr(db_model, field_name)
            update_value = getattr(self, field)
            if isinstance(update_value, ORMBaseSchema):
                if db_value:
                    update_value.orm_update(db, db_value)
                else:
                    setattr(db_model, field_name, update_value.orm_create())

            elif isinstance(update_value, SUPPORTED_ITERABLES):
                parsed_items = set()
                for schema in update_value:
                    if not isinstance(schema, ORMBaseSchema):
                        raise ValueError(
                            "Lists should only contain other schemas "
                            f"inherited from '{ORMBaseSchema.__name__}' "
                            "(sqlalchemy-pydantic-orm)"
                        )
                    if item_id := getattr(schema, "id", None):
                        try:
                            db_item = next(
                                item for item in db_value if item.id == item_id
                            )
                        except StopIteration:
                            raise ValueError(
                                f"Provied id '{item_id}' "
                                f"for field '{field_name}' "
                                "can't be found in the database "
                                "(sqlalchemy-pydantic-orm)"
                            ) from None  # removes unnecessary traceback
                        schema.orm_update(db, db_item)
                        parsed_items.add(db_item)
                    else:
                        new_item = schema.orm_create()
                        parsed_items.add(new_item)
                        db_value.append(new_item)

                for db_item in db_value:
                    if db_item not in parsed_items:
                        db.delete(db_item)
            else:
                setattr(db_model, field_name, update_value)

# class _ORMBaseConfig(BaseConfig):
#     orm_mode = True
#
#
# def sqlalchemy_to_pydantic(
#         db_model: Type, *,
#         exclude: Container[str] = None,
# ) -> Type[BaseModel]:
#     if exclude is None:
#         exclude = ()
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
#                         f"Could not infer python_type for {column} "
#                         "(sqlalchemy-pydantic-orm)"
#                     )
#                 default = None
#                 if column.default is None and not column.nullable:
#                     default = ...
#
#                 fields[name] = (python_type, default)
#
#     fields["_orm_model"] = PrivateAttr(db_model)
#     pydantic_model = create_model(
#         db_model.__name__,
#         __base__=ORMBaseSchema,  # Cant go together with __config__
#         **fields
#     )
#     return pydantic_model
