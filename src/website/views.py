from flask import Blueprint, render_template, redirect, url_for,request, flash
from flask_login import login_required, current_user
from data.supa import supabase
from middleware.role_required import role_required
from controllers.admin_control import updated_user_role, created_new_user, toggle_user_status

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








#RECTOR AND HOD
@views.route('/approval')
@login_required
def approval():
    response = supabase.from_('user').select('*').execute()
    users = response.data or []
    return render_template('approval.html', users=users)