
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