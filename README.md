# MessengerApp

## Datenbank einrichten

Die SQLite-Datenbank wird mit SQLCipher verschlüsselt. Vor dem Start des Backends
muss ein geheimer Schlüssel als Umgebungsvariable gesetzt und die Abhängigkeit
installiert werden:

```bash
pip install -r requirements.txt
export MESSENGER_DB_KEY="ein-langes-geheimes-passwort"
python BackendtoFrontend.py
```

Ohne `MESSENGER_DB_KEY` verweigert die Anwendung den Datenbankzugriff. Der
Schlüssel darf nicht in den Quellcode oder ins Repository eingecheckt werden.