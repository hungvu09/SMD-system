# src/website/services/auth_service.py
from data.supa import supabase
from flask import flash

class Authservice:
    # def signup(self, username, email, password1, password2, phone=None):
    #     if len(username) < 2:
    #         return {'error': 'Họ tên phải lớn hơn 1 ký tự.'}
    #     if len(email) < 4:
    #         return {'error': 'Email phải lớn hơn 3 ký tự.'}
    #     if password1 != password2:
    #         return {'error': 'Mật khẩu không khớp.'}
    #     if len(password1) < 7:
    #         return {'error': 'Mật khẩu phải ít nhất 7 ký tự.'}
        
    #     try:
    #             auth_response = supabase.auth.sign_up({
    #                 "email": email,
    #                 "password": password1
    #             })
    #             if auth_response.user:
    #                 # Lưu vào bảng public.user với role mặc định 'student'
    #                 supabase.from_('user').insert({
    #                     "user_id": str(auth_response.user.id),
    #                     "username": username,
    #                     "email": email,
    #                     "phone": phone,
    #                     "status": 'active',
    #                     "role": 'student'  # Mặc định 'student', admin duyệt sau
    #                 }).execute()
    #                 flash("Đăng ký thành công! Role mặc định: student.", category='success')
    #             else:
    #                 flash("Đăng ký thất bại. Vui lòng thử lại.", category='error')
    #     except Exception as e:
    #             return {"success": False, "message": str(e)}
    





    def login(self, email, password):
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.user:
                user_id = str(response.user.id)
                # lấy thông tin ở trong bảng user
                user_data = supabase.table('user')\
                .select('user_id', 'username', 'email', 'status', 'role')\
                .eq('user_id', user_id)\
                .single()\
                .execute()

                # check xem có data hay không có
                if user_data.data:
                     role = user_data.data['role']
                     username = user_data.data['username']
                     status = user_data.data['status']
                     if status != 'active':
                        flash('Tài khoản của bạn không hoạt động. Vui lòng liên hệ quản trị viên.', category='error')
                        return {"success": False, "message": "Tài khoản không hoạt động."}
                     return {   #trả về thông tin user
                            'success': True,
                            'user_id': user_id,
                            'username': username,
                            'role': role,
                            'email': email
                    }
            else:
                 flash('Email hoặc mật khẩu không đúng.', category='error')
                     
        except Exception as e:
            return {"error": str(e)}



def get_user_info(self, user_id):
     response = supabase.table('user')\
            .select('user_id, username, email, role, phone, status')\
            .eq('user_id', user_id)\
            .single()\
            .execute()
     return response.data if response.data else None
    