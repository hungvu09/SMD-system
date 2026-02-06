from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Vui lòng đăng nhập", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
