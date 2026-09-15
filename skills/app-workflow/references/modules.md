# Zusatzbausteine

Für jedes Modul ausdrücklich `YES`, `NO` oder `UNKNOWN` eintragen. `NO` braucht eine projektbezogene Begründung. `YES` lädt die zugehörigen Checks. Ein später aktiviertes Modul wird durch `catalog` ausgegeben und in den Plan aufgenommen.

## Modules

| ID | When |
|---|---|
| auth | Anmeldung, Konten, Rollen oder persönliche Zugriffsrechte |
| remote | Backend, externe API oder mehrere Betriebsumgebungen |
| sync | Lokale und entfernte Daten oder mehrere Geräte |
| ai | Generierte oder klassifizierte Inhalte, lokale oder externe Modelle |
| payments | Käufe, Abonnements oder andere kostenpflichtige Aktionen |
| sensors | Kamera, Mikrofon, Standort, Bluetooth oder andere Sensoren |
| notify | Benachrichtigungen, Hintergrundarbeit oder zeitgesteuerte Aufgaben |
| files | Nutzergesteuerter Import, Export, Dokumente, Photos oder Zugriff außerhalb app-eigener Daten; interne Persistenz gehört zu CORE-010 |

## auth

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| AUTH-001 | P03 | always | Anmeldung, Abmeldung und Sitzungsablauf | Modul aktiv | Vollständige Abläufe einschließlich abgelaufener Sitzung prüfen |
| AUTH-002 | P03 | always | Zugriffsgrenzen und Kontowechsel | Modul aktiv | Falsches Konto oder fehlende Rolle erhält keine fremden Inhalte; Wechsel räumt passenden Zustand auf |
| AUTH-003 | P03 | conditional | Konto- und Datenlöschung | Konto wird angelegt oder entsprechende Löschung zugesagt | Vereinbarten Löschweg einschließlich entferntem Bestand prüfen |

## remote

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| REMOTE-001 | P02 | always | Erreichbarkeit und passende Konfiguration | Modul aktiv | Gewähltes Gerät erreicht den richtigen Dienst; localhost und Gerät sind getrennt bedacht |
| REMOTE-002 | P03 | always | Fehler, Timeout und verspätete Antworten | Modul aktiv | Fehler und Kontextwechsel überschreiben keinen neueren Nutzerzustand |
| REMOTE-003 | P05 | conditional | Betrieb, Wiederherstellung und Diagnose | Betrieb des Dienstes gehört zum Auftrag | Vereinbarten Betrieb und datensparsame Fehlerdiagnose prüfen |

## sync

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| SYNC-001 | P03 | always | Lokaler Stand und verzögerte Übertragung | Modul aktiv | Offline ändern, neu starten, verbinden; erwartete Daten kommen genau passend an |
| SYNC-002 | P03 | always | Konflikt, Wiederholung und Mehrfachzustellung | Modul aktiv | Konflikte und wiederholte Übertragung führen zum definierten Ergebnis |

## ai

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| AI-001 | P03 | always | Verfügbarkeit, Unsicherheit und brauchbarer Fallback | Modul aktiv | Nicht verfügbares Modell, unsichere Ausgabe und Fehler sind verständlich bedienbar |
| AI-002 | P03 | always | Ausgabeprüfung und Autorität der Anwendung | Modul aktiv | Ungültige oder verspätete Ausgabe wird geprüft; Vorschlag verändert keine unbestätigte feste Entscheidung |
| AI-003 | P01 | always | Datenumfang und Ressourcenbedarf | Modul aktiv | Reale Datenweitergabe, Gesamtverbrauch und vorhandene Freigaben passen zum Auftrag |

## payments

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| PAYMENTS-001 | P03 | always | Kauf, Abbruch und Wiederherstellung | Modul aktiv | Passende Testumgebung belegt Zustände und Wiederherstellung |
| PAYMENTS-002 | P03 | always | Berechtigung und wiederholte Ereignisse | Modul aktiv | Ausstehender, abgelaufener oder wiederholt gemeldeter Kauf gewährt nur korrekte Rechte |

## sensors

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| SENSORS-001 | P03 | always | Erlauben, Verweigern und nachträglicher Entzug | Modul aktiv | Passende Systemdialoge und Rückkehr aus Einstellungen auf geeignetem Ziel prüfen |
| SENSORS-002 | P03 | always | Echte Fähigkeit, Unterbrechung und frische Messung | Modul aktiv | Geeignetes Gerät liefert neue Daten nach Start; Unterbrechung und Wiederaufnahme sind geprüft |

## notify

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| NOTIFY-001 | P03 | conditional | Zustellung und Öffnen der richtigen Ansicht | Benachrichtigungen werden verwendet | Erlaubnis, Zeitbezug, Zustellung und Einstieg prüfen |
| NOTIFY-002 | P03 | conditional | Hintergrund, Suspendierung und Wiederaufnahme | Hintergrundarbeit wird verwendet | Systemunterbrechung erzeugt keinen erfundenen Fortschritt; Fortsetzung prüfen |

## files

| ID | Stage | Rule | Check | When | Proof |
|---|---|---|---|---|---|
| FILES-001 | P03 | always | Auswahl, begrenzter Zugriff und Abbruch | Modul aktiv | Gewählte Quelle und Zugriffsumfang bleiben korrekt; Abbruch verändert keinen Bestand |
| FILES-002 | P03 | always | Fehlerhafter Import oder unterbrochener Export | Modul aktiv | Ungültige Eingabe, Wiederholung und passender Wiederanlauf erhalten Daten und Herkunft |
