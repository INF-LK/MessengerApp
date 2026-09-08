# Infcord — A Lightweight Local Messenger

Infcord is a small, open-source messenger built in Python for local and small-network messaging. It's designed to be simple to run, easy to extend, and a good starting point for learning how chat applications connect frontend, backend, and a simple database layer.

Features

- Simple local or LAN messaging (prototype)
- GUI frontend with `FrontendGUI.py`
- Clear separation between frontend and backend bridge scripts
- Lightweight database/backing store (see `Datenbank.py`)
- Easy to read and extend Python code — great for learning and hacking

Quick start

1. Install Python 3.9+ (3.10 recommended).
2. From the project root, install dependencies (none by default):

    python3 -m pip install -r requirements.txt

This project currently uses only the Python standard library; `requirements.txt` is intentionally empty (comments only).

Run the app (development)

- Start the backend bridge / server (if applicable):

```bash
python3 Backend.py
```

- Start the GUI frontend:

```bash
python3 FrontendGUI.py
```

Project layout

- `Backend.py` — bridge/server that forwards messages from backend to frontend
- `Client.py` — bridge/client that forwards messages from frontend to backend
- `FrontendGUI.py` — the GUI application for users
- `Datenbank.py` — persistence layer / simple database helper
- `assets/` — images and static assets used by the GUI
- `Docs/` — documentation and API reference (see [Docs/API.md](Docs/API.md))

Usage examples

- To send a message, open the GUI and type your message in the input box, then press send.
- For headless testing, you can import the messaging functions from the bridge scripts and call them from a Python REPL or test script.

Configuration

- The project currently uses simple file- and script-based configuration. If you want to change network ports, database filenames, or other settings, look for constants at the top of the corresponding Python files and update them.
