from data.supa import supabase
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, email, phone=None, status='active', faculty=None,created_at=None, updated_at=None,role='student', notifications=None):
        self.id = user_id
        self.username = username
        self.email = email
        self.phone = phone
        self.status = status
        self.faculty = faculty
        self.created_at = created_at
        self.updated_at = updated_at
        self.role = role
        self.noti = notifications


    @staticmethod
    def get(user_id):
        response = supabase.from_('user').select('*').eq('user_id', user_id).execute()
        data = response.data
        if data:
            user_data = data[0]
            return User(
                user_id=user_data['user_id'], 
                username=user_data['username'], 
                email=user_data['email'],
                phone=user_data['phone'], 
                status=user_data['status'], 
                faculty=user_data['faculty'],
                created_at=user_data['created_at'], 
                updated_at=user_data['updated_at'], 
                role=user_data['role'])
        return None
    
    # Các method

    @property
    def is_active(self):
        return self.status == 'active'


    def get_id(self):
        return str(self.id)
