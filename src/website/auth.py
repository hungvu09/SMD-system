from flask import Blueprint, render_template, request, flash, redirect, url_for
from data.supa import supabase
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash #Hàm băm mật khẩu
from services.auth_service import Authservice
from _object.entities.model_users import User

auth = Blueprint('auth', __name__)


# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        auth_service = Authservice()
        result = auth_service.login(email, password)

        if result.get('success'):
            # tạo đối tượng  user
            user = User.get(result['user_id'])


            user_id = result.get('user_id')
            role = result.get('role')
            username = result.get('username')
            if user:
                login_user(user)
                flash('Đăng nhập thành công!', category='success')


                # chuyển hướng đến trang dựa trên vai trò của người dùng
                if role == 'student':
                    return redirect(url_for('views.student'))
                elif role == 'aa':
                    return redirect(url_for('views.academic'))
                
                elif role in ['hod', 'rector']:
                    return redirect(url_for('views.approval'))
                
                elif role == 'lecturer':
                    return redirect(url_for('views.lecturer'))
                
                else:
                    return redirect(url_for('views.admin'))
            else:
                flash('Dữ liệu người dùng không tồn tại!', category='error')
        else:
            flash(result.get('message', 'Sai email hoặc mật khẩu!'), category='error')

    return render_template('login.html', user=current_user)


# Logout route
@auth.route('/logout')
def logout():
    supabase.auth.sign_out()
    flash('Đăng xuất thành công!', category='success')
    return redirect(url_for('auth.login'))


# Signup route
# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():

#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         phone = request.form.get('phone', None)
        
#         auth_service = Authservice()
#         result = auth_service.signup(username, email, password1, password2, phone)

#         if result == 'success':
#            return redirect(url_for('auth.login'))

#     return render_template('signup.html', user=current_user)