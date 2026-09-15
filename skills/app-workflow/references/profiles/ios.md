# Native iOS-App

## Reihenfolge

1. **P01 – Einordnen:** Xcode-Projekt beziehungsweise Generatorquelle, Scheme, Deployment Target, Paketabhängigkeiten und gewählte Simulator-/Geräteziele feststellen. Bestehende Signing-Konfiguration verwenden.
2. **P02 – Starten:** Gewähltes Scheme bauen und die App auf dem vorgesehenen Ziel über den normalen Einstieg öffnen. Startargumente, lokale Stores und Fixture-Dienste benennen.
3. **P03 – Use Cases:** Native Nutzerabläufe einschließlich Navigation, Daten, Zugriffsrechten und Zustandswechseln umsetzen. Verfügbarkeit genutzter Apple-Fähigkeiten und benötigte Fallbacks prüfen.
4. **P04 – Zusammenspiel:** App beenden und neu starten, relevante Rechte verweigern oder ändern, Kernablauf erneut bedienen. Hardwareabhängige Aussagen auf geeignetem physischen Gerät prüfen.
5. **P05 – Ausliefern:** Vereinbartes Bundle installieren beziehungsweise vorbereiteten Distributionsweg ausführen. Bundle, Scheme, Modus und tatsächlichen Nutzerpfad beim Hand-off festhalten.

Vorhandene Build-/Run-Skripte oder verfügbare Xcode-Werkzeuge nutzen. Beispielsweise `xcodebuild -list` zur Erkundung und `xcrun simctl list devices available` zur Zielauswahl. Ein bereits gewähltes Gerät weiterverwenden. Systemdialoge und Hardwareverhalten brauchen einen passenden Prüfweg; reine Simulator-Demos belegen nur ihren ausgeführten Umfang.

## Identität, Ressourcen und Produktionsweg

Bundle-IDs aller Targets/Erweiterungen, Team, Version/Build, Asset-Catalog/AppIcon, Startdarstellung, Info.plist-Werte und Entitlements am tatsächlich gebauten Target prüfen. Usage Descriptions lokalisieren, soweit Produktsprachen dies erfordern; benötigte Privacy-Manifeste und SDK-Deklarationen einbeziehen. Erlauben, Verweigern und nachträglichen Entzug relevanter Rechte im normalen Ablauf prüfen.

Lokalen Simulator-/Gerätestart, TestFlight und App Store nach [release.md](../release.md) unterscheiden. Ein LIVE-Ziel plant bereits vor Implementierungsbeginn eine zugeordnete normale Prüfung auf ios-device ein. Ein fehlendes Gerät blockiert diesen Nachweis und wird als konkrete Aufgabe sichtbar.

## Checks

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| IOS-001 | P01 | always | Projektquelle, Scheme und Zielkompatibilität | iOS-Projekt | Build-Einstieg und gewählte OS-/Geräteziele sind eindeutig |
| IOS-002 | P02 | always | Normalstart und isolierter Prüfbestand | iOS-Projekt | Startargumente und Datenquelle passen zum behaupteten App-Modus |
| IOS-003 | P03 | conditional | Berechtigungen und Verfügbarkeit nativer Fähigkeiten | Geschützte oder bedingt verfügbare Apple-APIs | Erlauben, Verweigern und Fallback auf passendem Ziel prüfen |
| IOS-004 | P03 | always | Navigation, Eingabe und Lebenszyklus | iOS-Projekt | Rückweg, Eingabe, relevante Größen und Wiederaufnahme bedienen |
| IOS-005 | P04 | conditional | Simulator-/Gerätegrenze | Benötigtes Verhalten ist im Simulator nicht hinreichend prüfbar | Benanntes physisches Ziel und tatsächlich beobachteter Ablauf |
| IOS-006 | P05 | always | Bundle und konkreter Nutzerstart | iOS-Projekt | Richtiges Artefakt öffnet vorgesehenen normalen Einstieg |

Quelle: [Apple: Simulierte und physische Geräte](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices), geprüft 2026-09-15.
