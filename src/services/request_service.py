# src/services/request_service.py
from data.supa import supabase
from datetime import datetime

class RequestService:

    def create_request(self, title, content, user_id):
        """
        User gửi request
        status mặc định = pending (DB tự set)
        """
        try:
            response = supabase.table("requests").insert({
                "title": title,
                "content": content,
                "created_by": user_id
            }).execute()

            return {
                "success": True,
                "data": response.data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_all_requests(self):
        """
        Reviewer / Approver xem danh sách request
        """
        try:
            response = supabase.table("requests") \
                .select("*") \
                .order("created_at", desc=True) \
                .execute()

            return response.data
        except Exception as e:
            return []

    def review_request(self, request_id, new_status, reviewer_id):
        """
        Reviewer / Approver duyệt request
        new_status: approved | rejected
        """
        try:
            response = supabase.table("requests") \
                .update({
                    "status": new_status,
                    "reviewed_by": reviewer_id,
                    "reviewed_at": datetime.utcnow().isoformat()
                }) \
                .eq("id", request_id) \
                .execute()

            return {
                "success": True,
                "data": response.data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
