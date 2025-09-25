# LogLoom

LogLoom ist ein leichtgewichtiges Kommandozeilenwerkzeug, das unterschiedliche Logformate einliest, parst und mit hilfreichen Analysen aufbereitet. Der Fokus liegt auf einfacher Bedienbarkeit, modularem Aufbau und klar strukturierten Ausgaben, damit du dich schnell in unbekannten Logdateien zurechtfindest.

## Inhalt
- [Schnellstart](#schnellstart)
- [Lokale Installation als CLI](#lokale-installation-als-cli)
- [Verzeichnisstruktur](#verzeichnisstruktur)
- [Programmablauf](#programmablauf)
- [Kommandozeilenoberfläche](#kommandozeilenoberflche)
- [Parser-Architektur](#parser-architektur)
- [Hilfsfunktionen & Analysen](#hilfsfunktionen--analysen)
- [Erweiterbarkeit](#erweiterbarkeit)
- [Nächste Schritte für Einsteiger:innen](#nächste-schritte-für-einsteigerinnen)
- [Beitrag leisten](#beitrag-leisten)
- [Lizenz](#lizenz)

## Schnellstart

```bash
# Repository klonen
git clone https://github.com/<dein-account>/LogLoom.git
cd LogLoom

# Beispiel: Apache-Zugriffslog im Common Log Format analysieren
python app/main.py --file-path pfad/zur/access.log --format clf
```

Während der Analyse kannst du interaktiv auswählen, welche Felder angezeigt oder welche Auswertungen ausgeführt werden sollen.

## Lokale Installation als CLI

LogLoom benötigt nur eine Standard-Python-Installation (ab Version 3.9). So richtest du das Tool als CLI in deiner Umgebung ein:

1. **Virtuelle Umgebung anlegen (optional, aber empfohlen):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   ```
2. **Abhängigkeiten installieren:**
   Das Projekt kommt ohne zusätzliche Pakete aus, daher reicht es, das Repository verfügbar zu machen.
3. **CLI-Befehl einrichten:**
   Lege ein kleines Wrapper-Skript oder Alias an, das auf `app/main.py` verweist. Beispiel für Unix-Shells:
   ```bash
   echo "alias logloom='python /pfad/zu/LogLoom/app/main.py'" >> ~/.bashrc
   source ~/.bashrc
   ```
   Anschließend kannst du LogLoom überall mit `logloom --help` aufrufen. Unter Windows funktioniert das analog über die PowerShell-Profil-Datei.

> Tipp: Wenn du lieber direkt einen Befehl erzeugen möchtest, kannst du das Repository in einen Ordner legen, der bereits in deinem `PATH` liegt, und eine ausführbare Datei mit dem Inhalt `python /pfad/zu/LogLoom/app/main.py %*` (Windows) bzw. `python /pfad/zu/LogLoom/app/main.py "$@"` (Unix) anlegen.

## Verzeichnisstruktur

```
LogLoom/
├── app/
│   ├── main.py          # Einstiegspunkt der Anwendung
│   ├── cli.py           # Interaktive Kommandozeilenlogik
│   ├── output_cli.py    # Formatierte Konsolen-Ausgaben
│   ├── utils.py         # Hilfsfunktionen für Analyse und Statistik
│   └── parsers/         # Sammlung format-spezifischer Parser
├── README.md            # Diese Dokumentation
└── LICENSE              # Projektlizenz
```

## Programmablauf

1. **Start** – `app/main.py` ruft `parse_arguments()` auf, entscheidet zwischen reinem Anzeigen und vollständigem Parsen und validiert Eingaben.
2. **Verarbeitung** – `parsers_util.process_log_file()` liest die Datei zeilenweise, entfernt ANSI-Steuerzeichen, matcht reguläre Ausdrücke oder JSON-Strukturen und normalisiert Zeitstempel.
3. **Interaktive Analyse** – `cli.user_interaction()` bietet dir im Terminal Auswahlmenüs, um Felder anzeigen zu lassen, Analysen zu starten oder erneut durch die Daten zu navigieren.

Fehler (fehlende Datei, ungültiger Wert) werden abgefangen und verständlich ausgegeben, damit du schnell korrigieren kannst.

## Kommandozeilenoberfläche

- `parse_arguments()` definiert Dateipfad, Format (CLF, Syslog, Systemd, JSON) und einen Schalter zum reinen Ausgeben (`--print`).
- `user_interaction()` listet verfügbare Felder, validiert Eingaben und stellt Tabellen mit dynamischer Spaltenbreite dar – ideal für große Logfiles.

## Parser-Architektur

Alle Parser erben von `BaseParser` und bringen ihren eigenen regulären Ausdruck bzw. JSON-Parser mit.

- **`parsers_util.get_parser_for_format()`** liefert je nach CLI-Argument den passenden Parser.
- **Zeitstempel-Normalisierung:** `convert_to_standard_timestamp()` führt Datumsangaben in ein einheitliches Format über.
- **Unterstützte Formate:**
  - **CLFParser** – Für Apache/Nginx-Access-Logs, inkl. Mehrfach-Datumsformaten und Analysen zu Statuscodes oder IPs.
  - **SyslogParser** – Extrahiert PRI, Timestamp, Hostname etc. aus klassischen Syslog-Meldungen.
  - **SystemdJournalParser** – Erkennt typische Systemd-Zeilen, inklusive optionaler PID, und bietet Analysen nach Host, Service, PID oder Zeitbereichen.
  - **JSONParser** – Liest jede Zeile als JSON, normalisiert Zeitfelder und ignoriert ungültige Einträge; Analysen umfassen Log-Level oder Services.

Neue Formate lassen sich hinzufügen, indem du einen weiteren Parser definierst und ihn in `get_parser_for_format()` registrierst.

## Hilfsfunktionen & Analysen

`app/utils.py` bündelt wiederverwendbare Bausteine:

- Dateiverarbeitung über Generatoren (`read_log_file`, `count_lines_in_file`).
- Begrüßungstext und Menüführung (`print_greeting`, `user_interaction`).
- Statistische Auswertungen wie Wertebereiche, Zeitdifferenzen oder Häufigkeiten.
- `analyze_log_data()` ordnet diese Funktionen den vom Parser gelieferten Analysekonfigurationen zu und bereitet die Ergebnisse für `output_cli.py` auf.

`app/output_cli.py` sorgt anschließend für eine gut lesbare Darstellung der Resultate – von Häufigkeitslisten bis zu Zeitintervallen.

## Erweiterbarkeit

1. Parser-Datei im Ordner `app/parsers/` anlegen (idealerweise auf Basis von `BaseParser`).
2. Deinen Parser in `parsers_util.get_parser_for_format()` registrieren.
3. Optional eine `analysis_config` definieren, um neue Auswertungen anzubieten.

Damit bleibt LogLoom modular und lässt sich schnell an neue Logquellen anpassen.

## Nächste Schritte für Einsteiger:innen

- **Python-Grundlagen vertiefen:** Besonders `argparse`, Module und Generatoren werden hier intensiv genutzt.
- **Reguläre Ausdrücke üben:** Für strukturierte Textlogs unverzichtbar.
- **Eigene Analysen schreiben:** Ergänze in `utils.py` neue Auswertefunktionen und binde sie über die Analysekonfiguration ein.
- **Neue Parser bauen:** Übe dich daran, weitere Logformate zu unterstützen und in den CLI-Workflow einzubetten.

## Beitrag leisten

Beiträge sind willkommen – ob Dokumentationsverbesserung, neue Parser oder zusätzliche Analysefunktionen. Erstelle einfach einen Pull Request oder melde dich über Issues.

## Lizenz

LogLoom steht unter der [MIT-Lizenz](LICENSE).
