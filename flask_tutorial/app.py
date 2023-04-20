from flask import Flask
from views import views

app = Flask(__name__)

#Registering the route blueprints
app.register_blueprint(views, url_prefix = "/")
#here there is nothing after / because we have kept the "" blank. We can pass any name and can register it here.
#For example, if the name

if __name__ == "__main__":
    app.run(debug=True)
