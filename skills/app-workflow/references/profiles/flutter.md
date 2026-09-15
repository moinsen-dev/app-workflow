# Flutter

## Reihenfolge

1. **P01 – Einordnen:** Tatsächliches Flutter-Paket, `pubspec.yaml`, Lockfile, SDK-Bindung, Zielplattformen, Flavors, Entrypoints und native Plugins prüfen.
2. **P02 – Starten:** Verfügbares Ziel bestimmen und die normale App mit passendem Flavor und Konfiguration starten. Ein abweichender Smoke-Entrypoint ist als solcher zu kennzeichnen.
3. **P03 – Use Cases:** Nutzerabläufe mit Navigation, Datenhaltung und Plattformdiensten umsetzen. Rechte und Verhalten nativer Plugins auf geeigneten Geräten prüfen.
4. **P04 – Zusammenspiel:** Komplette Abläufe, Neustart und relevante Unterbrechungen bedienen. Flutter-Widget-Ergebnisse und tatsächliches Systemverhalten getrennt belegen.
5. **P05 – Ausliefern:** Passendes Artefakt bauen, installieren und mit dem vereinbarten Entrypoint öffnen; Konfiguration und Wiederöffnen prüfen.

Typische Prüfwerkzeuge: `flutter doctor`, `flutter devices`, `flutter analyze`, `flutter run -d <ziel>` mit vorhandenen Flavors/Defines. Bestehende Integrationstests gezielt verwenden; neue nur bei konkret wiederholbarem Nutzen. Browser-Success ersetzt keine Sensor- oder Plugin-Prüfung auf dem Telefon.

## Identität, Ressourcen und Produktionsweg

Bundle-/Paketidentität, Launcher-Icons, Startressourcen und Rechte pro gewählter nativer Runner-/Plattformkonfiguration und Flavor prüfen. `pubspec.yaml` und Dart-Code allein belegen die Werte im Android-Manifest, Apple-Bundle oder Desktop-Paket nicht. Vom Plugin eingebrachte Fähigkeiten und generierte Artefakte einbeziehen; persönliche Präfix-Vorgaben überschreiben keine vorhandene AppID.

Für jedes gewählte Ziel den Kanal aus [release.md](../release.md) ergänzen: iOS/Android, Web und bei Bedarf macOS/Windows/Linux. Paketierung und echte Installation auf der jeweiligen Zielplattform prüfen; der gemeinsame Flutter-Code ersetzt diesen Schritt nicht.

## Checks

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| FLUTTER-001 | P01 | always | Paketwurzel, SDK und Plugin-Unterstützung | Flutter-Projekt | Gewählte Ziele und tatsächlich verwendete Plugins passen zusammen |
| FLUTTER-002 | P02 | always | Flavor, Entrypoint und Define-Konfiguration | Flutter-Projekt | Normaler Nutzerstart mit richtiger Dienstumgebung ist beobachtet |
| FLUTTER-003 | P03 | conditional | Native Plugins und Systemberechtigungen | Native Plugins werden verwendet | Geeignetes Ziel belegt Funktion und Verweigerung |
| FLUTTER-004 | P03 | always | Navigation, Rückweg und Zustandslebensdauer | Flutter-Projekt | Nutzerwechsel zwischen Ansichten und App-Neustart ergeben vorgesehenen Zustand |
| FLUTTER-005 | P04 | always | Zielplattformgerechte Ablaufprüfung | Flutter-Projekt | Beobachtete Nutzeraktionen auf allen vereinbarten Zielen |
| FLUTTER-006 | P05 | always | Richtiger Build und installierter Startweg | Flutter-Projekt | Artefakt des gewählten Flavors startet den zugesagten Modus |

Quelle: [Flutter Integration Tests](https://docs.flutter.dev/testing/integration-tests), geprüft 2026-09-15.
