from base_handler import BaseHandler

class AddTicketsHandler(BaseHandler):
    def get(self):
        event_rows = self.mysql_db.execute("SELECT name FROM Events where id = %(eid)s", {"eid": self.get_argument("eid")})
        event_name = event_rows[0]["name"]
        print(f"Create event handler event name {event_name}")
        self.render("add_tickets.html", event_name=event_name)

    def post(self):
        print(f"in post with params {self.user_input}")
        quantity = int(self.user_input["quantity"])
        ticket_params = {
            "description": self.user_input["description"],
            "price": self.user_input["price"],
            "event_id": self.user_input["event_id"],
        }
        # Insert all tickets.
        try:
            with self.mysql_db.transaction():
                for _ in range(quantity):
                    self.mysql_db.insert("Tickets", ticket_params)
        except Exception as e:
             print(f"Error while inserting tickets {e}") 
             self.redirect("/add_tickets")  
             return
        
        print(f"Successfully added {quantity} tickets to DB")
        self.redirect("/")