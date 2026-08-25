# Cards

Standalone HTML session cards — one file per session, openable in any browser with no server,
no build step and no network dependency beyond the webfont (which falls back cleanly offline).

A card is a **convenience view of a session**, never a source of truth. The programme lives in
`programme/`, the record lives in `logs/`. If a card and the programme disagree, the programme
is right and the card is stale.

Naming: `YYYY-MM-DD-<session>.html`.

## Opening one on a phone

The files are local, so a phone can't open them directly. Serve the directory over your LAN:

```bash
cd ~/src/training/cards && python3 -m http.server 8000
```

Then browse to `http://<your-laptop-ip>:8000/` from the phone on the same wifi. Stop it with
Ctrl-C when you're done.
