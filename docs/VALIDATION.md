# Prüfumfang und Grenzen

Der veröffentlichte Skill enthält seine Vorlagen, Referenzen, den Python-Controller und eigenständig ausführbare Regressionen. Persönliche Nutzerprofile, lokale Entwicklungsnotizen, App-Binaries und Protokolle interner App-Durchläufe sind nicht Bestandteil dieses Repositorys.

## Reproduzierbare Prüfungen

Im Repository mit Python 3.10 oder neuer ausführen:

```sh
python3 evals/check_workflow.py
```

Die 29 gezielten Fälle prüfen unter anderem:

- Erzeugung aller vier Profile; ein neuer Entwurf behauptet keine fertige Planung.
- Erhaltung vorhandener Dateien, lesende Statusaufrufe und Erkennung veralteter STATE-Dateien.
- Vollständige Anforderungen, Katalog-/Modulzuordnung, passende Prüfziele und gültige Abhängigkeiten.
- Fehlende Belege, geänderte Kriterien/Quelldateien sowie unpassende Build- oder Fixture-Nachweise.
- Persönliche Vorgaben mit Herkunft, Konfliktauflösung und unveränderte Nutzerprofile.
- Kanalabhängige Release-Anforderungen, früh erforderliche Geräteaufgaben, Identität, Build-Zuordnung und den tatsächlich erklärten Auslieferungszustand.
- Unveränderte Fingerprint-Berechnung für einen älteren Vertrag. Das fest gespeicherte [Fixture 1.0](../evals/fixtures/legacy-v1/AGENTS.md) enthält ausschließlich synthetische Daten und behauptet keinen App-Durchlauf. Seine Fingerprints bei einem Fehler nicht automatisch neu erzeugen.

Die positiven Nachweisdaten in dieser Testsuite sind synthetische Eingaben. Die Tests prüfen, welche Aussagen der Controller akzeptiert oder zurückweist; sie beweisen nicht den Wahrheitsgehalt eines geschriebenen App-Berichts.

## Paket und reale Anwendung

Vor der Erstveröffentlichung wurden das installierbare Paket und die README-Befehle in isolierten Verzeichnissen für Codex und Claude Code geprüft. Dabei wurden neue Markdown-Unterlagen erzeugt, kollidierende Bestandsdateien geschützt und lesende Statusaufrufe verglichen. Zusätzlich wurden alle acht optionalen Module mit den vier Profilen sowie die unterstützten Plattform-/Kanal-/Goal-Kombinationen erzeugt.

Während der Entwicklung fanden unabhängige Plan-/Vertragsprüfungen, die Übernahme eines bestehenden Expo-Plans und ein normal bedienter nativer Mac-Pilot statt. Die lokalen Rohprotokolle gehören nicht zur öffentlichen Testsuite; diese Aussage ersetzt keine reproduzierbare App-Abnahme. Die öffentliche Testsuite braucht keine solchen lokalen Dateien.

## Inhaltliche Abdeckung

| Bereich | Referenz |
|---|---|
| Nummerierte Phasen, Aufgaben, App-Verhalten, Icons und Rechte | [Gemeinsamer Katalog](../skills/app-workflow/references/catalogue.md) |
| Persönliche Konventionen und Herkunft | [Personalisierung](../skills/app-workflow/references/personalization.md) |
| Übernahme vorhandener Apps und Dokumentrollen | [Brownfield](../skills/app-workflow/references/brownfield.md) |
| Anmeldung, Backend, Sync, KI, Käufe, Sensoren, Push und Dateien | [Zusatzmodule](../skills/app-workflow/references/modules.md) |
| Vorbereitung, Einreichung und tatsächliche Nutzerverfügbarkeit | [Release-Katalog](../skills/app-workflow/references/release.md) |
| Nachweise, Kritiker, Fingerprints und Wiederaufnahme | [Markdown-Vertrag](../skills/app-workflow/references/format.md) |

Der Prüfer kontrolliert Struktur, erklärte Abdeckung und Aktualität der benannten Quellen. Tatsächliche Bedienung, Vollständigkeit der Dateiauswahl, native Berechtigungen, Assetqualität, Accountrechte und Store-Verfügbarkeit benötigen passende Beobachtungen am konkreten Produkt. Aktuelle Plattformvorgaben bei dessen Release erneut prüfen. Ein grüner Werkzeugtest ist kein Nachweis einer produktiv verfügbaren App.
