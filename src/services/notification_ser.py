# src/services/notification_ser.py
from data.supa import supabase
from _object.entities.notifications import Notifications

class NotificationService:
    @staticmethod
    def get_personal_notifications(user_id, limit=5):
        # thông bao cá nhân cho người dùng
        response = supabase.table('notifications')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return response.data

    @staticmethod
    def create_system_notification(user_id, message):
        # tạo thông báo mới khi có sự kiện xảy ra
        new_notif = Notifications(user_id=user_id, message=message)
        return supabase.table('notifications').insert(new_notif.to_dict()).execute()

    @staticmethod
    def get_system_banner():
        # thông báo từ hệ thống
        res = supabase.table('system_settings').select('static_inf').eq('id_settings', 1).single().execute()
        return res.data.get('static_inf') if res.data else None