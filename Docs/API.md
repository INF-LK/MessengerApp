# API-Dokumentation

## Überblick

- Port: 5000

## Verbindungsaufbau

### Bereits authentifiziert

- `RECONNECT [Token]`: Wenn im Frontend bereits ein Token vorhanden ist, wird erneut eine Autorisierung versucht.
- `CONNECT [Token]`: Das Backend bestätigt die Autorisierung und gibt dem Frontend ein neues Token zurück. Wenn der Login fehlschlägt, wird kein Token zurückgegeben.

### Neuer Login

- `LOGIN [Benutzername] [Passwort]`: Das Frontend identifiziert sich beim Backend.
- `CONNECT [Token]`: Das Backend bestätigt die Autorisierung und gibt dem Frontend ein Token zurück. Wenn der Login fehlschlägt, wird kein Token zurückgegeben.

### Registrierung

- `REGISTER [Benutzername] [Passwort]`
- `CONNECT [Token]`: Das Backend bestätigt die Autorisierung und gibt dem Frontend ein Token zurück. Wenn die Registrierung fehlschlägt, wird kein Token zurückgegeben.

## Datenabruf

- `CHATS [Chats]`: Das Backend schickt die Chats des Nutzers als Liste, zum Beispiel `Alice, Bob, Cedrik`.
- `MESSAGES [Nachrichtenverlauf]`: Das Backend schickt den Nachrichtenverlauf als Dictionary im Format `Chat: Nachrichtenverlauf`.

## Befehle

- `SEND_MESSAGE [Token] [Empfänger] [Nachricht]`: Das Frontend sendet eine Nachricht an das Backend; die Autorisierung erfolgt über den Token.
- `RECEIVE_MESSAGE [Sender] [Nachricht]`: Das Backend sendet eine Nachricht an das Frontend; die Autorisierung erfolgt ebenfalls über den Token.

## Löschfristen

- Token: 30 Tage
- Benutzer, Nachrichtenverlauf, Chats und ähnliche Daten: 6 Monate ohne Login
