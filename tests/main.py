from typing import List, Optional

from pydantic import Field, PrivateAttr
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base, relationship

from sqlalchemy_pydantic_orm import ORMBaseSchema

Base: DeclarativeMeta = declarative_base()


class Parent(Base):  # type: ignore
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    children = relationship("Child", cascade="all, delete")
    car = relationship(
        "Car", cascade="all, delete", uselist=False, back_populates="owner"
    )


class Child(Base):  # type: ignore
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    popsicles = relationship("Popsicle", cascade="all, delete")


class Popsicle(Base):  # type: ignore
    __tablename__ = "popsicles"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    flavor = Column(String, nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)


class Car(Base):  # type: ignore
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    color = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    owner = relationship("Parent", back_populates="car")


class PydanticCar(ORMBaseSchema):
    id: Optional[int]
    colour: str = Field(alias="color")  # mostly used for reserved names

    _orm_model = PrivateAttr(Car)


class PydanticPopsicle(ORMBaseSchema):
    id: Optional[int]
    flavor: str

    _orm_model = PrivateAttr(Popsicle)


class PydanticChild(ORMBaseSchema):
    id: Optional[int]
    name: str
    popsicles: List[PydanticPopsicle]

    _orm_model = PrivateAttr(Child)


class PydanticParent(ORMBaseSchema):
    id: Optional[int]
    name: str
    children: List[PydanticChild]
    car: PydanticCar

    _orm_model = PrivateAttr(Parent)


orm_create_input_data = {
    "name": "Bob",
    "children": [
        {"name": "Tim", "popsicles": [{"flavor": "Strawberry"}]},
        {
            "name": "Ana",
            "popsicles": [
                {"flavor": "Melon"},
                {"flavor": "Orange"},
                {"flavor": "Cola"},
            ],
        },
    ],
    "car": {"color": "Blue"},
}

orm_create_output_data = {
    "name": "Bob",
    "id": 1,
    "children": [
        {
            "name": "Tim",
            "id": 1,
            "popsicles": [{"flavor": "Strawberry", "id": 1}],
        },
        {
            "name": "Ana",
            "id": 2,
            "popsicles": [
                {"flavor": "Melon", "id": 2},
                {"flavor": "Orange", "id": 3},
                {"flavor": "Cola", "id": 4},
            ],
        },
    ],
    "car": {"color": "Blue", "id": 1},
}

orm_update_input_data = {
    "name": "Henk",
    "id": 1,
    "children": [
        {
            "name": "Jane",
            "id": 2,
            "popsicles": [
                {"flavor": "Lemon", "id": 2},
                {"flavor": "Cola", "id": 4},
                {"flavor": "Apple"},
            ],
        },
        {"name": "Jack", "popsicles": [{"flavor": "Strawberry"}]},
    ],
    "car": {"color": "Red", "id": 1},
}

orm_update_output_data = {
    "name": "Henk",
    "id": 1,
    "children": [
        {
            "name": "Jane",
            "id": 2,
            "popsicles": [
                {"flavor": "Lemon", "id": 2},
                {"flavor": "Cola", "id": 4},
                {"flavor": "Apple", "id": 5},
            ],
        },
        {
            "name": "Jack",
            "id": 3,
            "popsicles": [{"flavor": "Strawberry", "id": 6}],
        },
    ],
    "car": {"color": "Red", "id": 1},
}
