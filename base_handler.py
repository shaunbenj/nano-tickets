import tornado.web
from mysql_db.cursor import Cursor
import types

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mysql_db = Cursor()

    def prepare(self):
        if self.current_user is None:
            print(f"{self.__class__.__name__} User is not logged in redirect to login")
            return self.redirect("/login")
            
        # Place user input into a frozen dictionary.
        raw_input = {name: self.get_arguments(name) for name in self.request.arguments}
        for key in raw_input:
            if len(raw_input[key]) == 1:
                raw_input[key] = raw_input[key][0]
        self.user_input = types.MappingProxyType(raw_input)
        
    def get_current_user(self):
        user_bytes = self.get_secure_cookie("user_id")
        if user_bytes:
           return user_bytes.decode("utf-8")
        else:
            return None
