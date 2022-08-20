import json
import inspect
import six
from easy_ioc.injectable import *


class ContainerMeta(type):
    def __new__(mcls, name, bases, namespaces):
        cls = super(ContainerMeta, mcls).__new__(mcls, name, bases, namespaces)
        dependencies = Dependencies()
        for base in bases:
            base_deps = getattr(base, '_dependencies', None)
            if isinstance(base_deps, Dependencies):
                dependencies.update(base_deps)
        for k, v in namespaces.items():
            if isinstance(v, Injectable):
                dependencies[k] = v
            if getattr(v, '__set_name__', None) is not None:
                v.__set_name__(cls, k)
        cls._dependencies = dependencies
        return cls


class Container(six.with_metaclass(ContainerMeta, object)):
    _dependencies = Dependencies()

    def __init__(self, **kwargs):
        pass

    @classmethod
    def get_dependencies(cls, url=None, ctx=None):
        if ctx is None:
            ctx = {
                'container': {},
                'container_dependencies': {}
            }
        if url is None:
            url = cls.__name__
            # url = cls.__name__
        spec = inspect.getargspec(cls.__init__)
        ctx['container'][url] = {k: None for k in spec.args[1:]}
        for k, v in cls._dependencies.items():
            assert isinstance(v, Injectable)
            if issubclass(v.cls, Container):
                v.cls.get_dependencies(url + '.' + k, ctx)
            else:
                ctx['container_dependencies'][url + '.' + k] = None
        return ctx

    @classmethod
    def inject(cls, dependencies, url=None):
        if url is None:
            url = cls.__name__
        obj = object.__new__(cls)
        for k, v in cls._dependencies.items():
            sub_url = url + '.' + k
            assert isinstance(v, Injectable)
            if issubclass(v.cls, Container):
                dep = v.cls.inject(dependencies, sub_url)
            else:
                dep = dependencies['container_dependencies'].get(sub_url)
            setattr(obj, k, dep)
        kw = dependencies['container'].get(url) or {}
        obj.__init__(**kw)
        assert isinstance(obj, cls)
        return obj

    @classmethod
    def generate(cls, file):
        deps = cls.get_dependencies()
        file.write(u'dependencies = ' + \
                   json.dumps(deps, indent=2).replace(u'null', u'None'))


__all__ = ['Injectable', 'Container', 'DependencyError']
