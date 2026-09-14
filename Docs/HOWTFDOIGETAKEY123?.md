# Lokales TLS-Zertifikat anlegen

Für die lokale Entwicklung kann ein einfaches selbstsigniertes Zertifikat mit OpenSSL erzeugt werden:

```bash
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt
```

Wenn du das Zertifikat nicht für ein Quiz oder einen Test brauchst, kannst du die Fragen einfach mit Enter überspringen.
