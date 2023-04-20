#Making blueprint of the routes in a separate file

from flask import Blueprint, render_template, request, jsonify, redirect, url_for

#Initialize Blueprint
views = Blueprint(__name__, "")

#Returning HTML files using render_template module of flask
@views.route("/")
def home():
    return render_template("index.html", name = "Sunil")
    #passing variable while rending the template(it is called template because variables can be passed through them)

@views.route("/profile")
def profile1():
    return render_template("profile.html")

@views.route("/profile/<username>") #passing parameter using <>.
def profile2(username):
    return render_template("index.html", name = username)

@views.route("/query") #passing query parameter using request. Ex: /query?name= variable. Here the name after ? and name inside args.get is same
def query():
    args = request.args #using the request module of flask
    name = args.get("name") #here the "name" fetches the variable passed after /query?name= and args.get assigns its value to the left side written name
    return render_template("index.html", name = name) #then the left side written name is passed as a variable into the index.html while rendering it

#Returning JSON file using jsonify moudule of the flask. Put everything inside a pythn dictionary and pass it inside jsonify() as a parameter
@views.route("/json")
def get_json():
    return jsonify({"name": "Sunil", "coolness": 10})

@views.route("/data") #collecting the data in json format
def get_data():
    data = request.json
    return jsonify(data)

#Redirecting using redirect, url_for module of flask
@views.route("/go-to-home")
def go_to_home():
    return redirect((url_for("views.home"))) #here views is the name of the variable views in line 6 and home is the function to be redirected to

