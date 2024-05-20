
from base_handler import BaseHandler

class CreateEventHandler(BaseHandler):
    def get(self):
        self.render("create_event.html")

    def post(self):
        params = {
            "name": self.user_input["name"],
            "location": self.user_input["location"],
            "time": self.user_input["date"],
            "description": self.user_input["description"],
            "creator_id": self.current_user,
        }
        event_id = self.mysql_db.insert("Events", params)

        self.redirect(f"/add_tickets?eid={event_id}")



    # def get(self):
    #     if self.current_user:
    #        self.write("Unable to sign up as you are already logged in.")
    #        return
        
    #     self.render("signup/signup.html")
    
    # def post(self):
    #     if self.current_user:
    #        self.write("Unable to sign up as you are already logged in.")
    #        return
        
    #     # Hash the raw password.
    #     raw_password = self.get_argument("password").encode("utf-8")
    #     hashed_password = bcrypt.hashpw(raw_password, bcrypt.gensalt())
    #     try:
    #         # Create a user if the email id is unique.
    #         mysql_db.insert("Users", {
    #             "first_name": self.get_argument("first_name"),
    #             "last_name": self.get_argument("last_name"),
    #             "email": self.get_argument("email"),
    #             "password": hashed_password,           
    #         })
    #     except mysql.connector.IntegrityError:  
    #         # Email ID is not unique.
    #         print(f"Email {self.get_argument("email")} is not unique")
    #         self.write("Email ID is not unique")
    #         return
    #     except Exception as e:
    #         print(f"Exception during SignUp {e}")
    #         self.write("Something went wrong, make sure all inputs are valid")
    #         return

    #     print(f"Sign Up Successful for {self.get_argument("email")}")
    #     self.redirect("/login")