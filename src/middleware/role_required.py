from functools import wraps
from flask import session, redirect, url_for, abort, request,flash
from flask_login import current_user

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:  
                flash('Vui lòng đăng nhập.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in allowed_roles:
                flash('Bạn không có quyền truy cập trang này.', 'error')
                return redirect(url_for('views.home'))  
            
            return f(*args, **kwargs)
        return decorated
    return decorator