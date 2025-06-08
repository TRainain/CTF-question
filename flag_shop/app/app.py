import os
import uuid
from flask import Flask, render_template, request, session, redirect, url_for
import threading
import random
import string

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
flag = os.environ.get("FLAG")

def generate_random_users(n):
    users = {}
    for _ in range(n):
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        users[username] = {"password": password, "money": 0}
    return users


users = generate_random_users(1000)
users["Infernity"] = {"password": "Infernity", "money": 6000}

admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
users["admin"] = {"password": admin_password, "money": 10000}

flag_price = 10000
mutex = threading.Lock()


@app.route('/')
def index():
    if "username" in session:
        return render_template("index.html", logged_in=True, username=session["username"],money=users[session["username"]]["money"])
    return render_template("index.html", logged_in=False)


@app.route('/reset', methods=['GET'])
def reset():
    global users
    users = {}
    users = generate_random_users(1000)
    users["Infernity"] = {"password": "Infernity", "money": 6000}
    global admin_password
    admin_password = {}
    admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

    users["admin"] = {"password": admin_password, "money": 10000}

    return redirect(url_for('index'))


@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in users and users[username]["password"] == password:
        session["username"] = username
        return redirect(url_for('index'))
    return "Invalid credentials", 403


@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))


@app.route('/transfer', methods=["POST"])
def transfer():
    if "username" not in session:
        return "Not logged in", 403

    receiver = request.form.get("receiver")
    amount = float(request.form.get("amount"))
    if amount < 0:
        return "Insufficient funds", 400

    if session["username"] in receiver:
        return "Cannot transfer to self", 400

    if receiver not in users:
        return f"Invalid user {receiver}", 400

    if users[session["username"]]["money"] >= amount:
        mutex.acquire()
        users[session["username"]]["money"] -= int(amount)
        users[receiver]["money"] += amount
        mutex.release()
        return redirect(url_for('index'))
    return "Insufficient funds", 400


@app.route('/buy_flag')
def buy_flag():
    if "username" not in session:
        return "Not logged in", 403

    if users[session["username"]]["money"] >= flag_price:
        users[session["username"]]["money"] -= flag_price
        return f"Here is your flag: {flag}"
    return "You don't have enough money!", 400


@app.route('/get_users', methods=["GET"])
def get_users():
    num = int(request.args.get('num', 1000))
    selected_users = random.sample(list(users.keys()), num)
    return {"users": selected_users}


@app.route('/view_money', methods=["GET"])
def view_money():
    username = request.args.get('username')
    if username in users:
        return {"username": username, "money": users[username]["money"]}
    return "User not found", 404


@app.route('/force_buy_flag', methods=["POST"])
def force_buy_flag():
    if "username" not in session or session["username"] != "Infernity":
        return "Permission denied", 403

    target_user = request.form.get("target_user")
    if target_user not in users:
        return "User not found", 404

    if "admin" in users:
        return "Admin can't buy flag", 403

    if users[target_user]["money"] >= flag_price:
        users[target_user]["money"] -= flag_price
        return f"User {target_user} successfully bought the flag!," + f"Here is your flag: {flag}"
    return f"User {target_user} does not have sufficient funds", 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
