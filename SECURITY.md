# Security Policy

## Grundsatz

Dieses Projekt verarbeitet potenziell vertrauliche Microsoft-365-Daten. In produktiver Umgebung gelten mindestens:

- Least privilege
- Human-in-the-loop
- No autonomous external communication
- Redaction in logs
- Prompt-injection-resistant processing
- Audit trail for every recommended and executed action

## Secrets

Keine Secrets in Git. Verwende:

- Azure Key Vault
- Managed Identity
- Power Platform Connection References
- GitHub Environments / Actions Secrets nur für CI/CD-Metadaten

## Reporting

Sicherheitsprobleme nicht als öffentliches GitHub Issue mit Datenbeispielen melden.
