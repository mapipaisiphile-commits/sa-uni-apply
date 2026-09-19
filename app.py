from flask import Flask, render_template, request, send_from_directory
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROSPECTUS_FOLDER = 'prospectus'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROSPECTUS_FOLDER, exist_ok=True)

UNIVERSITIES_DATA = [
    {"code": "UJ", "name": "University of Johannesburg", "location": "Johannesburg", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f", "prospectus": "UJ_Prospectus_2026.pdf"},
    {"code": "WITS", "name": "University of the Witwatersrand", "location": "Johannesburg", "image": "https://images.unsplash.com/photo-1562774053-701939374585", "prospectus": "Wits_Prospectus_2026.pdf"},
    {"code": "UP", "name": "University of Pretoria", "location": "Pretoria", "image": "https://images.unsplash.com/photo-1498243790137-0c08d6ed5de3", "prospectus": "UP_Prospectus_2026.pdf"},
    {"code": "STELLENBOSCH", "name": "Stellenbosch University", "location": "Stellenbosch", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1", "prospectus": "Stellenbosch_Prospectus_2026.pdf"},
    {"code": "UCT", "name": "University of Cape Town", "location": "Cape Town", "image": "https://images.unsplash.com/photo-1498243790137-0c08d6ed5de3", "prospectus": "UCT_Prospectus_2026.pdf"},
    {"code": "UKZN", "name": "University of KwaZulu-Natal", "location": "Durban", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f", "prospectus": "UKZN_Prospectus_2026.pdf"},
]

# FULL COURSE DATABASE WITH REQUIREMENTS
COURSES_DATA = [
    # Stellenbosch - like your screenshot
    {"id": 1, "uni_code": "STELLENBOSCH", "name": "BScAgric in Agricultural Economics", "faculty": "Faculty of AgriSciences", "type": "Bachelor's Degree", "duration": "4 years", "aps": "N/A", "status": "Closed", "subjects": ["English or Afrikaans · L4", "Mathematics · L5", "Physical Sciences · L4"]},
    {"id": 2, "uni_code": "STELLENBOSCH", "name": "BSc in Computer Science", "faculty": "Faculty of Science", "type": "Bachelor's Degree", "duration": "3 years", "aps": "32", "status": "Open", "subjects": ["English · L4", "Mathematics · L6", "Physical Sciences · L4"]},

    # UJ
    {"id": 3, "uni_code": "UJ", "name": "BSc Information Technology", "faculty": "Faculty of Science", "type": "Bachelor's Degree", "duration": "3 years", "aps": "26", "status": "Open", "subjects": ["English · L5", "Mathematics · L5"]},
    {"id": 4, "uni_code": "UJ", "name": "BCom Accounting", "faculty": "College of Business", "type": "Bachelor's Degree", "duration": "3 years", "aps": "28", "status": "Open", "subjects": ["English · L4", "Mathematics · L4"]},
    {"id": 5, "uni_code": "UJ", "name": "BEng Mechanical Engineering", "faculty": "Faculty of Engineering", "type": "Bachelor's Degree", "duration": "4 years", "aps": "32", "status": "Open", "subjects": ["English · L5", "Mathematics · L6", "Physical Sciences · L5"]},

    # WITS
    {"id": 6, "uni_code": "WITS", "name": "Bachelor of Medicine (MBBCh)", "faculty": "Faculty of Health Sciences", "type": "Bachelor's Degree", "duration": "6 years", "aps": "44", "status": "Open", "subjects": ["English · L5", "Mathematics · L5", "Physical Sciences · L5", "Life Sciences · L5"]},
    {"id": 7, "uni_code": "WITS", "name": "BSc Computer Science", "faculty": "Faculty of Science", "type": "Bachelor's Degree", "duration": "3 years", "aps": "42", "status": "Open", "subjects": ["English · L5", "Mathematics · L6"]},

    # UP
    {"id": 8, "uni_code": "UP", "name": "BSc Computer Science", "faculty": "EBIT", "type": "Bachelor's Degree", "duration": "3 years", "aps": "32", "status": "Open", "subjects": ["English · L4", "Mathematics · L6"]},
    {"id": 9, "uni_code": "UP", "name": "BVSc Veterinary Science", "faculty": "Veterinary Science", "type": "Bachelor's Degree", "duration": "6 years", "aps": "36", "status": "Closed", "subjects": ["English · L5", "Mathematics · L5", "Physical Sciences · L5"]},
]

def init_db():
    conn = sqlite3.connect('uniapply.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, aps INTEGER, course TEXT, universities TEXT, id_doc TEXT, report_doc TEXT)''')
    conn.commit(); conn.close()
init_db()

@app.route('/')
def home():
    search = request.args.get('search','').lower()
    # Filter courses by search
    if search:
        filtered = [c for c in COURSES_DATA if search in c['name'].lower() or search in c['uni_code'].lower() or search in c['faculty'].lower()]
    else:
        filtered = COURSES_DATA
    conn = sqlite3.connect('uniapply.db')
    count = conn.execute('SELECT COUNT(*) FROM applications').fetchone()[0]
    conn.close()
    return render_template('index.html', courses=filtered, universities=UNIVERSITIES_DATA, count=count, search=search)

@app.route('/university/<code>')
def university_detail(code):
    uni = next((u for u in UNIVERSITIES_DATA if u['code'] == code), None)
    uni_courses = [c for c in COURSES_DATA if c['uni_code'] == code]
    if not uni: return "University not found", 404
    return render_template('university.html', uni=uni, courses=uni_courses)

@app.route('/prospectus/<filename>')
def prospectus_file(filename):
    return send_from_directory(PROSPECTUS_FOLDER, filename)

@app.route('/apply', methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        #... keep your old apply logic...
        conn = sqlite3.connect('uniapply.db')
        conn.execute("INSERT INTO applications (name, email, phone, aps, course, universities) VALUES (?,?,?,?,?,?)",
            (request.form.get('name'), request.form.get('email'), request.form.get('phone'), request.form.get('aps'), request.form.get('course'), ", ".join(request.form.getlist('universities'))))
        conn.commit(); conn.close()
        return render_template('success.html')
    return render_template('apply.html', universities=UNIVERSITIES_DATA, courses=COURSES_DATA)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('uniapply.db'); conn.row_factory = sqlite3.Row
    apps = conn.execute('SELECT * FROM applications ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin.html', applications=apps)

if __name__ == '__main__':
    app.run(debug=True, port=5001)