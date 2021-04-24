import schemas
from database import ConnectionDatabase, engine, Base

Base.metadata.create_all(bind=engine)

create_dict = {
    "name": "Bob",
    "children": [
        {
            "name": "Tim",
            "popsicles": [
                {"flavor": "Strawberry"}
            ]
        },
        {
            "name": "Ana",
            "popsicles": [
                {"flavor": "Melon"},
                {"flavor": "Orange"},
                {"flavor": "Cola"}
            ]
        }
    ],
    "car": {"color": "Blue"}
}

update_dict = {
    "name": "Henk",
    "id": 1,
    "children": [
        {
            "name": "Jane",
            "id": 2,
            "popsicles": [
                {"flavor": "Lemon", "id": 2},
                {"flavor": "Cola", "id": 4},
                {"flavor": "Apple"}
            ]
        },
        {
            "name": "Jack",
            "popsicles": [
                {"flavor": "Strawberry"}
            ]
        },
    ],
    "car": {"color": "Red", "id": 1}
}

with ConnectionDatabase() as db:
    create_schema = schemas.ParentCreate.parse_obj(create_dict)
    parent_db = create_schema.orm_create()
    db.add(parent_db)
    db.commit()

    db_create_schema = schemas.Parent.from_orm(parent_db)
    print(db_create_schema.dict())

    update_schema = schemas.ParentCreate.parse_obj(update_dict)
    update_schema.orm_update(db, parent_db)
    db.commit()

    db_update_schema = schemas.Parent.from_orm(parent_db)
    print(db_update_schema.dict())

