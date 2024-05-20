import tornado.web
import tornado.ioloop
import asyncio
import os
import bcrypt
import logging
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from mysql_db.table_manager import TableManager

from base_handler import BaseHandler
from tickets.add_tickets_handler import AddTicketsHandler
from events.create_event_handler import CreateEventHandler


class MainHandler(BaseHandler):
    def get(self):
        print("Welcoming user")
        self.render("index.html")
        
class LoginHandler(BaseHandler):
    def prepare(self):
        # Skip logged in user check
        pass

    def get(self):
        if self.current_user:
            self.redirect("/")
        else:
            self.render("login/login.html")

    def post(self):
        email = self.get_argument("email")
        password_to_check = self.get_argument("password").encode("utf-8")
        query = f'SELECT * FROM Users WHERE email = %s'
        values = self.mysql_db.execute(query, (email,))

        if values and bcrypt.checkpw(password_to_check, bytes(values[0]['password'])):
            print(f"Login successful for {values[0]['id']}")
            self.set_secure_cookie("user_id", str(values[0]['id']))
            self.redirect("/")
        else:
            print("Login unsuccessful")
            self.write("Invalid email or password.")

class SignupHandler(BaseHandler):
    def prepare(self):
        # Override logged in user check.
        pass

    def get(self):
        if self.current_user:
           self.write("Unable to sign up as you are already logged in.")
           return
        
        self.render("signup/signup.html")
    
    def post(self):
        if self.current_user:
           self.write("Unable to sign up as you are already logged in.")
           return
        
        # Hash the raw password.
        raw_password = self.get_argument("password").encode("utf-8")
        hashed_password = bcrypt.hashpw(raw_password, bcrypt.gensalt())
        try:
            # Create a user if the email id is unique.
            self.mysql_db.insert("Users", {
                "first_name": self.get_argument("first_name"),
                "last_name": self.get_argument("last_name"),
                "email": self.get_argument("email"),
                "password": hashed_password,           
            })
        except mysql.connector.IntegrityError:  
            # Email ID is not unique.
            print(f"Email {self.get_argument("email")} is not unique")
            self.write("Email ID is not unique")
            return
        except Exception as e:
            print(f"Exception during SignUp {e}")
            self.write("Something went wrong, make sure all inputs are valid")
            return

        print(f"Sign Up Successful for {self.get_argument("email")}")
        self.redirect("/login")
        

if __name__ == "__main__":
    # Drop all existing tables and rebuild them from scratch.
    TableManager().rebuild_all()
    # Uncomment line below to only build tables that don't exist.
    # TableManager().build_all() 
    
    # If running on windows uncomment the line below
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Set up web app and handlers.
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/signup", SignupHandler),
        (r"/create_event", CreateEventHandler),
        (r"/add_tickets", AddTicketsHandler)
        ],
        cookie_secret=os.urandom(32).hex()
    )
    # Start the server.
    server = HTTPServer(app)
    server.listen(80)
    print("App is listening on port 80")
    logging.info("Logger: App is listening on port 80")
    IOLoop.current().start()
