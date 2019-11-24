from flask_login import UserMixin
from travelplanner import db, loginManager

class User(UserMixin):
    def __init__(self, id, username, active=True):
        self.id = id 
        self.username = username 
        self.active = active 

    def isActive(self):
        return self.active 

loginManager.login_view = "login"
loginManager.login_message = "Please log in"
loginManager.refresh_view = "index"

@loginManager.user_loader
def loadUser(userId):
    query = "SELECT id, username FROM user WHERE id = %s"
    params = (userId,)

    result = db.runQuery(query, params)

    if result:
        return User(id=result[0][0], username=result[0][1])
    
    return None