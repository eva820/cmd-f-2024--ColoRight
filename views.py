from flask import Blueprint, render_template, request, jsonify
from processImage import processImg

views = Blueprint(__name__, "views")
retImg = ''

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
        # print(retimg)
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

@views.route("/base")
def bases():
    return render_template("base.html")

@views.route("/info")
def info():
    return render_template("info.html")
