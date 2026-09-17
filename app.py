from flask import Flask, render_template, request, redirect, url_for
import os, datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

unis = [
    {"name":"University of Johannesburg (UJ)","status":"Open","date":"30 Sep 2026","color":"green"},
    {"name":"University of Pretoria (UP)","status":"Open","date":"30 Sep 2026","color":"green"},
    {"name":"WITS","status":"Open","date":"30 Sep 2026","color":"green"},
    {"name":"UNISA","status":"Open","date":"15 Oct 2026","color":"green"},
    {"name":"TUT","status":"Open","date":"30 Sep 2026","color":"green"},
    {"name":"University of Limpopo","status":"Closing Soon","date":"25 Sep 2026","color":"yellow"},
]

@app.route('/')
def home():
    return render_template('home.html', unis=unis)

@app.route('/apply')
def apply_page():
    return render_template('apply.html')

@app.route('/aps', methods=['GET','POST'])
def aps():
    score = None
    if request.method == 'POST':
        try:
            total = sum(int(request.form.get(f's{i}',0)) for i in range(1,8))
            score = total // 7
        except: score = 0
    return render_template('aps.html', score=score)

@app.route('/status')
def status():
    return render_template('status.html', unis=unis)

@app.route('/submit', methods=['POST'])
def submit():
    f = request.files.get('file')
    if f:
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_") + f.filename
        f.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template('succes.html')

@app.route('/admin')
def admin():
    if request.args.get('pwd') != 'Isiphile2026':
        return "Unauthorized - Add ?pwd=Isiphile2026", 401
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('admin.html', files=files, total=len(files))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)