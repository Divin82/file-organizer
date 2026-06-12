from flask import Flask, render_template, request, jsonify
import os
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ORGANIZED_FOLDER = 'organized'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FILE_TYPES = {
    "Code": [".py", ".js", ".sql", ".c", ".html", ".css"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Data": [".csv", ".json", ".xlsx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    results = []
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        ext = Path(filename).suffix.lower()
        category = next((cat for cat, exts in FILE_TYPES.items() if ext in exts), "Others")
        dest_folder = os.path.join(ORGANIZED_FOLDER, category)
        os.makedirs(dest_folder, exist_ok=True)
        shutil.move(filepath, os.path.join(dest_folder, filename))
        results.append({"file": filename, "category": category})
    return jsonify({"success": True, "results": results})

if __name__ == '__main__':
    app.run(debug=True)
