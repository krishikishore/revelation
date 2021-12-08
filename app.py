import os
import random
import math
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk import tokenize
from operator import itemgetter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime 
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///revelation.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if session.get("user_id") is None:
        articlerow = db.execute("SELECT * FROM articles WHERE status = 1 ORDER BY RANDOM() LIMIT 5")
        communityrow = db.execute("SELECT * FROM users ORDER BY RANDOM() LIMIT 8")
        return render_template("index.html", articles=articlerow, community=communityrow)
    else:
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        if userrow[0]["re"] == 0:
            articlerow = db.execute("SELECT * FROM articles WHERE status = 1 ORDER BY RANDOM() LIMIT 5")
            communityrow = db.execute("SELECT * FROM users WHERE user_id != ? ORDER BY RANDOM() LIMIT 8", session["user_id"])
            return render_template("index.html", users=userrow, articles=articlerow, community=communityrow)
        else:
            articlerow = db.execute("SELECT * FROM articles WHERE editor = ?", session["user_id"])
            return render_template("editor_dashboard.html", users=userrow, articles=articlerow)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("fname"):
            error = 'Missing first name'
            return render_template('register.html', error=error)
        elif not request.form.get("lname"):
            error = 'Missing last name'
            return render_template('register.html', error=error)
        elif not request.form.get("uname"):
            error = 'Missing username'
            return render_template('register.html', error=error)
        elif not request.form.get("pword"):
            error = 'Missing password'
            return render_template('register.html', error=error)
        elif not request.form.get("email"):
            error = 'Missing email'
            return render_template('register.html', error=error)
        elif not request.form.get("school"):
            error = 'Missing school'
            return render_template('register.html', error=error)
        elif not request.form.get("hsc"):
            error = 'Missing high school/undegraduate'
            return render_template('register.html', error=error)
        elif not request.form.get("re"):
            error = 'Missing researcher/editor'
            return render_template('register.html', error=error)

        usernamerows = db.execute("SELECT * FROM users WHERE user_id = ?", request.form.get("uname"))
        if len(usernamerows) > 0:
            error = 'Username already taken'
            return render_template('register.html', error=error)

        emailrows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        if len(emailrows) > 0:
            error = 'Email already exists'
            return render_template('register.html', error=error)

        if request.form.get("hsc") == "hs":
            hscvalue = 0
        elif request.form.get("hsc") == "c":
            hscvalue = 1
        if request.form.get("re") == "r":
            revalue = 0
        elif request.form.get("re") == "e":
            revalue = 1

        # Add user to database
        db.execute("INSERT INTO users (firstname, lastname, username, password, email, school, hsc, re) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                        request.form.get("fname"),
                        request.form.get("lname"),
                        request.form.get("uname"),
                        generate_password_hash(request.form.get("pword")),
                        request.form.get("email"),
                        request.form.get("school"),
                        hscvalue,
                        revalue)

        currentuser = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("uname"))

        # Log user in
        session["user_id"] = currentuser[0]["user_id"]

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        if session.get("user_id") is None:
            return render_template("register.html")
        else:
            return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            error = 'Missing username'
            return render_template('login.html', error=error)
        elif not request.form.get("password"):
            error = 'Missing password'
            return render_template('login.html', error=error)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search")
def search():

    # Select articles whose information matches that of the search keyword(s)
    if session.get("user_id") is None:
        if request.args.get("keyword"):
            articlerow = db.execute("SELECT * FROM articles WHERE title LIKE ? OR abstract LIKE ? OR introduction LIKE ? OR materials_methods LIKE ? OR results LIKE ? OR discussion LIKE ? OR conclusion LIKE ?",
                                        "%"+str(request.args.get("keyword"))+"%", 
                                        "%"+str(request.args.get("keyword"))+"%", 
                                        "%"+str(request.args.get("keyword"))+"%", 
                                        "%"+str(request.args.get("keyword"))+"%", 
                                        "%"+str(request.args.get("keyword"))+"%", 
                                        "%"+str(request.args.get("keyword"))+"%", 
                                        "%"+str(request.args.get("keyword"))+"%")
        
            return render_template("search_results.html", articles=articlerow)
        
        # Bring to homepage if nothing is inputted in the search box
        else:
            return redirect("/")
    # Same as above, but pass user_id to template in order to display username
    else:
        if request.args.get("keyword"):
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            articlerow = db.execute("SELECT * FROM articles WHERE title LIKE ? OR abstract LIKE ? OR introduction LIKE ? OR materials_methods LIKE ? OR results LIKE ? OR discussion LIKE ? OR conclusion LIKE ?", "%"+str(request.args.get("keyword"))+"%", "%"+str(request.args.get("keyword"))+"%", "%"+str(request.args.get("keyword"))+"%", "%"+str(request.args.get("keyword"))+"%", "%"+str(request.args.get("keyword"))+"%", "%"+str(request.args.get("keyword"))+"%", "%"+str(request.args.get("keyword"))+"%")
            return render_template("search_results.html", users=userrow, articles=articlerow)
        else:
            return redirect("/")

@app.route("/explore")
def explore():
    
    # Randomly add ten published articles from database to explore page
    if session.get("user_id") is None:
        articlerow = db.execute("SELECT * FROM articles WHERE status = 1 ORDER BY RANDOM() LIMIT 10")
        return render_template("explore.html", articles=articlerow)
    
    # Same as above, but pass user_id to template in order to display username
    else:
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        articlerow = db.execute("SELECT * FROM articles WHERE status = 1 ORDER BY RANDOM() LIMIT 10")
        return render_template("explore.html", users=userrow, articles=articlerow)

@app.route("/article")
def article():

    # Pass the necessary information of a given article to article.html
    if session.get("user_id") is None:
        if request.args.get("id") and request.args.get("id").isnumeric():
            articlerow = db.execute("SELECT * FROM articles WHERE article_id = ? AND status = 1", request.args.get("id"))
            if len(articlerow) > 0:
                authorrow = db.execute("SELECT * FROM users WHERE user_id = ?", articlerow[0]["primary_author_id"])
                editorrow = db.execute("SELECT * FROM users WHERE user_id = ?", articlerow[0]["editor"])
                return render_template("article.html", articles=articlerow, authors=authorrow, editors=editorrow)
            else:
                return redirect("/")
        else:
            return redirect("/")
    
    # Same as above, but also pass user_id to template in order to display username
    else:
        if request.args.get("id") and request.args.get("id").isnumeric():
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            articlerow = db.execute("SELECT * FROM articles WHERE article_id = ? AND status = 1", request.args.get("id"))
            if len(articlerow) > 0:
                authorrow = db.execute("SELECT * FROM users WHERE user_id = ?", articlerow[0]["primary_author_id"])
                editorrow = db.execute("SELECT * FROM users WHERE user_id = ?", articlerow[0]["editor"])
                return render_template("article.html", users=userrow, articles=articlerow, authors=authorrow, editors=editorrow)
            else:
                return redirect("/")
        else:
            return redirect("/")

@app.route("/publish", methods=["GET", "POST"])
@login_required
def publish():

    if request.method == "POST":

        # Validate form submission
        if not request.form.get("article_title"):
            error = 'Missing title'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_topic"):
            error = 'Missing topic'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_abstract"):
            error = 'Missing abstract'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_introduction"):
            error = 'Missing introduction'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_materials_methods"):
            error = 'Missing materials and methods'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_results"):
            error = 'Missing results'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_discussion"):
            error = 'Missing discussion'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_conclusion"):
            error = 'Missing conclusion'
            return render_template('publish.html', error=error)
        elif not request.form.get("article_references"):
            error = 'Missing references'
            return render_template('publish.html', error=error)

        # Grab current date
        now = datetime.now()

        # Generate random color
        color = "#%06x" % random.randint(0, 0xFFFFFF)

        # Get a string of entire article
        doc = request.form.get("article_abstract") + "  " + request.form.get("article_materials_methods") + " " + request.form.get("article_results") + " " + request.form.get("article_discussion") + " " + request.form.get("article_conclusion")

        # Keyword extraction
        stop_words = set(stopwords.words('english'))
        total_words = doc.split()
        total_word_length = len(total_words)
        total_sentences = tokenize.sent_tokenize(doc)
        total_sent_len = len(total_sentences)

        tf_score = {}
        for each_word in total_words:
            each_word = each_word.replace('.','')
            if each_word not in stop_words:
                if each_word in tf_score:
                    tf_score[each_word] += 1
                else:
                    tf_score[each_word] = 1

        # Dividing by total_word_length for each dictionary element
        tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

        def check_sent(word, sentences): 
            final = [all([w in x for w in word]) for x in sentences] 
            sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
            return int(len(sent_len))

        idf_score = {}
        for each_word in total_words:
            each_word = each_word.replace('.','')
            if each_word not in stop_words:
                if each_word in idf_score:
                    idf_score[each_word] = check_sent(each_word, total_sentences)
                else:
                    idf_score[each_word] = 1

        idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())
        tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}

        def get_top_n(dict_elem, n):
            result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
            return result

        editorrow = db.execute("SELECT * FROM users WHERE re = 1 ORDER BY RANDOM() LIMIT 1")
        labels = str(list(get_top_n(tf_idf_score, 8).keys()))

        # Add user to database
        db.execute("INSERT INTO articles (primary_author_id, secondary_authors, topic, labels, date, color, title, abstract, introduction, materials_methods, results, discussion, conclusion, articlereferences, editor) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        session["user_id"],
                        request.form.get("article_secondary_authors"),
                        request.form.get("article_topic"),
                        labels[1:-1],
                        now,
                        color,
                        request.form.get("article_title"),
                        request.form.get("article_abstract"),
                        request.form.get("article_introduction"),
                        request.form.get("article_materials_methods"),
                        request.form.get("article_results"),
                        request.form.get("article_discussion"),
                        request.form.get("article_conclusion"),
                        request.form.get("article_references"),
                        editorrow[0]["user_id"])
        
        # Let user know they're registered
        flash("Sent for publishing!")
        return redirect("/profile_articles")
    else:
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        return render_template("publish.html", users=userrow)

@app.route("/community")
def community():

    # Randomly add ten users from database to community page
    if session.get("user_id") is None:
        communityrow = db.execute("SELECT * FROM users ORDER BY RANDOM() LIMIT 7")
        return render_template("community.html", community=communityrow)
    
    # Same as above, but also pass user_id to template in order to display username
    else:
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        communityrow = db.execute("SELECT * FROM users WHERE user_id != ? ORDER BY RANDOM() LIMIT 7", session["user_id"])
        return render_template("community.html", users=userrow, community=communityrow)

@app.route("/about")
def about():
    if session.get("user_id") is None:
         return render_template("about.html")
    else:
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        return render_template("about.html", users=userrow)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":

        # Ensure person inputted email
        if not request.form.get("email"):
            error = 'Missing email'
            if session.get("user_id") is None:
                return render_template("contact.html", error=error)
            else:
                userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
                return render_template('contact.html', error=error, users=userrow)
        
        # Ensure person inputted message
        if not request.form.get("message"):
            error = 'Missing message'
            if session.get("user_id") is None:
                return render_template("contact.html", error=error)
            else:
                userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
                return render_template('contact.html', error=error, users=userrow)
        
        # Update messages table
        db.execute("INSERT INTO messages (email, message) VALUES (?, ?)", request.form.get("email"), request.form.get("message"))

        # Confirm success of outreach with message
        success = "Message has been sent!"
        if session.get("user_id") is None:
            return render_template("contact.html", success=success)
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("contact.html", success=success, users=userrow)
    
    # Bring user to contact page if they click on it
    else:
        if session.get("user_id") is None:
            return render_template("contact.html")
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("contact.html", users=userrow)

@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    
    # Ensure they have inputted their email
    if request.method == "POST":
        if not request.form.get("email"):
            error = 'Missing email'
            if session.get("user_id") is None:
                return render_template("subscribe.html", error=error)
            else:
                userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
                return render_template('subscribe.html', error=error, users=userrow)
        check = db.execute("SELECT * FROM subscribers WHERE email = ?", request.form.get("email"))
        
        # Ensure person is not already subscribed (1:1 email:user), then update subscribers table
        if len(check) > 0:
            error = 'Already subscribed!'
            if session.get("user_id") is None:
                return render_template("subscribe.html", error=error)
            else:
                userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
                return render_template('subscribe.html', error=error, users=userrow)
        db.execute("INSERT INTO subscribers (email) VALUES (?)", request.form.get("email"))
        
        # Confirm success of updates with message
        success = "You are now subscribed!"
        if session.get("user_id") is None:
            return render_template("subscribe.html", success=success)
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("subscribe.html", success=success, users=userrow)
    
    # Bring user to subscribe page
    else:
        if session.get("user_id") is None:
            return render_template("subscribe.html")
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("subscribe.html", users=userrow)

@app.route("/profile_articles")
@login_required
def profile_articles():

    # Display all articles written by given user
    if session.get("user_id") is None:
        return render_template("index.html")
    else:
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        articlerow = db.execute("SELECT * FROM articles WHERE primary_author_id = ? ORDER BY date DESC", session["user_id"])
        return render_template("profile_articles.html", users=userrow, articles=articlerow)

@app.route("/password_change", methods=['GET', 'POST'])
@login_required
def password_change():
    if request.method == "POST":

        # Validate form submission
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        if not request.form.get("currentpassword"):
            error = 'Missing current password'
            return render_template('settings.html', users=userrow, passerror=error)
        elif not request.form.get("confirmpassword"):
            error = 'Missing password confirmation'
            return render_template('settings.html', users=userrow, passerror=error)
        elif not request.form.get("newpassword"):
            error = 'Missing new password'
            return render_template('settings.html', users=userrow, passerror=error)
        elif str(request.form.get("currentpassword")).strip() != str(request.form.get("confirmpassword")).strip():
            error = 'Passwords don\'t match'
            return render_template('settings.html', users=userrow, passerror=error)
        elif not check_password_hash(userrow[0]["password"], request.form.get("currentpassword")):
            error = 'Invalid current password'
            return render_template('settings.html', users=userrow, passerror=error)
        
        # Update password
        db.execute("UPDATE users SET password = ? WHERE user_id = ?",
                        generate_password_hash(request.form.get("newpassword")),
                        session["user_id"])

        # Confirm success of updates with message
        success = 'Successfully changed password'
        return render_template('settings.html', users=userrow, passsuccess=success)
    
    # Bring user to index page
    else:
        if session.get("user_id") is None:
            return render_template("index.html")
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("settings.html", users=userrow)

@app.route("/profile_settings", methods=['GET', 'POST'])
@login_required
def profile_settings():
    if request.method == "POST":
        
        # Validate form submission
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        if not request.form.get("firstname"):
            error = 'Missing first name'
            return render_template('settings.html', users=userrow, error=error)
        elif not request.form.get("lastname"):
            error = 'Missing last name'
            return render_template('settings.html', users=userrow, error=error)
        elif not request.form.get("username"):
            error = 'Missing username'
            return render_template('settings.html', users=userrow, error=error)
        elif not request.form.get("email"):
            error = 'Missing email'
            return render_template('settings.html', users=userrow, error=error)
        elif not request.form.get("school"):
            error = 'Missing school'
            return render_template('settings.html', users=userrow, error=error)
        elif not request.form.get("hsc"):
            error = 'Missing high school/undegraduate'
            return render_template('settings.html', users=userrow, error=error)
        
        # Update user's high-school/college status
        if request.form.get("hsc") == "hs":
            hscvalue = 0
        elif request.form.get("hsc") == "c":
            hscvalue = 1
        
        # Update all other information for user
        db.execute("UPDATE users SET firstname = ?, lastname = ?, username = ?, email = ?, school = ?, hsc = ? WHERE user_id = ?",
                        request.form.get("firstname"),
                        request.form.get("lastname"),
                        request.form.get("username"),
                        request.form.get("email"),
                        request.form.get("school"),
                        hscvalue,
                        session["user_id"])
        
        # Confirm success of updates with message
        success = 'Successfully updated settings!'

        return render_template('settings.html', users=userrow, success=success)
    else:
        if session.get("user_id") is None:
            return render_template("index.html")
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("settings.html", users=userrow)

@app.route("/editor_article", methods=['GET', 'POST'])
@login_required
def editor_article():
    if request.method == "POST":
        
        # Validate form submission
        if not request.form.get("article_title"):
            error = 'Missing title'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_topic"):
            error = 'Missing topic'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_abstract"):
            error = 'Missing abstract'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_introduction"):
            error = 'Missing introduction'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_materials_methods"):
            error = 'Missing materials and methods'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_results"):
            error = 'Missing results'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_discussion"):
            error = 'Missing discussion'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_conclusion"):
            error = 'Missing conclusion'
            return render_template('editor_article.html', error=error)
        elif not request.form.get("article_references"):
            error = 'Missing references'
            return render_template('editor_article.html', error=error)
        
        # Update status of editor's article (0 = submitted, 1 = approved/published, 2 = rejected)
        status = 0
        if request.form.get("article_status") == "Approve":
            status = 1
        elif request.form.get("article_status") == "Reject":
            status = 2

        # Update all other information of edited article
        security = db.execute("SELECT * FROM articles WHERE article_id = ?", request.form.get("article_id"))
        if (security[0]["editor"] == session["user_id"]):
            db.execute("UPDATE articles SET secondary_authors = ?, topic = ?, title = ?, abstract = ?, introduction = ?, materials_methods = ?, results = ?, discussion = ?, conclusion = ?, articlereferences = ?, status = ? WHERE article_id = ?",
                            request.form.get("article_secondary_authors"),
                            request.form.get("article_topic"),
                            request.form.get("article_title"),
                            request.form.get("article_abstract"),
                            request.form.get("article_introduction"),
                            request.form.get("article_materials_methods"),
                            request.form.get("article_results"),
                            request.form.get("article_discussion"),
                            request.form.get("article_conclusion"),
                            request.form.get("article_references"),
                            status,
                            request.form.get("article_id"))

            return redirect("/")
        else:
            return redirect("/")

    # If user accesses editor article page, then display the article for editing
    else:
        if session.get("user_id") is None:
            return redirect("/")
        else:
            if request.args.get("id") and request.args.get("id").isnumeric():
                userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
                articlerow = db.execute("SELECT * FROM articles WHERE article_id = ? AND editor = ?", request.args.get("id"), session["user_id"])
                if len(articlerow) > 0:
                    authorrow = db.execute("SELECT * FROM users WHERE user_id = ?", articlerow[0]["primary_author_id"])
                    return render_template("editor_article.html", users=userrow, articles=articlerow, authors=authorrow)
                else:
                    return redirect("/")
            else:
                return redirect("/")

@app.route("/editor_password_change", methods=['GET', 'POST'])
@login_required
def editor_password_change():
    if request.method == "POST":

        # Validate form submission
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        if not request.form.get("currentpassword"):
            error = 'Missing current password'
            return render_template('editor_settings.html', users=userrow, passerror=error)
        elif not request.form.get("confirmpassword"):
            error = 'Missing password confirmation'
            return render_template('editor_settings.html', users=userrow, passerror=error)
        elif not request.form.get("newpassword"):
            error = 'Missing new password'
            return render_template('editor_settings.html', users=userrow, passerror=error)
        elif str(request.form.get("currentpassword")).strip() != str(request.form.get("confirmpassword")).strip():
            error = 'Passwords don\'t match'
            return render_template('editor_settings.html', users=userrow, passerror=error)
        elif not check_password_hash(userrow[0]["password"], request.form.get("currentpassword")):
            error = 'Invalid current password'
            return render_template('editor_settings.html', users=userrow, passerror=error)
        
        # Update the password
        db.execute("UPDATE users SET password = ? WHERE user_id = ?",
                        generate_password_hash(request.form.get("newpassword")),
                        session["user_id"])
        
        # Confirm success of updates with message
        success = 'Successfully changed password'
        return render_template('editor_settings.html', users=userrow, passsuccess=success)
    
    # Bring user to index page
    else:
        if session.get("user_id") is None:
            return render_template("index.html")
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("editor_settings.html", users=userrow)

@app.route("/editor_profile_settings", methods=['GET', 'POST'])
@login_required
def editor_profile_settings():
    if request.method == "POST":
        
        # Validate form submission
        userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
        if not request.form.get("firstname"):
            error = 'Missing first name'
            return render_template('editor_settings.html', users=userrow, error=error)
        elif not request.form.get("lastname"):
            error = 'Missing last name'
            return render_template('editor_settings.html', users=userrow, error=error)
        elif not request.form.get("username"):
            error = 'Missing username'
            return render_template('editor_settings.html', users=userrow, error=error)
        elif not request.form.get("email"):
            error = 'Missing email'
            return render_template('editor_settings.html', users=userrow, error=error)
        elif not request.form.get("school"):
            error = 'Missing school'
            return render_template('editor_settings.html', users=userrow, error=error)
        elif not request.form.get("hsc"):
            error = 'Missing high school/undegraduate'
            return render_template('editor_settings.html', users=userrow, error=error)
        
        # Update high-school/college status of editor
        if request.form.get("hsc") == "hs":
            hscvalue = 0
        elif request.form.get("hsc") == "c":
            hscvalue = 1
        
        # Update all other information for editor
        db.execute("UPDATE users SET firstname = ?, lastname = ?, username = ?, email = ?, school = ?, hsc = ? WHERE user_id = ?",
                        request.form.get("firstname"),
                        request.form.get("lastname"),
                        request.form.get("username"),
                        request.form.get("email"),
                        request.form.get("school"),
                        hscvalue,
                        session["user_id"])
        
        # Confirm success of updates with message
        success = 'Successfully updated settings!'
        return render_template('editor_settings.html', users=userrow, success=success)
    
    # Bring user to index page
    else:
        if session.get("user_id") is None:
            return render_template("index.html")
        else:
            userrow = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            return render_template("editor_settings.html", users=userrow)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)