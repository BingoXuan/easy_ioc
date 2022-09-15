import typing
from easy_ioc.injectable import Injectable

T = typing.TypeVar('T')


def inject(cls: typing.Type[T]) -> T:
    """
    if you're using python3.7 or higher
    inject is typed, it returns a descriptor with your input
    inject accepts Type[T]
    it will hint T or Type[T]
    when you assess as an attribute of an object
    the descriptor always returns Type[T] or T
    the type is safe
    when no dependency has been injected
    it raises an exception
    >>> class ToBeInjected:
    >>>     pass
    >>> class A:
    >>>     b = inject(ToBeInjected)
    >>>     # ide like pycharm or editor plugin like jedi
    >>>     # will tell you type of b is ToBeInjected
    :param cls: T as a generic Type
    :return: T
    """
    return Injectable(cls)


__all__ = ['inject']
