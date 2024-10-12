from flask import Blueprint, render_template, request, jsonify, current_app
import os
import uuid

upload = Blueprint('upload', __name__)


@upload.route('/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({"code": 400, "message": "No file part"}), 200
    
    if request.files['file'].filename == '':
        return jsonify({"code": 400, "message": "No selected file"}), 200
        
    file = request.files['file']
    _, file_extension = os.path.splitext(file.filename)
    
    if file_extension not in current_app.config['ALLOWED_EXTENSIONS']:
        return jsonify({"code": 400, "message": "File extension is not allowed"}), 200
    
    new_filename = str(uuid.uuid4()) + file_extension
    
    if file:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        return jsonify({"code": 200, "message": "Upload successfully", "file_path": f"/static/uploads/{new_filename}"}), 200
    
    return jsonify({"code": 400, "message": "Upload failed"}), 200
