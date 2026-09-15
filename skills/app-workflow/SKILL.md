---
name: app-workflow
description: Plane, implementiere und setze Expo-, Flutter-, native iOS- oder macOS-Apps mit persönlichen Vorgaben, nummerierten Checklisten, Markdown-Status und Kritiker-Schleifen fort. Nutze dies für neue Apps (Greenfield), die ausdrückliche Übernahme bestehender Apps (Brownfield) und die Fortsetzung ihres vereinbarten Auslieferungsziels.
---

# App Workflow

Führe das vereinbarte App-Ziel anhand eines passenden Templates bis zum überprüften Ergebnis. Das Template erinnert an wiederkehrende Arbeit; der Nutzerauftrag bestimmt Inhalt und Umfang. Bei reiner Planung endet der Auftrag mit dem vollständigen Plan, bei Umsetzung setzt du ihn ohne Routinefreigabe um.

## 1. Einstieg bestimmen

Den Einstieg aus Auftrag und tatsächlichem App-Bestand ableiten:

| Situation | Vorgehen |
|---|---|
| Neue App (Greenfield) | Ziel, Plattform und persönliche Vorgaben konkretisieren; neue Projektunterlagen erzeugen und die beauftragte App aufbauen |
| Bestehende App ohne diesen Workflow (Brownfield) | [Bestand übernehmen](references/brownfield.md): bisherigen Stand belegen, vorhandene Dokumentrollen integrieren und nur beauftragte Änderungen sowie dafür nötige Lücken bearbeiten |
| Vorhandener App-Workflow | AGENTS/STATE mit dem Checkout abgleichen und innerhalb des bestehenden Auftrags fortsetzen; bei einer neuen Änderung den betroffenen Plan erweitern |
| Nur Status angefragt | Unterlagen und tatsächlichen Stand lesend abgleichen; Ergebnis und nächsten Schritt nennen, ohne zu initialisieren, State zu schreiben oder Umsetzung zu starten |

Greenfield/Brownfield beschreiben den Ausgangsbestand. Ob nur geplant oder auch implementiert wird, bestimmt separat der Nutzerauftrag. Ein vorhandener Git-Ordner oder eine README allein machen ein Projekt noch nicht zur bestehenden App. Bei mehreren Apps das beauftragte Paket als Arbeitswurzel bestimmen.

1. Vorhandene Projektanweisungen, Arbeitsstand, relevanten Code und Änderungen lesen. Nutzerkorrekturen gelten für das aktive Ziel.
   Persönliche Konventionen, Grafikstil, verfügbare Design-Skills, Identifier- und GitHub-Defaults anhand [Personalisierung](references/personalization.md) auflösen. Einen bekannten Profilpfad verwenden; wirksame Vorgaben samt Herkunft im Projekt festhalten. Bestehende App-Identitäten und Repository-Eigentümer anhand aktueller Dateien prüfen.
2. Profil aus Auftrag und Manifesten bestimmen: `expo`, `flutter`, `ios` oder `macos`. Gewählte Ziele konkret benennen: `web`, `android`, `ios-simulator`, `ios-device`, `macos`; Flutter unterstützt zusätzlich `windows` und `linux`. Ein mehrdeutiges Projekt anhand des beauftragten App-Pakets eingrenzen.
3. Nur das passende Plattform-Template laden: [Expo](references/profiles/expo.md), [Flutter](references/profiles/flutter.md), [iOS](references/profiles/ios.md) oder [macOS](references/profiles/macos.md). Dazu den [gemeinsamen Katalog](references/catalogue.md) und die Entscheidungstabelle der [Zusatzmodule](references/modules.md) lesen. Detailchecks eines Moduls nur bei Bedarf verwenden.
4. Vorhandene Harness-Fähigkeiten feststellen: Ziele, Fortsetzung, unabhängige Kritik und tatsächliche App-Bedienung. Nutze verfügbare native Funktionen innerhalb bestehender Autorisierung. Erfinde keine `/goal`-/`/loop`-Befehle oder Hintergrundausführung. Einzelheiten: [Harness-Anbindung](references/harnesses.md).
5. Pro Plattform den beauftragten Auslieferungsweg bestimmen. Die [Release-Zielmatrix](references/release.md) und nur passende Kanäle lesen. Produktionsvoraussetzungen früh sichtbar machen: Konten/Rollen, reale Identität, Icons, Permissions, Signierung, Metadaten und Betrieb. Ein lokaler Auftrag endet weiterhin lokal; bei beauftragter Veröffentlichung diese bis zum tatsächlichen Zielzustand ausführen.

## 2. Projektunterlagen erzeugen oder integrieren

Bei neuen Arbeitsunterlagen den Generator aus diesem Skill verwenden; `SKILL_DIR` bezeichnet den tatsächlich geladenen Skillordner:

```sh
python3 "$SKILL_DIR/scripts/workflow.py" init /absoluter/projektpfad \
  --profile expo --targets ios-simulator,android \
  --goal 'Das konkrete vereinbarte Nutzerziel' --modules auth,sync --claude
```

Argumente aus dem Auftrag ableiten; die Beispielmodule sind keine Vorgabe. `--claude` erzeugt eine kleine `CLAUDE.md`, die `AGENTS.md` importiert. Das Werkzeug benötigt Python 3.10+ und keine Zusatzpakete.

Optional `--user-profile /pfad/USER_PROFILE.md` sowie beispielsweise `--delivery ios:testflight:live,android:google-play:ready` angeben; für iOS LIVE die Ziele im Beispiel um ios-device ergänzen. Ohne Wahl bleiben die Auslieferungswege offen; der Generator verkürzt einen unklaren Auftrag nicht stillschweigend auf einen lokalen Build. `profile /pfad/USER_PROFILE.md` erzeugt ein wiederverwendbares Profil ohne Überschreiben bestehender Dateien.

Bestehende AGENTS-/Plan-/Statusdateien zuerst lesen. Bei Brownfield nach der [Bestandsübernahme](references/brownfield.md) vorgehen. Bei Namenskonflikten in einem separaten Verzeichnis einen Entwurf erzeugen und die vorhandenen Rollen gezielt integrieren. Das Werkzeug überschreibt sie nicht. Ein ungeeignetes Altschema nicht einfach umetikettieren; Inhalte und Nachweise nachvollziehbar zuordnen. Noch notwendige Migration vollständig innerhalb des autorisierten Umfangs erledigen.

Die Initialisierung ist ein Planungsstand. **Danach den Plan konkretisieren:**

- Ursprünglichen Auftrag und spätere Korrekturen in stabile Anforderungen zerlegen.
- Personalization-Werte mit Herkunft und Begründung konkretisieren. UNKNOWN und CONFLICT vor dem betroffenen App-Bau auflösen; NONE ist eine bewusste fehlende Präferenz. Persönliche Defaults erteilen keine externe Befugnis und ändern vorhandene Identitäten nicht automatisch.
- Beobachtbare Use Cases, Aufgaben, Abschlusskriterien und Abhängigkeiten formulieren. Ganze Nutzerabläufe je Feature-Phase bauen; Reihenfolge separat von stabilen IDs führen.
- Jeden Katalogpunkt und jedes Modul als `YES`, `NO` mit konkreter Begründung oder `UNKNOWN` einordnen. Relevante Punkte Aufgaben zuordnen. `always`-Punkte im vereinbarten Umfang abdecken.
- Ausgewählte Module vollständig aufnehmen. `catalog --profile ... --modules ...` zeigt die erwarteten Checks. Neue Produktanforderungen auch dann einplanen, wenn der Katalog sie nicht nennt.
- Alle tatsächlichen Prüfziele und den App-Modus pro Aufgabe festlegen. Pro gewähltem Ziel mindestens einen vollständigen normalen UI-Nutzerablauf einplanen. Zusätzlich nötige Hardware- oder Live-Prüfung ausdrücklich zuordnen.
- Delivery pro Plattform mit Kanal, Endzustand, AppID, zuständigem Eigentümer/Konto und Tasks planen. `catalog --profile ... --delivery ...` ergänzt die passenden Release-Checks. AppID/Owner dürfen während der Vorbereitung offen sein, wenn ihre Klärung konkret eingeplant ist; vor Abschluss müssen sie feststehen.
- App-Icons/Varianten, Startdarstellung und Assetherkunft konkret prüfen. Berechtigungen aus App und SDKs mit Zweck, Daten, Deklarationen und Prüfaufgaben im Abschnitt Permissions abgleichen; im relevanten Build tatsächliche Manifest-/Usage-Description-/Entitlement-Werte prüfen.
- Grenzen, vorhandene Freigaben, Auslieferungsziel und passende Start-/Build-Befehle in den Projektunterlagen konkretisieren. Keine festen Framework-Versionen oder Dienste aus Beispielen übernehmen.

Das genaue lesbare Format steht in [Markdown-Vertrag](references/format.md). Status und Nachweise ausschließlich im Tracker führen; State ist der daraus erzeugte Wiedereinstieg.

## 3. Plan prüfen

Einen Kritiker mit Nutzerauftrag, Plan, relevantem Katalog und aktuellen Einschränkungen prüfen lassen. Bei verfügbarer und erlaubter Delegation einen unabhängigen Agenten einsetzen. Andernfalls als Selbstprüfung erfassen und die fehlende Unabhängigkeit transparent halten. Kein unabhängiges Urteil erfinden.

Der Kritiker benennt konkrete fehlende Anforderungen, ungedeckte Katalogpunkte, unbrauchbare Reihenfolge oder nicht überprüfbare Kriterien. Ergebnis als Review für `PLAN` samt Bericht und aktuellem Fingerprint erfassen. Autorisierte Korrekturen vornehmen; Umfangsänderungen aus Kritik nicht automatisch zu Nutzerentscheidungen machen.

Danach State aktualisieren und `check --ready` ausführen. Offene Umsetzungsaufgaben sind dabei normal; fehlende Planung und offene Einordnungen müssen geklärt werden. Eine benötigte Gerätefreigabe lässt sich als blockierte Aufgabe planen und hindert unabhängige Arbeit nicht.

## 4. Umsetzen und fortsetzen

1. State und tatsächlichen Projektstand abgleichen. Den nächsten ausführbaren Task anhand Phase und Abhängigkeiten auswählen.
2. Aktiven Task festhalten und einen zusammenhängenden Teil des Nutzerablaufs implementieren. Bestehende fremde Änderungen schützen.
3. Im passenden Browser, Android-Gerät, iOS-Simulator/-Gerät oder der nativen Mac-App bedienen. Erwartetes Ergebnis tatsächlich beobachten. Lokale Unit-/Integrationsprüfungen gezielt für fehleranfällige Logik, wiederkehrende Fehler oder notwendige Grenzen einsetzen; sinnvolle bestehende Checks berücksichtigen.
4. In `Files` die für das geprüfte Verhalten maßgeblichen Quellen und Abhängigkeiten benennen. Das Werkzeug bildet daraus und aus den Kriterien einen Fingerprint. Erst nach der Prüfung einen Beleg für genau diesen Stand erfassen. Bericht: Ausgangslage, Schritte, Erwartung, tatsächliche Beobachtung, Umgebung, Modus, Zeitpunkt, Build und verbleibende Grenzen.
5. Vollständigen Use Case durch den Kritiker anhand Auftrag, aktuellem Code und Belegen bewerten lassen. Urteil `PASS`, `REWORK` oder `BLOCKED` mit konkreten Befunden erfassen. Betroffene Korrekturen und Prüfungen ausführen.
6. Tracker, dann State aktualisieren und `check` ausführen. Vor dem Phasenwechsel zusätzlich `check --phase <ID>` verwenden. Innerhalb des vereinbarten Goals weiterarbeiten.

Bei Auslieferung den tatsächlich erreichten Zustand in TRACKER/Releases erfassen: LOCAL, READY, SUBMITTED oder LIVE, zusammen mit Build, konkretem Artefakt-/Release-Verweis und aktuellen Evidence-IDs mit identischer Build-Kennung. Kriterien nach dem beauftragten Goal auslegen: READY endet mit geprüftem Paket und vorbereiteten Unterlagen; Store-Einreichung und Nutzerverfügbarkeit gehören zu SUBMITTED beziehungsweise LIVE. Ein Transport-/Upload-Erfolg wird nicht zu LIVE umgedeutet. Für LIVE den normalen Nutzerstart des ausgelieferten Builds belegen; auf iOS gehört dafür ios-device zu den Prüfzielen und zu einer Delivery-Aufgabe. Benötigte Konto-, Geräte- oder Review-Handgriffe im betroffenen Task festhalten; bereits erteilte Freigaben gelten weiter.

Kritik findet am vollständigen Use Case oder Phasenabschluss statt; kleine Zwischentasks brauchen nicht jeweils einen separaten Kritiker. Die Phase schließt erst nach ihrer erforderlichen Kritik. Bei Wiederholungen ohne neue Erkenntnis Ursache und Ansatz neu prüfen. Unabhängige Arbeit fortsetzen; notwendige externe Handgriffe konkret festhalten.

Bei neuer Anforderung oder verändertem Verhalten betroffene Aufgaben und Nachweise neu prüfen. Der Prüfer erkennt Änderungen der benannten Quelldateien und Kriterien. Ob die benannte Dateimenge vollständig ist oder externe Dienste verändert wurden, prüft der Agent zusätzlich. Ein grüner Strukturcheck bestätigt keine Produktqualität.

## 5. Abschluss

Bei einem **reinen Planungsauftrag** endet die Arbeit nach vollständiger Planung und aktueller Kritik mit `check --ready`. State bleibt auf der konkreten Fortsetzung; die spätere Umsetzung bleibt offen und braucht einen Umsetzungsauftrag. Keine App-Tasks oder Produktphasen als fertig markieren, um den Planungsauftrag abzuschließen.

Bei einem **Umsetzungsauftrag** vor dem Produktabschluss `check --complete` ausführen und danach `state --complete`. Alle vereinbarten Zielumgebungen und erforderlichen Kritikerurteile müssen belegt sein. Ein fehlendes physisches Gerät oder eine ausstehende notwendige Nutzerabnahme bleibt offen; übrige autorisierte Arbeit wird erledigt.

Für nichtlokale Auslieferung zusätzlich `check --release` verwenden. Ein vollständiger lokaler Plan oder der historische 1.0-Pilot erfüllt diesen Release-Vertrag nicht. Der Prüfer kontrolliert erklärte Vollständigkeit; tatsächliche Manifestinhalte, Assetqualität, Rechteinhaberschaft und Store-Zustände benötigen die beschriebenen Beobachtungen und Kritik.

Die Schlussantwort nennt Ergebnis, die tatsächlich geprüften Abläufe, den installierten Startpfad beziehungsweise das Artefakt und verbleibende Grenzen. Technischen Nachweis und ausdrücklich erforderliche persönliche Nutzerabnahme unterscheiden.

## Werkzeuge

```sh
python3 "$SKILL_DIR/scripts/workflow.py" catalog --profile ios
python3 "$SKILL_DIR/scripts/workflow.py" check /projekt --ready
python3 "$SKILL_DIR/scripts/workflow.py" fingerprint /projekt --scope T002
python3 "$SKILL_DIR/scripts/workflow.py" fingerprint /projekt --scope UC02
python3 "$SKILL_DIR/scripts/workflow.py" state /projekt --task T002 --next 'Eintrag speichern und nach Neustart wieder öffnen'
python3 "$SKILL_DIR/scripts/workflow.py" status /projekt
python3 "$SKILL_DIR/scripts/workflow.py" check /projekt --phase P03
python3 "$SKILL_DIR/scripts/workflow.py" check /projekt --complete
python3 "$SKILL_DIR/scripts/workflow.py" check /projekt --release
```

`check`, `status`, `catalog` und `fingerprint` sind lesend. `init` erzeugt neue Dateien; `state` aktualisiert ausschließlich die abgeleitete STATE-Datei. Details und Grenzen stehen im Markdown-Vertrag. Verwende den Code des geladenen Skills; kopiere keinen zweiten Controller in jede App.

Version 1.1 liest frühere 1.0-Pläne weiterhin mit ausdrücklichem Legacy-Hinweis. Bei beauftragter Übernahme der Ergänzung die [Versionsübernahme](references/format.md#versionsübernahme-10-auf-11) vollständig durchführen; nicht nur die Versionsnummer ändern oder historische Beleg-Fingerprints neu schreiben.
