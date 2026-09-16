# App Workflow

Ein wiederverwendbarer Skill für neue und bestehende Expo-, Flutter-, native iOS- und native macOS-Apps. Version 1.1 berücksichtigt persönliche Konventionen und den vollständigen Weg bis zum vereinbarten Auslieferungsziel. Nummerierte Projektunterlagen, tatsächliche App-Prüfung und Kritiker verbinden Anforderungen, Umsetzung und belegten Abschluss.

## Schnellstart

1. Das gewünschte App-Projekt im Coding-Harness öffnen. Für eine neue App einen eigenen Projektordner verwenden.
2. `app-workflow` dort verfügbar machen; die [Installation](#installation-in-einem-anderen-projekt) ist unten beschrieben. In diesem Skill-Projekt ist er bereits für Codex und Claude Code eingebunden.
3. Einen der folgenden Startaufträge senden. Ziel, Plattform, Umfang und gegebenenfalls Profilpfad anpassen. Der Agent übernimmt dann Bestandsprüfung, Planung, Unterlagen, Kritik und die beauftragte Umsetzung.

In Codex lässt sich der Skill mit `$app-workflow` ausdrücklich auswählen. In einem anderen Harness den installierten Skill `app-workflow` ausdrücklich nennen und dessen verfügbaren Einstieg verwenden. Die Beispiele sind Chat-Aufträge; sie werden nicht im Terminal ausgeführt.

### Greenfield: Eine neue App bauen

Greenfield bedeutet: Für dieses Produkt gibt es noch keine bestehende App. Ein vorbereiteter Ordner mit Git oder README ist dafür in Ordnung.

```text
Nutze $app-workflow für ein Greenfield-Projekt im aktuellen Ordner.
Plane und implementiere eine Expo-App für lokale Textnotizen:
anlegen, bearbeiten, löschen und nach einem Neustart wiederfinden.
Prüfziele: Android und iOS-Simulator.
Auslieferungsziel: lokal installierte Apps im normalen Modus.
Erzeuge AGENTS.md, PLAN.md, TRACKER.md und STATE.md.
Arbeite mit den Checklisten und Kritiker-Schleifen bis zum belegten Ziel.
```

Für Flutter, natives iOS oder macOS die App-Familie und passenden Prüfziele im Auftrag ersetzen. Es genügt, das Produktziel natürlich zu beschreiben; der Nutzer muss keine Task-IDs oder CLI-Parameter vorgeben.

### Brownfield: Eine bestehende App übernehmen und erweitern

Brownfield bedeutet: Die App besitzt bereits Code und Projektentscheidungen. Der Agent erfasst den vorhandenen Stand, integriert die Dokumentrollen und plant den beauftragten Änderungsumfang. Vorhandene Funktionen werden mit passenden Nachweisen übernommen; offene Nachweise bleiben sichtbar.

```text
Nutze $app-workflow für dieses bestehende Expo-Projekt (Brownfield).
Übernimm das Projekt in den Workflow und implementiere den Export
einer vorhandenen Notiz als Textdatei über das System-Teilen-Menü.
Erhalte den bestehenden Stack, die App-IDs, den Git-Remote,
das festgelegte Design, vorhandene Daten und unbeteiligte Änderungen.
Prüfziele: Android und iOS-Simulator; Auslieferungsziel: lokal.
Integriere vorhandene AGENTS-, Plan- und Statusdateien.
Prüfe den Export und die davon betroffenen bisherigen Notizabläufe.
```

Bei einem Repository mit mehreren Apps das Paket oder seinen Pfad nennen. Der Auftrag umfasst die Übernahme und Umsetzung; dafür ist keine weitere Routinefreigabe nötig. [Ablauf für bestehende Apps](skills/app-workflow/references/brownfield.md).

### Zuerst ausschließlich planen

```text
Nutze $app-workflow für dieses bestehende Projekt.
Übernimm ausschließlich die Planung in den Workflow und plane
die noch nötige Arbeit bis zu einem vorbereiteten TestFlight-Build (READY).
Erhalte vorhandene Projektentscheidungen und Unterlagen.
Beende den Auftrag mit geprüftem Plan und konkretem Wiedereinstieg.
App-Umsetzung und Einreichung bleiben offen.
```

Das funktioniert ebenso für Greenfield. „Nur planen“ und „planen und implementieren“ bestimmen den Arbeitsumfang unabhängig davon, ob die App neu oder vorhanden ist. Für einen tatsächlich verfügbaren TestFlight-Zugang stattdessen LIVE als Ziel nennen; dann gehört ein physisches iOS-Gerät zur Planung.

### Fortsetzen oder nur den Stand ansehen

Bei vorhandenen Workflow-Unterlagen ohne erneute Initialisierung fortsetzen:

```text
Nutze $app-workflow. Setze das vereinbarte Ziel anhand von AGENTS.md,
STATE.md, PLAN.md und TRACKER.md fort. Gleiche den tatsächlichen
Checkout ab und bearbeite die nächste ausführbare Aufgabe.
```

Eine reine Statusabfrage lautet beispielsweise:

```text
Nutze $app-workflow und zeige nur den belegten aktuellen Stand,
offene Punkte und den nächsten Schritt. Ändere keine Dateien.
```

Zum Verwenden persönlicher Vorgaben einem Startauftrag hinzufügen:

```text
Verwende meine persönlichen Standards aus /absoluter/pfad/USER_PROFILE.md.
```

Einen echten bekannten Pfad einsetzen. In diesem Paket liegt eine [neutrale Profilvorlage](skills/app-workflow/assets/USER_PROFILE.md). Fehlende Profilwerte werden aus konkreten Projektentscheidungen oder begründeten Defaults aufgelöst; nur wesentliche fehlende Entscheidungen brauchen eine Rückfrage.

## Installation in einem anderen Projekt

Für den folgenden Installationsweg werden Node.js ab 22.20.0 und verfügbares npm/npx benötigt; das ist die Node-Voraussetzung der hier verwendeten Skills-CLI 1.5.26. Das Workflow-Werkzeug benötigt zusätzlich Python 3.10 oder neuer. Das gilt auch bei nativen iOS-/macOS-Projekten, deren eigentlicher App-Build kein Node.js benötigt.

Das installierbare Paket liegt unter `skills/app-workflow/`; die Prüfdateien in `evals/` gehören nicht dazu. Vorhandene gleichnamige Installationen vor einem Ersetzen abgleichen. Im gewünschten App-Projekt ausführen:

```sh
npx skills@1.5.26 add moinsen-dev/app-workflow \
  --skill app-workflow --agent codex
```

Für Claude Code `--agent claude-code` verwenden; für beide `--agent codex claude-code`. Projektlokale Installation ist der Standard. Für eine bewusst gewünschte benutzerweite Installation kann `--global` ergänzt werden. Die Beispiele verwenden die hier geprüfte CLI-Version 1.5.26. Für eine lokale Kopie statt `moinsen-dev/app-workflow` ihren absoluten Verzeichnispfad angeben. Quellen, gezielte Skill-/Agent-Auswahl und Installationsumfang beschreibt die [Vercel-Skills-Dokumentation](https://github.com/vercel-labs/skills#install-a-skill).

Die Installation macht den Skill verfügbar. Anschließend im App-Projekt einen der Startaufträge senden. Sie erzeugt selbst weder eine App noch einen fertigen Projektplan. Die persönliche Profildatei wird separat über ihren bekannten Pfad verwendet und nicht automatisch global installiert. Falls die laufende Sitzung neue Skills noch nicht erkennt, den Skill-Katalog neu laden beziehungsweise eine neue Sitzung im Zielprojekt öffnen.

Direkter Einstieg für Agenten: [SKILL.md](skills/app-workflow/SKILL.md).

## Die vier Projektdateien

| Datei | Aufgabe |
|---|---|
| `AGENTS.md` | Verbindlicher Einstieg, Arbeitsregeln und Fortsetzung |
| `PLAN.md` | Wirksame persönliche Vorgaben mit Herkunft, Anforderungen, Phasen, Use Cases, Aufgaben, Checkliste und Auslieferungsziele |
| `TRACKER.md` | Einzige Quelle für Aufgabenstatus, Prüfbelege, Kritikerurteile und tatsächlich erreichte Auslieferungszustände |
| `STATE.md` | Daraus erzeugter Wiedereinstieg mit aktiver Phase, Aufgabe und nächstem Schritt |

Für Claude Code kann zusätzlich eine kurze `CLAUDE.md` mit `@AGENTS.md` erzeugt werden. Vorhandene Projektdateien werden bei der Initialisierung nicht überschrieben.

## Persönliche Konventionen

Die [Profilvorlage](skills/app-workflow/assets/USER_PROFILE.md) hält persönliche Standards für Grafikstil, Design-Skill, Brand-Assets, Bundle-Präfix, GitHub-User/-Organisation, Sichtbarkeit und weitere Konventionen fest. Unbestimmte Angaben beginnen als UNKNOWN. Mit `workflow.py profile /absoluter/pfad/USER_PROFILE.md` lässt sich ein eigenes Profil anlegen; ein vorhandenes wird nicht überschrieben. Das persönliche Profil bleibt außerhalb der Veröffentlichung; eine USER_PROFILE.md in der Wurzel dieses Repositorys wird durch .gitignore ausgeschlossen.

Der Agent übernimmt ein Profil nur über einen bekannten Pfad. Im jeweiligen Plan hält er den wirksamen Wert, die eindeutig auffindbare Quelle und die Begründung fest. Reihenfolge: aktueller ausdrücklicher Auftrag → konkrete Projektentscheidung → anwendbarer Nutzerstandard → begründeter Default. Ein anderer Bundle-Präfix benennt bestehende Apps nicht um; ein anderer GitHub-Default verschiebt kein vorhandenes Repository. [Personalisierungsregeln](skills/app-workflow/references/personalization.md).

## Produktionsvoraussetzungen

Jedes Projekt ordnet früh Identität, Icons/Startressourcen, Berechtigungen einschließlich SDKs, Signierung, Konten/Rollen, Store-Unterlagen und Betrieb ein. Für tatsächlich gewählte Verteilungswege kommen konkrete Kriterien hinzu: TestFlight/App Store, Google Play/Testtracks, direkte Android-/Mac-Pakete, Web sowie Flutter auf Windows/Linux. Updates, Datenschutzangaben, Konfiguration und Wiederherstellung werden passend zum Produkt geprüft.

| Ziel | Was als erreicht gelten darf |
|---|---|
| LOCAL | Lokaler normaler App-Start belegt |
| READY | Artefakt und nötige Unterlagen vorbereitet und geprüft; keine Store-Einreichung oder öffentliche Bereitstellung erforderlich |
| SUBMITTED | Tatsächlich im vorgesehenen Kanal eingereicht; Status und Version belegt |
| LIVE | Für die benannte Zielgruppe verfügbar und der ausgelieferte Build normal geöffnet |

Bei TestFlight bedeutet LIVE Testerzugang. Ein Upload reicht dafür nicht. Für iOS LIVE muss schon im Plan eine zugeordnete Prüfung auf einem physischen iOS-Gerät stehen. Pro Ziel wird der tatsächliche Zustand mit Artefaktverweis und passenden aktuellen Build-Belegen festgehalten. [Kanalabhängiger Release-Katalog](skills/app-workflow/references/release.md).

## Ablauf

1. Ist-Zustand, persönliche Vorgaben, Plattform, Zielumgebungen und Auslieferungsziel bestimmen.
2. Gemeinsame Checkliste und Plattformvorlage auf konkrete Anforderungen und Aufgaben abbilden; Zusatzmodule begründet auswählen.
3. Plan kritisch prüfen und Vollständigkeitsprüfung ausführen.
4. Einen vollständigen Nutzerablauf bauen, in der tatsächlichen App bedienen und Beobachtungen festhalten.
5. Kritik bearbeiten, betroffene Abläufe erneut prüfen und Tracker sowie State aktualisieren.
6. Nächste ausführbare Aufgabe bearbeiten; erst mit den vereinbarten Nachweisen abschließen.

23 gemeinsame Checks plus je 6 Plattformchecks bilden den Grundumfang. Acht bedingte Module ergänzen Authentifizierung, entfernte Dienste, Synchronisierung, KI, Käufe, Sensoren, Benachrichtigungen und Datei-/Medienzugriff; passende Auslieferungschecks kommen pro Kanal hinzu. Produktanforderungen bleiben zusätzlich maßgeblich; kein Katalog kann jedes unbekannte Problem vorwegnehmen.

## Direkte Werkzeugaufrufe

Normalerweise verwendet der Agent diese Befehle selbst. Das Werkzeug benötigt Python 3.10 oder neuer und keine zusätzlichen Python-Pakete. `init` erzeugt ausschließlich Markdown-Unterlagen; es generiert keinen Expo-/Flutter-/Xcode-App-Code und nimmt keine automatische Brownfield-Migration vor.

Für neue Unterlagen aus dem Ordner dieses Skill-Pakets:

```sh
python3 skills/app-workflow/scripts/workflow.py init /absoluter/projektpfad \
  --profile macos --targets macos --goal 'Lokale Notizen verwalten' \
  --delivery macos:local:local \
  --user-profile "$PWD/skills/app-workflow/assets/USER_PROFILE.md" --claude
python3 skills/app-workflow/scripts/workflow.py check /absoluter/projektpfad
```

Das Beispiel verwendet die neutrale Profilvorlage; für eigene Standards deren bekannten Pfad angeben. Nach `init` ist ein konsistenter Entwurf mit offenen Entscheidungen zu erwarten. Erst nachdem der Agent Anforderungen, Aufgaben, Katalog und Planreview konkretisiert hat:

```sh
python3 skills/app-workflow/scripts/workflow.py check /absoluter/projektpfad --ready
python3 skills/app-workflow/scripts/workflow.py status /absoluter/projektpfad
```

Greenfield und Brownfield nutzen denselben Prüfer. Bei vorhandenen kollidierenden AGENTS-/Plan-/Statusdateien verweigert `init` das Überschreiben mit `EXISTS`. Der Agent erzeugt dann einen separaten Entwurf und integriert ihn gezielt nach der [Brownfield-Anleitung](skills/app-workflow/references/brownfield.md). Für ein bereits eingerichtetes Projekt mit `status`/`check` einsteigen. Es gibt keine CLI-Schalter `--greenfield` oder `--brownfield`; der Skill entscheidet den passenden Weg anhand des Bestands.

Belege, Kritikerurteile, Auslieferungszustände und Aufgabenstatus trägt der Agent mit `evidence`, `review`, `release` und `task` ein. Die Befehle berechnen den Fingerprint des geprüften Stands, vergeben die nächste ID und verweigern Zeilen, denen der Prüfer einen Fehler zuordnet, etwa eine Fertigmeldung ohne aktuellen Beleg. [Format und weitere Befehle](skills/app-workflow/references/format.md) beschreiben Phasenprüfung, Fingerprints und Abschluss. `--claude` legt bei neuen Unterlagen den Import `@AGENTS.md` an; bei einer vorhandenen CLAUDE.md wird dieser gezielt ergänzt und ihr übriger Inhalt erhalten.

Der Prüfer erkennt unter anderem verschwundene Katalogpunkte, fehlende Zielabdeckung, unbelegte Fertigmeldungen und veraltete Nachweise für explizit benannte Quelldateien. Er kann weder die Wahrheit eines geschriebenen Berichts noch die Vollständigkeit der Dateiauswahl automatisch beweisen. Dafür bleiben App-Bedienung und Kritik erforderlich.

`--ready` prüft den vollständigen Plan; `check --release` prüft den Gesamtabschluss eines nichtlokalen Auslieferungsziels, auch wenn das vereinbarte Ziel READY lautet. Das sind verschiedene Aussagen. Mit `profile /bekannter/pfad/USER_PROFILE.md` lässt sich ein weiteres neutrales Profil erzeugen. Versionsübernahmen bestehender 1.0-Projekte erfolgen durch gezielte Integration; alte Nachweise bleiben als Historie erhalten und werden nicht nachträglich zu Release-Belegen erklärt.

## Harness und Installation

Das öffentliche Paket verwendet das `SKILL.md`-Format. Seine projektlokale Installation für Codex und Claude Code wurde mit der [Vercel-Skills-CLI](https://github.com/vercel-labs/skills) geprüft. Beide Verweise dieses Repositorys zeigen auf dieselbe Skill-Quelle.

Goals, Fortsetzung und unabhängige Agenten werden über tatsächlich verfügbare Funktionen des jeweiligen Harness genutzt. Der Skill besitzt keinen eigenen Hintergrunddienst. [Harness-Anbindung](skills/app-workflow/references/harnesses.md).

## Nachweise

- [Prüfumfang und Grenzen](docs/VALIDATION.md): reproduzierbare Werkzeugprüfungen und deren Aussagekraft.
- [Gezielte Regressionen](evals/check_workflow.py): fehlende Checks, stale Nachweise, Bestandsschutz, Personalisierung und Release-Vertrag.
- [Synthetischer Vertrag 1.0](evals/fixtures/legacy-v1/AGENTS.md): feste Fingerprints für die Abwärtskompatibilität; keine App-Abnahme.

Die gezielten Prüfungen des Markdown-Werkzeugs laufen mit `python3 evals/check_workflow.py`. Zusätzliche App-Tests werden nach konkretem Nutzen ausgewählt; Testanzahl und grüner Build ersetzen keine geprüften Nutzerabläufe.

## Lizenz

[MIT](LICENSE), Copyright 2026 moinsen-dev.
