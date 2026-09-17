from flask import Flask, render_template, request, redirect, send_from_directory
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
]

@app.route('/')
def home():
    return render_template('home.html', unis=unis)

@app.route('/apply', methods=['GET','POST'])
def apply_page():
    if request.method == 'POST':
        return handle_upload(request)
    return render_template('apply.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        return handle_upload(request)
    return redirect('/apply')

def handle_upload(req):
    fullname = req.form.get('fullname','').replace(' ','_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []
    for key in ['file_id','file_grade11','file_grade12_mid','file_matric','file_proof']:
        f = req.files.get(key)
        if f and f.filename != '':
            filename = f"{timestamp}_{fullname}_{key}_{f.filename}"
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            saved.append(filename)
    # You can see all files in /admin?pwd=Isiphile2026
    return render_template('succes.html', ref=f"{timestamp}", count=len(saved), name=req.form.get('fullname'))

@app.route('/aps', methods=['GET','POST'])
def aps():
    score=None
    if request.method=='POST':
        try: score=sum(int(request.form.get(f's{i}',0)) for i in range(1,8))//7
        except: score=0
    return render_template('aps.html', score=score)

@app.route('/status')
def status(): return render_template('status.html', unis=unis)

@app.route('/admin')
def admin():
    if request.args.get('pwd')!='Isiphile2026': return "Unauthorized - ?pwd=Isiphile2026",401
    files=os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    return render_template('admin.html', files=files, total=len(files))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename): return send_from_directory(UPLOAD_FOLDER, filename)

if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)