from flask import Blueprint, render_template, redirect, url_for,request, flash
from flask_login import login_required, current_user
from data.supa import supabase
from middleware.role_required import role_required
from controllers.admin_control import system_config_up, updated_user_role, created_new_user, toggle_user_status, admin_publish_management
from services.notification_ser import NotificationService


views = Blueprint('views', __name__)

#HOME
@views.route('/')
def home():
    return render_template('home.html')



#STUDENT
@views.route('/student')
@login_required
def student():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('student.html', users=users)




#ADMIN
@views.route('/admin')
@login_required
def admin():
    
    return render_template('_admin/admin.html',  current_user=current_user)

@views.route('/admin/manager', methods = ['GET','POST'])
@login_required
@role_required('admin')

def manager():
    users = supabase.table('user')\
        .select('user_id', 'username', 'email', 'role', 'status', 'created_at', 'faculty')\
        .neq('role', 'admin')\
        .execute().data
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')


        if action == 'update_role':
            new_role = request.form.get('role')
    
            success, message = updated_user_role(current_user, user_id, new_role)
            flash(message, category='success' if success else 'error')
        elif action =='toggle_status':
            toggle_user_status(user_id)
        return redirect(url_for('views.manager'))
    return render_template('_admin/manager.html',users=users, current_user=current_user)



@views.route('/admin/manager/create_user',methods = ['GET','POST'] )
@login_required
@role_required('admin')
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        faculty = request.form.get('faculty')
        role = request.form.get('role')
        phone = request.form.get('phone')

        success, message = created_new_user(username, email, password, role, phone, faculty)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('views.manager'))

    return render_template('_admin/create_user.html', current_user=current_user)


@views.route('/admin/publish_a', methods = ['GET','POST'])
@login_required
@role_required('admin')
def publish_a():
    if request.method == 'POST':
        syllabus_id = request.form.get('syllabus_id')
        action = request.form.get('action')

        success = admin_publish_management(syllabus_id, action)
        if success:
            flash('Cập nhật trạng thái giáo trình thành công!', category='success')
        else:
            flash('Cập nhật trạng thái giáo trình thất bại!', category='error')
        return redirect(url_for('views.publish_a'))

    pending_list = supabase.table('syllabus').select('*').eq('status', 'pending').execute().data
    return render_template('_admin/publish_a.html', documents=pending_list, user=current_user)

@views.route('/admin/system_config', methods = ['GET','POST'])
@login_required
@role_required('admin')
def system_config():
    if request.method == 'POST':
        semester = request.form.get('semester')
        static_inf = request.form.get('static_inf')
        score_scale = request.form.get('score_scale')
        clo_plo_template = request.form.get('clo_plo_template')
        id_settings = request.form.get('id_settings')

        success,message = system_config_up(semester, static_inf, score_scale, clo_plo_template, id_settings)
        flash(message, category='success' if success else 'error')
        return redirect(url_for('views.system_config'))

    config = supabase.table('system_settings').select('*').execute().data
    return render_template('_admin/system_config.html', config=config, current_user=current_user)



#LECTURER
@views.route('/lecturer')
@login_required
def lecturer():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('lecturer.html', users=users)





#ACADEMIC AFFAIRS
@views.route('/academic')
@login_required
def academic():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('academic.html', users=users)








#rector
@views.route('/rector')
@login_required
def rector():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('rector.html', users=users)


#rector
@views.route('/hod')
@login_required
def hod():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('hod.html', users=users)



@views.route('/notifications')
@login_required
def all_notifications():
    # lấy thông báo 
    notifications = NotificationService.get_personal_notifications(current_user.id)
    return render_template('notifications_all.html', notifications=notifications, user=current_user)