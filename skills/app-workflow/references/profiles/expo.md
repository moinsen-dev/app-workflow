# Expo

## Reihenfolge

1. **P01 – Einordnen:** `package.json`, Lockfile, App-Konfiguration, vorhandene native Verzeichnisse, SDK-Linie, Provider-Modi und bestehende Projektregeln prüfen. iOS, Android und Web als tatsächlich gewählte Ziele festhalten.
2. **P02 – Starten:** Passenden Development Build beziehungsweise vorhandenen Startweg wählen. Native Fähigkeiten und Konfiguration bestimmen die Laufzeit. App über den normalen Einstieg öffnen; Backend-Erreichbarkeit vom gewählten Ziel prüfen.
3. **P03 – Use Cases:** Navigation, Daten und native Integrationen je vollständigem Nutzerablauf bauen. Tastatur, Insets, Zurück-Navigation und vorhandene Deep Links im betroffenen Ablauf prüfen.
4. **P04 – Zusammenspiel:** Kernablauf, Wiederöffnen, relevante Netzfehler und Gegenfälle auf den vereinbarten Plattformen bedienen. Kritiker mit Nutzerauftrag und aktuellen Belegen einsetzen.
5. **P05 – Ausliefern:** Vereinbarten lokalen oder verteilten Build mit richtigem Profil, Kanal und Provider-Modus öffnen. Updates auf ihre tatsächlich passende native Laufzeit prüfen, wenn Updates zum Produkt gehören.

Vorhandene Skripte verwenden. Typische Einstiegspunkte sind `npx expo start --dev-client` und `npx expo run:ios`/`run:android`; zuerst deren Eignung für den Checkout prüfen. Native Verzeichnisse und manuelle Änderungen vor einer Regenerierung untersuchen. Kein pauschales `prebuild --clean` oder Versionsupgrade als Initialisierungsschritt.

## Identität, Ressourcen und Produktionsweg

App-Konfiguration und deren tatsächliche Auswertung prüfen: `ios.bundleIdentifier`, `android.package`, Besitzer/Projektzuordnung, Anzeigename, Icons und Startressourcen. Config-Plugins und native SDKs können Rechte hinzufügen; maßgeblich sind das erzeugte Android-Manifest beziehungsweise Info.plist/Entitlements des gewählten Builds. Geänderte native Berechtigungen oder Ressourcen benötigen den passenden neuen Build; ein JS-Update belegt ihre Übernahme nicht. Bei vorhandenen nativen Verzeichnissen deren Rolle als Quelle oder Generat beachten.

Für iOS, Android und gegebenenfalls Web jeweils einen eigenen Delivery-Weg anhand von [release.md](../release.md) planen. EAS-Build und EAS-Submit sind einzelne Schritte; Testerzugang und Store-Verfügbarkeit separat belegen. Details zu [Expo Permissions](https://docs.expo.dev/guides/permissions/), geprüft 2026-09-15.

## Checks

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| EXPO-001 | P01 | always | SDK, Abhängigkeiten und native Projektquelle | Expo-Projekt | Manifest, Lockfile, bewusste Pins und Generierungsweg stimmen zusammen |
| EXPO-002 | P02 | always | Laufzeit für tatsächlich benötigte native Funktionen | Expo-Projekt | Gewählter Client kann die benötigten Module und Konfiguration ausführen |
| EXPO-003 | P02 | always | Richtiger App- und Provider-Modus | Expo-Projekt | Normalen Startweg und sichtbares Zielsystem prüfen |
| EXPO-004 | P03 | always | Mobile Bedienung und Navigation | Expo-Projekt | Eingabe, Tastatur, Insets und Rückweg auf gewählten mobilen Zielen; bei reinem Web entsprechend im Browser |
| EXPO-005 | P03 | conditional | Deep Links und Rückkehr aus externen Abläufen | Links, Login oder externe App-Wechsel | Kalt-/Warmstart landen mit richtigem Zustand am vorgesehenen Ort |
| EXPO-006 | P05 | conditional | Build-Profil und Update-Kompatibilität | Verteilung oder Updates im Auftrag | Artefakt und Runtime passen zum vorgesehenen Ziel |

Quelle: [Expo Development Builds](https://docs.expo.dev/develop/development-builds/introduction/), geprüft 2026-09-15.
