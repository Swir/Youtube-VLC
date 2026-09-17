from __future__ import annotations

import locale

SUPPORTED = {"en", "pl", "no"}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "title": "VLCTube 3",
        "subtitle": "Resolve online video with yt-dlp and play it directly in VLC",
        "url": "Video or playlist URL",
        "add": "Add to queue",
        "paste": "Paste",
        "expand": "Expand playlist",
        "quality": "Quality",
        "vlc": "VLC Player",
        "auto_detect": "Auto-detect",
        "browse": "Browse…",
        "queue": "Queue",
        "history": "History",
        "play_selected": "Play selected",
        "play_all": "Play all",
        "remove": "Remove",
        "clear": "Clear queue",
        "clear_history": "Clear history",
        "status_ready": "Ready",
        "invalid_url": "Enter a valid http:// or https:// media URL.",
        "no_vlc": "VLC Player was not found. Use Browse to select vlc.exe.",
        "resolving": "Resolving stream…",
        "launched": "Opened in VLC: {title}",
        "added": "Added {count} item(s) to the queue",
        "expanded": "Playlist expanded: {count} item(s)",
        "failed": "Operation failed: {error}",
        "no_selection": "Select an item in the queue first.",
        "vlc_found": "VLC detected: {path}",
        "vlc_missing": "VLC not detected",
        "queued": "Queued",
        "playing": "Playing",
        "error": "Error",
        "about": "VLCTube streams through VLC; it does not download media files. Respect the source site's terms and content rights.",
    },
    "pl": {
        "title": "VLCTube 3",
        "subtitle": "Rozwiąż strumień przez yt-dlp i odtwórz go bezpośrednio w VLC",
        "url": "Adres filmu lub playlisty",
        "add": "Dodaj do kolejki",
        "paste": "Wklej",
        "expand": "Rozwiń playlistę",
        "quality": "Jakość",
        "vlc": "VLC Player",
        "auto_detect": "Wykryj automatycznie",
        "browse": "Wybierz…",
        "queue": "Kolejka",
        "history": "Historia",
        "play_selected": "Odtwórz zaznaczone",
        "play_all": "Odtwórz wszystko",
        "remove": "Usuń",
        "clear": "Wyczyść kolejkę",
        "clear_history": "Wyczyść historię",
        "status_ready": "Gotowe",
        "invalid_url": "Podaj poprawny adres multimediów http:// lub https://.",
        "no_vlc": "Nie znaleziono VLC Player. Użyj przycisku Wybierz, aby wskazać vlc.exe.",
        "resolving": "Rozwiązywanie strumienia…",
        "launched": "Otwarto w VLC: {title}",
        "added": "Dodano do kolejki: {count}",
        "expanded": "Rozwinięto playlistę: {count} pozycji",
        "failed": "Operacja nie powiodła się: {error}",
        "no_selection": "Najpierw zaznacz pozycję w kolejce.",
        "vlc_found": "Wykryto VLC: {path}",
        "vlc_missing": "Nie wykryto VLC",
        "queued": "W kolejce",
        "playing": "Odtwarzanie",
        "error": "Błąd",
        "about": "VLCTube przesyła strumień do VLC i nie pobiera plików multimedialnych. Przestrzegaj zasad serwisu źródłowego i praw do treści.",
    },
    "no": {
        "title": "VLCTube 3",
        "subtitle": "Løs nettvideo med yt-dlp og spill den direkte i VLC",
        "url": "Video- eller spilleliste-URL",
        "add": "Legg i kø",
        "paste": "Lim inn",
        "expand": "Utvid spilleliste",
        "quality": "Kvalitet",
        "vlc": "VLC Player",
        "auto_detect": "Finn automatisk",
        "browse": "Velg…",
        "queue": "Kø",
        "history": "Historikk",
        "play_selected": "Spill valgte",
        "play_all": "Spill alle",
        "remove": "Fjern",
        "clear": "Tøm kø",
        "clear_history": "Tøm historikk",
        "status_ready": "Klar",
        "invalid_url": "Skriv inn en gyldig http:// eller https:// medie-URL.",
        "no_vlc": "VLC Player ble ikke funnet. Bruk Velg for å finne vlc.exe.",
        "resolving": "Løser strøm…",
        "launched": "Åpnet i VLC: {title}",
        "added": "La til {count} element(er) i køen",
        "expanded": "Spilleliste utvidet: {count} element(er)",
        "failed": "Operasjonen mislyktes: {error}",
        "no_selection": "Velg et element i køen først.",
        "vlc_found": "VLC funnet: {path}",
        "vlc_missing": "VLC ikke funnet",
        "queued": "I kø",
        "playing": "Spiller",
        "error": "Feil",
        "about": "VLCTube strømmer gjennom VLC og laster ikke ned mediefiler. Følg kildesidens vilkår og innholdsrettigheter.",
    },
}


def detect_language() -> str:
    code = (locale.getlocale()[0] or "en").split("_")[0].lower()
    if code in {"nb", "nn"}:
        code = "no"
    return code if code in SUPPORTED else "en"


def tr(language: str, key: str, **values: object) -> str:
    table = TRANSLATIONS.get(language, TRANSLATIONS["en"])
    template = table.get(key, TRANSLATIONS["en"].get(key, key))
    return template.format(**values)
