#Hard at work or hardly working
# or hard while working :)

# format zum speichern: (Nutzer, Nachricht)

import sqlite3


def setup_db():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS nachrichten
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         nutzer TEXT NOT NULL,
         nachricht TEXT NOT NULL)'''
    )
    cursor.execute(
           '''CREATE TABLE IF NOT EXISTS nutzer
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE)'''
        )
    conn.commit()
    conn.close()


def speichern_nachricht(nutzer, nachricht):
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO nachrichten (nutzer, nachricht) VALUES (?, ?)",
        (nutzer, nachricht)
    )
    conn.commit()
    conn.close()


def auslesen_nachrichten():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nachrichten")
    daten = cursor.fetchall()
    conn.close()
    return daten


def speichern_nutzer(name):
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO nutzer (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def auslesen_nutzer():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nutzer ORDER BY name")
    daten = cursor.fetchall()
    conn.close()
    return daten


def datenbank_reset():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS nachrichten")
    cursor.execute("DROP TABLE IF EXISTS nutzer")
    conn.commit()
    conn.close()
    setup_db()


setup_db()
speichern_nutzer("Max")
print(auslesen_nutzer())