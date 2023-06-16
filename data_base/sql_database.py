import sqlite3,random
def db_connect():
    with sqlite3.connect("MGE_Bratki.db") as db:
        cr=db.cursor()
        cr.execute("""CREATE TABLE IF NOT EXISTS MGE_pics(id INTEGER PRIMARY KEY AUTOINCREMENT,photo TEXT)""")
        if db:
            print("база данных подключена успешна!")
async def sql_input(photo_id):
        try:
            db=sqlite3.connect("MGE_Bratki.db")
            cr=db.cursor()
            cr.execute("""INSERT INTO MGE_pics(photo) VALUES(?)""",(photo_id,))
            db.commit()
        except sqlite3.Error as e:
            print("error",e)
        finally:
            cr.close()
            db.close()
def sql_send():
    try:
        db=sqlite3.connect("MGE_Bratki.db")
        cr=db.cursor()
        id_length=cr.execute("SELECT id FROM MGE_pics").fetchall()
        random_id=random.randint(1,len(id_length))
        random_photo=cr.execute("SELECT photo FROM MGE_pics WHERE id=?",(random_id,)).fetchone()[0]
        return random_photo
    except sqlite3.Error as e:
        print("error",e)
    finally:
        cr.close()
        db.close()