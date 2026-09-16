from flask import Flask, render_template, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
os.makedirs('uploads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        name = request.form.get('fullname')
        idnum = request.form.get('idnum')
        with open(f"uploads/{idnum}_{name}.txt", "w", encoding="utf-8") as f:
            f.write(f"Name: {name}\nID: {idnum}\nPhone: {request.form.get('phone')}\nAverage: {request.form.get('average')}\nCourse: {request.form.get('course')}\nDate: {datetime.now()}\n")
        file = request.files.get('iddoc')
        if file and file.filename:
            file.save(os.path.join('uploads', f"{idnum}_{file.filename}"))
        return f"<div style='text-align:center;padding:50px'><h1>✅ Thank You {name}!</h1><p>Your application for {request.form.get('course')} is received.</p><p>We will WhatsApp you on {request.form.get('phone')}</p><a href='/'>Home</a></div>"
    return render_template('apply.html')

@app.route('/admin')
def admin():
    files = os.listdir('uploads')
    return render_template('admin.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)