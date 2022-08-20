from example.dependencies import *
from example.todo_with_ioc import new_todo_service, TodoServiceContainer
from easy_ioc import DependencyError


def test_ioc():
    service = new_todo_service()
    assert service.todo_module.todo_db is todo_db
    assert service.login_module.user_db is user_db
    assert service.login_module.token_library is token_library
    assert service.vip_login_module.user_db is vip_db
    assert service.vip_login_module.token_library is openssl_token_library
    assert service.host is host
    assert service.port is port


def test_missing_injection():
    container_dependencies = dependencies["container_dependencies"]
    container_dependencies["TodoServiceContainer.todo_module.todo_db"] = None
    try:
        TodoServiceContainer.inject(dependencies)
    except DependencyError:
        pass
