from data.supa import supabase
from flask_login import UserMixin

class Notifications():
    def __init__(self, user_id, message, is_read=False, created_at=None):
        self.id = user_id#Tham chiếu khoá ngoại đến bảng user (one to many)
        self.message = message
        self.is_read = is_read
        self.created_at = created_at(timezone=True)