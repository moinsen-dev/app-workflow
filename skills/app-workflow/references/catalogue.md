# Gemeinsamer Katalog

Version: 1.1.0. `always` bedeutet: im vereinbarten Umfang abdecken. `conditional` verlangt eine explizite Entscheidung anhand der Bedingung. Ein Punkt kann mehrere Tasks benötigen; ein Task kann mehrere Punkte abdecken. Die Prüfungen CORE-019 bis CORE-023 ergänzen Version 1.0.

## Checks

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| CORE-001 | P01 | always | Nutzerziel und beobachtbare Abschlusskriterien | Jedes Projekt | Auftrag und Korrekturen sind Anforderungen und Use Cases zugeordnet |
| CORE-002 | P01 | always | Ist-Zustand, bestehende Anweisungen und Toolchain | Jedes Projekt | Relevante Dateien, Änderungen, Versionen und Startwege sind abgeglichen |
| CORE-003 | P01 | always | Zielplattformen, App-Modus und Auslieferungsziel | Jedes Projekt | Gewählte Ziele, Normal-/Demobetrieb und vereinbarter Endzustand sind eindeutig |
| CORE-004 | P01 | always | Phasen, Abhängigkeiten und Wiederaufnahme | Jedes Projekt | Vollständiger Plan und nachvollziehbarer Einstieg über AGENTS und STATE |
| CORE-005 | P02 | always | Startbare App und verständlicher Einstieg | Jedes Projekt | App auf Zielplattform öffnen und ersten Nutzerweg tatsächlich erreichen |
| CORE-006 | P03 | always | Navigation und komplette Kernabläufe | Jedes Projekt | Einstieg, Aktionen, Ergebnis und Rückweg im normalen App-Modus bedienen |
| CORE-007 | P03 | always | Leere Daten, Fehler, Abbruch und erneuter Versuch | Jedes Projekt im Umfang seiner Nutzerabläufe | Relevante Gegenfälle bedienen und sichtbare Ergebnisse prüfen |
| CORE-008 | P03 | conditional | Eingaben, Validierung und Mehrfachaktionen | Formulare oder verändernde Aktionen | Ungültige Eingabe und Doppelauslösung verursachen keine falschen Daten |
| CORE-009 | P03 | always | Verständliche, zugängliche und passende Darstellung | Jedes Projekt | Gewählte Größen, Eingabemethoden, Beschriftungen und relevante Bedienhilfen prüfen |
| CORE-010 | P03 | conditional | Datenhaltung und Wiederöffnen | Die App speichert Nutzerdaten oder Arbeitsfortschritt | Anlegen oder ändern, App beenden, neu öffnen und Inhalt prüfen; bei relevanten Lade-/Schreibfehlern vorhandenen Bestand erhalten und Wiederholung prüfen |
| CORE-011 | P03 | conditional | Offline-Verhalten und Wiederverbindung | Netzwerk oder unterbrechbare Dienste werden verwendet | Verbindungsausfall und Wiederkehr lassen Zustand nachvollziehbar |
| CORE-012 | P03 | conditional | Löschen, Rückgängig oder Wiederherstellung | Verlustbehaftete oder korrigierbare Aktionen | Vorschau oder passende Bestätigung, Abbruch und vorgesehenen Rückweg prüfen |
| CORE-013 | P03 | conditional | Datenzugriff, Geheimnisse und minimale Protokolle | Sensible Daten, Konten, externe Dienste oder Gerätezugriff | Richtiger Zugriff und relevante Verweigerung sind geprüft; Belege enthalten keine privaten Inhalte |
| CORE-014 | P03 | conditional | Daten- und Schemaänderungen | Vorhandene gespeicherte Daten ändern ihr Format | Repräsentativen Altbestand öffnen und Verlust-/Fehlerfall prüfen |
| CORE-015 | P04 | always | Zusammenhängender Nutzerablauf und unabhängige Kritik | Jedes Projekt | Frischer Ablauf über Funktionsgrenzen mit konkreter Ergebnisprüfung und dokumentiertem Kritikerurteil |
| CORE-016 | P04 | conditional | Reaktionsfähigkeit und längere Abläufe | Lange Arbeit, größere Datenmengen oder bekannte Verzögerungen | Repräsentative Last, sichtbarer Fortschritt, Abbruch und neue Eingabe prüfen |
| CORE-017 | P05 | always | Vereinbarte Installation oder Auslieferung | Jedes Projekt bis zum vereinbarten Endzustand | Exakten Startpfad und Nutzermodus des Artefakts prüfen; verbleibende externe Schritte konkret benennen |
| CORE-018 | P05 | always | Ehrlicher Abschluss und fortsetzbarer Reststand | Jedes Projekt | Alle relevanten Kriterien belegt; Grenzen, offene Aufgaben und nächster Schritt stimmen |
| CORE-019 | P01 | always | Persönliche Standards und konkrete Projektentscheidungen | Jedes Projekt | Konventionen, Grafikstil, Design-Skill, Anbieter- und GitHub-Präferenzen mit Herkunft aufgelöst; bestehende Entscheidungen berücksichtigt |
| CORE-020 | P01 | always | App-Identität und Eigentümer | Jedes Projekt | Anzeigename, Bundle-/Package-ID oder Web-Origin, Repository-Owner und Version/Build-Zuordnung am tatsächlichen Projekt abgeglichen |
| CORE-021 | P03 | always | App-Icons, Startdarstellung und Grafikressourcen | Jedes Projekt im vereinbarten Umfang | Vorgesehene Icons und Varianten im tatsächlichen Launcher, Dock oder Browser prüfen; finale Ressourcen, Herkunft und Nutzungsrechte für Auslieferung abgleichen |
| CORE-022 | P03 | always | Vollständige Berechtigungsdeklaration | Jedes Projekt einschließlich seiner SDKs | Benötigte Rechte mit Zweck, Daten, Manifest/Usage Description/Entitlements und Tasks inventarisiert; relevante Systemzustände und erzeugtes Artefakt geprüft, auch bei keiner nötigen Berechtigung |
| CORE-023 | P01 | always | Produktionsvoraussetzungen und beauftragter Endzustand | Jedes Projekt | Pro Plattform Auslieferungsweg, Konto/Rollen, Signierung, Assets, Store-Angaben und Betrieb früh einordnen; aktuelle lokale Grenze oder geplante Release-Aufgaben konkret nennen |

P01–P05 sind Ausgangsphasen. Weitere Feature-Phasen erhalten stabile IDs und eine eigene Reihenfolge. Verschobene Tasks behalten ihre IDs.
