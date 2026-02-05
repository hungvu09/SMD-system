from urllib import response
from flask import Flask
from flask_login import LoginManager, current_user
import os
from _object.entities.model_users import User
from services.notification_ser import NotificationService
from infrastructure.ai.ai_controller import ai_bp


from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjhjhjhj'
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')
#Init - login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        
        user = User.get(user_id)
        return user
    
#ket noi supabase va debug ket noi
    from data.supa import supabase
    #print("Supabase connected:", supabase is not None)

    from .auth import auth
    from .views import views

#import cac cau truc du lieu tu model
    

    #dang ky blueprint
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(ai_bp, url_prefix='/ai')


    @app.context_processor
    def inject_notifications():
        # Khởi tạo giá trị mặc định
        notifications_data = {
            'system_banner': NotificationService.get_system_banner(),
            'personal_notifications': [],
            'unread_count': 0
        }

        # Nếu có người dùng đăng nhập, lấy thông báo cá nhân từ Service
        if current_user.is_authenticated:
            try:
                # Gọi tầng Service đã định nghĩa để lấy data
                notifications_data['personal_notifications'] = NotificationService.get_personal_notifications(current_user.id)
                
                # Đếm số lượng chưa đọc (Có thể viết thêm hàm count trong Service nếu cần tối ưu)
                unread_list = [n for n in notifications_data['personal_notifications'] if not n.get('is_read')]
                notifications_data['unread_count'] = len(unread_list)
            except Exception as e:
                print(f"Lỗi load thông báo trong __init__: {e}")

        return notifications_data

    return app