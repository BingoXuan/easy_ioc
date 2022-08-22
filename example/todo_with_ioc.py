from example.todo_without_ioc import SQLite, TodoModule, TodoService, LoginModule, TokenLibrary, DB
from easy_ioc import Container, inject
from example.dependencies import dependencies
import logging
import io


class LoginModuleContainer(LoginModule, Container):
    user_db = inject(DB)  # using DB, the parent class as interface
    token_library = inject(TokenLibrary)

    def __init__(self):
        super(LoginModuleContainer, self).__init__(self.user_db, self.token_library)


class TodoModuleContainer(TodoModule, Container):
    todo_db = inject(DB)  # using DB, the parent class as interface

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

    # I updated the dependencies as example/dependencies.py
    # let's inject the dependencies
    return TodoServiceContainer.inject(dependencies)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    new_todo_service()
