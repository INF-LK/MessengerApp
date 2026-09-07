import socket
import threading

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
        try:
            reader = client.makefile("r", encoding="utf-8")
            client.sendall(b"WELCOME Please connect with CONNECT <username>\n")
            for raw_line in reader:
                line = raw_line.rstrip("\r\n")
                if not line:
                    continue
                response = self.choose_method(line, username, client)
                client.sendall((response + "\n").encode("utf-8"))
                if response.startswith("CONNECTED "):
                    username = response.split(maxsplit=1)[1]
        except (ConnectionError, OSError, UnicodeError):
            pass
        finally:
            if username:
                with self.lock:
                    if self.clients.get(username) is client:
                        del self.clients[username]
            client.close()

    def choose_method(self, line, sender=None, client=None):
        parts = line.split(maxsplit=2)
        if not parts:
            return "ERROR empty command"
        method = parts[0]

        if method == "CONNECT":
            if len(parts) != 2 or not parts[1].strip():
                return "ERROR CONNECT requires a username"
            username = parts[1].strip()
            if client is None:
                return "ERROR connection is required"
            with self.lock:
                if username in self.clients:
                    return "ERROR username already connected"
                self.clients[username] = client
            return f"CONNECTED {username}"

        if method == "SEND_MESSAGE":
            if sender is None:
                return "ERROR connect before sending"
            if len(parts) != 3 or not parts[1] or not parts[2]:
                return "ERROR SEND_MESSAGE requires recipient and message"
            return self.send_message(parts[1], parts[2], sender)

        return "ERROR unknown method"

    def send_message(self, recipient, message, sender):
        with self.lock:
            client = self.clients.get(recipient)
        if client is None:
            return "ERROR recipient not connected"
        try:
            client.sendall(f"RECEIVE_MESSAGE {sender} {message}\n".encode("utf-8"))
        except (ConnectionError, OSError):
            return "ERROR could not deliver message"
        return "SENT"


if __name__ == "__main__":
    BackendtoFrontend().start()
