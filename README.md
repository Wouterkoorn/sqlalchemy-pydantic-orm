# sqlalchemy-pydantic-orm
CRUD operations on nested SQLAlchemy ORM models using Pydantic schemas.
# Installation
```shell
$ pip install sqlalchemy-pydantic-orm
```
To tinker with the code yourself, install the full dependencies with:
```shell
$ pip install sqlalchemy-pydantic-orm[dev]
```

# Examples
Below 2 small examples are provided. 
The first one is a more manual setup, the second does all the work for you.
For a bigger and more detailed examples you can look at the ./examples folder.
## Example 1 - Using manual created schemas
Create your own Pydantic schemas and link them to the SQLAlchemy ORM-models.
### Create your SQLAlchemy ORM-models (one-to-many or one-to-one)
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
### Create your Pydantic base and CRU~~D~~ schemas using these ORM models, and the imported ORMBaseSchema
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

    db_update_schema = schemas.Parent.from_orm(parent_db)
    print(db_update_schema.dict())
```
Note: with `.orm_create()` you have to call `db.add()`
before calling `db.commit()`. 
With orm_update you give the db session as parameter,
and you only have to call `db.commit()`.

## Example 2 - Usign generated schemas
TODO: Integrate with https://github.com/tiangolo/pydantic-sqlalchemy