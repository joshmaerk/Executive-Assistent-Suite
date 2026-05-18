# API Contracts

## POST /api/v1/morning-briefing

### Request

See:

```text
schemas/requests/morning_briefing_request.schema.json
```

### Response

See:

```text
schemas/responses/morning_briefing_response.schema.json
```

## Error Model

```json
{
  "error": {
    "code": "schema_validation_failed",
    "message": "Model output did not match response schema.",
    "request_id": "uuid",
    "details": []
  }
}
```

## Policy

The API must never return executable unsafe actions. If the model proposes unsafe actions, they must be rewritten to safe recommendations or blocked.
