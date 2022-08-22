import json
import inspect
from easy_ioc.injectable import *
import sys

need_patch_set_name = sys.version_info.major == 3 and sys.version_info.minor == 5


class ContainerMeta(type):
    def __new__(mcls, name, bases, namespaces):
        dependencies = Dependencies()
        # namespaces['_dependencies'] = dependencies
        cls = super(ContainerMeta, mcls).__new__(mcls, name, bases, namespaces)
        dependencies = Dependencies()
        for base in bases:
            base_deps = getattr(base, '_dependencies', None)
            if isinstance(base_deps, Dependencies):
                dependencies.update(base_deps)
        for k, v in namespaces.items():
            if isinstance(v, Injectable):
                dependencies[k] = v
            if need_patch_set_name:
                if getattr(v, '__set_name__', None) is not None:
                    v.__set_name__(cls, k)
        cls._dependencies = dependencies
        return cls


class Container(metaclass=ContainerMeta):
    _dependencies = Dependencies()
    _injected = Dependencies()

    def __init__(self, **kwargs):
        pass

    def inject_dependency(self, name, value):
        self._injected[name] = value

    def get_dependency(self, name):
        return self._injected.get(name)

    @classmethod
    def walk_dependencies(cls, url=None, ctx=None):
        if ctx is None:
            ctx = {
                'container': {},
                'container_dependencies': {}
            }
        if url is None:
            url = cls.__name__
        spec = inspect.getfullargspec(cls.__init__)
        ctx['container'][url] = {k: None for k in spec.args[1:]}
        for k, v in cls._dependencies.items():
            assert isinstance(v, Injectable)
            if issubclass(v.cls, Container):
                v.cls.walk_dependencies(url + '.' + k, ctx)
            else:
                ctx['container_dependencies'][url + '.' + k] = None
        return ctx

    @classmethod
    def inject(cls, dependencies, url=None):
        if url is None:
            url = cls.__name__
        obj = object.__new__(cls)
        setattr(obj, '_injected', Dependencies())
        for k, v in cls._dependencies.items():
            sub_url = url + '.' + k
            assert isinstance(v, Injectable)
            if issubclass(v.cls, Container):
                dep = v.cls.inject(dependencies, sub_url)
            else:
                dep = dependencies['container_dependencies'].get(sub_url)
            obj.inject_dependency(k, dep)
        kw = dependencies['container'].get(url) or {}
        obj.__init__(**kw)
        assert isinstance(obj, cls)
        return obj

    @classmethod
    def generate(cls, file):
        deps = cls.walk_dependencies()
        file.write('dependencies = ' + \
                   json.dumps(deps, indent=2).replace('null', 'None'))


__all__ = ['Injectable', 'Container', 'DependencyError']
