class DependencyError(Exception):
    def __init__(self, owner, name, dep_type):
        message = '{}.{} should be instance of {}'.format(owner, name, dep_type)
        super(DependencyError, self).__init__(message)


class Dependencies(dict):
    pass

class Injectable(object):
    __slots__ = ['instance', 'cls', 'name']

    def __init__(self, cls):
        self.instance = None
        self.cls = cls
        self.name = None

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, owner, cls):
        if self.instance:
            return self.instance
        else:
            raise DependencyError(owner, self.name, self.cls)

    def __set__(self, owner, value):
        if isinstance(value, self.cls) or value is None:
            self.instance = value

__all__ = ['Injectable','Dependencies','DependencyError']