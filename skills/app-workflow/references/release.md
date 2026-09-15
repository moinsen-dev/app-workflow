# Auslieferung und Produktionsvoraussetzungen

Version 1.1.0. Beim Planen CORE-023 und die folgende Zielmatrix lesen; Detailtabellen nur für die gewählten Kanäle laden. Das Werkzeug nimmt diese Tabellen anhand von `PLAN/Delivery` in den Katalog auf. Aktuelle Vorgaben beim konkreten Release erneut an offiziellen Quellen prüfen: Datum, geltende SDK-/Target-Anforderungen und tatsächlichen Konto-/Projektstand in der zugeordneten Aufgabe festhalten. Keine eingefrorenen SDK-Mindestversionen aus einem Beispiel übernehmen.

## Zielmatrix

| Plattform | Kanäle | Tatsächlich zu unterscheidende Ergebnisse |
|---|---|---|
| iOS | local, testflight, app-store | Simulator/Gerät; Beta für gewählte Tester; Store-Version für gewählte Regionen verfügbar |
| Android | local, direct, play-testing, google-play | Lokaler Build; signiertes APK; freigegebener Testkanal; Produktionsrollout |
| macOS | local, direct, testflight, app-store | Lokales Bundle; verteiltes Developer-ID-Paket; Beta; Mac-App-Store-Version |
| Web | local, web | Lokaler Entwicklungsserver; erreichbare Release-URL |
| Windows | local, direct, microsoft-store | Lokale App; gewähltes Installationspaket; Store-Verfügbarkeit |
| Linux | local, direct, linux-store | Lokale App; gewähltes Paket; benannter Paket-/Store-Kanal |

`Goal` bestimmt die Abschlusskriterien jeder zugeordneten Aufgabe. Bei mehreren Delivery-Zeilen dieselben Katalogpunkte je Ziel auslegen und die jeweiligen Aufgaben zuordnen:

| Goal | Erforderlicher Nachweis | Passender Release-Verweis |
|---|---|---|
| local | Vereinbarten lokalen Build im normalen Modus starten und bedienen | Lokales Artefakt oder lokale URL |
| ready | Artefakt, Konfiguration, erforderliche Konten/Signierung und Einreichungs- beziehungsweise Verteilungsunterlagen vorbereiten und prüfen; Installation/Start soweit vor Einreichung möglich testen | Lokaler Paketpfad mit eindeutiger Build-Kennung und vorbereiteten Unterlagen; Ziel-URL oder Store-Eintrag als geplant kennzeichnen |
| submitted | Zusätzlich die tatsächliche Einreichung im vorgesehenen Review-/Testkanal mit Version und beobachtetem Verarbeitungsstatus belegen | Konkrete Einreichung im Zielsystem; ein bloß erfolgreicher Upload genügt nicht |
| live | Zusätzlich Verfügbarkeit für die benannte Zielgruppe und normalen Start des ausgelieferten Builds belegen | Erreichbarer Verteilungsweg mit Version, Zielgruppe/Region und UI-Nachweis |

READY verlangt keine Einreichung im Store, Freigabe für Tester oder öffentliche Bereitstellung. Prüfungen, die erst dort möglich sind, als späteren Schritt in der Übergabe benennen; sie gehören nur bei SUBMITTED/LIVE zum aktiven Abschluss. Vorbereitende Dienste wie die Notarisierung eines direkt verteilbaren Mac-Pakets bleiben erforderlich, soweit der gewählte Weg sie braucht und die Handlung autorisiert ist. Falls echte Voraussetzungen für READY fehlen, bleibt die Aufgabe offen oder blockiert. Ein repräsentativer Release-Testbuild darf vor einer Store-Einreichung verwendet werden, wenn Unterschiede zu Signierung und Installation des finalen Pakets genau benannt werden. Er belegt keinen LIVE-Start.

LIVE bei TestFlight bezeichnet Testerzugang; es behauptet keine App-Store-Veröffentlichung. Ein lokaler Auftrag erhält keine automatischen Veröffentlichungsaufgaben; spätere Produktionsvoraussetzungen bleiben in den Entscheidungen benannt. Katalog und Zielwahl sind keine zusätzliche Befugnis für externe Aktionen; bereits erteilte Autorisierung gilt weiter.

Beispiel: `--delivery ios:testflight:live,android:google-play:ready`. Die Profile Expo und Flutter übernehmen zusätzlich die jeweils zutreffenden nativen Anforderungen. UI-Ziele wie ios-simulator und Auslieferungskanäle sind verschiedene Angaben. Für LIVE auf iOS ist ein normaler Start des ausgelieferten Builds auf ios-device vorgesehen. Bei fehlenden externen Voraussetzungen bleibt die betroffene Aufgabe offen oder blockiert; unabhängige Umsetzung läuft weiter.

## common

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| REL-001 | P01 | always | Aktuelle Voraussetzungen und verantwortliches Konto | Nichtlokaler Auslieferungsweg | Kontoinhaber, Rollen, erreichbarer Dienst, benötigte Verträge und aktuelle Toolchain-/Store-Vorgaben konkret einordnen; notwendige externe Handgriffe Aufgaben zuordnen |
| REL-002 | P05 | always | Identität und Version des Release-Artefakts | Nichtlokaler Auslieferungsweg | Anzeigename, AppID, verantwortliches Team, Version und Build mit Paket und vorbereiteten Zielangaben abgleichen; ab SUBMITTED mit tatsächlicher Einreichung abgleichen |
| REL-003 | P05 | always | Finale Icons und Startressourcen | Nichtlokaler Auslieferungsweg | Zum Ziel passende Varianten im Paket und tatsächlichen System prüfen; keine versehentlichen Default-Icons, lesbare Startdarstellung und nachvollziehbare Assetrechte |
| REL-004 | P05 | always | Rechte im erzeugten Release-Artefakt | Nichtlokaler Auslieferungsweg | Genutzte Fähigkeiten und SDK-Rechte mit zusammengeführtem Manifest, Usage Descriptions und Entitlements abgleichen; relevante erlaubte, verweigerte, eingeschränkte und entzogene Zustände bedienen |
| REL-005 | P05 | always | Tatsächliche Produktionskonfiguration | Nichtlokaler Auslieferungsweg | Richtige Dienste, Redirects, Featureflags, Push-/Kaufumgebung und sichere Secret-Bereitstellung prüfen, soweit verwendet; kein Demo-Einstieg oder versehentliches Debug-Verhalten |
| REL-006 | P05 | always | Datenangaben und erforderliche Produktinformationen | Nichtlokaler Auslieferungsweg | Tatsächliche Datenflüsse einschließlich SDKs, erforderliche Datenschutz-/Inhaltsangaben, Support-/Rechtslinks, Asset-/Abhängigkeitslizenzen und zugesagte Lokalisierung abgleichen |
| REL-007 | P05 | always | Paket, Installation und normaler Start | Nichtlokaler Auslieferungsweg | READY: Paket prüfen und lokal installierbaren Release-Build normal bedienen, Unterschiede zum späteren Store-Weg benennen; LIVE: tatsächlich ausgelieferten Build über den vorgesehenen Nutzerweg installieren und starten |
| REL-008 | P05 | conditional | Update einer vorhandenen Installation | Updates oder bestehende Nutzerdaten | Richtige Identität und Version, Migration, erhaltener Bestand und angemessener Wiederherstellungsweg tatsächlich prüfen |
| REL-009 | P05 | always | Betrieb und Rückmeldung im vereinbarten Umfang | Nichtlokaler Auslieferungsweg | Verantwortlicher Support, nutzbarer Diagnoseweg und Wiederherstellungs-/Rücknahmeweg benannt; bei Diensten Verfügbarkeit, Quoten/Kosten und Datensicherung prüfen; vorhandene Infrastruktur bevorzugen |
| REL-010 | P05 | always | Beobachteter Auslieferungszustand | Nichtlokaler Auslieferungsweg | Gemäß Goal-Tabelle READY am vorbereiteten Paket, SUBMITTED an der tatsächlichen Einreichung oder LIVE an Verfügbarkeit und normalem Nutzerstart belegen; identische Build-Kennung im Release-Eintrag und seinen Belegen verwenden |

## apple

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| APPLE-001 | P01 | always | Apple-Identität, Team und Signierung | App Store oder TestFlight | Bundle-IDs aller Targets/Erweiterungen, Team, Zertifikat, Profile und passende Capabilities zusammenführen; Angaben für App-Record vorbereiten oder bestehenden Record abgleichen; ab SUBMITTED tatsächliche Zuordnung prüfen |
| APPLE-002 | P05 | always | Apple-Ressourcen und Privacy-Manifeste | App Store oder TestFlight | Icon/Launch-Ressourcen im richtigen Target; zutreffende PrivacyInfo.xcprivacy, Required-Reason-APIs und SDK-Anforderungen im gebauten Paket prüfen |
| APPLE-003 | P05 | always | Apple-Artefakt gemäß beauftragtem Endzustand | App Store oder TestFlight | READY: Archiv/Export, Signierung, Version und aktuelle Upload-Voraussetzungen prüfen; ab SUBMITTED: Einreichung und Verarbeitung im Zielsystem belegen; Transporter/EAS-Erfolg allein genügt nicht |

Grundlage: [Apple-Distributionsvorbereitung](https://developer.apple.com/documentation/xcode/preparing-your-app-for-distribution), [Privacy-Manifeste](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files), geprüft 2026-09-15.

## app-store

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| STOREAPPLE-001 | P05 | always | App-Store-Eintrag und Review-Zugang | App-Store-Kanal | READY: passende Screenshots, Beschreibung, Kategorie/Altersangaben, Datenschutzdaten/-URL, Inhalts-/Exportangaben, Preis/Regionen und benötigten Review-Zugang vorbereiten; ab SUBMITTED mit eingereichten Angaben abgleichen; Kontolöschung/Käufe bei zutreffenden Funktionen prüfen |
| STOREAPPLE-002 | P05 | always | Tatsächlicher App-Store-Endzustand | App-Store-Kanal | READY: einreichbare Version und Materialien; SUBMITTED: nachgewiesene Review-Einreichung; LIVE: veröffentlichte Version in der Zielregion mit erreichbarem Nutzerpfad; Akzeptanz ohne Veröffentlichung getrennt benennen |

Grundlage: [App-Angaben](https://developer.apple.com/help/app-store-connect/reference/app-information/required-localizable-and-editable-properties), [Screenshots](https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots), [Datenschutzangaben](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy), geprüft 2026-09-15. Store-Pflichten sind kein Auftrag, einen Account zu erstellen oder eine rechtliche Erklärung ungeprüft abzugeben.

## testflight

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| BETAAPPLE-001 | P05 | always | TestFlight für die vorgesehene Gruppe | TestFlight-Kanal | READY: Build, Beta-Angaben, Zielgruppe und nötigen Review-Weg vorbereiten; SUBMITTED: Verarbeitung und gegebenenfalls Beta-Review-Einreichung belegen; LIVE: Gruppenfreigabe und Installation/normaler Start durch vorgesehenen Tester |

[Expo-Auslieferung](https://docs.expo.dev/deploy/submit-to-app-stores/) unterscheidet Upload, TestFlight und App-Store-Veröffentlichung ausdrücklich. Geprüft 2026-09-15.

## play

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| PLAY-001 | P01 | always | Play-Konto, Paket und Signierweg | Google Play oder Play-Testkanal | Verantwortliches Konto/Rollen, Paketname, App Signing/Upload-Schlüssel, Version und aktuelle Target-/gegebenenfalls Kontotest-Anforderungen prüfen |
| PLAY-002 | P05 | always | Play-Inhalte und Datenschutz | Google Play oder Play-Testkanal im zutreffenden Umfang | READY: Icon/Grafiken/Screenshots, Data Safety einschließlich SDKs, Datenschutzerklärung, Alters-/Werbe-/Zielgruppenangaben, sensible Permissions und benötigten Review-Zugang vorbereiten; ab SUBMITTED mit tatsächlich eingereichten Angaben abgleichen |
| PLAY-003 | P05 | always | Richtiger Play-Track und Rollout | Google Play oder Play-Testkanal | READY: Paket, Track, Tester/Länder und Rollout-Einstellungen vorbereiten; SUBMITTED: Version und Verarbeitungs-/Reviewzustand im richtigen Track belegen; LIVE: tatsächliche Verfügbarkeit und normalen Nutzerstart prüfen |

Grundlage: [Android-Release](https://developer.android.com/studio/publish/preparing), [Play-Review](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en), [Play-Rollout](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en), geprüft 2026-09-15.

## macos-direct

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| MACDIST-001 | P05 | always | Developer-ID-Verteilung | Direkte Mac-Verteilung | Signatur aller Komponenten, Hardened Runtime, Entitlements, Notarisierung, Ticket/Stapling und Gatekeeper-Verhalten am vorbereiteten Paket prüfen; LIVE zusätzlich am tatsächlich angebotenen Download belegen |
| MACDIST-002 | P05 | always | Mac-Paket und Wiederöffnung | Direkte Mac-Verteilung | Gewähltes ZIP/DMG/PKG tatsächlich installieren, normales Icon/Fenster öffnen und spätere Updates im beauftragten Umfang prüfen |

Grundlage: [Mac-Notarisierung](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), geprüft 2026-09-15. Ein lokales ad-hoc-Bundle belegt diesen Verteilungsweg nicht.

## android-direct

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| ANDROID-001 | P05 | always | Direkt verteilbares Android-Paket | Direkte Android-Verteilung | READY: signiertes installierbares APK, richtige Identität/Version/Architektur und lokalen Installationsweg mit normalem Start prüfen; LIVE zusätzlich Zugang über den angebotenen Verteilungsweg belegen; ein AAB allein ist kein direkt installierbares APK |

## web

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| WEB-001 | P05 | always | Release-URL und Web-Ressourcen | Web-Verteilung | READY: Produktionsbuild lokal oder in beauftragter Vorschau öffnen, direkte Routen/Neuladen, Ressourcen und Favicon prüfen; LIVE zusätzlich an tatsächlicher HTTPS-Origin prüfen; Manifest/installierbare Icons nur bei beauftragter PWA |
| WEB-002 | P05 | always | Browser- und Hosting-Konfiguration | Web-Verteilung | READY: passende Dienste, Auth-Redirects, Browserrechte, Domain-/TLS-Konfiguration und relevante Cache-/Service-Worker-Updates sowie Rücknahmeweg vorbereiten; LIVE an tatsächlicher Origin und Hosting-Konfiguration prüfen |

## windows

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| WIN-001 | P05 | always | Windows-Paket und Systemintegration | Windows-Verteilung | Passendes Paketformat, Publisher/Identität, Icon/Version, Laufzeitabhängigkeiten und geeignete Signatur/Vertrauensprüfung erfassen; auf Windows installieren und normal öffnen |

## microsoft-store

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| WINSTORE-001 | P05 | always | Microsoft-Store-Voraussetzungen | Microsoft-Store-Kanal | READY: Paketidentität, Publisher, aktuelle Zertifizierungsanforderungen und Partner-Center-Metadaten vorbereiten; SUBMITTED: Einreichung/Verarbeitung belegen; LIVE: Store-Zugang und normalen Start prüfen |

Grundlage: [Flutter Windows](https://docs.flutter.dev/deployment/windows), geprüft 2026-09-15.

## linux

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| LINUX-001 | P05 | always | Linux-Paket und Desktopintegration | Linux-Verteilung | Gewähltes Paketformat, Zielsystem/Architektur, Bibliotheken, Desktop-Datei/Icon und zutreffende Sandbox-Rechte prüfen; dort installieren und normal öffnen |

## linux-store

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| LINUXSTORE-001 | P05 | always | Gewählter Linux-Paketkanal | Linux-Store-Kanal | READY: konkreten Store/Repository, Publisher, Paketmetadaten, Signierung und erforderliche Prüfung für gewählten Weg vorbereiten; SUBMITTED: Einreichung/Verarbeitung belegen; LIVE: Installation aus dem Zielkanal und normalen Start prüfen |

Grundlage: [Flutter Linux](https://docs.flutter.dev/deployment/linux), geprüft 2026-09-15. Ein Build auf dem Mac ist keine Windows-/Linux-Installationsprüfung.
