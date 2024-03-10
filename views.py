from flask import Blueprint, render_template, request, jsonify
from processImage import processImg

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/plots", methods = ['POST','GET'])
def plots():
    if request.method == 'POST':
        img = request.form['imageData']
        # print(img)
        retimg = processImg(img)
        # print(retimg)
        return render_template("plots.html", argImg = retimg)
    else:
        return render_template("plots.html",argImg = '')

@views.route("/strangers", methods = ['POST','GET'])
def strangers():
    global resp, msgcount, msgLst
    if request.method == 'POST':
        msg = request.form['qns']
        if len(resp)==0 or msg!=msgLst[-1]:
            msgLst.append(msg)
            resp.append(getReturnMsg(msg))
            msgcount = msgcount+1
        return render_template("strangers.html", arg0=resp, arg1 = msgcount, arg2 = msgLst)
    else:
        return render_template("strangers.html", arg0=resp, arg1 = msgcount, arg2 = msgLst)


@views.route("/test")
def tests():
    return render_template("test.html")

@views.route("/info")
def info():
    return render_template("info.html")
