class DependencyError(Exception):
    def __init__(self, owner, name, dep_type):
        message = '{}.{} should be instance of {}'.format(owner, name, dep_type)
        super(DependencyError, self).__init__(message)


class Dependencies(dict):
    pass


class Injectable(object):
    __slots__ = ['cls', 'name']

    def __init__(self, cls):
        self.cls = cls
        self.name = None

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, owner, cls):
        instance = owner.get_dependency(self.name)
        if instance:
            return instance
        else:
            raise DependencyError(owner, self.name, self.cls)

    def __set__(self, owner, value):
        # print(owner,self.name,value)
        if isinstance(value, self.cls) or value is None:
            owner.inject_dependency(self.name,value)


__all__ = ['Injectable', 'Dependencies', 'DependencyError']
