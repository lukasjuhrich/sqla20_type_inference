from sqlalchemy import Column
from sqlalchemy.orm import registry, as_declarative
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.types import Integer


mapper_registry = registry()

class MyMeta(DeclarativeMeta): pass


@as_declarative(metaclass=MyMeta)
class ModelBase:
    """Base class for all database models."""

    __abstract__ = True
    # explicit registry definitions for mypy
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


class Stub(ModelBase):
    id = Column(Integer, primary_key=True)


if __name__ == "__main__":
    import typing

    stub = Stub(id=5)
    if typing.TYPE_CHECKING:
        reveal_type(stub.id)

    assert stub.id.startswith("foo")
