from flask import Blueprint, render_template, request, jsonify

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/plots")
def plots():
    return render_template("plots.html")

@views.route("/test")
def tests():
    return render_template("test.html")

@views.route("/info")
def info():
<<<<<<< HEAD
    return render_template("info.html")

=======
    return render_template("info.html")
>>>>>>> 29fb28e74f18cc99da72a80efd23ce1c98807698
