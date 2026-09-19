from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# UNIVERSITIES
UNIVERSITIES_DATA = [
    {'code': 'STELLENBOSCH', 'name': 'Stellenbosch University', 'location': 'Stellenbosch', 'prospectus': 'stellenbosch_prospectus.pdf'},
    {'code': 'UJ', 'name': 'University of Johannesburg', 'location': 'Johannesburg', 'prospectus': 'uj_prospectus.pdf'},
    {'code': 'WITS', 'name': 'University of the Witwatersrand', 'location': 'Johannesburg', 'prospectus': 'wits_prospectus.pdf'},
    {'code': 'UCT', 'name': 'University of Cape Town', 'location': 'Cape Town', 'prospectus': 'uct_prospectus.pdf'},
    {'code': 'UP', 'name': 'University of Pretoria', 'location': 'Pretoria', 'prospectus': 'up_prospectus.pdf'},
    {'code': 'UKZN', 'name': 'University of KwaZulu-Natal', 'location': 'Durban', 'prospectus': 'ukzn_prospectus.pdf'},
    {'code': 'UFS', 'name': 'University of the Free State', 'location': 'Bloemfontein', 'prospectus': 'ufs_prospectus.pdf'},
    {'code': 'NWU', 'name': 'North-West University', 'location': 'Potchefstroom', 'prospectus': 'nwu_prospectus.pdf'},
    {'code': 'CPUT', 'name': 'Cape Peninsula University of Technology', 'location': 'Cape Town', 'prospectus': 'cput_prospectus.pdf'},
    {'code': 'TUT', 'name': 'Tshwane University of Technology', 'location': 'Pretoria', 'prospectus': 'tut_prospectus.pdf'},
]

# 40+ REAL COURSES WITH REQUIREMENTS
COURSES_DATA = [
    # STELLENBOSCH
    {'name': 'BScAgric in Agricultural Economics', 'uni_code': 'STELLENBOSCH', 'faculty': 'Faculty of AgriSciences', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': 'N/A', 'subjects': ['English or Afrikaans - L4', 'Mathematics - L5', 'Physical Sciences - L4'], 'status': 'Open'},
    {'name': 'BSc in Computer Science', 'uni_code': 'STELLENBOSCH', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '32', 'subjects': ['English - L4', 'Mathematics - L6', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'MBChB Medicine', 'uni_code': 'STELLENBOSCH', 'faculty': 'Faculty of Medicine', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '38', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L6', 'Life Sciences - L6'], 'status': 'Open'},
    {'name': 'BCom Accounting (CA Stream)', 'uni_code': 'STELLENBOSCH', 'faculty': 'Faculty of Economic Sciences', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '34', 'subjects': ['English - L5', 'Mathematics - L6', 'Accounting - L5'], 'status': 'Open'},

    # UJ
    {'name': 'BSc Information Technology', 'uni_code': 'UJ', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '26', 'subjects': ['English - L5', 'Mathematics - L5'], 'status': 'Open'},
    {'name': 'BEng in Mechanical Engineering', 'uni_code': 'UJ', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '32', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'BCom Finance', 'uni_code': 'UJ', 'faculty': 'College of Business', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '28', 'subjects': ['English - L4', 'Mathematics - L5'], 'status': 'Open'},
    {'name': 'LLB Law', 'uni_code': 'UJ', 'faculty': 'Faculty of Law', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '30', 'subjects': ['English - L6', 'Mathematics - L4', 'Mathematical Literacy - L6'], 'status': 'Open'},
    {'name': 'Diploma in Nursing', 'uni_code': 'UJ', 'faculty': 'Faculty of Health', 'type': 'Diploma', 'duration': '3 years', 'aps': '24', 'subjects': ['English - L4', 'Mathematics - L3', 'Life Sciences - L4'], 'status': 'Open'},

    # WITS
    {'name': 'BSc Computer Science', 'uni_code': 'WITS', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '34', 'subjects': ['English - L5', 'Mathematics - L6'], 'status': 'Open'},
    {'name': 'MBBCh Medicine', 'uni_code': 'WITS', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '42', 'subjects': ['English - L5', 'Mathematics - L5', 'Physical Sciences - L5', 'Life Sciences - L5'], 'status': 'Open'},
    {'name': 'BSc Actuarial Science', 'uni_code': 'WITS', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '42', 'subjects': ['English - L5', 'Mathematics - L8'], 'status': 'Open'},
    {'name': 'BCom Accounting', 'uni_code': 'WITS', 'faculty': 'Faculty of Commerce', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '36', 'subjects': ['English - L5', 'Mathematics - L5'], 'status': 'Open'},
    {'name': 'BEng Civil Engineering', 'uni_code': 'WITS', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '36', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L6'], 'status': 'Open'},

    # UCT
    {'name': 'BSc Computer Science', 'uni_code': 'UCT', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '36', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'MBChB Medicine', 'uni_code': 'UCT', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '45', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L5', 'Life Sciences - L5'], 'status': 'Open'},
    {'name': 'BCom Finance & Accounting', 'uni_code': 'UCT', 'faculty': 'Faculty of Commerce', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '38', 'subjects': ['English - L5', 'Mathematics - L6'], 'status': 'Open'},
    {'name': 'BSc Electrical Engineering', 'uni_code': 'UCT', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '40', 'subjects': ['English - L5', 'Mathematics - L7', 'Physical Sciences - L6'], 'status': 'Open'},

    # UP
    {'name': 'BSc Computer Science', 'uni_code': 'UP', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '30', 'subjects': ['English - L5', 'Mathematics - L6'], 'status': 'Open'},
    {'name': 'MBChB Medicine', 'uni_code': 'UP', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '35', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L6'], 'status': 'Open'},
    {'name': 'LLB Law', 'uni_code': 'UP', 'faculty': 'Faculty of Law', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '32', 'subjects': ['English - L5'], 'status': 'Open'},
    {'name': 'BCom Investment Management', 'uni_code': 'UP', 'faculty': 'Faculty of Economic', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '34', 'subjects': ['English - L5', 'Mathematics - L6'], 'status': 'Open'},
    {'name': 'BEd Foundation Phase', 'uni_code': 'UP', 'faculty': 'Faculty of Education', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '28', 'subjects': ['English - L5', 'Mathematics - L4'], 'status': 'Open'},

    # UKZN
    {'name': 'MBChB Medicine', 'uni_code': 'UKZN', 'faculty': 'College of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '33', 'subjects': ['English - L5', 'Mathematics - L5', 'Life Sciences - L5', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'BSc Computer Science', 'uni_code': 'UKZN', 'faculty': 'College of Agriculture', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '28', 'subjects': ['English - L4', 'Mathematics - L5'], 'status': 'Open'},
    {'name': 'BCom Accounting', 'uni_code': 'UKZN', 'faculty': 'College of Law & Management', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '30', 'subjects': ['English - L5', 'Mathematics - L5'], 'status': 'Open'},

    # OTHER UNIVERSITIES
    {'name': 'BSc in IT', 'uni_code': 'NWU', 'faculty': 'Faculty of Natural Sciences', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '26', 'subjects': ['English - L4', 'Mathematics - L5'], 'status': 'Open'},
    {'name': 'B Nursing', 'uni_code': 'UFS', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '30', 'subjects': ['English - L4', 'Mathematics - L4', 'Life Sciences - L5'], 'status': 'Open'},
    {'name': 'National Diploma in IT', 'uni_code': 'CPUT', 'faculty': 'Faculty of Informatics', 'type': 'Diploma', 'duration': '3 years', 'aps': '22', 'subjects': ['English - L4', 'Mathematics - L4'], 'status': 'Open'},
    {'name': 'Diploma in Electrical Engineering', 'uni_code': 'TUT', 'faculty': 'Faculty of Engineering', 'type': 'Diploma', 'duration': '3 years', 'aps': '24', 'subjects': ['English - L4', 'Mathematics - L5', 'Physical Sciences - L4'], 'status': 'Open'},
    {'name': 'BSc Biotechnology', 'uni_code': 'UJ', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '26', 'subjects': ['English - L5', 'Mathematics - L4', 'Life Sciences - L4', 'Physical Sciences - L4'], 'status': 'Closed'},
    {'name': 'BCom Marketing', 'uni_code': 'WITS', 'faculty': 'Faculty of Commerce', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '32', 'subjects': ['English - L5', 'Mathematics - L4'], 'status': 'Open'},
    {'name': 'BSc Civil Engineering', 'uni_code': 'UCT', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '38', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L6'], 'status': 'Open'},
]

NSFAS_INFO = {
    'closing_date': '31 October 2026',
    'documents': [
        '✅ Certified copy of your ID (not older than 3 months)',
        '✅ Certified ID copies of parents/guardian/spouse',
        '✅ Proof of income - payslips (if employed) or affidavit if unemployed',
        '✅ SASSA grant letter (if receiving grant)',
        '✅ Consent form signed by parents/guardian',
        '✅ Proof of residence (municipal account or letter)',
        '✅ Academic results - Grade 11 final + Grade 12 latest results',
        '✅ University acceptance letter or provisional offer (if available)',
        '✅ Disability certificate (if applicable)',
        '✅ Death certificates if parents are deceased',
    ]
}

def init_db():
    conn = sqlite3.connect('uniapply.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, aps INTEGER, course TEXT, universities TEXT, id_doc TEXT, report_doc TEXT, status TEXT DEFAULT 'Pending')''')
    conn.commit(); conn.close()
init_db()

@app.route('/')
def home():
    search = request.args.get('search','').lower()
    if search:
        filtered = [c for c in COURSES_DATA if search in c['name'].lower() or search in c['uni_code'].lower() or search in c['faculty'].lower()]
    else:
        filtered = COURSES_DATA
    uni_map = {u['code']: u for u in UNIVERSITIES_DATA}
    conn = sqlite3.connect('uniapply.db')
    count = conn.execute('SELECT COUNT(*) FROM applications').fetchone()[0]
    conn.close()
    return render_template('index.html', courses=filtered, universities=UNIVERSITIES_DATA, uni_map=uni_map, count=count, search=search, nsfas=NSFAS_INFO)

@app.route('/apply', methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        aps = request.form.get('aps')
        course = request.form.get('course')
        universities = request.form.get('universities')
        conn = sqlite3.connect('uniapply.db')
        conn.execute('INSERT INTO applications (name,email,phone,aps,course,universities) VALUES (?,?,?,?,?,?)', (name,email,phone,aps,course,universities))
        conn.commit(); conn.close()
        return render_template('succes.html', name=name)
    course_q = request.args.get('course','')
    return render_template('apply.html', courses=COURSES_DATA, selected_course=course_q, universities=UNIVERSITIES_DATA)

@app.route('/prospectus/<filename>')
def prospectus(filename):
    return send_from_directory('prospectus', filename)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('uniapply.db')
    apps = conn.execute('SELECT * FROM applications ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin.html', apps=apps)

if __name__ == '__main__':
    app.run(debug=True, port=5001)