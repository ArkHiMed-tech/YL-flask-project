from flask import Flask, render_template, request
import hashlib
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

payments = {'01': 100, '02': 200}
notification_secret = "h1KPMxY/JxcuINbeQsAQTeyd"


@app.route("/")
def main():
    return render_template('main.html', context={})


@app.route("/payment_notifications", methods=['POST'])
def check_notification():
    notification_data = request.get_json()
    if notification_data:
        pre_hash = bytes(f"{notification_data['notification_type']}&{notification_data['operation_id']}&{notification_data['amount']}&{notification_data['currency']}&{notification_data['datetime']}&{notification_data['sender']}&{notification_data['codepro']}&{notification_secret}&{notification_data['label']}", encoding='utf-8')
        hashed_obj = hashlib.sha1(pre_hash)
        hashed = hashed_obj.hexdigest()
        if notification_data['sha1_hash'] == hashed:
            if notification_data['label'] in payments.keys():
                if notification_data['payment'] == payments[notification_data['label'][0:2]]:
                    cursor.execute(f"INSERT INTO owned (user_id, {notification_data['label'][0:2]}) VALUES (?, ?)",
                                   (notification_data['label'][2:], 1))  # putting TRUE in user's owned games
    return "OK"


if __name__ == '__main__':
    app.run()