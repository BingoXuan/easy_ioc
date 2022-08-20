from example.todo_without_ioc import SQLite, TokenLibrary, Mongo
import logging

logging.getLogger().setLevel(logging.INFO)
todo_db = Mongo('https://user.mongo.local:27017')
user_db = SQLite(':memory:')
token_library = TokenLibrary(use_openssl=False)
host = "localhost"
port = 8080
dependencies = {
    "container": {
        "TodoServiceContainer": {
            "host": host,
            "port": port
        },
        "TodoServiceContainer.todo_module": {},
        "TodoServiceContainer.login_module": {}
    },
    "container_dependencies": {
        "TodoServiceContainer.todo_module.todo_db": todo_db,
        "TodoServiceContainer.login_module.user_db": user_db,
        "TodoServiceContainer.login_module.token_library": token_library
    }
}
