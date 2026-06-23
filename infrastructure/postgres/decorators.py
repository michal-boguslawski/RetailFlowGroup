# infrastructure/postgres/decorators.py

from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Concatenate, Protocol
from sqlalchemy.orm import sessionmaker, Session

from infrastructure.postgres.session import get_session


class _HasFactory(Protocol):
    _factory: sessionmaker


P = ParamSpec("P")
R = TypeVar("R")
Self = TypeVar("Self", bound=_HasFactory)


def with_session(
    func: Callable[Concatenate[Self, Session, P], R]
) -> Callable[Concatenate[Self, P], R]:
    """
    Wraps a repository method, injecting a fresh `session` argument.
    The method must accept `self` then `session: Session` as its first two arguments.
    """
    @wraps(func)
    def wrapper(self: Self, /, *args: P.args, **kwargs: P.kwargs) -> R:
        with get_session(self._factory) as session:
            return func(self, session, *args, **kwargs)
    return wrapper
