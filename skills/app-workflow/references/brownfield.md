# Bestehende Apps übernehmen

Lesen, wenn eine vorhandene App neu in diesen Workflow übernommen wird oder ihr vorhandener Plan einen beauftragten Änderungsumfang aufnehmen soll. Greenfield braucht diesen Bestandsabgleich nicht. Der Markdown-Vertrag und die CLI bleiben gleich; es gibt keinen gesonderten `--brownfield`-Schalter.

## 1. Auftrag und Arbeitswurzel abgleichen

Die tatsächliche App anhand ihrer Manifeste, Projektdateien und Einstiegspunkte bestimmen. Bei mehreren Apps im Repository das beauftragte Paket wählen. Ein leerer Ordner mit Git/README ist weiterhin ein möglicher Greenfield-Start.

Bestehende AGENTS-/CLAUDE-Regeln, relevante Änderungen, Architektur, Datenhaltung, App-IDs, Eigentümer, Design, Toolchain und Release-Stand lesen. Der bestehende Stack ist Ausgangspunkt. Eine neue persönliche Präferenz begründet weder einen Neuaufbau noch eine ID-/Repository-Änderung.

Den aktiven Auftrag konkret festhalten: zum Beispiel Workflow-Übernahme und Planung, Umsetzung einer Exportfunktion oder Vorbereitung einer vorhandenen App für TestFlight. Ein produktiv veröffentlichtes Gesamtprodukt macht einen lokalen Änderungsauftrag nicht automatisch zu einer neuen Veröffentlichung. Bereits autorisierte Umsetzung läuft nach der Integration weiter; eine zusätzliche Routinefreigabe ist nicht erforderlich.

## 2. Bestand und Änderung auseinanderhalten

Im Abschnitt `Bestand und Änderungsumfang` von PLAN.md knapp festhalten:

| Bereich | Benötigte Information |
|---|---|
| Ausgangsstand | Relevanter Checkout/Dateistand, vorhandene Änderungen, tatsächlicher Build, Modus und Zielumgebung, soweit bekannt |
| Vorhandene Funktion | Was Code oder Unterlagen zeigen und was tatsächlich geprüft wurde; passende Quelle beziehungsweise aktueller Beleg |
| Gewünschte Änderung | Nutzeranforderung, erwartetes Verhalten und betroffene Use Cases |
| Zu erhaltendes Verhalten | Relevante bestehende Abläufe, Daten, Identitäten, Designentscheidungen und fremde Änderungen |
| Offene Lücke | Noch fehlende Umsetzung oder Prüfung, zugehörige Aufgabe, gegebenenfalls konkrete Blockade |

Dafür keine zweite Statusliste anlegen: Aufgabenstatus bleiben ausschließlich in TRACKER.md. Eine existierende Implementierung muss nicht erneut gebaut werden, um einen Check abzudecken. Im vereinbarten Umfang eine passende Bestandsprüfung zuordnen; vorhandene aktuelle Belege können nach inhaltlichem Abgleich verwendet werden. Code vorhanden, Build erfolgreich und Nutzerablauf beobachtet sind verschiedene Aussagen. Alte Fertigmeldungen ohne passenden aktuellen Nachweis werden nicht als ERLEDIGT übernommen.

Bei einem reinen Planungsauftrag genügt die gelesene und klar als ungeprüft gekennzeichnete Ausgangslage mit konkreten späteren Prüfaufgaben. Der Auftrag erfordert keinen zusätzlichen Live-App-Start. Bei Umsetzung betroffene bestehende Abläufe vor beziehungsweise nach der Änderung passend prüfen, sodass eine Verschlechterung des zugesagten Verhaltens erkennbar wird.

Den Katalog vollständig einordnen, aber auf den vereinbarten Änderungsumfang beziehen. Bereits erfüllte Punkte durch passende Nachweise abdecken; bedingte, unzutreffende Punkte begründen. Bekannte unabhängige Altprobleme knapp in den Entscheidungen erhalten; sie werden nur bei Relevanz für das aktive Ziel zu dessen Aufgaben. Eine einzelne Feature-Änderung erteilt keinen Auftrag, das gesamte Produkt zu überarbeiten.

## 3. Vorhandene Dokumentrollen integrieren

- **Keine kollidierenden Workflow-Dateien:** `init` in der tatsächlichen App-Wurzel erzeugt neue Unterlagen. Es untersucht oder verändert keinen App-Code; den gelesenen Bestand anschließend in den Plan übernehmen.
- **AGENTS.md, PLAN.md, TRACKER.md, STATE.md oder gewünschte CLAUDE.md bereits vorhanden:** Vor dem Schreiben lesen. Der Generator verweigert ein Überschreiben. Einen separaten Entwurf erzeugen und Definitionen, Regeln, Status und Belege gezielt integrieren.
- **Andere Dokumentnamen oder eigenes Altschema:** Rollen im neuen Einstieg benennen. Produktwissen und aktive Anweisungen erhalten; bisherige Aufgaben-/Statusangaben in die maßgeblichen Tabellen überführen. Falls eine Umstrukturierung erforderlich ist, den bisherigen Stand nachvollziehbar als Historie erhalten und die aktive Fortsetzung eindeutig verlinken. Keine zwei konkurrierenden bearbeitbaren Tracker führen.
- **Dieser Workflow bereits vorhanden:** Direkt daraus fortsetzen; für eine neue Anforderung stabile neue IDs ergänzen. Bei älterer Vorlage die [Versionsübernahme](format.md#versionsübernahme-10-auf-11) anwenden und historische Belege nicht nachstempeln.

Die vier maßgeblichen Dateien liegen in der tatsächlichen App-Wurzel. Das Werkzeug erwartet sie dort und erlaubt für `Files`/`Report` nur Pfade innerhalb dieser Wurzel. Der separate Entwurf ist keine zweite aktive App und wird nicht als Nachweis für den vorhandenen Code geprüft. Sind maßgebliche Quellen außerhalb eines App-Pakets geteilt, eine passende gemeinsame Arbeitswurzel wählen und die relevante App darin eindeutig benennen.

## 4. Übergang in den normalen Ablauf

1. Bestand, persönlichen Projektschnappschuss, Katalog und konkrete Änderungsaufgaben samt Abhängigkeiten abgleichen. Zu erhaltende relevante Abläufe in die Prüfkriterien aufnehmen.
2. Planreview erfassen, Tracker/State aktualisieren und `check --ready` bestehen. Der Prüfer validiert die dokumentierten Zuordnungen; er entdeckt vorhandene Funktionen nicht selbstständig.
3. Bei reiner Planung hier mit offenem Umsetzungsstand abschließen. Bei autorisierter Umsetzung die nächste ausführbare Aufgabe bearbeiten, betroffene neue und bestehende Abläufe prüfen und den Kritiker einsetzen.
4. Nur den vereinbarten Umfang abschließen. Ein erfolgreicher Bestandscheck ist kein Nachweis einer neuen Funktion; eine alte Store-Version ist kein Nachweis der Auslieferung des neuen Builds.
