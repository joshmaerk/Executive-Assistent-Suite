# Security and Governance

## Required Controls

1. Human-in-the-loop for all write actions.
2. Least privilege Graph permissions.
3. No full mail body logging.
4. Prompt injection defense.
5. Sensitive topic detection.
6. Audit trail for recommended and approved actions.
7. Environment separation: dev / test / prod.
8. No secrets in Git.
9. No automatic external communication.
10. No autonomous calendar mutation.

## Least Privilege Orientation

For MVP prefer delegated permissions and existing Outlook connector where possible.

Graph permissions should be documented before tenant approval.

## Data Classification

Sensitive topics:

- HR
- Legal
- Compliance
- Board / Vorstand
- Customer complaint
- Audit / Revision
- Regulator
- Personal data
- Confidential strategy

Behavior:

- force review
- no auto action
- allow draft only as editable suggestion
