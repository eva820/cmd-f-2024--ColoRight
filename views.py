from flask import Blueprint, render_template, request, jsonify

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/description")
def links():
    return render_template("description.html")
