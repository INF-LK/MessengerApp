import json
import queue
import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


class MessengerClient:
	def __init__(self, username, password, host=HOST, port=PORT):
		self.username = username
		self.password = password
		self.host = host
		self.port = port
		self.socket = None
		self.reader = None
		self.running = False
		self.token = None
		self.chats = []
		self.messages = {}
		self.messageList = []
		self.send_lock = threading.Lock()
		self.response_queue = queue.Queue()

	def connect(self, mode="LOGIN", token=None):
		try:
			self.socket = socket.create_connection((self.host, self.port))
			self.reader = self.socket.makefile("r", encoding="utf-8")

			welcome = self.reader.readline().rstrip("\r\n")
			if welcome:
				print(welcome)

			self.running = True
			threading.Thread(target=self.receive_messages, daemon=True).start()

			if mode == "RECONNECT":
				if not token:
					raise ValueError("Für RECONNECT wird ein Token benötigt.")
				response = self.request(f"RECONNECT {token}")
			else:
				if mode not in ("LOGIN", "REGISTER"):
					raise ValueError("Ungültiger Anmeldemodus.")
				response = self.request(f"{mode} {self.username} {self.password}")
				if not response.startswith("TOKEN "):
					raise ConnectionError(response)
				token = response.split(maxsplit=1)[1]
				response = self.request(f"CONNECT {token}")

			if not response.startswith("CONNECTED "):
				raise ConnectionError(response)
			fields = response.split(maxsplit=2)
			if len(fields) != 3:
				raise ConnectionError("Ungültige CONNECT-Antwort vom Backend.")
			if self.username and fields[1] != self.username:
				raise ConnectionError("Backend hat einen anderen Benutzer verbunden.")
			self.username = fields[1]
			self.token = fields[2]
		except (ConnectionError, OSError, ValueError):
			self.close()
			raise

	def request(self, command):
		self.send_command(command)
		try:
			response = self.response_queue.get(timeout=10)
		except queue.Empty as error:
			raise ConnectionError("Keine Antwort vom Server") from error
		if response.startswith("ERROR "):
			raise ConnectionError(response)
		return response

	def send_command(self, command):
		if self.socket is None:
			raise ConnectionError("Keine Verbindung zum Server")
		with self.send_lock:
			self.socket.sendall((command + "\n").encode("utf-8"))

	def send_message(self, recipient, message):
		return self.request(f"SEND_MESSAGE {self.token} {recipient} {message}")

	def load_chats(self):
		response = self.request(f"CHATS {self.token}")
		if response.startswith("CHATS "):
			self.chats = json.loads(response[6:])
		else:
			raise ConnectionError(response)
		return self.chats

	def load_messages(self):
		response = self.request(f"MESSAGES {self.token}")
		if response.startswith("MESSAGES "):
			self.messages = json.loads(response[9:])
		else:
			raise ConnectionError(response)
		return self.messages

	def receive_messages(self):
		try:
			for raw_line in self.reader:
				line = raw_line.rstrip("\r\n")
				if not line:
					continue
				if line.startswith("RECEIVE_MESSAGE "):
					_, sender, message = line.split(maxsplit=2)
					print(f"\nNachricht von {sender}: {message}")
					self.messageList.append([sender, 1, "foreign", message])
				else:
					self.response_queue.put(line)
					continue
				print("> ", end="", flush=True)
		except (ConnectionError, OSError, UnicodeError, ValueError):
			if self.running:
				print("\nVerbindung zum Server verloren.")
		finally:
			self.running = False

	def run(self):
		try:
			self.connect()
			print("Nachricht senden mit: <Empfänger> <Nachricht>")
			print("/chats, /messages oder /quit")

			while self.running:
				command = input("> ").strip()
				if not command:
					continue
				if command == "/quit":
					break
				if command == "/chats":
					print(self.load_chats())
					continue
				if command == "/messages":
					print(json.dumps(self.load_messages(), ensure_ascii=False, indent=2))
					continue

				parts = command.split(maxsplit=1)
				if len(parts) != 2:
					print("Format: <Empfänger> <Nachricht>")
					continue
				self.send_message(parts[0], parts[1])
		except (ConnectionError, OSError, ValueError) as error:
			print(f"Fehler: {error}")
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
	password = input("Passwort: ").strip()
	if not username or not password:
		raise SystemExit("Benutzername und Passwort sind erforderlich.")
	MessengerClient(username, password).run()
