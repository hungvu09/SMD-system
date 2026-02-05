
import ollama

class AIService:
    # kiểm tra logic clo plo
    @staticmethod
    def check_clo_plo_logic(clo_text, plo_text):

        prompt = f""" Bạn là một chuyên gia đầy thông minh và tài năng trong lĩnh vực đào tạo và đánh giá chất lượng giáo dục ở môi trường Đại học (Higher Education)
    Nhiệm vụ : Phân tích và đánh giá xem nội dung của chuẩn đầu ra học phần (CLO) có phù hợp và hỗ trợ cho việc đạt được chuẩn đầu ra chương trình (PLO) tương ứng hay không.

    Dữ liệu đầu vào:
    - Chuẩn đầu ra học phần (CLO): {clo_text}
    - Chuẩn đầu ra chương trình (PLO): {plo_text}

    Yêu cầu trả về:
    - Phân tích và đánh giá một cách có logic và chính xác, không lan man, không thêm thông tin không liên quan.
    - Đánh giá: (Phù hợp / Không phù hợp / Cần chỉnh sửa).
    - Giải thích ngắn gọn lý do.
    - Đề xuất đưa ra các chỉnh sửa cụ thể nếu cần thiết.
    - Thêm emoji để tạo cảm giác thân thiện.

    Trả lời bằng tiếng Việt. Định dạng câu trả lời dạng JSON."""
        
        try:
            response = ollama.chat(model = "llama3.2", messages = [
                {"role": "user", "content": prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Không thể đưa ra câu trả lời vào lúc này. {str(e)}"
        
# tóm tắt
    @staticmethod
    def summarize_syllabus(syllabus_content):
        
        try:
            response = ollama.chat(model='llama3', messages=[
                {
                    'role': 'user',
                    'content': f"Hãy tóm tắt nội dung đề cương môn học sau đây trong khoảng 100 từ, tập trung vào mục tiêu chính và phương pháp đánh giá: \n\n {syllabus_content}",
                },
            ])
            return response['message']['content']
        except Exception as e:
            return "Không thể tóm tắt lúc này."
        
# kiểm tra thay đổi
    @staticmethod
    def semantic_diff(self, old_content, new_content):
        prompt = f"""So sánh và phát hiện sự thay đổi ngữ nghĩa giữa hai đoạn văn bản nội dung cũ và nội dung mới. 


        Dữ liệu đầu vào:
        - Nội dung cũ'{old_content}' 
        - Nội dung mới: '{new_content}'. 
        
        Yêu cầu trả về:
        - Liệt kê các thay đổi chính giữa nội dung cũ và mới.
        - Trả lời bằng tiếng Việt."""

        return self.generate_response(prompt)