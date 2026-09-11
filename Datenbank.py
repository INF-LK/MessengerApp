import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from sqlcipher3 import dbapi2 as sqlite3


DATABASE = "datenbank.db"
TOKEN_LIFETIME = timedelta(days=30)
DATABASE_KEY_ENV = "MESSENGER_DB_KEY"


def _now():
    return datetime.now(timezone.utc).isoformat()


def _connection():
    connection = sqlite3.connect(DATABASE)
    key_material = os.environ.get(DATABASE_KEY_ENV)
    if not key_material:
        connection.close()
        raise RuntimeError(
            f"{DATABASE_KEY_ENV} muss zum Zugriff auf die verschlüsselte Datenbank gesetzt sein"
        )
    key = hashlib.sha256(key_material.encode("utf-8")).hexdigest()
    connection.execute(f'PRAGMA key = "x\'{key}\'"')
    connection.execute("PRAGMA cipher_compatibility = 4")
    connection.row_factory = sqlite3.Row
    return connection


def setup_db():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS nachrichten
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         sender TEXT NOT NULL,
         empfaenger TEXT NOT NULL,
         nachricht TEXT NOT NULL,
         erstellt_am TEXT NOT NULL)"""
    )
    cursor.execute(
           """CREATE TABLE IF NOT EXISTS nutzer
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            passwort TEXT NOT NULL,
            letzter_login TEXT)"""
        )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tokens
        (token TEXT PRIMARY KEY,
         nutzer TEXT NOT NULL,
         erstellt_am TEXT NOT NULL,
         FOREIGN KEY (nutzer) REFERENCES nutzer(name))"""
    )
    conn.commit()
    conn.close()


def speichern_nachricht(sender, empfaenger, nachricht):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO nachrichten (sender, empfaenger, nachricht, erstellt_am) VALUES (?, ?, ?, ?)",
        (sender, empfaenger, nachricht, _now())
    )
    conn.commit()
    conn.close()


def auslesen_nachrichten():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nachrichten ORDER BY id")
    daten = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return daten


def auslesen_nachrichten_von_nutzer(nutzer, chat=None):
    conn = _connection()
    cursor = conn.cursor()
    if chat is None:
        cursor.execute(
            "SELECT * FROM nachrichten WHERE sender = ? OR empfaenger = ? ORDER BY id",
            (nutzer, nutzer),
        )
    else:
        cursor.execute(
            """SELECT * FROM nachrichten
               WHERE (sender = ? AND empfaenger = ?)
                  OR (sender = ? AND empfaenger = ?)
               ORDER BY id""",
            (nutzer, chat, chat, nutzer),
        )
    daten = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return daten


def speichern_nutzer(name, password):
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO nutzer (name, passwort, letzter_login) VALUES (?, ?, NULL)",
        (name, password),
    )
    conn.commit()
    conn.close()


def auslesen_nutzer():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nutzer ORDER BY name")
    daten = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return daten


def datenbank_reset():
    conn = _connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tokens")
    cursor.execute("DROP TABLE IF EXISTS nachrichten")
    cursor.execute("DROP TABLE IF EXISTS nutzer")
    conn.commit()
    conn.close()
    setup_db()


def registrieren(name, password):
    setup_db()
    try:
        speichern_nutzer(name, password)
    except sqlite3.IntegrityError:
        return None
    return anmelden(name, password)


def anmelden(name, password):
    setup_db()
    conn = _connection()
    user = conn.execute(
        "SELECT name FROM nutzer WHERE name = ? AND passwort = ?",
        (name, password),
    ).fetchone()
    if user is None:
        conn.close()
        return None
    conn.execute("UPDATE nutzer SET letzter_login = ? WHERE name = ?", (_now(), name))
    token = secrets.token_urlsafe(32)
    conn.execute("INSERT INTO tokens (token, nutzer, erstellt_am) VALUES (?, ?, ?)", (token, name, _now()))
    conn.commit()
    conn.close()
    return token


def benutzer_zu_token(token):
    setup_db()
    conn = _connection()
    row = conn.execute("SELECT nutzer, erstellt_am FROM tokens WHERE token = ?", (token,)).fetchone()
    if row is None or datetime.fromisoformat(row["erstellt_am"]) < datetime.now(timezone.utc) - TOKEN_LIFETIME:
        if row is not None:
            conn.execute("DELETE FROM tokens WHERE token = ?", (token,))
            conn.commit()
        conn.close()
        return None
    conn.close()
    return row["nutzer"]


def token_erneuern(token):
    username = benutzer_zu_token(token)
    if username is None:
        return None
    conn = _connection()
    new_token = secrets.token_urlsafe(32)
    conn.execute("DELETE FROM tokens WHERE token = ?", (token,))
    conn.execute("INSERT INTO tokens (token, nutzer, erstellt_am) VALUES (?, ?, ?)", (new_token, username, _now()))
    conn.commit()
    conn.close()
    return new_token


def chats_von_nutzer(nutzer):
    conn = _connection()
    rows = conn.execute(
        """SELECT DISTINCT CASE WHEN sender = ? THEN empfaenger ELSE sender END AS chat
           FROM nachrichten WHERE sender = ? OR empfaenger = ? ORDER BY chat""",
        (nutzer, nutzer, nutzer),
    ).fetchall()
    conn.close()
    return [row["chat"] for row in rows]

