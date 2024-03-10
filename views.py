from flask import Blueprint, render_template, request, jsonify
from processImage import processImg
from cohereApi import getReturnMsg


views = Blueprint(__name__, "views")
retImg = ''
resp = []
msgLst = []
msgcount = 0

forums = []


@views.route("/", methods = ['POST','GET'])
def home():
    global forums
    if request.method == 'POST':
        msg = request.form['fr']
        print(msg)
        if len(forums)==0 or msg!=forums[-1]:
            forums.append(msg)
        return render_template("index.html", frm = forums, frmln = len(forums))
    else:
        return render_template("index.html", frm = forums,frmln = len(forums))


@views.route("/plots", methods = ['POST','GET'])
def plots():
    global retImg
    if request.method == 'POST':
        try:
            msg = request.form['fr']
            print(msg)
            if len(forums)==0 or msg!=forums[-1]:
                forums.append(msg)
        except:
            try:
                img = request.form['imageData']
                # print(img)
                retImg = processImg(img)
            except:
                print('no image processed')
        return render_template("plots.html",retImg = '', frm = forums, frmln = len(forums))
    else:
        return render_template("plots.html",retImg = '', frm = forums, frmln = len(forums))

@views.route('/get_image_data')
def get_image_data():
    image_data = retImg
    return jsonify(image_data=image_data)

@views.route("/test", methods = ['POST','GET'])
def tests():
    global forums
    if request.method == 'POST':
        msg = request.form['fr']
        print(msg)
        if len(forums)==0 or msg!=forums[-1]:
            forums.append(msg)
        return render_template("test.html", frm = forums, frmln = len(forums))
    else:
        return render_template("test.html", frm = forums,frmln = len(forums))

@views.route("/chatbot", methods = ['POST','GET'])
def chatbot():
    global resp, msgcount, msgLst
    if request.method == 'POST':
        try:
            ff = request.form['fr']
            print(ff)
            if len(forums)==0 or ff!=forums[-1]:
                forums.append(ff)
        except:
            try:
                msg = request.form['qns']
                if len(resp)==0 or msg!=msgLst[-1]:
                    msgLst.append(msg)
                    resp.append(getReturnMsg(msg))
                    msgcount = msgcount+1
            except:
                print('no message')
        return render_template("chatbot.html", arg0=resp, arg1 = msgcount, arg2 = msgLst, frm = forums, frmln = len(forums))
    else:
        return render_template("chatbot.html", arg0=resp, arg1 = msgcount, arg2 = msgLst, frm = forums, frmln = len(forums))
    # return render_template("chatbot.html")

@views.route("/base", methods = ['POST','GET'])
def bases():
    return render_template("base.html")

@views.route("/info", methods = ['POST','GET'])
def info():
    global forums
    if request.method == 'POST':
        msg = request.form['fr']
        print(msg)
        if len(forums)==0 or msg!=forums[-1]:
            forums.append(msg)
        return render_template("info.html", frm = forums, frmln = len(forums))
    else:
        return render_template("info.html", frm = forums,frmln = len(forums))
