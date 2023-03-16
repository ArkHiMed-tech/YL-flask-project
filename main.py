from flask import Flask, render_template, request, redirect, session, url_for
import hashlib
import logging
import sqlite3

logging.basicConfig(filename='logs.txt', level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = '$tr0ng pa$$w0rd'

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

games_info = dict()
client_id = "20EB4A616D297EC0B26A1B9A6D6C712AD71CF5399781B7F53D5F17FED125E24B"
notification_secret = "h1KPMxY/JxcuINbeQsAQTeyd"
for game in cursor.execute("SELECT id, price, name FROM games").fetchall():
    games_info[game[0]] = (game[1], game[2])


@app.route("/")
def main():
    return render_template('main.html', context={'session': session})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html', context={})
    else:
        if request.form['type'] == 'registration':
            session['user'] = request.form['email']
            session['password'] = request.form['password']
            session['type'] = 'registered'
        else:
            session['type'] = 'logined'
            session['user'] = request.form['email']
            session['password'] = request.form['password']
        return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))


@app.route("/payment_notifications", methods=['POST'])
def check_notification():
    logging.info(request.form)
    pre_hash = bytes(f"{request.form.get('notification_type')}&{request.form.get('operation_id')}&{request.form.get('amount')}&{request.form.get('currency')}&{request.form.get('datetime')}&{request.form.get('sender')}&{request.form.get('codepro')}&{notification_secret}&{request.form.get('label')}", encoding='utf-8')
    hashed_obj = hashlib.sha1(pre_hash)
    hashed = hashed_obj.hexdigest()
    if request.form.get('sha1_hash') == hashed:
        print('hash_check passed')
        if request.form.get('label') in games_info.keys():
            if request.form.get('payment') == request.form.get('label')[0:2]:
                cursor.execute(f"INSERT INTO owned (user_id, {request.form.get('label')[0:2]}) VALUES (?, ?)",
                               (request.form.get('label')[2:], 1))  # putting TRUE in user's owned games
    return "OK"


if __name__ == '__main__':
    app.run()