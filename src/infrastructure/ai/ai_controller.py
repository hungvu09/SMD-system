from flask import Blueprint, render_template, request, jsonify
from infrastructure.ai.ai_service import AIService


ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/ai/check-clo-plo', methods=['POST'])
def check_clo_plo():
    data = request.json
    clo = data.get('clo')
    plo = data.get('plo')
    
    if not clo or not plo:
        return jsonify({'error': 'Thiếu dữ liệu CLO hoặc PLO'}), 400
        
    # Gọi Service AI
    result = AIService.check_clo_plo_logic(clo, plo)
    
    return jsonify({'result': result})

@ai_bp.route('/ai/summarize', methods=['POST'])
def summarize():
    data = request.json
    content = data.get('content')
    
    result = AIService.summarize_syllabus(content)
    return jsonify({'result': result})

@ai_bp.route('/ai/semantic-diff', methods=['POST'])
def semantic_diff():
    data = request.json
    old_content = data.get('old_content')
    new_content = data.get('new_content')
    
    result = AIService.semantic_diff(old_content, new_content)
    return jsonify({'result': result})