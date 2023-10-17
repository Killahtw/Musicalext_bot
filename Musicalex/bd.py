import sqlite3 as sq
sqcon = sq.connect('../Musicalex/trll.db')
cur = sqcon.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS accounts("
            "tg_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "fname TEXT, "
            "username TEXT, "
            "right INTEGER DEFAULT 0)"
            )
sqcon.commit()


async def sq_start():
    sqcon.commit()

async def cmd_start_db(user_id, fname, username):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id, fname, username, right) VALUES (?, ?, ?, ?)",
                    (user_id, fname, username, 0))
        sqcon.commit()



async def song_count(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id = ?", (user_id,)).fetchone()
    if user:
        right_count = user[3]
        right_count = int(right_count)
        cur.execute("UPDATE accounts SET right = ? WHERE tg_id = ?", (right_count + 1, user_id))
        sqcon.commit()
