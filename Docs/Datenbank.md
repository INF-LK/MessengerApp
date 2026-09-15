# Datenbank einrichten

Die SQLite-Datenbank wird mit SQLCipher verschlüsselt. Vor dem Start des Backends muss ein geheimer Schlüssel als Umgebungsvariable gesetzt und die Abhängigkeit installiert werden:

Kopiere die .env.example zu .env und trage den MESSENGER_DB_KEY ein

```bash
pip install -r requirements.txt
python Backend.py
```

Ohne `MESSENGER_DB_KEY` verweigert die Anwendung den Datenbankzugriff. Der Schlüssel darf nicht im Quellcode oder im Repository gespeichert werden.
