---
name: n8n-workflow-design
description: >-
  Procedures and best practices for designing, testing, and debugging n8n workflows.
  Use when creating or refactoring n8n nodes, configuring webhooks, structuring JSON data flow,
  or debugging workflow execution errors.
---

# n8n Workflow Design & Debugging Runbook

## Core Concepts to Master

1. **Items and JSON Structure**:
   - In n8n, data travels between nodes as an array of objects: `[ { json: { ... } } ]`.
   - To reference a field from the previous node: `{{ $json.fieldName }}`.
   - To reference a field from an earlier named node: `{{ $('Node Name').item.json.fieldName }}`.

2. **Trigger Patterns**:
   - **Webhook Trigger**: Ideal for external events (form submissions, API webhooks). Always set `Response Mode` to `Using 'Respond to Webhook' Node` for custom responses.
   - **Schedule Trigger**: Ideal for recurring cron tasks (daily digests, hourly scraping).
   - **Manual Trigger**: Useful for ad-hoc testing during development.

3. **Standard Workflow Architecture**:
   ```text
   [Trigger: Webhook/Schedule]
            │
            ▼
   [Data Sanitization / Edit Fields]
            │
            ▼
   [AI Processing: LLM / LangChain / Agent]
            │
            ▼
   [Routing / Conditional: If / Switch]
           / \
     (True)   (False)
       /         \
   [Priority]   [Standard / Fallback]
       \         /
        ▼       ▼
   [Output: Telegram / Email / Sheet]
   ```

4. **Testing Workflow Steps**:
   - Never build an entire 10-node workflow before testing. Test **one node at a time**.
   - Use n8n's "Test step" button on each node to verify incoming data and output shape.
   - For webhooks, use `curl` to fire sample payloads against the Test Webhook URL.
