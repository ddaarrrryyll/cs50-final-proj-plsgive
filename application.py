import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

from helpers import apology

# Configure app
app = Flask(__name__)

# Auto-reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# No cached responses
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure Library to use SQLite database
db = SQL("sqlite:///wholesomev2.db")

@app.route("/", methods=["GET"])
def get_index():

    return redirect("/home")


# HOMEPAGE
@app.route("/home", methods=["GET"])
def get_home():

    # GET number of quotes from database
    quotes = db.execute("SELECT quotes FROM quotes")
    quoteno = len(quotes)

    # GET number of videos from database
    videos = db.execute("SELECT videos FROM videos")
    videono = len(videos)

    # GET number of cats from database
    cats = db.execute("SELECT cats FROM cats")
    catno = len(cats)

    # GET number of dogs from database
    dogs = db.execute("SELECT dogs FROM dogs")
    dogno = len(dogs)

    # GET number of others from database
    others = db.execute("SELECT others FROM others")
    otherno = len(others)


    return render_template("home.html", quoteno=quoteno, videono=videono, catno=catno, dogno=dogno, otherno=otherno)


# QUOTES
@app.route("/quotes", methods=["GET"])
def get_quotes():

    # GET number of quotes from database
    allquotes = db.execute("SELECT quotes FROM quotes")
    quoteno = len(allquotes)
    quotes = db.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")

    return render_template("quotes.html", quotes=quotes, quoteno=quoteno)

@app.route("/submitquote", methods=["POST"])
def submitquote():
    """Submit Quote"""
    if request.method == "POST":
        if not request.form.get("quote"):
             flash("quote submitted cannot be empty")
             return redirect("/quotes")

    # UPDATE wholesome.db
    db.execute("INSERT INTO quotes (quotes, person) VALUES(:quote, :person)",
                quote=request.form.get("quote"),
                person=request.form.get("person"))

    flash("Submitted!")
    return redirect("/quotes")


# VIDEOS
@app.route("/videos", methods=["GET"])
def get_videos():

    # GET number of videos from database
    allvideos = db.execute("SELECT videos FROM videos")
    videono = len(allvideos)
    videos = db.execute("SELECT * FROM videos ORDER BY RANDOM() LIMIT 1")

    return render_template("videos.html", videos=videos, videono=videono)

@app.route("/submitvideo", methods=["POST"])
def submitvideo():
    """Submit Quote"""
    if request.method == "POST":
        if not request.form.get("video"):
            flash("link submitted cannot be empty")
            return redirect("/videos")

    # UPDATE wholesome.db
    db.execute("INSERT INTO videos (videos) VALUES(:video)",
                video=request.form.get("video"))

    flash("Submitted!")
    return redirect("/videos")



# CATS
@app.route("/cats", methods=["GET", "POST"])
def get_cats():

    # GET number of cats from database
    allcats = db.execute("SELECT cats FROM cats")
    catno = len(allcats)

    cats = db.execute("SELECT * FROM cats ORDER BY RANDOM() LIMIT 1")


    return render_template("cats.html", cats=cats, catno=catno)

@app.route("/catlink", methods=["POST"])
def catlink():
    """Cat Link"""
    if request.method == "POST":
        if not request.form.get("catlink"):
            flash("Submission field cannot be empty")
            return redirect("/cats")

        if ("https://i.imgur.com/" not in request.form.get("catlink")):
            flash("Please provide imgur link starting with 'https://i.imgur.com/'")
            return redirect("/cats")

        if (".jpg" not in request.form.get("catlink") and ".gif" not in request.form.get("catlink")):
            flash("Please ensure links end with .jpg or .gif")
            return redirect("/cats")

        # Check for duplicates
        catcheck = db.execute("SELECT cats FROM cats WHERE cats=:catlink",
                                catlink=request.form.get("catlink"))
        if len(catcheck) == 1:
            flash("Link has been submitted before!")
            return redirect("/cats")
    # UPDATE wholesome.db
    db.execute("INSERT INTO cats (cats) VALUES(:catlink)",
                catlink=request.form.get("catlink"))

    flash("Submitted!")
    return redirect("/cats")


# DOGS
@app.route("/dogs", methods=["GET", "POST"])
def get_dogs():

    # GET number of dogs from database
    alldogs = db.execute("SELECT dogs FROM dogs")
    dogno = len(alldogs)

    dogs = db.execute("SELECT * FROM dogs ORDER BY RANDOM() LIMIT 1")


    return render_template("dogs.html", dogs=dogs, dogno=dogno)

@app.route("/doglink", methods=["POST"])
def doglink():
    """dog Link"""
    if request.method == "POST":
        if not request.form.get("doglink"):
            flash("Submission field cannot be empty")
            return redirect("/dogs")

        if ("https://i.imgur.com/" not in request.form.get("doglink")):
            flash("Please provide imgur link starting with 'https://i.imgur.com/'")
            return redirect("/dogs")

        if (".jpg" not in request.form.get("doglink") and ".gif" not in request.form.get("doglink")):
            flash("Please ensure links end with .jpg or .gif")
            return redirect("/dogs")

        # Check for duplicates
        catcheck = db.execute("SELECT dogs FROM dogs WHERE dogs=:doglink",
                                doglink=request.form.get("doglink"))
        if len(catcheck) == 1:
            flash("Link has been submitted before!")
            return redirect("/dogs")

    # UPDATE wholesome.db
    db.execute("INSERT INTO dogs (dogs) VALUES(:doglink)",
                doglink=request.form.get("doglink"))

    flash("Submitted!")
    return redirect("/dogs")



# OTHER ANIMALS
@app.route("/others", methods=["GET", "POST"])
def get_others():

    # GET number of others from database
    allothers = db.execute("SELECT others FROM others")
    otherno = len(allothers)

    others = db.execute("SELECT * FROM others ORDER BY RANDOM() LIMIT 1")

    return render_template("others.html", others=others, otherno=otherno)

@app.route("/otherlink", methods=["POST"])
def otherlink():
    """other Link"""
    if request.method == "POST":
        if not request.form.get("otherlink"):
            flash("Submission field cannot be empty")
            return redirect("/others")

        if ("https://i.imgur.com/" not in request.form.get("otherlink")):
            flash("Please provide imgur link starting with 'https://i.imgur.com/'")
            return redirect("/others")

        if (".jpg" not in request.form.get("otherlink") and ".gif" not in request.form.get("otherlink")):
            flash("Please ensure links end with .jpg or .gif")
            return redirect("/others")

        # Check for duplicates
        catcheck = db.execute("SELECT others FROM others WHERE others=:otherlink",
                                otherlink=request.form.get("otherlink"))
        if len(catcheck) == 1:
            flash("Link has been submitted before!")
            return redirect("/others")

    # UPDATE wholesome.db
    db.execute("INSERT INTO others (others) VALUES(:otherlink)",
                otherlink=request.form.get("otherlink"))

    flash("Submitted!")
    return redirect("/others")

# REPORT
@app.route("/reportquote", methods=["POST"])
def reportquote():

    reportquote=int(request.form.get("reportquote"))

    # Get reported content
    report = db.execute("SELECT quotes, person FROM quotes WHERE id= :reportquote",
                        reportquote=reportquote)
    print(report)
    deadquote = str(report[0])

    # UPDATE wholesome.db
    db.execute("INSERT INTO reports (category, content) VALUES (:category, :reportquote)",
                category="quotes",
                reportquote=deadquote)

    # UPDATE wholesome.db
    db.execute("DELETE FROM quotes WHERE id = :reportquote",
                reportquote=reportquote)

    flash("Reported")
    return redirect("/quotes")


@app.route("/reportvideo", methods=["POST"])
def reportvideo():

    reportvideo=int(request.form.get("reportvideo"))

    # Get reported content
    report = db.execute("SELECT videos FROM videos WHERE id= :reportvideo",
                        reportvideo=reportvideo)
    print(report)
    deadvideo = str(report[0])

    # UPDATE wholesome.db
    db.execute("INSERT INTO reports (category, content) VALUES (:category, :reportvideo)",
                category="videos",
                reportvideo=deadvideo)

    # UPDATE wholesome.db
    db.execute("DELETE FROM videos WHERE id = :reportvideo",
                reportvideo=reportvideo)

    flash("Reported")
    return redirect("/videos")


@app.route("/reportcat", methods=["POST"])
def reportcat():
    if request.method == "POST":
        if not request.form.get("reportcat"):
            return apology("provide image id")

    reportcat=int(request.form.get("reportcat"))

    # Get reported content
    report = db.execute("SELECT cats FROM cats WHERE id = :reportcat",
                        reportcat=reportcat)

    print(report)

    deadcat = str(report[0])

    # UPDATE wholesome.db
    db.execute("INSERT INTO reports (category, content) VALUES (:category, :reportcat)",
                category="cat",
                reportcat=deadcat)

    # UPDATE wholesome.db
    db.execute("DELETE FROM cats WHERE id = :reportcat",
                reportcat=reportcat)


    flash("Removed!")
    return redirect("/cats")


@app.route("/reportdog", methods=["POST"])
def reportdog():
    if request.method == "POST":
        if not request.form.get("reportdog"):
            return apology("provide image id")

    reportdog=int(request.form.get("reportdog"))

    # Get reported content
    report = db.execute("SELECT * FROM dogs WHERE id = :reportdog",
                        reportdog=reportdog)

    deaddog = str(report[0])

    # UPDATE wholesome.db
    db.execute("INSERT INTO reports (category, content) VALUES (:category, :reportdog)",
                category="dog",
                reportdog=deaddog)

    # UPDATE wholesome.db
    db.execute("DELETE FROM dogs WHERE id = :reportdog",
                reportdog=reportdog)


    flash("Removed!")
    return redirect("/dogs")

@app.route("/reportother", methods=["POST"])
def reportother():
    if request.method == "POST":
        if not request.form.get("reportother"):
            return apology("provide image id")

    reportother=int(request.form.get("reportother"))

    # Get reported content
    report = db.execute("SELECT * FROM others WHERE id = :reportother",
                        reportother=reportother)

    deadother = str(report[0])

    # UPDATE wholesome.db
    db.execute("INSERT INTO reports (category, content) VALUES (:category, :reportother)",
                category="other",
                reportother=deadother)

    # UPDATE wholesome.db
    db.execute("DELETE FROM others WHERE id = :reportother",
                reportother=reportother)


    flash("Removed!")
    return redirect("/others")
