# Fränkische Schweiz – Veranstaltungskalender

Eine datenschutzfreundliche Web-App, die täglich um 8:00 Uhr automatisch
Veranstaltungen von fraenkische-schweiz.com abruft und als iCal-Downloads
anbietet.

## Features

- **Täglicher Datenabruf** via GitHub Actions (08:00 Uhr MEZ)
- **Kein Tracking, keine Cookies, keine Nutzerdaten** (Play Store / App Store konform)
- **iCal-Download** pro Veranstaltung oder als Monatspaket mit Kategoriefilter
- **Suche & Filter** nach Kategorie und Monat
- Dark-Mode-Unterstützung

## Setup

### 1. Repository erstellen

```bash
git clone <dieses-repo>
cd fraenkische-events
```

### 2. Anthropic API Key hinterlegen

Im GitHub Repository unter **Settings → Secrets and variables → Actions**
einen neuen Secret anlegen:

| Name | Wert |
|------|------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` |

### 3. GitHub Pages aktivieren

Unter **Settings → Pages**:
- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/public`

Die App ist dann erreichbar unter:
`https://<dein-username>.github.io/<repo-name>/`

### 4. Ersten Abruf manuell starten

Unter **Actions → Fetch Events Daily → Run workflow** den Workflow
manuell anstoßen, um sofort Daten zu erhalten.

Ab dann läuft der Abruf jeden Morgen automatisch um 08:00 Uhr MEZ.

## Dateistruktur

```
.
├── .github/
│   └── workflows/
│       └── fetch-events.yml   ← GitHub Action (tägl. 8 Uhr)
├── scripts/
│   └── fetch_events.py        ← Python-Skript für den Datenabruf
└── public/
    ├── index.html             ← Web-App
    └── data/
        └── events.json        ← Automatisch aktualisierte Daten
```

## Datenschutz

- Die App liest ausschließlich die statische `events.json` Datei
- Keinerlei Nutzerdaten werden erfasst oder übertragen
- Keine Cookies, kein LocalStorage, kein Analytics
- Keine externen Tracker oder Werbenetze
- Fonts werden von Google Fonts geladen (optional: lokal hosten für vollständige Unabhängigkeit)

## Lokale Entwicklung

```bash
# Einfacher lokaler Server
python3 -m http.server 8080 --directory public
# → http://localhost:8080
```

## Abhängigkeiten

- Python 3.12+
- `anthropic` Python-Paket (nur für den Fetch-Skript)
- Keine JS-Abhängigkeiten in der App selbst
