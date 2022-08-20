from easy_ioc.injectable import Injectable


def inject(cls):
    """
    if you're using python3.5 or lower,
    function inject may hint nothing to return.
    Don't worry. we have a solution to fix it.
    >>> class ToBeInject:
    >>>     def do_something(self):
    >>>         pass
    >>> class A:
    >>>     b = inject(ToBeInject) # type: ToBeInject
    >>>     def __init__(self):
    >>>         # for tell ide or editor type of self.b
    >>>         # use assert or typed be comment
    >>>         assert isinstance(self.b,ToBeInject)
    >>>         # if dependencies injected properly,
    >>>         # b is instance of ToBeInject
    >>>         # otherwise, it raises Exception
    >>>         # because you injected in wrong way
    :param cls: any
    :return: any
    """
    return Injectable(cls)


__all__ = ['inject']
