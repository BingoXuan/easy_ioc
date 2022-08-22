# EASY\_IOC

a simple dependency-injection python library, which implemented with pure python and meta-programming. It is non-invasive and progressive to refactor your code without learning complex concepts.

## Install

```bash
pip install easy-ioc
```

## FAQ
### Why I need dependency-injection?
See the example below. Basically, you always need to manually pass dependencies of class
to the constructor of class. And constructor should set instance attribute from parameters.
It wastes lots of time and coupling instances each other.

### How it works?
Meta-programming is key of how to make a class. easy-ioc use meta-programming to save the
dependencies of class inside. It cost little performance to achieve. When you try to figure
out the map of your project, easy-ioc can generate the flat tree of dependencies. Then you
can inject all dependencies you need.

### Can I use in Python 3.5 lower?
If you're still using 2.7. Pull origin and checkout branch **python2.7**. And for python 
version greater 3 but lower 3.5, you just need to remove typing in **easy_ioc.inject**.

### Why all dependencies save as class attributes, all instance share same dependencies?
the **inject** function create an **Injectable** instance which help you access own dependencies
correctly. Different instance share same dependencies map, but access own dependencies privately.
If you want to know more, 


## Example

### project without easy\_ioc

```python
# example/todo_without_ioc.py
import random
import logging

class DB(object):
    def __init__(self,url):
        pass
    def find(self, index):
        return self

    def delete(self, index):
        return self

    def update(self, index):
        return self

    def get(self, index):
        return self

class SQLite(DB):
    def __init__(self, url):
        super(SQLite,self).__init__(url)
        logging.info("using SQLite with {}".format(url))

class Mongo(DB):
    def __init__(self,url):
        super(Mongo, self).__init__(url)
        logging.info("using MongoDB with {}".format(url))



class TokenLibrary(object):
    def __init__(self, use_openssl):
        logging.info('{}using openssl '.format('not ' if not use_openssl else ''))

    def generate(self, index, expire_time):
        return b''.join([chr(random.randint(65, 90)).encode() for i in range(64)])


class LoginModule(object):
    def __init__(self, db, token_library):
        self.db = db
        self.token_library = token_library
        logging.info("using {} and {}".format(db, token_library))

    def get_token(self, user_id, password):
        if self.db.find(user_id, password=password):
            return self.token_library.generate(user_id, expire_time=7200)


class TodoModule(object):
    def __init__(self, db):
        self.db = db
        logging.info("using {}".format(db))

    def add(self, todo):
        self.db.add(todo)

    def delete(self, todo):
        self.db.find(todo).delete()

    def update(self, todo):
        self.db.find(todo.id).update(todo)

    def get(self, user):
        return self.db.find(user=user.id)


class TodoService(object):
    def __init__(self, todo_module, login_module, vip_login_module):
        self.todo_module = todo_module
        self.login_module = login_module
        self.vip_login_module = vip_login_module
        logging.info("todo_module:{}".format(todo_module))
        logging.info("login_module:{}".format(login_module))
        logging.info("login_module:{}".format(vip_login_module))
        super(TodoService, self).__init__()


def new_todo_service():
    user_db = Mongo('https://user.mongo.local:27017'),
    todo_db = SQLite(':memory:')
    token_library = TokenLibrary(False)
    openssl_token_library = TokenLibrary(True)
    login_module = LoginModule(user_db, token_library)
    vip_login_module = LoginModule(user_db, openssl_token_library)
    todo_module = TodoModule(todo_db)
    return TodoService(todo_module, login_module,vip_login_module)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    new_todo_service()

```

### refactor project with easy\_ioc

```python
# example/todo_with_ioc.py
from example.todo_without_ioc import SQLite, TodoModule, TodoService, LoginModule, TokenLibrary,DB
from easy_ioc import Container, inject
from example.dependencies import dependencies
import logging
import io


class LoginModuleContainer(LoginModule, Container):
    user_db = inject(DB) # using DB, the parent class as interface
    token_library = inject(TokenLibrary)

    def __init__(self):
        super(LoginModuleContainer, self).__init__(self.user_db, self.token_library)


class TodoModuleContainer(TodoModule, Container):
    todo_db = inject(DB) # using DB, the parent class as interface

    def __init__(self):
        super(TodoModuleContainer, self).__init__(self.todo_db)


class TodoServiceContainer(TodoService, Container):
    todo_module = inject(TodoModuleContainer)  # type: TodoModuleContainer
    vip_login_module = inject(LoginModuleContainer)  # type: LoginModuleContainer
    login_module = inject(LoginModuleContainer)  # type: LoginModuleContainer

    def __init__(self, host, port):
        self.host = host
        self.port = port
        # If you're using python doesn't support typing
        # you can add comment like upper to help ide or editor to know what type should be
        # or assert with isinstance(attr,type), and it won't raise AssertionError.
        # Because it raises an DependencyError before assert isinstance
        # this library also can use in python2.7(not tested under lower version)
        # it can use to refactor project too old too coupled by each module
        super(TodoServiceContainer, self).__init__(self.todo_module, self.login_module)


def new_todo_service():
    file = io.StringIO()
    TodoServiceContainer.generate(file)
    file.seek(0)
    print(file.read())
    # what file read should be as below
    # dependencies = {
    #     "container": {
    #         "TodoServiceContainer": {
    #             "host": None,
    #             "port": None
    #         },
    #         "TodoServiceContainer.todo_module": {},
    #         "TodoServiceContainer.vip_login_module": {},
    #         "TodoServiceContainer.login_module": {}
    #     },
    #     "container_dependencies": {
    #         "TodoServiceContainer.todo_module.todo_db": None,
    #         "TodoServiceContainer.vip_login_module.user_db": None,
    #         "TodoServiceContainer.vip_login_module.token_library": None,
    #         "TodoServiceContainer.login_module.user_db": None,
    #         "TodoServiceContainer.login_module.token_library": None
    #     }
    # }

    # I updated the dependencies as example/dependencies.py like below
    # from example.todo_without_ioc import SQLite, TokenLibrary, Mongo
    # import logging
    # logging.getLogger().setLevel(logging.INFO)
    # todo_db = Mongo('https://user.mongo.local:27017')
    # vip_db = Mongo('https://vip-user.mongo.local:27017')
    # user_db = SQLite(':memory:')
    # token_library = TokenLibrary(use_openssl=False)
    # openssl_token_library = TokenLibrary(use_openssl=True)
    # host = "localhost"
    # port = 8080
    # dependencies = {
    #     "container": {
    #         "TodoServiceContainer": {
    #             "host": host,
    #             "port": port
    #         },
    #         "TodoServiceContainer.todo_module": {},
    #         "TodoServiceContainer.login_module": {},
    #         "TodoServiceContainer.vip_login_module": {}
    #     },
    #     "container_dependencies": {
    #         "TodoServiceContainer.todo_module.todo_db": todo_db,
    #         "TodoServiceContainer.login_module.user_db": user_db,
    #         "TodoServiceContainer.login_module.token_library": token_library,
    #         "TodoServiceContainer.vip_login_module.user_db": vip_db,
    #         "TodoServiceContainer.vip_login_module.token_library": openssl_token_library
    #     }
    # }

    # let's inject the dependencies
    return TodoServiceContainer.inject(dependencies)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    # all dependencies were injected into service
    service = new_todo_service()
   
```

