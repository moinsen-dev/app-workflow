# Projektplan

## Project

- schema: app-workflow/1
- profile: {{PROFILE}}
- template_version: 1.1.0
- targets: {{TARGETS}}
- goal: {{GOAL}}

## Personalization

{{PERSONALIZATION}}

## Delivery

{{DELIVERY}}

## Requirements

| ID | Outcome |
|---|---|
| R001 | {{GOAL}} |

## Phases

| ID | Order | Outcome | Depends |
|---|---|---|---|
| P01 | 1 | Auftrag, Umfang und ausführbarer Plan | - |
| P02 | 2 | Startbare App auf den gewählten Zielen | P01 |
| P03 | 3 | Vollständige Nutzerabläufe | P02 |
| P04 | 4 | Geprüftes Zusammenspiel und Gegenfälle | P03 |
| P05 | 5 | Vereinbarte Auslieferung und Abschluss | P04 |

## UseCases

| ID | Phase | Outcome | Requirements | Review |
|---|---|---|---|---|
| UC01 | P01 | Anforderungen und vollständigen Ablauf konkretisieren | R001 | required |

## Tasks

| ID | Phase | UseCase | Requirements | Accept | Verify | Mode | Depends | Files |
|---|---|---|---|---|---|---|---|---|
| T001 | P01 | UC01 | R001 | Katalog eingeordnet, alle Anforderungen konkreten Aufgaben und Kriterien zugeordnet, Plan auf Vollständigkeit geprüft | inspection | any | - | - |

## Modules

{{MODULES}}

## Checklist

{{CHECKLIST}}

## Entscheidungen

Persönliche Vorgaben anhand Auftrag, vorhandenen Projektentscheidungen und benanntem Nutzerprofil auflösen. Bewusst fehlende Präferenz als NONE mit Herkunft und Begründung erfassen. Bestehende Identifier und Remotes mit ihren tatsächlichen Quellen festhalten; keine fremden Zugangsdaten oder vollständigen privaten Profilinhalte übernehmen.

Pro Plattform den Auslieferungskanal und beauftragten Endzustand eintragen: local, ready, submitted oder live. AppID ist die tatsächliche Bundle-/Paketidentität oder Web-Origin; Owner nennt den verantwortlichen Eigentümer und das nötige Konto/Team ohne Geheimnisse. Die zugeordneten Tasks behandeln frühe Voraussetzungen und den konkreten Endzustand.

Produktionsvoraussetzungen auch bei lokalem Auftrag sichtbar einordnen: Was wird später für Identität, finale Assets, Permissions, Signierung, Store-Angaben und Betrieb benötigt? Nur beauftragte Auslieferungsarbeit ausführen; lokale Fertigstellung ist keine Produktionsfreigabe.

Die Initialisierung liefert einen Planungsstand; vor dem App-Bau Use Cases und Tasks vervollständigen. Zusätzliche Phasen bekommen stabile IDs und eine passende Order/Depends-Zuordnung.

## Permissions

Benötigte Fähigkeiten einschließlich eingebundener SDKs erfassen: konkreter Zweck, betroffene Daten, Plattform, Manifest-/Usage-Description-/Entitlement-Quelle und zugeordnete Prüfaufgabe. Bei keiner benötigten Berechtigung den Abgleich mit Abhängigkeiten und erzeugtem Artefakt dokumentieren. Erwartete Deklaration und tatsächlicher Systemdialog sind getrennte Nachweise.
