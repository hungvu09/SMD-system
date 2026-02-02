# src/_object/entities/notifications.py
from data.supa import supabase
from flask_login import UserMixin

class Notifications:
    def __init__(self, user_id, message,title, is_read=False, created_at=None, notification_id=None):
        self.notification_id = notification_id 
        self.user_id = user_id
        self.message = message
        self.title = title
        self.is_read = is_read
        self.created_at = created_at

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "message": self.message,
            "title": self.title,
            "is_read": self.is_read

        }