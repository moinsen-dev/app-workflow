# Persönliche Standards anwenden

Ein Nutzerprofil hält wiederverwendbare Wünsche fest. `PLAN.md/Personalization` hält die im konkreten Projekt wirksamen Vorgaben mit Herkunft und Begründung fest. Der Tracker führt weiterhin allein Fortschritt und Belege.

## Einlesen und entscheiden

1. Aktuellen Auftrag, vorhandene AGENTS-/Projektregeln und tatsächlichen Projektstand lesen. Einen ausdrücklich angegebenen oder im Projekt referenzierten Profilpfad verwenden. Nicht alle privaten Verzeichnisse nach vermeintlichen Präferenzen durchsuchen.
2. Bei Bedarf ein neues Profil mit `workflow.py profile /gewählter/pfad/USER_PROFILE.md` erzeugen. Mit `init --user-profile /gewählter/pfad/USER_PROFILE.md` werden nur bekannte Felder übernommen. Das Profil selbst bleibt unverändert; es muss nicht im App-Repository veröffentlicht werden.
3. Werte im Projekt auflösen: aktuelle ausdrückliche Anweisung, konkrete Projektentscheidung, anwendbarer Nutzerstandard, begründeter Default. Ein Konflikt zwischen Auftrag und bestehender Identität verlangt den tatsächlichen Abgleich; eine Präferenz ist kein Auftrag zum Umbenennen.
4. `UNKNOWN` bis zur Klärung verwenden; `CONFLICT` markiert einen echten Widerspruch. `NONE` bedeutet bewusst keine zusätzliche Vorgabe. Für einen ausführbaren Plan jeden Wert mit `Source` und `Reason` konkretisieren. Naheliegende reversible Defaults entscheidet der Agent selbst; nur wesentliche fehlende Entscheidungen zurückfragen.

## Was die Felder bedeuten

| Bereich | Anwendung |
|---|---|
| language, collaboration | Sprache, Kommunikationsform, Grad der Autonomie und gewünschte Zusammenarbeit aus dem Auftrag |
| code_conventions | Bestehende Benennung, Struktur, Formatter, Paketmanager und sinnvolle Prüfregeln berücksichtigen |
| graphic_style, design_skill, brand_assets | Gewünschte Bildsprache, konkrete verfügbare Design-Fachhilfe, vorhandene Logos/Fonts/Farben und ihre Herkunft |
| bundle_prefix | Vorgabe für neue IDs; tatsächliche IDs jedes Targets stehen im Projekt und in Delivery/AppID |
| github_user, github_org, repo_visibility | Gewünschte Eigentümer und Sichtbarkeit; tatsächlichen Remote, angemeldetes Konto und Zielrechte vor Repository-Aktionen prüfen |
| preferred_stack, preferred_services | Passende Defaults; festgelegte Technologie oder produktive Anbieter werden nicht automatisch ersetzt |
| localization | Vorgesehene Produktsprachen; Antwortsprache und App-Lokalisierung getrennt entscheiden |
| release_defaults | Bevorzugte Verteilung; der konkrete Endzustand wird pro Plattform in Delivery gewählt |

Beispiel einer begründeten Abweichung: `github_org` stammt im Nutzerprofil aus Organisation A, das vorhandene Repository gehört Organisation B. Im Projekt wird B mit Quelle `project:git remote` und Begründung „bestehendes Produkt unverändert übernommen“ festgehalten. Keine Repository-Verschiebung ableiten. Entsprechend bleiben bereits verwendete Bundle-IDs erhalten; ein anderer Präfix gilt zunächst für neue Apps.

Bevorzugte Skills anhand tatsächlich verfügbarer Fähigkeiten prüfen. Wenn eine gewünschte Fachhilfe fehlt, Auswirkung benennen und innerhalb des Auftrags mit einer passenden vorhandenen Fähigkeit arbeiten. Eine persönliche Präferenz erlaubt keine ungefragte Installation, Veröffentlichung, Kontoerstellung oder Zahlung. Bereits erteilte konkrete Autorisierung gilt weiter.

Profiländerungen werden nicht automatisch in laufende Projekte gezogen. Bei beauftragter Übernahme den Unterschied prüfen, betroffene Projektwerte ändern und zugehörige Planung/Nachweise aktualisieren. Beim Import bleibt der aufgelöste Profilpfad mit Feldreferenz als Source erhalten; gleichnamige Profile sind dadurch unterscheidbar. Bei einem Rechnerwechsel die Referenz bewusst zuordnen, statt ein ähnlich benanntes Profil stillschweigend zu übernehmen. Geheimnisse, Zertifikatsinhalte, API-Tokens und private Accountausgaben gehören weder ins Profil noch in die kopierten Werte.
