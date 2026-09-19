from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__)

UNIVERSITIES_DATA = [
    {'code': 'UJ', 'name': 'University of Johannesburg (UJ)', 'location': 'Johannesburg', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=500', 'prospectus': 'uj_prospectus.pdf', 'apply_link': 'https://www.uj.ac.za'},
    {'code': 'UP', 'name': 'University of Pretoria (UP)', 'location': 'Pretoria', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500', 'prospectus': 'up_prospectus.pdf', 'apply_link': 'https://www.up.ac.za'},
    {'code': 'WITS', 'name': 'WITS', 'location': 'Johannesburg', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=500', 'prospectus': 'wits_prospectus.pdf', 'apply_link': 'https://www.wits.ac.za'},
    {'code': 'UCT', 'name': 'University of Cape Town (UCT)', 'location': 'Cape Town', 'closing': '31 Jul', 'image': 'https://images.unsplash.com/photo-1588075592446-265fd1e4e76f?w=500', 'prospectus': 'uct_prospectus.pdf', 'apply_link': 'https://www.uct.ac.za'},
    {'code': 'STELLENBOSCH', 'name': 'Stellenbosch University', 'location': 'Stellenbosch', 'closing': '31 Jul', 'image': 'https://images.unsplash.com/photo-1498243793788-2be5d4346f13?w=500', 'prospectus': 'stellenbosch_prospectus.pdf', 'apply_link': 'https://www.sun.ac.za'},
    {'code': 'UKZN', 'name': 'University of KwaZulu-Natal (UKZN)', 'location': 'Durban', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500', 'prospectus': 'ukzn_prospectus.pdf', 'apply_link': 'https://ukzn.ac.za'},
    {'code': 'UFS', 'name': 'University of Free State (UFS)', 'location': 'Bloemfontein', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=500', 'prospectus': 'ufs_prospectus.pdf', 'apply_link': 'https://www.ufs.ac.za'},
    {'code': 'NWU', 'name': 'North-West University (NWU)', 'location': 'Potchefstroom', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=500', 'prospectus': 'nwu_prospectus.pdf', 'apply_link': 'https://www.nwu.ac.za'},
]

COURSES_DATA = [
    {'name': 'BSc Information Technology', 'uni_code': 'UJ', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '26', 'subjects': ['English - L5 (60%)', 'Mathematics - L5 (60%)'], 'status': 'Open'},
    {'name': 'BEng Mechanical Engineering', 'uni_code': 'UJ', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '32', 'subjects': ['English - L5', 'Mathematics - L6 (70%)', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'BCom Finance', 'uni_code': 'UJ', 'faculty': 'College of Business', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '28', 'subjects': ['English - L4', 'Mathematics - L5'], 'status': 'Open'},
    {'name': 'LLB Law', 'uni_code': 'UJ', 'faculty': 'Faculty of Law', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '30', 'subjects': ['English - L6', 'Mathematics - L4'], 'status': 'Open'},
    {'name': 'Diploma in Nursing', 'uni_code': 'UJ', 'faculty': 'Faculty of Health', 'type': 'Diploma', 'duration': '3 years', 'aps': '24', 'subjects': ['English - L4', 'Mathematics - L3', 'Life Sciences - L4'], 'status': 'Open'},
    {'name': 'BSc Computer Science', 'uni_code': 'WITS', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '34', 'subjects': ['English - L5', 'Mathematics - L6'], 'status': 'Open'},
    {'name': 'MBBCh Medicine', 'uni_code': 'WITS', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '42', 'subjects': ['English - L5', 'Mathematics - L5', 'Physical Sciences - L5', 'Life Sciences - L5'], 'status': 'Open'},
    {'name': 'BSc Actuarial Science', 'uni_code': 'WITS', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '42', 'subjects': ['English - L5', 'Mathematics - L8 (80%)'], 'status': 'Open'},
    {'name': 'BEng Civil Engineering', 'uni_code': 'WITS', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '36', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L6'], 'status': 'Open'},
    {'name': 'BSc Computer Science', 'uni_code': 'UCT', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '36', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'MBChB Medicine', 'uni_code': 'UCT', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '45', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L5', 'Life Sciences - L5'], 'status': 'Open'},
    {'name': 'BSc in Computer Science', 'uni_code': 'STELLENBOSCH', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '32', 'subjects': ['English - L4', 'Mathematics - L6', 'Physical Sciences - L5'], 'status': 'Open'},
    {'name': 'BScAgric in Agricultural Economics', 'uni_code': 'STELLENBOSCH', 'faculty': 'Faculty of AgriSciences', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '30', 'subjects': ['English - L4', 'Mathematics - L5', 'Physical Sciences - L4'], 'status': 'Open'},
    {'name': 'BSc Computer Science', 'uni_code': 'UP', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '30', 'subjects': ['English - L5', 'Mathematics - L6'], 'status': 'Open'},
    {'name': 'MBChB Medicine', 'uni_code': 'UP', 'faculty': 'Faculty of Health', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '35', 'subjects': ['English - L5', 'Mathematics - L6', 'Physical Sciences - L6'], 'status': 'Open'},
    {'name': 'LLB Law', 'uni_code': 'UP', 'faculty': 'Faculty of Law', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '32', 'subjects': ['English - L5'], 'status': 'Open'},
]

NSFAS_INFO = {
    'closing_date': '31 October 2026',
    'documents': [
        'Certified copy of your ID (not older than 3 months)',
        'Certified ID copies of parents/guardian/spouse',
        'Proof of income - payslips or affidavit if unemployed',
        'SASSA grant letter (if receiving)',
        'Consent form signed by parents/guardian',
        'Proof of residence',
        'Grade 11 final + Grade 12 latest results',
        'Disability certificate (if applicable)',
    ]
}

def init_db():
    conn = sqlite3.connect('uniapply.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, aps INTEGER, course TEXT, universities TEXT, status TEXT DEFAULT 'Pending')''')
    conn.commit(); conn.close()
init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('uniapply.db')
    count = conn.execute('SELECT COUNT(*) FROM applications').fetchone()[0]
    conn.close()
    return render_template('landing.html', count=count, nsfas=NSFAS_INFO)

@app.route('/universities')
def universities():
    return render_template('universities.html', universities=UNIVERSITIES_DATA)

@app.route('/courses/<uni_code>')
def courses_by_uni(uni_code):
    search = request.args.get('search','').lower()
    uni = next((u for u in UNIVERSITIES_DATA if u['code'] == uni_code), None)
    filtered = [c for c in COURSES_DATA if c['uni_code'] == uni_code]
    if search:
        filtered = [c for c in filtered if search in c['name'].lower()]
    uni_map = {u['code']: u for u in UNIVERSITIES_DATA}
    return render_template('courses.html', courses=filtered, uni=uni, uni_map=uni_map, search=search, universities=UNIVERSITIES_DATA)

@app.route('/prospectus/<filename>')
def prospectus(filename):
    return send_from_directory('prospectus', filename)

@app.route('/apply', methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        conn = sqlite3.connect('uniapply.db')
        conn.execute('INSERT INTO applications (name,email,phone,aps,course,universities) VALUES (?,?,?,?,?,?)',
                     (request.form.get('name'), request.form.get('email'), request.form.get('phone'), request.form.get('aps'), request.form.get('course'), request.form.get('universities')))
        conn.commit(); conn.close()
        return render_template('succes.html', name=request.form.get('name'))
    course_q = request.args.get('course','')
    uni_q = request.args.get('uni','')
    return render_template('apply.html', courses=COURSES_DATA, selected_course=course_q, selected_uni=uni_q, universities=UNIVERSITIES_DATA)

if __name__ == '__main__':
    app.run(debug=True, port=5001)