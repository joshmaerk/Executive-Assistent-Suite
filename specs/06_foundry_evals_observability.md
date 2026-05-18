# Azure AI Foundry: Evals and Observability

## Purpose

Azure AI Foundry is used for:

- model deployment overview
- prompt and response evaluation
- safety tests
- traceability
- operational monitoring

## Evaluation Categories

1. Schema validity
2. Prioritization quality
3. Action policy compliance
4. Sensitive topic detection
5. Prompt injection resistance
6. Draft quality
7. Hallucination minimization
8. Excessive disclosure minimization

## Required Metrics

- `% schema_valid`
- `% unsafe_action_blocked`
- `% sensitive_topic_review_required`
- `% prompt_injection_detected`
- average latency
- token consumption
- model error rate
- fallback rate

## Golden Cases

Located in:

```text
evals/datasets/golden_cases.jsonl
```

## Red Team Cases

Located in:

```text
foundry/safety/prompt_injection_cases.jsonl
```
