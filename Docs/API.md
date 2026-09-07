# API Docs

- Port: 5000

## Verbindungsaufbau:

- Falls Token vorhanden: RECONNECT [Token] -> Wenn bereits Token im Frontend vorhanden, erneut authorisieren
- CONNECT [Token] -> Backend bestätigt authorisierung, indem es dem Frontend ein neues Token gibt. Falls der Login nicht erfolgreich war, wird kein Token zurückgegeben

---

- Sonst: LOGIN [Benutzername] [Passwort] -> Frontend identifiziert sich beim Backend
- CONNECT [Token] -> Backend bestätigt authorisierung, indem es dem Frontend ein Token gibt. Falls der Login nicht erfolgreich war, wird kein Token zurückgegeben

---

- Sonst: REGISTER [Benutzername] [Passwort]
- CONNECT [Token] -> Backend bestätigt authorisierung, indem es dem Frontend ein Token gibt. Falls der Login nicht erfolgreich war, wird kein Token zurückgegeben

---

- CHATS [Chats] -> Backend schickt Chats des Users als Liste (Alice, Bob, Cedrik, ...)
- MESSAGES [Nachrichtenverlauf] -> Backend schickt Nachrichtenverlauf als Dictionary (Chat : Nachrichtenverlauf)

## Befehle

- SEND_MESSAGE [Token] [Empfänger] [Nachricht] -> Frontend schickt Nachricht an Backend, authorisierung über Token
- RECEIVE_MESSAGE [Token] [Sender] [Nachricht] -> Backend schickt Nachricht an Frontend, authorisierung über Token

# Löschfristen

- Token: 30 Tage
- Benutzer, Nachrichtenverlauf, Chats, ...: 6 Monate ohne Login
