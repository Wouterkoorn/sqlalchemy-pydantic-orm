# sqlalchemy-pydantic-orm
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


# Requirements
- Python 3.8+
- SQLAlchemy 1.4+
- Pydantic 1.8+

# Installation
```shell
$ pip install sqlalchemy-pydantic-orm
```
To tinker with the code yourself, install the full dependencies with:
```shell
$ pip install sqlalchemy-pydantic-orm[dev]
```

# Useful references
- https://pydantic-docs.helpmanual.io/usage/models/
- https://fastapi.tiangolo.com/tutorial/sql-databases/


# Examples
Below 1 example is provided (more coming).

[comment]: <> (The first one is a more manual setup, the second does all the work for you.)
For a bigger and more detailed example you can look at the /examples/ folder.

## Example 1 - Using manual created schemas
Create your own Pydantic schemas and link them to the SQLAlchemy ORM-models.

### Create your SQLAlchemy ORM-models (one-to-one or one-to-many)
```python
class Parent(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    car = relationship("Car", cascade="all, delete", uselist=False, back_populates="owner")
    children = relationship("Child", cascade="all, delete")
    
class Car(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    color = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    owner = relationship("Parent", back_populates="car")

class Child(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
```

### Create your Pydantic base and CRUD schemas using these ORM models, and the imported ORMBaseSchema

#### Base schemas
```python
from sqlalchemy_pydantic_orm import ORMBaseSchema
from .models import Parent, Car, Child

class ParentBase(ORMBaseSchema):
    name: str
    _orm_model = PrivateAttr(Parent)

class CarBase(ORMBaseSchema):
    color: str
    _orm_model = PrivateAttr(models.Car)

class ChildBase(ORMBaseSchema):
    name: str
    _orm_model = PrivateAttr(models.Child)
```

#### GET schemas
```python
class Parent(ParentBase):
    id: int
    children: List[Child]
    car: Car

class Car(CarBase):
    id: int

class Child(ChildBase):
    id: int
```

#### CREATE/UPDATE schemas
```python
class ParentCreate(ParentBase):
    id: Optional[int]
    children: List[ChildCreate]
    car: CarCreate

class CarCreate(CarBase):
    id: Optional[int]

class ChildCreate(ChildBase):
    id: Optional[int]
```

### Use your schemas to do nested CRU~~D~~ operations.
```python
with ConnectionDatabase() as db:
    create_schema = schemas.ParentCreate.parse_obj(create_dict)
    parent_db = create_schema.orm_create()
    db.add(parent_db)
    db.commit()

    db_create_schema = schemas.Parent.from_orm(parent_db)
    print(db_create_schema.dict())

    update_schema = schemas.ParentUpdate.parse_obj(update_dict)
    update_schema.to_orm(db)
    db.commit()

    db_update_schema = schemas.Parent.orm_update(parent_db)
    print(db_update_schema.dict())
```
Note: with `.orm_create()` you have to call `db.add()`
before calling `db.commit()`. 
With orm_update you give the db session as parameter,
and you only have to call `db.commit()`.


## ~~Example 2 - Using generated schemas~~
TODO: Integrate with https://github.com/tiangolo/pydantic-sqlalchemy