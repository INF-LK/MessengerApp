import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


class MessengerClient:
	def __init__(self, username, host=HOST, port=PORT):
		self.username = username
		self.host = host
		self.port = port
		self.socket = None
		self.reader = None
		self.running = False

	def connect(self):
		self.socket = socket.create_connection((self.host, self.port))
		self.reader = self.socket.makefile("r", encoding="utf-8")
		self.running = True

		welcome = self.reader.readline().rstrip("\r\n")
		if welcome:
			print(welcome)

		self.send_command(f"CONNECT {self.username}")
		threading.Thread(target=self.receive_messages, daemon=True).start()

	def send_command(self, command):
		if self.socket is None:
			raise ConnectionError("Not connected to the server")
		self.socket.sendall((command + "\n").encode("utf-8"))

	def send_message(self, recipient, message):
		self.send_command(f"SEND_MESSAGE {recipient} {message}")

	def receive_messages(self):
		try:
			for raw_line in self.reader:
				line = raw_line.rstrip("\r\n")
				if line:
					print(f"\n{line}")
					print("> ", end="", flush=True)
		except (ConnectionError, OSError, UnicodeError):
			if self.running:
				print("\nVerbindung zum Server verloren.")
		finally:
			self.running = False

	def run(self):
		self.connect()
		print("Nachricht senden mit: <Empfänger> <Nachricht>")
		print("Beenden mit: /quit")

		try:
			while self.running:
				command = input("> ").strip()
				if not command:
					continue
				if command == "/quit":
					break

				parts = command.split(maxsplit=1)
				if len(parts) != 2:
					print("Format: <Empfänger> <Nachricht>")
					continue
				self.send_message(parts[0], parts[1])
		except (EOFError, KeyboardInterrupt):
			pass
		finally:
			self.close()

	def close(self):
		self.running = False
		if self.reader is not None:
			self.reader.close()
			self.reader = None
		if self.socket is not None:
			self.socket.close()
			self.socket = None


if __name__ == "__main__":
	username = input("Benutzername: ").strip()
	if not username:
		raise SystemExit("Ein Benutzername ist erforderlich.")
	MessengerClient(username).run()
