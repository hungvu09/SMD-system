from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from data.supa import supabase

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            # Chưa login
            if not current_user.is_authenticated:
                flash("Vui lòng đăng nhập", "warning")
                return redirect(url_for("auth.login"))

            try:
                # Lấy role từ database
                user_data = supabase.table("user") \
                    .select("role") \
                    .eq("user_id", current_user.user_id) \
                    .single() \
                    .execute()

                role = user_data.data["role"]

                # Check quyền
                if role not in allowed_roles:
                    flash("Bạn không có quyền truy cập", "error")
                    return redirect(url_for("views.home"))

            except Exception as e:
                print("Role check error:", e)
                return redirect(url_for("views.home"))

            return f(*args, **kwargs)

        return decorated
    return decorator
