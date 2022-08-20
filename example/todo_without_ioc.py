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
    def __init__(self, todo_module, login_module):
        self.todo_module = todo_module
        self.login_module = login_module
        logging.info("todo_module:{}".format(todo_module))
        logging.info("login_module:{}".format(login_module))
        super(TodoService, self).__init__()


def new_todo_service():
    user_db = Mongo('https://user.mongo.local:27017'),
    todo_db = SQLite(':memory:')
    token_library = TokenLibrary(False)
    login_module = LoginModule(user_db, token_library)
    todo_module = TodoModule(todo_db)
    return TodoService(todo_module, login_module)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    new_todo_service()
