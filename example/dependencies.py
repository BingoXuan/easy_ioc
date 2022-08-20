from example.todo_without_ioc import SQLite, TokenLibrary, Mongo
import logging

logging.getLogger().setLevel(logging.INFO)
todo_db = Mongo('https://user.mongo.local:27017')
vip_db = Mongo('https://vip-user.mongo.local:27017')
user_db = SQLite(':memory:')
token_library = TokenLibrary(use_openssl=False)
openssl_token_library = TokenLibrary(use_openssl=True)
host = "localhost"
port = 8080
dependencies = {
    "container": {
        "TodoServiceContainer": {
            "host": host,
            "port": port
        },
        "TodoServiceContainer.todo_module": {},
        "TodoServiceContainer.login_module": {},
        "TodoServiceContainer.vip_login_module": {}
    },
    "container_dependencies": {
        "TodoServiceContainer.todo_module.todo_db": todo_db,
        "TodoServiceContainer.login_module.user_db": user_db,
        "TodoServiceContainer.login_module.token_library": token_library,
        "TodoServiceContainer.vip_login_module.user_db": vip_db,
        "TodoServiceContainer.vip_login_module.token_library": openssl_token_library
    }
}
