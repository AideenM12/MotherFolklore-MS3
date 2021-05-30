import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import (
    Form, TextField, 
    PasswordField, validators)
from wtforms.validators import (
    DataRequired, Length, 
    EqualTo, ValidationError)

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", error=error), 500


@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html", error=error), 400


@app.errorhandler(401)
def unauthorized_access(e):
    return render_template("401.html", error=error), 401


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/index")
def index():
    articles = mongo.db.articles.find()
    return render_template("index.html", articles=articles)

# The below code was taken from https://wtforms.readthedocs.io/en/stable/crash_course/
class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')


# This below code was found on Python Programming.net
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20),
                                      validators.Regexp(r'^\w+$',
                                                        message="Password must contain only letters numbers or underscore")])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Regexp(r'^\w+$',
                          message="Password must contain only letters numbers or underscore")
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



@app.route("/login", methods=["GET", "POST"])
def login():
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
            
            if existing_user:
                if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome back {}!".format(
                    request.form.get("username")))
                    return redirect(url_for(
                            "profile", username=session["user"]))
                else:
                    flash("Incorrect Username/password, Please try again")
                    return redirect(url_for("login"))
            else:
                flash("Incorrect Username/password, Please try again")
                return redirect(url_for("login"))
            
        return render_template("login.html",title='Login', form=form )
   

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have logged out successfully!")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
