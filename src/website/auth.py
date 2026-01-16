from flask import Blueprint, render_template, request, flash, redirect, url_for
from data.supa import supabase
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash #Hàm băm mật khẩu
from .services.auth_service import Authservice
from website.model.model_users import User

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
            user = User.get(result['user_id'])
            if user:
                login_user(user)
                flash('Đăng nhập thành công!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Dữ liệu người dùng không tồn tại!', category='error')
        else:
            flash(result.get('message', 'Đăng nhập thất bại!'), category='error')

    return render_template('login.html', user=current_user)


# Logout route
@auth.route('/logout')
def logout():
    supabase.auth.sign_out()
    flash('Đăng xuất thành công!', category='success')
    return redirect(url_for('auth.login'))


# Signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phone', None)
        
        auth_service = Authservice()
        result = auth_service.signup(username, email, password1, password2, phone)

        if result == 'success':
           return redirect(url_for('auth.login'))

    return render_template('signup.html', user=current_user)