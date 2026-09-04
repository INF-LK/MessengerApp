#Hard at work or hardly working

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


def datenbank_reset():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS nachrichten")
    conn.commit()
    conn.close()
    setup_db()
