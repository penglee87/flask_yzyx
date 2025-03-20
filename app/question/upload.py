from flask import request, jsonify, current_app
from app.question import bp
from app import csrf
import os
from werkzeug.utils import secure_filename
import uuid

# 允许的图片文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload_image', methods=['POST'])
@csrf.exempt
def upload_image():
    """处理富文本编辑器的图片上传"""
    if 'upload' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
        
    file = request.files['upload']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加唯一标识符，避免文件名冲突
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        # 确保上传目录存在
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        # 保存文件
        image_path = os.path.join(upload_folder, unique_filename)
        file.save(image_path)
        # 设置图片URL（相对路径，用于在模板中显示）
        image_url = f"/static/uploads/{unique_filename}"
        
        # 返回上传成功的响应，包含图片URL
        return jsonify({
            'url': image_url
        })
    
    return jsonify({'error': '不允许的文件类型'}), 400