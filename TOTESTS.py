
import sqlite3
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
payments = dict()
games_info = cursor.execute("SELECT id, price, name FROM games").fetchall()
for game in games_info:
    payments[game[0]] = (game[1], game[2])
print(payments)
