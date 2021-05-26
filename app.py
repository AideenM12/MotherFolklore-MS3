import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    articles = mongo.db.articles.find()
    return render_template("index.html", articles=articles)


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

# This below code was found on Python Programming.net
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    


@app.route("/registration", methods=["GET", "POST"])
def registration():
    try:
        form = RegistrationForm(request.form)
        
        if request.method == 'POST' and form.validate():
            existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

            if existing_user:
                flash("Username already exists")
                return redirect(url_for("registration"))
                     
            signup = {
              "username": request.form.get("username").lower(),
              "email": request.form.get("email").lower(),
              "password": generate_password_hash(request.form.get("password"))
            }
            mongo.db.users.insert_one(signup)

            session["user"] = request.form.get("username").lower()
            flash('You have signed up successfully!')
            
        return render_template('sign-up.html', form=form)
        
    except Exception as e:
        return (str(e))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) 
