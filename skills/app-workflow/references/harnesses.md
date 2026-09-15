# Harness-Anbindung

Gemeinsame Arbeitsanweisungen liegen in `AGENTS.md`; Plan und Tracker bleiben von einer Sitzung unabhängig. Der Skill ergänzt die vorhandenen Fähigkeiten des tatsächlich laufenden Harnesses.

## Einstieg

- **Codex:** Skill aus einem unterstützten Skill-Verzeichnis laden. Die erzeugte `AGENTS.md` verweist auf State und den konkreten Arbeitsablauf. Vorhandene native Goal-Werkzeuge nur verwenden, wenn der Nutzer ein aktives Goal anlegen lassen möchte; ein Goal im Projektplan allein startet keinen Hintergrundlauf.
- **Claude Code:** Bei Bedarf `CLAUDE.md` mit einer Zeile `@AGENTS.md` erzeugen oder diesen Import gezielt in eine bestehende Datei integrieren. Die [offizielle Anleitung](https://code.claude.com/docs/en/memory#agentsmd) beschreibt diesen gemeinsamen Einstieg. Vorhandene Claude-spezifische Regeln erhalten.
- **Andere Harnesses:** Tatsächlich dokumentierten Einstieg verwenden und auf dieselben Projektanweisungen verweisen. Unterstützung von Skills bedeutet noch keine identischen Loop-/Goal-/Review-Funktionen.

## Ausführung

1. Verfügbare Funktionen aus Werkzeugen oder aktueller CLI-Hilfe ermitteln; keine erfundenen Slash-Befehle.
2. Ein natives Goal an das konkrete vereinbarte Ergebnis und seine Abschlusskriterien binden, sofern dessen Anlage beauftragt ist.
3. Im aktiven Lauf nach jedem belegten Schritt fortsetzen. Echte Hintergrundfortsetzung braucht eine vorhandene, eingerichtete Harness-Funktion und entsprechende Autorisierung.
4. Für Kritik einen unabhängigen Agenten verwenden, wenn verfügbar und erlaubt. Auftrag, relevante Kriterien, Ist-Zustand und Rohbelege geben; keine gewünschte Bewertung vorgeben.
5. Fehlt eine Funktion, den ausführbaren Teil mit Markdown-Fortsetzung erledigen. Ein fehlendes UI-Werkzeug ist eine konkrete Prüflücke; es verwandelt einen Build nicht in eine UI-Abnahme.

## Lokale Nutzung und Verteilung

Der Ordner mit `SKILL.md`, `references/`, `assets/` und `scripts/` ist die gemeinsame Quelle. Die [Vercel-Skills-CLI](https://github.com/vercel-labs/skills) kann solche Skills aus einem lokalen Verzeichnis installieren. Vorhandene Installationen zuerst prüfen, Ziel-Harnesses gezielt auswählen. Kein pauschales Installieren in alle Harnesses.

Eine Installation und ein gültiges Skill-Manifest belegen Erkennung und Struktur. Die praktische Anwendung wird gesondert durch eine neue Sitzung beziehungsweise einen unabhängigen Agenten und einen fortgesetzten Nutzerablauf geprüft.
