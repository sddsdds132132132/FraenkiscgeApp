"""
fetch_events.py
Fetches events from fraenkische-schweiz.com via Anthropic API (web search)
and saves them to public/data/events.json
"""

import anthropic
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "public" / "data" / "events.json"

PROMPT = """Bitte besuche die Webseite https://www.fraenkische-schweiz.com/erleben/veranstaltungen
und extrahiere ALLE Veranstaltungen, die du findest — auch zukünftige Monate.

Gib die Ergebnisse NUR als reines JSON zurück (kein Markdown, keine Backticks, kein Kommentar davor oder danach).
Format:
{
  "events": [
    {
      "title": "Titel der Veranstaltung",
      "date_start": "YYYY-MM-DD",
      "date_end": "YYYY-MM-DD oder null",
      "time": "HH:MM oder null",
      "location": "Ort oder null",
      "category": "Kategorie oder null",
      "description": "Kurzbeschreibung oder null",
      "url": "https://... vollständige URL oder null"
    }
  ]
}

Wichtig: Extrahiere so viele Veranstaltungen wie möglich. Gib wirklich NUR JSON zurück, absolut nichts anderes."""


def fetch_events() -> list[dict]:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": PROMPT}],
    )

    # Collect all text blocks
    text = "".join(b.text for b in response.content if hasattr(b, "text"))

    # Strip markdown fences if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    # Find JSON boundaries
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON found in response: {text[:300]}")

    parsed = json.loads(text[start:end])
    return parsed.get("events", [])


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Fetching events...")

    try:
        events = fetch_events()
    except Exception as e:
        print(f"ERROR fetching events: {e}", file=sys.stderr)
        sys.exit(1)

    if not events:
        print("WARNING: No events returned. Keeping existing data.")
        sys.exit(0)

    # Add numeric IDs
    for i, ev in enumerate(events):
        ev["id"] = i

    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(events),
        "events": events,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"Saved {len(events)} events to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
