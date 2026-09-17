import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ADMIN_PASSWORD = "M@pip@isiphile05"  # Change this to your secret password!
WHATSAPP_NUMBER = "27631266734"  # Put your WhatsApp number here e.g. 27821234567 (no +)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        uni = request.form.get('university')
        
        files_saved = []
        for file in request.files.getlist('documents'):
            if file.filename:
                filename = f"{datetime.now().strftime('%m%d%H%M%S')}_{phone}_{secure_filename(name)}_{secure_filename(file.filename)}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                files_saved.append(filename)
        
        # Save info as txt
        info_file = f"{datetime.now().strftime('%m%d%H%M%S')}_{phone}_{secure_filename(name)}.txt"
        with open(os.path.join(UPLOAD_FOLDER, info_file), 'w') as f:
            f.write(f"Name: {name}\nPhone: {phone}\nUniversity: {uni}\nDate: {datetime.now()}\nFiles: {files_saved}")
        
        return render_template('success.html', name=name, phone=phone, whatsapp=WHATSAPP_NUMBER)
    return render_template('apply.html')

@app.route('/admin')
def admin():
    pwd = request.args.get('pwd')
    if pwd != ADMIN_PASSWORD:
        return '''
        <div style="text-align:center; margin-top:100px; font-family:sans-serif">
        <h2>🔒 Admin Locked</h2>
        <p>Add password to link: ?pwd=Isiphile2026</p>
        <p>Example: /admin?pwd=Isiphile2026</p>
        <a href="/">Back Home</a>
        </div>
        '''
    files = os.listdir(UPLOAD_FOLDER)
    files.sort(reverse=True)
    return render_template('admin.html', files=files, total=len(files))

@app.route('/uploads/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)