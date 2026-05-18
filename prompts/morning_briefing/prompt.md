# Use Case: EA_MorningBriefing

Analysiere den folgenden JSON-Input aus Outlook-Kalender und E-Mails.

Erstelle ein Morning Briefing für eine Führungskraft.

Bewerte:

- kritische Termine
- Vorbereitungserfordernisse
- Terminüberschneidungen
- fehlende Puffer
- relevante E-Mails vor Terminen
- offene Entscheidungen
- empfohlene E-Mail-Markierungen
- sinnvolle Antwortentwürfe

Regeln:

- Keine Termine verschieben.
- Keine E-Mails senden.
- Keine E-Mails löschen.
- Keine Archivierung empfehlen, wenn Unsicherheit besteht.
- Keine Annahmen treffen.
- Bei Unsicherheit "review_required": true.
- Bei HR-, Vorstand-, Compliance-, Kunden- oder Eskalationsthemen immer "review_required": true.
- Gib ausschließlich JSON gemäß Schema `morning_briefing_response` zurück.
