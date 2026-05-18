# Microsoft Graph Usage

Use Microsoft Graph for operations not sufficiently covered by the Outlook connector.

## Draft new message

```http
POST https://graph.microsoft.com/v1.0/me/messages
Content-Type: application/json

{
  "subject": "Subject",
  "body": {
    "contentType": "HTML",
    "content": "Draft body"
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "recipient@example.com"
      }
    }
  ]
}
```

## Create reply draft

```http
POST https://graph.microsoft.com/v1.0/me/messages/{message-id}/createReply
```

## Required Governance

Do not call `/send` in MVP.
