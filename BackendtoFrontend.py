import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
#wir brauchen:
#wir kriegen eine Nachricht+Sender+Endpoint+public key(wir machen kein RSA!)
#wir senden die nachricht an die Richtige person/port (->Von Datenbank)

class BackendtoFrontend:
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        # Allow quick restart after stopping the server
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        self.server.bind((HOST, PORT))
        self.server.listen()
    
        print(f"Server listening on {HOST}:{PORT}")
    
        while True:
            client, address = self.server.accept()
    
            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True,
            )
    
            thread.start()

    def send_message(self, message, sender):
        pass

    def choose_method(self, input):
        method, sender, message = input.split()[0], input.split()[1], input.split()[2]
        if method == "SEND_MESSAGE":
            self.send_message(message, sender)

if __name__ == "__main__":
    server = BackendtoFrontend()
