import pytest

from main import (
    db,
    Parent,
    PydanticParent,
    orm_create_input_data,
    orm_create_output_data,
    orm_update_input_data,
    orm_update_output_data
)


def test_orm_create():
    schema_in = PydanticParent.parse_obj(orm_create_input_data)
    db_model = schema_in.orm_create()
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    schema_out = PydanticParent.from_orm(db_model)
    assert schema_out.dict(by_alias=True) == orm_create_output_data


def test_orm_update():
    schema_in = PydanticParent.parse_obj(orm_update_input_data)
    db_model = db.query(Parent).one()
    schema_in.orm_update(db, db_model)
    db.commit()
    db.refresh(db_model)
    schema_out = PydanticParent.from_orm(db_model)
    assert schema_out.dict(by_alias=True) == orm_update_output_data
