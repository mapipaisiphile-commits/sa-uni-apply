from flask import Flask, render_template, request, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# ===== ALL 26 UNIVERSITIES =====
UNIVERSITIES_DATA = [
    {'code': 'UJ', 'name': 'University of Johannesburg (UJ)', 'location': 'Johannesburg', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=500', 'apply_link': 'https://www.uj.ac.za'},
    {'code': 'UP', 'name': 'University of Pretoria (UP)', 'location': 'Pretoria', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500', 'apply_link': 'https://www.up.ac.za'},
    {'code': 'WITS', 'name': 'University of the Witwatersrand (WITS)', 'location': 'Johannesburg', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=500', 'apply_link': 'https://www.wits.ac.za'},
    {'code': 'UCT', 'name': 'University of Cape Town (UCT)', 'location': 'Cape Town', 'closing': '31 Jul', 'image': 'https://images.unsplash.com/photo-1588075592446-265fd1e4e76f?w=500', 'apply_link': 'https://www.uct.ac.za'},
    {'code': 'STELLENBOSCH', 'name': 'Stellenbosch University', 'location': 'Stellenbosch', 'closing': '31 Jul', 'image': 'https://images.unsplash.com/photo-1498243793788-2be5d4346f13?w=500', 'apply_link': 'https://www.sun.ac.za'},
    {'code': 'UKZN', 'name': 'University of KwaZulu-Natal (UKZN)', 'location': 'Durban', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500', 'apply_link': 'https://www.ukzn.ac.za'},
    {'code': 'UFS', 'name': 'University of the Free State (UFS)', 'location': 'Bloemfontein', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=500', 'apply_link': 'https://www.ufs.ac.za'},
    {'code': 'NWU', 'name': 'North-West University (NWU)', 'location': 'Potchefstroom', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=500', 'apply_link': 'https://www.nwu.ac.za'},
    {'code': 'RHODES', 'name': 'Rhodes University', 'location': 'Makhanda', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500', 'apply_link': 'https://www.ru.ac.za'},
    {'code': 'UFH', 'name': 'University of Fort Hare (UFH)', 'location': 'Alice', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1498243793788-2be5d4346f13?w=500', 'apply_link': 'https://www.ufh.ac.za'},
    {'code': 'UL', 'name': 'University of Limpopo (UL)', 'location': 'Polokwane', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500', 'apply_link': 'https://www.ul.ac.za'},
    {'code': 'UNIVEN', 'name': 'University of Venda (UNIVEN)', 'location': 'Thohoyandou', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=500', 'apply_link': 'https://www.univen.ac.za'},
    {'code': 'WSU', 'name': 'Walter Sisulu University (WSU)', 'location': 'Mthatha', 'closing': '31 Oct', 'image': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=500', 'apply_link': 'https://www.wsu.ac.za'},
    {'code': 'UNIZULU', 'name': 'University of Zululand (UNIZULU)', 'location': 'Kwadlangezwa', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1588075592446-265fd1e4e76f?w=500', 'apply_link': 'https://www.unizulu.ac.za'},
    {'code': 'MUT', 'name': 'Mangosuthu University of Technology (MUT)', 'location': 'Umlazi', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=500', 'apply_link': 'https://www.mut.ac.za'},
    {'code': 'DUT', 'name': 'Durban University of Technology (DUT)', 'location': 'Durban', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1498243793788-2be5d4346f13?w=500', 'apply_link': 'https://www.dut.ac.za'},
    {'code': 'TUT', 'name': 'Tshwane University of Technology (TUT)', 'location': 'Pretoria', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500', 'apply_link': 'https://www.tut.ac.za'},
    {'code': 'CPUT', 'name': 'Cape Peninsula University of Technology (CPUT)', 'location': 'Cape Town', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1588075592446-265fd1e4e76f?w=500', 'apply_link': 'https://www.cput.ac.za'},
    {'code': 'CUT', 'name': 'Central University of Technology (CUT)', 'location': 'Bloemfontein', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=500', 'apply_link': 'https://www.cut.ac.za'},
    {'code': 'VUT', 'name': 'Vaal University of Technology (VUT)', 'location': 'Vanderbijlpark', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500', 'apply_link': 'https://www.vut.ac.za'},
    {'code': 'NMU', 'name': 'Nelson Mandela University (NMU)', 'location': 'Gqeberha', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=500', 'apply_link': 'https://www.mandela.ac.za'},
    {'code': 'UNISA', 'name': 'University of South Africa (UNISA)', 'location': 'Pretoria', 'closing': '15 Oct', 'image': 'https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=500', 'apply_link': 'https://www.unisa.ac.za'},
    {'code': 'UWC', 'name': 'University of the Western Cape (UWC)', 'location': 'Cape Town', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500', 'apply_link': 'https://www.uwc.ac.za'},
    {'code': 'SMU', 'name': 'Sefako Makgatho University (SMU)', 'location': 'Ga-Rankuwa', 'closing': '31 Jul', 'image': 'https://images.unsplash.com/photo-1588075592446-265fd1e4e76f?w=500', 'apply_link': 'https://www.smu.ac.za'},
    {'code': 'SPU', 'name': 'Sol Plaatje University (SPU)', 'location': 'Kimberley', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1498243793788-2be5d4346f13?w=500', 'apply_link': 'https://www.spu.ac.za'},
    {'code': 'UMP', 'name': 'University of Mpumalanga (UMP)', 'location': 'Mbombela', 'closing': '30 Sep', 'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500', 'apply_link': 'https://www.ump.ac.za'},
]

# Courses - auto-generated for all 26 so no empty page
BASE_COURSES = [
    {'name': 'BSc Information Technology', 'faculty': 'Faculty of Science', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '26', 'subjects': ['English L5 (60%)', 'Mathematics L5 (60%)'], 'status': 'Open'},
    {'name': 'Diploma in Nursing', 'faculty': 'Faculty of Health', 'type': 'Diploma', 'duration': '3 years', 'aps': '24', 'subjects': ['English L4', 'Life Sciences L4', 'Mathematics L3'], 'status': 'Open'},
    {'name': 'BEd Foundation Phase Teaching', 'faculty': 'Faculty of Education', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '24', 'subjects': ['English L5', 'Mathematics L3'], 'status': 'Open'},
    {'name': 'BCom Accounting', 'faculty': 'College of Business', 'type': "Bachelor's Degree", 'duration': '3 years', 'aps': '28', 'subjects': ['English L4', 'Mathematics L5'], 'status': 'Open'},
    {'name': 'BEng Mechanical Engineering', 'faculty': 'Faculty of Engineering', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '32', 'subjects': ['English L5', 'Mathematics L6 (70%)', 'Physical Sciences L5'], 'status': 'Open'},
]

COURSES_DATA = []
for uni in UNIVERSITIES_DATA:
    for bc in BASE_COURSES:
        new_c = bc.copy()
        new_c['uni_code'] = uni['code']
        COURSES_DATA.append(new_c)
# Add special courses for big unis
COURSES_DATA.extend([
    {'name': 'MBChB Medicine', 'uni_code': 'WITS', 'faculty': 'Health Sciences', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '42', 'subjects': ['English L5', 'Maths L5', 'Physics L5', 'Life Sciences L5'], 'status': 'Open'},
    {'name': 'LLB Law', 'uni_code': 'UP', 'faculty': 'Faculty of Law', 'type': "Bachelor's Degree", 'duration': '4 years', 'aps': '32', 'subjects': ['English L6'], 'status': 'Open'},
    {'name': 'MBChB Medicine', 'uni_code': 'UCT', 'faculty': 'Health Sciences', 'type': "Bachelor's Degree", 'duration': '6 years', 'aps': '45', 'subjects': ['English L5', 'Maths L6', 'Physics L5'], 'status': 'Open'},
])

NSFAS_INFO = {
    'closing_date': '31 October 2026',
    'documents': ['Certified ID copy (not older than 3 months)', 'Parents/guardian ID copies', 'Proof of income / SASSA letter / Affidavit', 'Consent form signed', 'Proof of residence', 'Grade 11 final + Grade 12 latest results', 'Disability certificate (if applicable)']
}

def init_db():
    conn = sqlite3.connect('uniapply.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, aps INTEGER, course TEXT, universities TEXT, status TEXT DEFAULT 'Pending')''')
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
    if not uni:
        return "University not found", 404
    filtered = [c for c in COURSES_DATA if c['uni_code'] == uni_code]
    if search:
        filtered = [c for c in filtered if search in c['name'].lower()]
    return render_template('courses.html', courses=filtered, uni=uni, search=search)

@app.route('/apply', methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        conn = sqlite3.connect('uniapply.db')
        conn.execute('INSERT INTO applications (name,email,phone,aps,course,universities) VALUES (?,?,?,?,?,?)',
                     (request.form.get('name'), request.form.get('email'), request.form.get('phone'), request.form.get('aps'), request.form.get('course'), request.form.get('universities')))
        conn.commit(); conn.close()
        return render_template('succes.html', name=request.form.get('name'))
    return render_template('apply.html', courses=COURSES_DATA, universities=UNIVERSITIES_DATA, selected_course=request.args.get('course',''), selected_uni=request.args.get('uni',''))

@app.route('/prospectus/<path:filename>')
def prospectus(filename):
    return send_from_directory('prospectus', filename)

if __name__ == '__main__':
    if not os.path.exists('prospectus'):
        os.makedirs('prospectus')
    app.run(debug=True, port=5001)