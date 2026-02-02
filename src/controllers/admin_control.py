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
    

def toggle_user_status(user_id):
    # lấy thong tin của user từ bảng user trên database
    user_data = supabase.table('user').select('status').eq('user_id', user_id).single().execute().data
    
    if user_data:
        # thay đổi trạng thái khi trỏ vào nút
        new_status = 'locked' if user_data['status'] == 'active' else 'active'
        
        # cập nhật trạng thái mới
        supabase.table('user').update({'status': new_status}).eq('user_id', user_id).execute()
        
        flash(f"Đã {'khóa' if new_status == 'locked' else 'mở khóa'} tài khoản thành công!", category='success')



def system_config_up(semester, static_inf, score_scale, clo_plo_template,id_settings):
      try:
          import json
          data = {
              "id_settings": id_settings,
              "semester": semester,
              "static_inf": static_inf,
              "score_scale": score_scale,
              "clo_plo_template": json.loads(clo_plo_template)
          }
          supabase.table('system_settings').upsert(data).eq('id_settings', 1).single().execute()
          
          return True,"Cập nhật cấu hình hệ thống thành công!"
      except Exception as e:
          
          return False, f"Lỗi hệ thống: {str(e)}"



def admin_publish_management(syllabus_id, new_status):
    try:
        syllabus_id = int(syllabus_id)
        data = {
              "status"  : new_status,
              "published_at": "now()" if "new_status" == 'approved' else None
          }

        supabase.table('syllabus').update(data).eq('syl_id', syllabus_id).execute()

        msg = "Đã phê duyệt giáo trình!" if new_status == "approved" else " Đã từ chối giáo trình."
        flash(msg, category='success' if new_status == "approved" else 'warning')
        return True,
    except Exception as e:
        flash(f"Lỗi hệ thống: {str(e)}", category='error')
        return False

