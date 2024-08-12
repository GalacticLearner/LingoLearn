from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session
from helpers import *
from mysql.connector import connect
import os
from random import choice
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "\xb3Xk\xe8ji\x05^\xd4\xce\xe3\x1c"

load_dotenv()

filters = {"split": splitlines, "refine": refine, "add_to_set": add_to_set}
app.jinja_env.filters.update(filters)

connection = connect(user="sql12725528", host = "sql12.freesqldatabase.com", password=os.getenv(sql_password), database="sql12725528")
database = connection.cursor(buffered=True)

scheduler = BackgroundScheduler()
scheduler.add_job(daily, 'interval', days=1)
scheduler.start()
daily()

@app.route("/", methods=['GET', 'POST'])
def index():
    wotd, potd = fetch_daily()
    print(wotd)
    if request.method == 'POST':
        if "user_id" in session:
            database.execute("select name, lingos from users where id=%s", (session["user_id"],))
            username, lingos = database.fetchall()[0]
            bookmark = False

            if request.form.get("bookmark"):
                word = request.form.get("bookmark")
                database.execute("update users set bookmarks=concat(bookmarks, %s) where id=%s", ('~'+word, session["user_id"]))
                connection.commit()
                bookmark = True
            else:
                word = request.form.get("word")

            word_data, api, error = fetch_word(word)[:3]
            return render_template("index.html", username=username, logged_in=True, word_data=word_data, api=api, error=error, query=word, bookmark=bookmark, lingos=lingos, wotd=wotd, potd=potd)
        
        else:
            if request.form.get("bookmark"):
                return redirect("/signin")
            else:
                word = request.form.get("word")

            word_data, api, error = fetch_word(word)[:3]

            return render_template("index.html", word_data=word_data, error=error, api=api, query=word, wotd=wotd, potd=potd)
        
    else:
        if "user_id" in session:
            database.execute("select name, lingos from users where id=%s", (session["user_id"],))
            username, lingos = database.fetchall()[0]
            return render_template("index.html", username=username, user_id=session["user_id"], logged_in=True, lingos=lingos, wotd=wotd, potd=potd)
        
        else:
            return render_template("index.html", wotd=wotd, potd=potd)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            return render_template("signup.html", error="Field cannot be empty")
        else:
            database.execute("SELECT name FROM users WHERE name = %s", (username,))
            if database.fetchall():
                return render_template("signup.html", error='Username Taken')    
                
            database.execute("insert into users (name, password_hash) values (%s, %s)",
                            (username, generate_password_hash(password)))
            connection.commit()
            return redirect("/signin")
    
    else:
        return render_template("signup.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            return render_template("signin.html", error="Field cannot be empty")
        
        else:
            database.execute("select id, name, password_hash from users where name = %s limit 1", (username,))
            user_data = database.fetchone()

            if user_data and check_password_hash(user_data[2], password):
                session["user_id"] = user_data[0]
                return redirect("/")
            else:
                return render_template("signin.html", error="Incorrect Password")
    
    else:
        return render_template("signin.html")
    
@app.route("/signout")
def signout():
    session.clear()
    return redirect("/")

@app.route("/practice", methods=['GET', 'POST'])
@login_required
def practice():
    database.execute("select name, lingos from users where id=%s", (session["user_id"],))
    username, lingos = database.fetchall()[0]

    words = []
    if request.args.get("book"):
        name = request.args.get("book")
        title, book = fetch_book(name)

        for word in book:
            words.append(rem_punc(word)) 
    else:
        with open('static/large_dictionary.txt', 'r') as file:
            words = file.read().splitlines()

    options = set()
    word_data = {"title": 0}
    difficulty = "NA"
    while "title" in word_data or (difficulty == "NA" or difficulty < 3):
        word = choice(words)
        word_data = fetch_def(word)
        difficulty = fetch_word(word)
        if len(difficulty) == 4:
            if difficulty[3] != "NA":
                difficulty = int(difficulty[3])
            else:
                difficulty = "NA"
        else:
            difficulty = "NA"

    for i in range(3):
        options.add(rem_punc(choice(words)))

    opt_list = list(options)[:2]
    definition = word_data["meanings"][0]["definitions"][0]["definition"]
    word = word_data["word"]

    return render_template("practice.html", logged_in=True, username=username, ans=word, definition=definition, options=options, opt_list=opt_list, lingos=lingos)

@app.route("/book-tutor", methods=["GET", "POST"])
@login_required
def book_tutor():
        database.execute("select name, books, lingos from users where id=%s", (session["user_id"],))
        username, books, lingos = database.fetchall()[0]

        if request.method == "POST":
            title = request.form.get("title")

            if title not in books:
                database.execute("update users set books=concat(books, %s) where id=%s", ('~'+title, session["user_id"]))
                connection.commit()
            return redirect("/practice?book=" + title)
        
        else:
            if books == None:
                books = ''
            books = books.strip(' ~').split('~')
            print(books)
            for book in books:
                img_search(book)
            return render_template("book-tutor.html", logged_in=True, username=username, books=books, lingos=lingos)

@app.route("/bookmarks")
@login_required
def bookmarks():
        database.execute("select name, lingos, bookmarks from users where id=%s", (session["user_id"],))
        data = database.fetchall()[0]
        username, lingos = data[:2]
        bookmarks = data[2].strip(' ~').split('~')
        words_data = {}

        for bookmark in bookmarks:
            word_data = fetch_word(bookmark)[0:2]
            words_data[bookmark] = word_data

        return render_template("bookmarks.html", logged_in=True, username=username, word_data=words_data, lingos=lingos)

@app.route("/lifeline")
def lifeline():
    database.execute("update users set lingos = lingos - 5 where id=%s", (session["user_id"],))
    connection.commit()
    return "database updated"

@app.route("/quiz-submit")
def quiz_submit():
    ans = request.args.get("ans")
    choice = request.args.get("choice")
    
    if choice == ans:
        database.execute("update users set lingos = lingos + 10 where id=%s", (session["user_id"],))
    else:
        database.execute("update users set lingos = lingos - 5 where id=%s", (session["user_id"],))

    connection.commit()
    return "database updated"