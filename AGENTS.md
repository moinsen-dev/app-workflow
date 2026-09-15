# App-Workflow-Skill entwickeln

## Einstieg

Lies `README.md` und den relevanten Teil von `skills/app-workflow/SKILL.md`. Falls lokale Entwicklungsunterlagen `STATE.md`, `PLAN.md` und `TRACKER.md` vorhanden sind, nutze ihren aktiven Stand für die Fortsetzung. Diese optionalen Arbeitsunterlagen sind nicht Teil des veröffentlichten Pakets.

## Arbeitsregeln

- Entwickle einen portablen Skill für Expo, Flutter, natives iOS und natives macOS. Fachdetails werden nur für das gewählte Profil geladen.
- Halte Quellprojekte der Bestandsaufnahme unverändert. Übernimm daraus technische Muster und anonymisierte Erkenntnisse, keine privaten Daten oder Zugangsdaten.
- Projektartefakte bleiben Markdown. `TRACKER.md` führt den Aufgabenstatus; `STATE.md` zeigt die aktive Arbeit und den nächsten Schritt.
- Prüfe den Skill durch tatsächlich erzeugte Projekte, absichtlich beschädigte Zustände und einen praktischen Durchlauf. Zusätzliche Tests sollen konkrete Fehler erkennen.
- Unterscheide Strukturprüfung, unabhängige Verhaltensprüfung und tatsächlich bediente App. Dokumentiere den belegten Umfang.
- Öffentliche Regressionen laufen mit `python3 evals/check_workflow.py`. Das synthetische Fixture unter `evals/fixtures/legacy-v1/` prüft den älteren Vertrag, ohne einen App-Nachweis zu behaupten. Lokale frühere App-Piloten sind keine Voraussetzung für diese Tests.
- Veröffentliche keine persönlichen Profile, Zugangsdaten oder lokalen App-Protokolle. Prüfe den vorgesehenen Git-Inhalt; `.gitignore` erhält die lokalen Arbeitsunterlagen.
- Arbeite innerhalb des freigegebenen Auftrags weiter. Vorhandene Freigaben nicht wiederholt abfragen; zusätzliche externe Veröffentlichung oder Eingriffe in fremde Projekte gehören nicht automatisch dazu.

## Ablage

- `skills/app-workflow/`: installierbarer Skill mit Katalog, Profilen, Projektvorlagen und Skripten.
- `docs/VALIDATION.md`: öffentlich dokumentierter Prüfumfang und seine Grenzen; weitere lokale Entwicklungshinweise können daneben vorhanden sein.
- `evals/`: gezielte Verhaltensprüfung des Skills und seiner Werkzeuge.

Die App-Vorlagen werden in getrennten Prüfverzeichnissen erprobt. Dieser Ordner entwickelt ein Werkzeug und wird nicht künstlich als App eines der vier Profile eingestuft. Für Beiträge gilt die MIT-Lizenz in LICENSE.
