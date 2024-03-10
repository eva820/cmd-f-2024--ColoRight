from flask import Blueprint, render_template, request, jsonify
from processImage import processImg
from cohereApi import getReturnMsg

views = Blueprint(__name__, "views")
retImg = ''
resp = []
msgLst = []
msgcount = 0

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/plots", methods = ['POST','GET'])
def plots():
    global retImg
    if request.method == 'POST':
        img = request.form['imageData']
        # print(img)
        retImg = processImg(img)
        return render_template("plots.html",retImg = '')
    else:
        return render_template("plots.html",retImg = '')

@views.route('/get_image_data')
def get_image_data():
    image_data = retImg
    return jsonify(image_data=image_data)

@views.route("/test")
def tests():
    return render_template("test.html")

@views.route("/chatbot", methods = ['POST','GET'])
def chatbot():
    global resp, msgcount, msgLst
    if request.method == 'POST':
        msg = request.form['qns']
        if len(resp)==0 or msg!=msgLst[-1]:
            msgLst.append(msg)
            resp.append(getReturnMsg(msg))
            msgcount = msgcount+1
        return render_template("chatbot.html", arg0=resp, arg1 = msgcount, arg2 = msgLst)
    else:
        return render_template("chatbot.html", arg0=resp, arg1 = msgcount, arg2 = msgLst)
    # return render_template("chatbot.html")

@views.route("/base")
def bases():
    return render_template("base.html")

@views.route("/info")
def info():
    return render_template("info.html")
