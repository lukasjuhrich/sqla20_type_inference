import typing
from dataclasses import dataclass
from typing import Optional, Any

from sqlalchemy import Column, TypeDecorator, Dialect
from sqlalchemy.orm import registry, as_declarative, Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.type_api import _T
from sqlalchemy.types import Integer


@dataclass
class Foo:
    bar: str


class FooType(TypeDecorator[Foo]):
    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        pass

    def process_literal_param(self, value: Optional[_T], dialect: Dialect) -> str:
        pass

    cache_ok = True

    def python_type(self) -> type:
        return Foo

    def process_result_value(
        self, value: typing.Any, dialect: typing.Any
    ) -> Foo | None:
        if value is None:
            return value
        return Foo(value)


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


class Thing(ModelBase):
    id = Column(Integer, primary_key=True)
    foo: Column[Foo] = Column(FooType)
    foo2 = Column(FooType)


def do(foo: Foo) -> None:
    print(foo.bar)


if __name__ == "__main__":
    thing = Thing(id=3, foo=Foo("bar"), foo2=Foo("bar2"))
    import typing

    if typing.TYPE_CHECKING:
        reveal_type(thing.id)
        reveal_type(thing.foo)
        reveal_type(thing.foo2)
    thing.id += 1
    do(thing.id)
    do(thing.foo)
    do(thing.foo2)
