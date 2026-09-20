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

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/universities')
def universities():
    return render_template('universities.html', universities=UNIVERSITIES)

@app.route('/university/<code>')
def uni_detail(code):
    uni = next((u for u in UNIVERSITIES if u['code']==code), None)
    if not uni:
        return "Not Found", 404
    return render_template('courses.html', uni=uni)

# NEW - FIXES YOUR NOT FOUND ERROR
@app.route('/aps')
def aps_page():
    return render_template('subjects.html')

@app.route('/subjects')
def subjects_page():
    return render_template('subjects.html')

@app.route('/check-requirements')
def check_req():
    return render_template('subjects.html')

if __name__ == '__main__':
    app.run(debug=True)