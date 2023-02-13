from flask import Flask, render_template, request, redirect, make_response
from datetime import date
from hashlib import sha256
import json
import random
import string
import os

app = Flask(__name__)

with open('./config.json', 'r') as file:
    CONFIG = json.load(file)


def get_random():
    r = ''
    for i in range(10):
        r += random.choice(list(string.ascii_letters))

    return r


def admin_check():
    cookies = [request.cookies.get('date'), request.cookies.get('random')]
    if str(date.today()) == cookies[0] and CONFIG['admin']['random'] == cookies[1]:
        return 1
    return 0


def config_dump():
    with open('./config.json', 'w') as file:
        json.dump(CONFIG, file, indent=4)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/akce")
def akce():
    return render_template("akce.html")


@app.route("/kontakty")
def kontakty():
    return render_template("kontakty.html")


@app.route("/fotky")
def fotky():
    groups = os.listdir('./static/img/groups')
    photos = {}

    for i in groups:
        photos[i] = os.listdir(f'./static/img/groups/{i}')

    return render_template("fotky.html", photos=photos)

@app.route("/admin")
def admin():
    if admin_check():
        return redirect('admin-panel')
    return redirect("admin-login")


@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("admin_login.html")

    hash = sha256(bytes(request.form['password'],
                  'ascii'))

    if hash.hexdigest() == CONFIG['admin']['hash']:
        r = get_random()

        resp = make_response(redirect('/admin'))
        resp.set_cookie('date', str(date.today()))
        CONFIG['admin']['date'] = str(date.today())
        resp.set_cookie('random', r)
        CONFIG['admin']['random'] = r

        config_dump()

        return resp


@app.route("/admin-panel")
def admin_panel():
    if admin_check():
        return render_template("admin_panel.html")

    return redirect("admin-login")


@app.route("/admin-panel/fotky", methods=['GET', 'POST'])
def admin_fotky():
    if admin_check():
        if request.method == 'GET':
            groups = os.listdir('./static/img/groups')
            photos = {}

            for i in groups:
                photos[i] = os.listdir(f'./static/img/groups/{i}')
            
            return render_template("admin_fotky.html", photos=photos)
        
        if method.form['do'] == 'del-group': pass

    return redirect("admin-login")


if __name__ == "__main__":
    app.run(debug=True)
