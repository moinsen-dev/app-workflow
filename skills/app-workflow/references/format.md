# Markdown-Vertrag 1, Vorlage 1.1

Alle maßgeblichen Projektinformationen liegen in Markdown. Die kleinen Tabellen haben feste Section- und Spaltennamen für den lesenden Prüfer; Ergebnisse und Begründungen werden frei und verständlich formuliert. Freitext außerhalb der Tabellen kann ergänzt werden.

## Formatregeln

- Section-Namen und Spaltennamen aus den Vorlagen beibehalten; Tabellenzeilen beginnen und enden mit `|`.
- Stabile IDs: Anforderungen `R001`, Phasen `P01`, Use Cases `UC01`, Tasks `T001`, Belege `E001`, Reviews `RV001`.
- Mehrere Referenzen durch Komma trennen. `-` steht für keine Referenz. In Textzellen einen senkrechten Strich als `\|` schreiben; Zeilenumbrüche durch einen verlinkten Bericht ersetzen.
- `Order` ordnet Phasen. `Depends` enthält Phase- beziehungsweise Task-IDs. Eine Task-Phase stimmt mit ihrer Use-Case-Phase überein. Abhängigkeiten müssen vor Beginn erledigt oder begründet entfallen sein; vorherige abhängige Phasen brauchen auch ihre Kritik.
- `YES`, `NO`, `UNKNOWN` sind Einordnungen. Bei `NO` eine konkrete Begründung; `UNKNOWN` bleibt nur während der Planung offen.
- Bei Änderungen am Auftrag Anforderungen ergänzen, statt sie hinter einer bestehenden Aufgabenbeschreibung zu verstecken.

## PLAN.md

`Project` enthält `schema: app-workflow/1`, Profil, Template-Version, explizite Prüfziele und Goal. Die Initialisierung nimmt das Goal als erste Anforderung auf. Der Agent zerlegt es beim Planen in die tatsächlichen Einzelanforderungen.

### Personalization

Die Tabelle enthält alle 14 benannten Felder aus dem Nutzerprofil, jeweils mit `ID`, wirksamem `Value`, `Source` und `Reason`. Die Herkunft kann beispielsweise `user:aktueller Auftrag`, `project:AGENTS.md`, `project:git remote`, `profile:/bekannter/pfad/USER_PROFILE.md#graphic_style` oder ein begründeter `default:Plattformkonvention` sein. Der Import erhält den aufgelösten Profilpfad, damit gleichnamige Profile unterscheidbar bleiben. Bei einem Rechnerwechsel die Quelle bei Bedarf ausdrücklich neu zuordnen; den wirksamen Projektschnappschuss dabei erhalten. UNKNOWN ist während der Planung erlaubt; CONFLICT bezeichnet einen aufzulösenden Widerspruch. NONE mit Begründung bedeutet keine zusätzliche Vorgabe.

Die Tabelle ist ein Projektschnappschuss. Der Prüfer lädt globale Profile nicht erneut und verändert sie nicht. Geänderte wirksame Vorgaben verändern Plan- und Task-Fingerprints; betroffene vorhandene Nachweise brauchen erneute Prüfung. Er prüft das Vorhandensein von Herkunft und Begründung, nicht deren Wahrheitsgehalt oder die semantisch richtige Auflösung.

### Delivery

| Feld | Bedeutung |
|---|---|
| ID | Stabiles Auslieferungsziel D001 usw. |
| Platform | ios, android, macos, web, windows oder linux; aus tatsächlichen UI-Zielen abgeleitet |
| Channel | local, app-store, testflight, google-play, play-testing, direct, web, microsoft-store oder linux-store, soweit zur Plattform passend |
| Goal | local, ready, submitted oder live; Bedeutung und Zielmatrix in release.md |
| AppID | Tatsächliche Bundle-/Paketidentität oder Web-Origin; keine bloße persönliche Präfix-Vorgabe |
| Owner | Verantwortlicher Eigentümer mit nötigem Konto/Team; keine Tokens oder Zertifikate |
| Tasks | Zugeordnete Aufgaben für Voraussetzungen und Endzustand, einschließlich erforderlichem normalen Nutzerstart |

Jede gewählte Plattform braucht mindestens einen Auslieferungsweg. Mehrere unterschiedliche Kanäle pro Plattform sind möglich. Vor `--ready` müssen Kanal, Goal und konkrete Aufgaben feststehen. Für local/live gehört ein normaler UI-Task zum jeweiligen Delivery; iOS live braucht dafür ios-device in den Prüfzielen. Ein derzeit fehlendes Gerät kann als blockierter Task eingeplant sein. AppID und Owner dürfen während ihrer eingeplanten Klärung UNKNOWN sein; Abschluss benötigt konkrete Werte ohne CONFLICT. AppID NONE ist kein Identitätsnachweis. Bei lokalen Apps ohne Anbieter kann Owner bewusst NONE sein. Profil-/Release-Änderungen sind kein automatischer Auftrag zu Veröffentlichung oder Umbenennung.

Neue Zielkanäle führen zu zusätzlichen Katalogchecks; die Ausgabe von `catalog --profile ... --delivery ...` übernehmen und konkret zuordnen. Delivery-Zeilen beeinflussen die Fingerprints ihrer zugeordneten Tasks; relevante Build-/Konfigurationsdateien gehören zusätzlich in Files.

`Phases` und `UseCases` enthalten Ergebnisse und Zuordnungen. `Review` ist `required` für Produktabläufe; `none` eignet sich nur für einen begründet rein technischen Hilfsumfang, der im übergeordneten Ablauf geprüft wird. Eine Planprüfung ist für `--ready` und Abschluss immer erforderlich.

`Tasks`:

| Feld | Bedeutung |
|---|---|
| ID, Phase, UseCase, Requirements | Stabile Kennungen und Zuordnung |
| Accept | Konkretes beobachtbares Abschlusskriterium |
| Verify | Erwartete Nachweisziele: web, android, ios-simulator, ios-device, macos, windows, linux, inspection, unit oder build |
| Mode | normal, fixture oder any; normale App-Abläufe planen normal |
| Depends | Vorausgesetzte Task-IDs |
| Files | Kommagetrennte relative Quelldateien, die das Verhalten und seine relevanten Abhängigkeiten bestimmen; keine Globs oder Verzeichnisse |

Ein Task mit mehreren Verify-Zielen benötigt Nachweise für alle. `inspection` passt beispielsweise zur Plan- oder Konfigurationsprüfung; es ersetzt keine UI-Abnahme. Benötigt derselbe Ablauf sowohl Fixture- als auch Normalprüfung, dafür getrennte Tasks mit passenden Kriterien anlegen.

`Modules` führt alle verfügbaren Modulentscheidungen. `Checklist` enthält exakt den gemeinsamen Katalog, das gewählte Profil und die Checks der aktiven Module. `YES`-Punkte referenzieren konkrete Tasks. Für Änderungen an der Auswahl die Ausgabe von `catalog` heranziehen. Versionswechsel bewusst migrieren; ein anderer installierter Katalog wird nicht stillschweigend akzeptiert.

## TRACKER.md

### Aufgabenstatus

- `OFFEN`: geplant.
- `IN_ARBEIT`: aktiver Umsetzungs- oder Planungsschritt.
- `ZUR_PRUEFUNG`: implementiert, Nachweis noch ausstehend.
- `ERLEDIGT`: Kriterien durch aktuelle passende Belege bestätigt.
- `BLOCKIERT`: Ursache und konkret benötigter nächster Handgriff in Reason.
- `NICHT_ZUTREFFEND`: begründete Ausnahme innerhalb des Auftrags. Keine Umgehung einer weiterhin relevanten Anforderung.

`Evidence` in einer Task-Zeile referenziert die aktuellen maßgeblichen Beleg-IDs. Ein Zwischentask darf mit seinem Nachweis fertig werden; der vollständige Use Case und die Phase brauchen zusätzlich ihre Kritik.

### Belege

| Feld | Bedeutung |
|---|---|
| ID, Task | Beleg und zugehöriger Task |
| Checks | Tatsächlich geprüfte Zielumgebungen; muss zum Task passen |
| Method | ui für App-Bedienung, inspection für Inspektion, unit für Logikprüfung oder build für Build |
| Mode | normal, fixture oder code |
| Date | Tatsächlicher Zeitpunkt in ISO-8601 mit Zeitzone, etwa 2026-09-15T15:00:00+02:00 |
| Build | Identifizierbarer Code-/Buildstand und bei Bedarf Laufzeitkonfiguration |
| Fingerprint | Vom Befehl `evidence` beim Eintragen berechnet; bei Handeintrag die Ausgabe von fingerprint --scope T001 nach der Prüfung desselben Stands |
| Report | Relative existierende, nicht leere Datei mit Beobachtung; kein Pfad außerhalb des Projekts |
| Result | PASS oder FAIL |

Im Bericht Ausgangslage, Schritte, Erwartung und Beobachtung festhalten. Beispieldaten und realen App-Modus getrennt benennen: Eine normale App mit isolierten künstlichen Nutzerdaten kann den normalen Ablauf belegen; eine Fixture-Abkürzung belegt nur diese Abkürzung. Persönliche Inhalte nicht in dauerhafte Belege kopieren.

Nach einer Änderung alte Belege als Historie erhalten, den Task wieder öffnen und seine aktuellen Evidence-Verweise nach der erneuten Prüfung aktualisieren. Ein geänderter Fingerprint macht einen alten aktiven Beleg ungültig. Es werden Kriterien und die explizit benannten Quelldateien berücksichtigt. Vollständigkeit dieser Dateiauswahl, externe Konfiguration, Systemrechte und Produktionszustand brauchen zusätzlich den Abgleich des Agenten.

### Reviews

| Feld | Bedeutung |
|---|---|
| ID | Review-ID |
| Scope | PLAN oder eine Use-Case-ID |
| Kind | independent oder self; tatsächliche Prüfart angeben |
| Result | PASS, REWORK oder BLOCKED |
| Fingerprint | Vom Befehl `review` berechnet; bei Handeintrag die Ausgabe von fingerprint --scope PLAN beziehungsweise UC01 für den tatsächlich geprüften Stand |
| Report | Relative Berichtsdatei mit konkreten Befunden und Belegen |

Die letzte Review-Zeile pro Scope ist maßgeblich. Für einen Abschluss muss diese PASS sagen und aktuell sein. Plan-Fingerprints binden die Planung, Use-Case-Fingerprints außerdem zugeordnete Quellen und aktuelle Belege. Die Quelldateiliste allein verändert den Plan-Fingerprint nicht, wohl aber Task- und Use-Case-Fingerprints.

Eine Selbstprüfung bleibt als Warnung sichtbar und darf nicht als unabhängige Abnahme bezeichnet werden. Wenn der Nutzer ausdrücklich unabhängige Prüfung verlangt, bleibt diese bis zu ihrer Durchführung eine offene Aufgabe.

### Releases

| Feld | Bedeutung |
|---|---|
| ID | Nachweis eines Auslieferungszustands, L001 usw. |
| Delivery | Ziel aus PLAN/Delivery, zum Beispiel D001 |
| Stage | Tatsächlich beobachtet: LOCAL, READY, SUBMITTED oder LIVE |
| Build | Eindeutige Build-Kennung, möglichst Artefakt-Hash; exakt dieselbe Kennung wie in den hier referenzierten Belegen |
| Locator | Konkreter Artefaktpfad oder Release-/Zielverweis; keine Zugangsgeheimnisse |
| Evidence | Aktuelle PASS-Belege aus zugeordneten Tasks, mit Datum und Bericht |

Die letzte Zeile je Delivery ist maßgeblich. Ein höherer Stand erfüllt die technisch vorangehenden Stufen desselben beauftragten Wegs, erteilt aber keine zusätzliche Autorisierung. LIVE bei einem Testkanal heißt für die benannte Testergruppe verfügbar. Ein lokal gebautes Artefakt oder ein Upload darf nicht als LIVE eingeordnet werden.

Zum Abschluss müssen die referenzierten Belege aktiv, aktuell und normal beziehungsweise code sein; Fixture-Belege genügen nicht. Reiner Build-Erfolg reicht nicht. Für LOCAL und LIVE ist normale UI-Bedienung auf der zugehörigen Plattform erforderlich; LIVE auf iOS benötigt ios-device. Für READY genügt als Release-Beleg die Inspektion des vorbereiteten Artefakts samt Unterlagen; der übrige Plan enthält weiterhin die passenden App-Prüfungen. Ein abweichender repräsentativer Testbuild erhält seine eigene Kennung und seinen eigenen Beleg. Unterschiede und Zuordnung zum Release-Artefakt im Bericht erklären, nicht unterschiedliche Builds durch dieselbe Kennung gleichsetzen.

Im Bericht müssen Beleg, Build, Zielgruppe und tatsächlich erreichter Status zusammenpassen. Dieses inhaltliche Urteil bleibt Aufgabe des ausführenden Agenten und Kritikers; eine ausgefüllte Tabelle beweist keinen externen Store-Zustand. Die nach Goal gestaffelten Anforderungen stehen in release.md: READY benötigt keinen Store-Upload und keine öffentliche URL; SUBMITTED/LIVE brauchen zusätzliche tatsächliche Beobachtungen.

Release-Zeilen fließen in die zugehörigen Use-Case-Fingerprints ein. Ein geänderter Release-Verweis oder Status kann daher nicht mit einem alten Kritikerurteil abgeschlossen werden.

### Tracker-Befehle

Die Tabellen bleiben von Hand lesbar und änderbar. Die Befehle ersparen die fehleranfällige Tabellenpflege und binden Fingerprints an den Stand, der beim Aufruf vorliegt:

```sh
python3 "$SKILL_DIR/scripts/workflow.py" evidence /projekt --task T003 --checks macos --mode normal --build 4f2a9c1 --report docs/t003-evidence.md --result PASS
python3 "$SKILL_DIR/scripts/workflow.py" task /projekt T003 --status ERLEDIGT --evidence E004
python3 "$SKILL_DIR/scripts/workflow.py" review /projekt --scope UC02 --kind independent --result PASS --report docs/uc02-review.md
python3 "$SKILL_DIR/scripts/workflow.py" release /projekt --delivery D001 --stage LOCAL --build 4f2a9c1 --locator .artifacts/App.app --evidence E004
```

`evidence`, `review` und `release` fügen eine neue Zeile mit der nächsten freien ID an. `task` legt die Zeile einer geplanten Aufgabe an oder ändert Status, Belege und Begründung; ohne Angabe bleibt der bisherige Wert. `Method` folgt aus den geprüften Zielen, `Date` ist der Zeitpunkt des Eintrags. Jeder Befehl prüft den entstehenden Tracker und verweigert eine Zeile, der der Prüfer einen Fehler zuordnet: ERLEDIGT ohne aktuellen passenden Beleg, ein Release-Beleg aus einer fremden Aufgabe, ein Endzustand, der nicht zum Kanal passt. Der übrige Text der Datei bleibt unverändert. Danach `state` ausführen. Ein Eintrag belegt weiterhin nur, was sein Bericht tatsächlich beschreibt.

## STATE.md

State ist abgeleitet. Nach Änderungen erst Plan/Tracker abgleichen, dann:

```sh
python3 "$SKILL_DIR/scripts/workflow.py" state /projekt --task T003 --next 'Den Fehlerfall bei verweigerter Berechtigung prüfen'
```

Die Datei enthält aktive Kennungen, nächsten Schritt und Prüfsummen der beiden maßgeblichen Dokumente. So wird ein veralteter Wiedereinstieg erkannt. Sie enthält keine zweite bearbeitbare Aufgabenstatusliste.

`state` bestätigt keine neue Beobachtung und markiert keine Aufgabe erledigt. Es weigert sich, widersprüchliche Pläne oder unbelegte Fertigmeldungen in einen frischen State zu übernehmen. Korrigiere den Tracker und die betroffenen Nachweise zuerst.

## Prüftiefen

| Aufruf | Bedeutung |
|---|---|
| check | Struktur, vorhandene Status, referenzierte Nachweise, Abhängigkeiten und State-Konsistenz; offene Planung wird gemeldet |
| check --ready | Zusätzlich alle Einordnungen, vollständige Aufgabenabdeckung und aktuelle Planprüfung |
| check --phase P03 | Zusätzlich Abschluss dieser Phase einschließlich Use-Case-Kritik |
| check --complete | Alle Phasen abgeschlossen; auch wirksam, wenn State bereits COMPLETE behauptet |
| check --release | Gesamtabschluss einschließlich eines nichtlokalen Auslieferungsziels der Vorlage 1.1; ein lokales Goal genügt nicht |
| status | Lesende Zusammenfassung des aktiven Stands und der Aufgaben |
| state --complete | Erst Gesamtabschluss prüfen, dann State auf COMPLETE setzen |

`--json` bei check/status liefert einen maschinenlesbaren Bericht auf stdout; Projektdateien bleiben Markdown. Exit-Code 1 bedeutet Fehler, 0 bedeutet formal gültigen Stand. `STRUCTURE_OK` ist ausdrücklich kein Qualitätsurteil über das Produkt.

## Bestehende Projekte

Für Auswahl der Arbeitswurzel, aktuellen Bestandsnachweis und beauftragten Änderungsumfang die [Brownfield-Anleitung](brownfield.md) verwenden. Der Datenvertrag bleibt gleich; Greenfield und Brownfield benötigen keine eigenen CLI-Modi.

Der Generator prüft vor dem Schreiben die Zielnamen und überschreibt keine vorhandenen oder symbolisch verlinkten Dateien. Bei bestehenden Unterlagen einen separaten Entwurf erzeugen, Anforderungen und Belege zuordnen und bestehende AGENTS-Regeln beibehalten. Alte Dateien nicht pauschal löschen. Nur der aktuelle Auftrag bestimmt, wie weit eine Übernahme geht.

## Versionsübernahme 1.0 auf 1.1

Der Prüfer kann frühere 1.0-Unterlagen mit unveränderter Fingerprint-Berechnung und ursprünglichem Katalog lesen. Er gibt LEGACY_TEMPLATE aus; `--release` lehnt diesen Stand ab. So bleibt der historische lokale Pilot prüfbar, ohne ihm nachträglich neue Fähigkeiten zuzuschreiben.

Für eine beauftragte Übernahme einen 1.1-Entwurf separat erzeugen. Bestehende Ziele, Regeln, IDs, Quellen und historische Belege erhalten; Personalization, Delivery, Releases sowie neue Katalogpunkte gezielt integrieren. Erst nach der inhaltlichen Zuordnung template_version auf 1.1.0 setzen. Neue Voraussetzungen als konkrete Tasks ergänzen. Bestehende Identitäten und Remotes beibehalten, sofern keine ausdrückliche Änderung beauftragt ist.

Die neuen Kontextfelder können bisherige Nachweise veralten lassen. Betroffene Aufgaben wieder öffnen und ihren tatsächlich nötigen Prüfumfang abgleichen; keine pauschale Nachstempelung alter Fingerprints. Unveränderten historischen Stand weiter als solchen referenzieren. Neue Planprüfung erfassen, Tracker und State aktualisieren. Ein vorbereitender Planungsauftrag endet mit `--ready`, eine autorisierte Übernahme einschließlich Umsetzung erfüllt anschließend die vereinbarten Aufgaben.
