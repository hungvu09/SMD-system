from data.supa import supabase, supabase_admin
from flask import flash
from flask_login import current_user


def updated_user_role(current_user, user_id, new_role):

    current_user_id = current_user.get_id()
    if user_id == current_user_id:
        return False, 'Không được cập nhật tài khoản admin'
    
    #cập nhật role cho user
    response = supabase.table('user')\
        .update({'role': new_role})\
        .eq('user_id', user_id)\
        .execute()

    if response.data:
        return True,'Cập nhật phân quyền mới cho người dùng thành công'
    else:
        return False,'Cập nhật phân quyền mới cho người dùng thất bại. Hãy kiểm tra lại!'
    

def created_new_user(username, email, password, role, phone, faculty):
    
    if len(username) < 2:
             return False, 'Họ tên phải lớn hơn 1 ký tự.'
    if len(email) < 4:
             return False, 'Email phải lớn hơn 3 ký tự.'
    if len(password) < 8:
             return False, 'Mật khẩu phải có ít nhất 8 kí tự.'
    if role not in['student', 'hod', 'lecturer', 'approval',]:
          return False, 'Phân quyền không hợp lệ'
    
    try:
          auth_response = supabase_admin.auth.admin.create_user({
                "email":email,
                'password':password,
                'email_confirm':True
          })
          user_id=str(auth_response.user.id)

          insert_response = supabase.table('user').insert ({
            "user_id": user_id,
            "username": username,
            "email": email,
            "faculty":faculty,
            "phone": phone,
            "role": role,
            "status": 'active',
            "created_at": 'now()'
        }).execute()
          
          if insert_response.data:
                return True, 'Tạo người dùng thành công'
          else:
                return False,'Tạo người dùng thất bại'
    except Exception as e:
          return False, f'Lỗi hệ thống {str(e)}'
    


