from flask import Flask, render_template, request

app = Flask(__name__)

UNIVERSITIES = [
    {"code":"UJ","name":"University of Johannesburg (UJ)","location":"Johannesburg","closing":"30 Sep","apply_link":"https://www.uj.ac.za/study-2/"},
    {"code":"UP","name":"University of Pretoria (UP)","location":"Pretoria","closing":"30 Sep","apply_link":"https://www.up.ac.za/online-application"},
    {"code":"WITS","name":"University of the Witwatersrand (WITS)","location":"Johannesburg","closing":"30 Sep","apply_link":"https://www.wits.ac.za/applications/"},
    {"code":"UCT","name":"University of Cape Town (UCT)","location":"Cape Town","closing":"31 Jul","apply_link":"https://applyonline.uct.ac.za/"},
    {"code":"STELL","name":"Stellenbosch University","location":"Stellenbosch","closing":"31 Jul","apply_link":"https://www.maties.com/apply.html"},
    {"code":"UKZN","name":"University of KwaZulu-Natal (UKZN)","location":"Durban","closing":"30 Sep","apply_link":"https://ukzn.ac.za/apply/"},
    {"code":"UFS","name":"University of the Free State (UFS)","location":"Bloemfontein","closing":"30 Sep","apply_link":"https://apply.ufs.ac.za/"},
    {"code":"NWU","name":"North-West University (NWU)","location":"Potchefstroom","closing":"30 Sep","apply_link":"https://studies.nwu.ac.za/studies/apply"},
    {"code":"RHODES","name":"Rhodes University","location":"Makhanda","closing":"30 Sep","apply_link":"https://ross.ru.ac.za/"},
    {"code":"UFH","name":"University of Fort Hare","location":"Alice","closing":"30 Sep","apply_link":"https://www.ufh.ac.za/apply/"},
    {"code":"UL","name":"University of Limpopo (UL)","location":"Polokwane","closing":"30 Sep","apply_link":"https://www.ul.ac.za/apply/"},
    {"code":"UNIVEN","name":"University of Venda (UNIVEN)","location":"Thohoyandou","closing":"30 Sep","apply_link":"https://www.univen.ac.za/apply/"},
    {"code":"WSU","name":"Walter Sisulu University (WSU)","location":"Mthatha","closing":"30 Sep","apply_link":"https://www.wsu.ac.za/"},
    {"code":"UNIZULU","name":"University of Zululand","location":"KwaDlangezwa","closing":"30 Sep","apply_link":"https://www.unizulu.ac.za/apply/"},
    {"code":"MUT","name":"Mangosuthu University of Technology (MUT)","location":"Umlazi","closing":"30 Sep","apply_link":"https://www.mut.ac.za/apply/"},
    {"code":"DUT","name":"Durban University of Technology (DUT)","location":"Durban","closing":"30 Sep","apply_link":"https://www.dut.ac.za/apply/"},
    {"code":"TUT","name":"Tshwane University of Technology (TUT)","location":"Pretoria","closing":"30 Sep","apply_link":"https://www.tut.ac.za/study-at-tut/i-want-to-study/apply"},
    {"code":"CPUT","name":"Cape Peninsula University of Technology (CPUT)","location":"Cape Town","closing":"30 Sep","apply_link":"https://www.cput.ac.za/study/apply"},
    {"code":"CUT","name":"Central University of Technology (CUT)","location":"Bloemfontein","closing":"30 Sep","apply_link":"https://www.cut.ac.za/application/"},
    {"code":"VUT","name":"Vaal University of Technology (VUT)","location":"Vanderbijlpark","closing":"30 Sep","apply_link":"https://www.vut.ac.za/apply/"},
    {"code":"NMU","name":"Nelson Mandela University (NMU)","location":"Gqeberha","closing":"30 Sep","apply_link":"https://apply.mandela.ac.za/"},
    {"code":"UNISA","name":"University of South Africa (UNISA)","location":"Distance Learning","closing":"31 Oct","apply_link":"https://www.unisa.ac.za/apply"},
    {"code":"UWC","name":"University of the Western Cape (UWC)","location":"Bellville","closing":"30 Sep","apply_link":"https://www.uwc.ac.za/study/apply/"},
    {"code":"SMU","name":"Sefako Makgatho University (SMU)","location":"Ga-Rankuwa","closing":"30 Sep","apply_link":"https://www.smu.ac.za/students/apply/online-application/"},
    {"code":"SPU","name":"Sol Plaatje University (SPU)","location":"Kimberley","closing":"30 Sep","apply_link":"https://www.spu.ac.za/apply/"},
    {"code":"UMP","name":"University of Mpumalanga (UMP)","location":"Mbombela","closing":"30 Sep","apply_link":"https://www.ump.ac.za/apply/"},
]

COURSES_DB = [
    {"name":"BSc Information Technology","uni":"UJ","code":"UJ","aps":26,"faculty":"Science","maths_req":50},
    {"name":"Diploma in Nursing","uni":"UJ","code":"UJ","aps":26,"faculty":"Health","maths_req":0},
    {"name":"BCom Accounting","uni":"UJ","code":"UJ","aps":28,"faculty":"Business","maths_req":50},
    {"name":"BSc Computer Science","uni":"UP","code":"UP","aps":30,"faculty":"Science","maths_req":60},
    {"name":"BSc Physics","uni":"UP","code":"UP","aps":32,"faculty":"Science","maths_req":60},
    {"name":"MBChB Medicine","uni":"UP","code":"UP","aps":35,"faculty":"Health","maths_req":60},
    {"name":"BSc Engineering","uni":"WITS","code":"WITS","aps":34,"faculty":"Engineering","maths_req":65},
    {"name":"BCom Law","uni":"WITS","code":"WITS","aps":32,"faculty":"Commerce","maths_req":0},
    {"name":"BSc Life Sciences","uni":"WITS","code":"WITS","aps":28,"faculty":"Science","maths_req":50},
    {"name":"BSc Computer Science","uni":"UCT","code":"UCT","aps":36,"faculty":"Science","maths_req":70},
    {"name":"BCom","uni":"UCT","code":"UCT","aps":32,"faculty":"Commerce","maths_req":50},
    {"name":"BA","uni":"UCT","code":"UCT","aps":28,"faculty":"Humanities","maths_req":0},
    {"name":"Diploma in Agriculture","uni":"UKZN","code":"UKZN","aps":22,"faculty":"Agriculture","maths_req":0},
    {"name":"BSc Agriculture","uni":"UKZN","code":"UKZN","aps":28,"faculty":"Science","maths_req":50},
    {"name":"BSc Life Sciences","uni":"UFS","code":"UFS","aps":24,"faculty":"Science","maths_req":40},
    {"name":"BEd Foundation Phase","uni":"NWU","code":"NWU","aps":22,"faculty":"Education","maths_req":0},
    {"name":"BSc IT","uni":"NWU","code":"NWU","aps":26,"faculty":"Science","maths_req":50},
    {"name":"Diploma in Tourism Management","uni":"TUT","code":"TUT","aps":20,"faculty":"Management","maths_req":0},
    {"name":"Diploma in IT","uni":"TUT","code":"TUT","aps":22,"faculty":"ICT","maths_req":0},
    {"name":"National Diploma Nursing","uni":"DUT","code":"DUT","aps":22,"faculty":"Health","maths_req":0},
    {"name":"BSc Biological Sciences","uni":"NMU","code":"NMU","aps":26,"faculty":"Science","maths_req":45},
    {"name":"Diploma in Business Management","uni":"CPUT","code":"CPUT","aps":20,"faculty":"Business","maths_req":0},
    {"name":"BEd","uni":"UNISA","code":"UNISA","aps":20,"faculty":"Education","maths_req":0},
    {"name":"Higher Certificate in Accounting","uni":"UNISA","code":"UNISA","aps":18,"faculty":"Business","maths_req":0},
    {"name":"BCom Accounting","uni":"UWC","code":"UWC","aps":28,"faculty":"Commerce","maths_req":50},
]

def pct_to_points(p):
    if p >= 80: return 7
    if p >= 70: return 6
    if p >= 60: return 5
    if p >= 50: return 4
    if p >= 40: return 3
    if p >= 30: return 2
    return 1

@app.route('/')
def home(): return render_template('landing.html')

@app.route('/universities')
def universities(): return render_template('universities.html', universities=UNIVERSITIES)

@app.route('/university/<code>')
def uni_detail(code):
    uni = next((u for u in UNIVERSITIES if u['code']==code), None)
    if not uni: return "Not Found", 404
    return render_template('courses.html', uni=uni)

@app.route('/aps')
def aps_page(): return render_template('subjects.html')

@app.route('/subjects')
def subjects_page(): return render_template('subjects.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        main_pcts = []
        for k in ['hl_pct','fal_pct','maths_pct','s5_pct','s6_pct','s7_pct']:
            v = request.form.get(k)
            if v and v.isdigit():
                main_pcts.append(int(v))
        aps = sum(pct_to_points(p) for p in main_pcts[:6]) if main_pcts else 0
        maths_pct = int(request.form.get('maths_pct') or 0)
        qualified = []
        for course in COURSES_DB:
            if aps >= course['aps'] and maths_pct >= course['maths_req']:
                uni_obj = next((u for u in UNIVERSITIES if u['code']==course['code']), None)
                course['apply_link'] = uni_obj['apply_link'] if uni_obj else "#"
                qualified.append(course)
        qualified = sorted(qualified, key=lambda x: x['aps'])
        return render_template('results.html', aps=aps, qualified=qualified, total=len(COURSES_DB))
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)