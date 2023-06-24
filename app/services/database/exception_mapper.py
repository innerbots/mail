from collections.abc import Callable
from functools import wraps
from typing import Any, Coroutine, ParamSpec, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import DaoError

Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")
Func = Callable[Param, ReturnType]


def exception_mapper(
        func: Callable[Param, Coroutine[Any, Any, ReturnType]]
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as err:
            raise DaoError from err

    return wrapped
