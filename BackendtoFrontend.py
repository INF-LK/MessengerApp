import socket
import threading
import json

from Datenbank import (
    anmelden,
    auslesen_nachrichten_von_nutzer,
    benutzer_zu_token,
    chats_von_nutzer,
    registrieren,
    speichern_nachricht,
    token_erneuern,
    setup_db,
)

HOST = "0.0.0.0"
PORT = 5000
#wir brauchen:
#wir kriegen eine Nachricht+Sender+Endpoint+public key(wir machen kein RSA!)
#wir senden die nachricht an die Richtige person/port (->Von Datenbank)

class BackendtoFrontend:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.clients = {}
        self.lock = threading.Lock()
        self.server = None
        setup_db()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.port = self.server.getsockname()[1]
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client, address = self.server.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(client, address),
                    daemon=True,
                ).start()
        except (KeyboardInterrupt, OSError):
            print("\nServer stopped")
        finally:
            self.stop()

    def stop(self):
        if self.server is not None:
            self.server.close()
            self.server = None

        with self.lock:
            clients = list(self.clients.values())
            self.clients.clear()
        for client in clients:
            client.close()

    def handle_client(self, client, address):
        username = None
        token = None
        try:
            reader = client.makefile("r", encoding="utf-8")
            client.sendall(b"WELCOME LOGIN or REGISTER, then CONNECT <token>\n")
            for raw_line in reader:
                line = raw_line.rstrip("\r\n")
                if not line:
                    continue
                response = self.choose_method(line, username, client, token)
                client.sendall((response + "\n").encode("utf-8"))
                if response.startswith("CONNECTED "):
                    fields = response.split()
                    username = fields[1]
                    token = fields[2]
        except (ConnectionError, OSError, UnicodeError):
            pass
        finally:
            if username:
                with self.lock:
                    if self.clients.get(username) is client:
                        del self.clients[username]
            client.close()

    def choose_method(self, line, username=None, client=None, active_token=None):
        parts = line.split(maxsplit=3)
        if not parts:
            return "ERROR empty command"
        method = parts[0]

        if method in ("CONNECT", "RECONNECT"):
            if len(parts) != 2 or not parts[1].strip():
                return f"ERROR {method} requires a token"
            if client is None:
                return "ERROR connection is required"
            connected_username = benutzer_zu_token(parts[1])
            if connected_username is None:
                return "ERROR invalid or expired token"
            with self.lock:
                if connected_username in self.clients and self.clients[connected_username] is not client:
                    return "ERROR username already connected"
            new_token = token_erneuern(parts[1])
            with self.lock:
                self.clients[connected_username] = client
            return f"CONNECTED {connected_username} {new_token}"

        if method == "LOGIN":
            if len(parts) != 3 or not parts[1] or not parts[2]:
                return "ERROR LOGIN requires username and password"
            new_token = anmelden(parts[1], parts[2])
            return f"TOKEN {new_token}" if new_token else "ERROR invalid username or password"

        if method == "REGISTER":
            if len(parts) != 3 or not parts[1] or not parts[2]:
                return "ERROR REGISTER requires username and password"
            new_token = registrieren(parts[1], parts[2])
            return f"TOKEN {new_token}" if new_token else "ERROR username already exists"

        if method in ("CHATS", "MESSAGES"):
            if username is None:
                return f"ERROR connect before {method.lower()}"
            if method == "CHATS":
                return f"CHATS {json.dumps(chats_von_nutzer(username), ensure_ascii=True)}"
            messages = {}
            for message in auslesen_nachrichten_von_nutzer(username):
                chat = message["empfaenger"] if message["sender"] == username else message["sender"]
                messages.setdefault(chat, []).append(message)
            return f"MESSAGES {json.dumps(messages, ensure_ascii=True)}"

        if method == "SEND_MESSAGE":
            if username is None:
                return "ERROR connect before sending"
            if len(parts) != 4 or not parts[1] or not parts[2] or not parts[3]:
                return "ERROR SEND_MESSAGE requires token, recipient and message"
            if parts[1] != active_token or benutzer_zu_token(parts[1]) != username:
                return "ERROR invalid token"
            return self.send_message(parts[2], parts[3], username)

        return "ERROR unknown method"

    def send_message(self, recipient, message, sender):
        speichern_nachricht(sender, recipient, message)
        with self.lock:
            client = self.clients.get(recipient)
        if client is None:
            return "SENT"
        try:
            client.sendall(f"RECEIVE_MESSAGE {sender} {message}\n".encode("utf-8"))
        except (ConnectionError, OSError):
            return "ERROR could not deliver message"
        return "SENT"


if __name__ == "__main__":
    BackendtoFrontend().start()
