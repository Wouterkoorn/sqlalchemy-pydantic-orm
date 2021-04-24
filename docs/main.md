Module sqlalchemy_pydantic_orm.main
===================================
TODO: Module documentation

Classes
-------

`ORMBaseSchema(**data: Any)`
:   TODO: Class documentation
    
    Init used for validation and throwing errors where needed.
    
    Pydantic catches all ValueError's in initialization, and then outputs
    the error message in a easy to read format with the specific class
    name displayed.
    Every error is given the "sqlalchemy-pydantic-orm" identifier to
    distinguish between Pydantic's or SQLAlchemy's own errors
    and those of this package.
    
    For performance its better to execute the `super().__init__()` as late
    as possible, only the _orm_model check requires it to work properly.
    
    Args:
        **data (Any):
            The fields and values to be validated.
    
    Raises:
        ValueError:
            When orm_mode is set to false /
            When the provided _orm_model is invalid

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Config`
    :   Pydantic's default config class except with orm_mode set to True.

    ### Methods

    `orm_create(self, **extra_fields: Any) ‑> sqlalchemy.orm.decl_api.DeclarativeMeta`
    :   Method to convert a (nested) pydantic schema to a SQLAlchemy model.
        
        Using the validated fields in this class, together with the defined
        _orm_model, this recursive methods creates a (nested) SQLAlchemy model.
        
        Args:
            extra_fields (Any):
                Extra fields (keyword arguments) not defined in the pydantic
                schema used by the top level ORM model. The fields in the
                schema itself have priority.
        
                Usage example:
                    When using an API like FastAPI or Flask, you often get
                    the data as body while getting the id (foreign key) as
                    path parameter. This argument lets you add such an id from
                    a separate source.
        
        Returns:
            A SQLAlchemy model instance, that still has to be added to the db.
        
        Raises:
            TypeError:
                When a list is not fully consisted of other ORM schemas.

    `orm_update(self, db: sqlalchemy.orm.session.Session, db_model: sqlalchemy.orm.decl_api.DeclarativeMeta) ‑> NoneType`
    :   Method to update a (nested) orm structure.
        
        This method recursively updates an orm model with it's relationships.
        
        In one-to-many relationships, each provided item without an id gets
        added as new item with the `orm_create()` method. When a valid id is
        provided it updates the item with the `orm_update()` method. It also
        keep track of the parsed database items, and afterwards deletes any
        unparsed item.
        
        Args:
            db (Session):
                Database session used for `.add()` and `.delete()`.
            db_model (DeclarativeMeta):
                The ORM model to be updated.
        
        Returns:
            Nothing, everything gets done in the provided db_model
        
        Raises:
            TypeError:
                When a list is not fully consisted of other ORM schemas.
            ValueError:
                When the provided db_model is not valid /
                When a given id is not found in the database

    `to_orm(self, db: sqlalchemy.orm.session.Session, **extra_fields: Any) ‑> sqlalchemy.orm.decl_api.DeclarativeMeta`
    :   Method that combines the functionality of orm_create & orm_update.
        
        This method is a wrapper around the other two methods. When no id is
        provided, it creates a new model with orm_create, and when an id ís
        provided, it retrieves and updates that model.
        
        In contrary to the orm_create function on its own, this function does
        add the newly created model to the database. So after the this method
        has been executed you only need to call `db.commit()` after.
        
        Args:
            db (Session):
            **extra_fields (Any):
        
        Returns:
            A SQLAlchemy model instance, which is either queried and updated,
                or newly created
        
        Raises:
            ValueError:
                When the provided id is not found in the database