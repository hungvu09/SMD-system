from flask import Blueprint, request, jsonify
from flask_login import current_user

from services.request_service import RequestService
from middleware.auth_required import auth_required
from middleware.role_required import role_required

request_bp = Blueprint("request", __name__)
request_service = RequestService()


# =======================
# USER: GỬI REQUEST
# =======================
@request_bp.route("/requests", methods=["POST"])
@auth_required
def create_request():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Thiếu title hoặc content"}), 400

    result = request_service.create_request(
        title=title,
        content=content,
        user_id=current_user.id

    )

    if result["success"]:
        return jsonify({
            "message": "Gửi request thành công",
            "data": result["data"]
        })
    else:
        return jsonify(result), 500


# =======================
# HoD / AA: XEM REQUEST
# =======================
@request_bp.route("/requests", methods=["GET"])
@auth_required
@role_required("hod", "approval", "admin")
def list_requests():
    data = request_service.get_all_requests()
    return jsonify(data)


# =======================
# HoD / AA: DUYỆT REQUEST
# =======================
@request_bp.route("/requests/<request_id>/review", methods=["PUT"])
@auth_required
@role_required("hod", "approval")
def review_request(request_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["approved", "rejected"]:
        return jsonify({"error": "Status không hợp lệ"}), 400

    result = request_service.review_request(
        request_id=request_id,
        new_status=new_status,
        reviewer_id=current_user.id
    )

    if result["success"]:
        return jsonify({"message": "Duyệt request thành công"})
    else:
        return jsonify(result), 500
