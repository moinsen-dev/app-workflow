# Native macOS-App

## Reihenfolge

1. **P01 – Einordnen:** SwiftPM-/Xcode-Struktur, Bundle-Erstellung, Mindestversion, Signing, Entitlements und benötigte Mac-Berechtigungen feststellen.
2. **P02 – Starten:** Das tatsächlich vorgesehene App-Bundle bauen und öffnen. Menüleiste, Dock, Hauptfenster und normaler Einstieg müssen zum Produkttyp passen.
3. **P03 – Use Cases:** Vollständige Desktop-Abläufe mit Fenstern, Auswahl, Tastatur, Dialogen und Datenhaltung bauen. Benötigte Dateizugriffe und Systemaktionen im vereinbarten Umfang prüfen.
4. **P04 – Zusammenspiel:** Fenster schließen und wieder öffnen, App beenden und neu starten, Auswahl und laufende Vorgänge prüfen. Relevante Resize-, Fokus-, Abbruch- und Fehlerfälle bedienen.
5. **P05 – Ausliefern:** Gewählten Bundle-/Installationsweg prüfen. Signing, Notarisierung und Updates nur entsprechend dem tatsächlich vereinbarten Verteilungsziel behandeln.

Vorhandene Build-/Run-Skripte bevorzugen. Ein SwiftPM-Executable, ein App-Bundle und ein für Verteilung signiertes Artefakt sind unterschiedliche Ausführungsstände. Benötigte macOS-Rechte müssen zum konkret gestarteten Bundle passen. Persönliche Bestände und laufende Prozesse bei Prüfungen schützen; isolierte Beispieldaten nutzen, wenn sie den Ablauf hinreichend belegen.

## Identität, Ressourcen und Produktionsweg

Bundle-ID, Team/Signierung, Version/Build, App-Icon und Startdarstellung im finalen App-Bundle prüfen; SwiftPM erzeugt diese Produktressourcen nicht automatisch für jeden eigenen Bundle-Weg. Info.plist, Sandbox/Entitlements, TCC-Rechte und gegebenenfalls Privacy-Manifeste mit den genutzten APIs und SDKs abgleichen. Die Rechte gelten für die konkret gestartete App-Identität; ein anderes Debug-Bundle kann sich anders verhalten.

Lokales Bundle, Developer-ID-Verteilung, TestFlight und Mac App Store erhalten unterschiedliche Aufgaben nach [release.md](../release.md). Notarisierung, Stapling, Gatekeeper und ZIP/DMG/PKG betreffen den tatsächlich vereinbarten direkten Verteilungsweg. Für Sandbox-Dateizugriff die zugesagte Wiederöffnung von Nutzerdokumenten prüfen, wenn die App diesen Zugriff benötigt.

## Checks

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| MACOS-001 | P01 | always | Build-, Bundle- und Signing-Weg | macOS-Projekt | Tatsächlich gestartetes Artefakt und Konfiguration sind eindeutig |
| MACOS-002 | P02 | always | App-Einstieg und Fensterverhalten | macOS-Projekt | Vorgesehene Fenster-/Menüleisten-/Dock-Bedienung funktioniert |
| MACOS-003 | P03 | always | Tastatur, Fokus, Größe und Dialoge | macOS-Projekt | Relevanten Ablauf bei passenden Fenstergrößen und mit vorgesehenen Eingaben bedienen |
| MACOS-004 | P03 | conditional | Systemrechte und konkrete Aktionsziele | Datei-, System-, Accessibility- oder geschützter Zugriff | Rechte, Zielidentität, Vorschau/Abbruch und Ergebnis passen zur Aktion |
| MACOS-005 | P04 | always | Fenster schließen, App-Neustart und Wiederaufnahme | macOS-Projekt | Richtiger Bestand und verständlicher Wiederanlauf nach vollständigem Neustart |
| MACOS-006 | P05 | always | Tatsächliches Installations- und Verteilungsziel | macOS-Projekt | Vereinbartes Bundle am vorgesehenen Ort im normalen Modus öffnen |

Einzelheiten zu Bundle-Erstellung, Fensterverhalten und Toolchain im jeweiligen Checkout verifizieren.
