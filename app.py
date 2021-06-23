import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, validate_csrf, ValidationError
from wtforms import (
    Form, TextField,
    PasswordField, validators)
from wtforms.validators import InputRequired, EqualTo

if os.path.exists("env.py"):
    import env

# Articles pagination limit
PER_PAGE = 6

app = Flask(__name__)
csrf = CSRFProtect(app)

csrf.init_app(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# @app.errorhandler(500)
# def server_error(error):
# return render_template("500.html", error=error), 500


# @app.errorhandler(400)
# def bad_request(error):
# return render_template("400.html", error=error), 400


# @app.errorhandler(401)
# def unauthorized_access(error):
#  return render_template("401.html", error=error), 401


# @app.errorhandler(404)
# def error404(e):
# return render_template('404.html'), 404


# https://github.com/Edb83/self-isolution/blob/master/app.py
def paginate(articles):
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    offset = page * PER_PAGE - PER_PAGE

    return articles[offset: offset + PER_PAGE]


def pagination_args(articles):
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = len(articles)

    return Pagination(page=page, per_page=PER_PAGE, total=total)


@app.route("/")
@app.route("/index")
def index():
    """
    Links to home page
    """
    articles = mongo.db.articles.find()

    return render_template("index.html",
                           articles=articles)


@app.route("/contact", methods=["GET", "POST"])
def contact():

    return render_template("contact.html")


@app.route("/further_reading")
def further_reading():

    further_reading = list(mongo.db.further_reading.find())

    return render_template("further_reading.html",
                           page_title="Further Reading",
                           further_reading=further_reading)


@app.route("/add_further_reading", methods=["GET", "POST"])
def add_further_reading():
    """
    Allows users to contribute towards the site
    with their own unique articles
    """
    topics = mongo.db.topics.find().sort("topic_name", 1)
   
    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))
    elif session["user"].lower() != "admin":
        flash("You are not authorized to view this page")
        return redirect(url_for("profile"))
    elif request.method != "POST":
        return render_template("add_further_reading.html",
                               further_reading=further_reading,
                               topics=topics)
    else:
        reading = {
            "topic_name": request.form.get("topic_name"),
            "book_title": request.form.get("book_title"),
            "website": request.form.get("website"),
            "article_title": request.form.get("article_title"),
            "author": request.form.get("author"),
            "date_published": request.form.get("date_published"),
            "publisher": request.form.get("publisher"),
        }
        mongo.db.further_reading.insert_one(reading)
        flash("Further Reading contribution successful!")
        print(topics)

        return redirect(url_for("topics"))

    return render_template("topics.html", topics=topics,
                           reading=reading,
                           further_reading=further_reading)


@app.route("/edit_article/<reading_id>", methods=["GET", "POST"])
def edit_further_reading(reading_id):
    """
    Allows users to edit their contributions to the site
    """
    reading = mongo.db.further_reading.find_one({"_id": ObjectId(reading_id)})
    topics = mongo.db.topics.find().sort("topic_name", 1)
    

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))
    elif session["user"].lower() != "admin":
        flash("You are not authorized to view this page")
        return redirect(url_for("profile"))

    elif request.method != "POST":
        return render_template("edit_further_reading.html", reading=reading,
                               topics=topics)
    
    else:
        adjust = {
             "topic_name": request.form.get("topic_name"),
            "book_title": request.form.get("book_title"),
            "website": request.form.get("website"),
            "article_title": request.form.get("article_title"),
            "author": request.form.get("author"),
            "date_published": request.form.get("date_published"),
            "publisher": request.form.get("publisher"),
        }
        mongo.db.further_reading.update({"_id": ObjectId(reading_id)}, adjust)
        flash("Article update successful!")

    return redirect(url_for("topics"))

@app.route("/filter_reading/further_reading/<topic_id>")
def filter_reading(topic_id):
    topics = list(mongo.db.topics.find())
    topic = mongo.db.topics.find_one({"_id": ObjectId(topic_id)})

    further_reading = list(mongo.db.further_reading.find(
        {"topic_name": topic["topic_name"]}).sort("_id", -1))
    return render_template("further_reading.html",
                           further_reading=further_reading,
                           topic=topic,
                           topics=topics,
                           page_title="Further Reading")


@app.route("/articles")
def articles():
    """
    Links articles from db to site
    """
    articles = list(mongo.db.articles.find())
    articles_paginate = paginate(articles)
    pagination = pagination_args(articles)
    topic = mongo.db.topics.find()
    topic_name = list(mongo.db.topics.find().sort("topic_name", 1))

    topics = {}
    for article in articles:
        if article["topic_name"] in topics:
            topics["article"].append(article._id)
        else:
            print(article["_id"])
            topics["article_id"] = article["_id"]

    return render_template("articles.html",
                           articles=articles_paginate,
                           page_title="Articles",
                           pagination=pagination,
                           topic=topic,
                           topics=topics,
                           topic_name=topic_name,
                           article=article)


@app.route("/search",  methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    articles = list(mongo.db.articles.find({"$text": {"$search": query}}))
    articles_paginate = paginate(articles)
    pagination = pagination_args(articles)

    return render_template("articles.html",
                           articles=articles_paginate,
                           page_title="Article Results",
                           pagination=pagination)


# The below code was taken from
# https://wtforms.readthedocs.io/en/stable/crash_course/


class LoginForm(Form):

    # Form fields for user login

    username = TextField('Username')
    password = PasswordField('Password')


# This below code was found on Python Programming.net
class RegistrationForm(Form):

    # Form fields and validators for registration

    username = TextField('Username',
                         [validators.Length(min=4, max=20),
                          validators.Regexp(r'^\w+$', message=(
                              "Username must contain only letters "
                              "numbers or underscore"))])

    email = TextField('Email Address', [validators.Length(min=6, max=50)])

    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Regexp(r'^\w+$', message=(
            "Password must contain only letters numbers or underscore"))
    ])

    confirm = PasswordField('Repeat Password')


@app.route("/registration", methods=["GET", "POST"])
def registration():
    """
    Allows users to sign up to the site and
    send data to the database
    """
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
                "password": generate_password_hash(
                    request.form.get("password"))
            }
            mongo.db.users.insert_one(signup)

            session["user"] = request.form.get("username").lower()
            flash('You have signed up successfully!')
            return redirect(url_for("profile", username=session['user']))

        return render_template('sign-up.html', form=form)

    except Exception as e:
        return (str(e))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Allows users to login and access their profile
    """
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

    return render_template("login.html", title='Login', form=form)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Links users to their profiles
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    articles = list(mongo.db.articles.find(
        {"created_by": session["user"]}).sort("_id", -1))

    if session["user"]:
        return render_template("profile.html", username=username,
                               articles=articles)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Allows users to logout of their profile
    """
    flash("You have logged out successfully!")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    """
    Allows users to contribute towards the site
    with their own unique articles
    """
    topics = mongo.db.topics.find().sort("topic_name", 1)
    locations = mongo.db.locations.find().sort("location_name", 1)

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))
    elif request.method != "POST":
        return render_template("add_article.html", topics=topics,
                               locations=locations)
    else:
        article = {
            "topic_name": request.form.get("topic_name"),
            "article_name": request.form.get("article_name"),
            "image_url": request.form.get("image_url"),
            "article_article": request.form.get("article_article"),
            "location_name": request.form.get("location_name"),
            "created_by": session["user"],
            "date_added": request.form.get("date_added")
        }
        mongo.db.articles.insert_one(article)
        flash("Article contribution successful!")
        return redirect(url_for("articles"))

    return render_template("add_article.html", topics=topics,
                           locations=locations)


@app.route("/edit_article/<article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    """
    Allows users to edit their contributions to the site
    """
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    topics = mongo.db.topics.find().sort("topic_name", 1)
    locations = mongo.db.locations.find().sort("location_name", 1)
    article_creator = article["created_by"]

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))

    elif request.method != "POST":
        return render_template("edit_article.html", article=article,
                               topics=topics, locations=locations)

    elif session["user"] != article_creator and session["user"] != "admin":
        flash("You are not authorized to edit this material")

    else:
        adjust = {
            "topic_name": request.form.get("topic_name"),
            "article_name": request.form.get("article_name"),
            "image_url": request.form.get("image_url"),
            "article_article": request.form.get("article_article"),
            "location_name": request.form.get("location_name"),
            "created_by": session["user"],
            "date_added": request.form.get("date_added")
        }
        mongo.db.articles.update({"_id": ObjectId(article_id)}, adjust)
        flash("Article update successful!")

    return redirect(url_for("articles"))


@app.route("/delete_article/<article_id>")
def delete_article(article_id):
    """
    Allows users to delete their contributions to site
    """
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    article_creator = article["created_by"]

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))

    elif session["user"] != article_creator and session["user"] != "admin":
        flash("You are not authorized to edit this material")
        return redirect(url_for("articles"))

    else:
        mongo.db.articles.remove({"_id": ObjectId(article_id)})
        flash("Article successfully deleted.")
        return redirect(url_for("articles"))


@app.route("/topics")
def topics():

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))

    else:
        topics = list(mongo.db.topics.find().sort("topic_name", 1))
        topic_name = list(mongo.db.topics.find())
        article_list = {}

        for topic in topics:
            if topic["topic_name"] in topics:
                topic["article_list"].append(topic._id)
            else:
                print(topic["_id"])
                topic["topic_id"] = topic["_id"]

        return render_template("topics.html",
                               topics=topics,
                               topic_name=topic_name,
                               article_list=article_list)


@app.route("/filter/topic/<topic_id>")
def filter_topics(topic_id):
    topics = list(mongo.db.topics.find())
    topic = mongo.db.topics.find_one({"_id": ObjectId(topic_id)})
    articles = list(mongo.db.articles.find(
        {"topic_name": topic["topic_name"]}).sort("_id", -1))
    pagination = pagination_args(articles)
    articles_paginate = paginate(articles)

    return render_template("articles.html",
                           articles=articles_paginate,
                           topic=topic,
                           topics=topics,
                           page_title=topic["topic_name"],
                           pagination=pagination)


@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    """
    Allows users to contribute towards the site
    with their own unique articles
    """
    topics = mongo.db.topics.find().sort("topic_name", 1)

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))
    elif session["user"].lower() != "admin":
        flash("You are not authorized to view this page")
        return redirect(url_for("profile"))
    elif request.method != "POST":
        return render_template("add_topic.html",
                               topics=topics)
    else:
        topic = {
            "topic_name": request.form.get("topic_name"),
            "article_list": [""]

        }
        mongo.db.topics.insert_one(topic)
        flash("Topic contribution successful!")
        return redirect(url_for("topics"))

    return render_template("topics.html", topics=topics,
                           topic=topic)


@app.route("/edit_topic/<topic_id>", methods=["GET", "POST"])
def edit_topic(topic_id):
    """
    Allows users to edit their contributions to the site
    """
    topic = mongo.db.topics.find_one({"_id": ObjectId(topic_id)})

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))

    elif request.method != "POST":
        return render_template("edit_topic.html", topic=topic)

    elif session["user"] != session["user"] != "admin":
        flash("You are not authorized to edit this material")

    else:
        adjust = {
            "topic_name": request.form.get("topic_name"),
            "article_list": []
        }
        mongo.db.topics.update({"_id": ObjectId(topic_id)}, adjust)
        flash("Topic update successful!")

    return redirect(url_for("topics"))


@app.route("/delete_topic/<topic_id>")
def delete_topic(topic_id):
    """
    Allows users to delete their contributions to site
    """
    topic = mongo.db.topics.find_one({"_id": ObjectId(topic_id)})

    if "user" not in session:
        flash("Please Log in to continue")
        return redirect(url_for("login"))

    elif session["user"] != session["user"] != "admin":
        flash("You are not authorized to edit this material")
        return redirect(url_for("topics"))

    else:
        mongo.db.topics.remove({"_id": ObjectId(topic_id)})
        flash("Topic successfully deleted.")
        return redirect(url_for("topics", topic=topic))


# Change to False before submission
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
