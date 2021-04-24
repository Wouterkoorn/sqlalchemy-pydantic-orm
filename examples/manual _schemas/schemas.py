from typing import Optional, List

from pydantic import PrivateAttr
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy_pydantic_orm import ORMBaseSchema

import models


# Base models
###############################################################################
class CarBase(ORMBaseSchema):
    # class Config:
    #     orm_mode = False  # Throws error

    color: str

    # _orm_model = 5  # Throws error
    # _orm_model = models.Car  # Throws error
    _orm_model = PrivateAttr(models.Car)  # valid


class PopsicleBase(ORMBaseSchema):
    flavor: str

    _orm_model: models.Popsicle = PrivateAttr(models.Popsicle)


class ChildBase(ORMBaseSchema):
    name: str

    _orm_model: models.Base = PrivateAttr(models.Child)


class ParentBase(ORMBaseSchema):
    name: str

    _orm_model: DeclarativeMeta = PrivateAttr(models.Parent)


# GET models
###############################################################################
class Car(CarBase):
    id: int


class Popsicle(PopsicleBase):
    id: int


class Child(ChildBase):
    id: int
    popsicles: List[Popsicle]


class Parent(ParentBase):
    id: int
    children: List[Child]
    car: Car


# CREATE/UPDATE models
###############################################################################
class CarCreate(CarBase):
    id: Optional[int]  # None for create, id for update


class PopsicleCreate(PopsicleBase):
    id: Optional[int]


class ChildCreate(ChildBase):
    id: Optional[int]
    popsicles: List[PopsicleCreate]


class ParentCreate(ParentBase):
    id: Optional[int]
    children: List[ChildCreate]
    car: CarCreate
