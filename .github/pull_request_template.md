## Summary

## Changes

-

## Scope

- [ ] Prompt
- [ ] Schema
- [ ] API
- [ ] Power Automate
- [ ] Policy
- [ ] Eval/Test

## Test plan

- [ ] `ruff format --check .` && `ruff check .`
- [ ] `mypy src`
- [ ] `pytest`
- [ ] `python scripts/validate_schemas.py`
-

## Risk assessment

<!-- Was kann brechen? Reversibilität, Blast Radius, betroffene Use Cases. -->

## Agent Checklist

- [ ] Nur spezifizierte Features umgesetzt (kein Scope-Creep)
- [ ] Verhaltensänderungen durch Tests belegt
- [ ] Schemas/Beispiele konsistent
- [ ] Betroffene Doku aktualisiert (`README.md`, `AGENTS.md`, `CLAUDE.md`, Specs)

## Safety Checklist

- [ ] No secrets
- [ ] No real personal data
- [ ] No autonomous sending
- [ ] No autonomous calendar mutation
- [ ] Tests pass
