---
name: ai-prompt-engineering
description: >-
  Guidelines and templates for designing reliable LLM prompts in automation workflows.
  Use when writing system prompts, structuring JSON schema outputs, setting up lead qualification criteria,
  or preventing LLM hallucinations.
---

# AI Prompt Engineering for Automations

## 1. The Structure of an Automation Prompt

Automation prompts differ from chat prompts: they require **strict predictability, zero conversational filler, and validated structured output**.

```text
[Role & Context]
You are an expert sales qualification analyst for [Company/Niche].

[Task]
Evaluate the provided inbound lead information and output a structured assessment.

[Evaluation Criteria & Scoring Rules]
- Tier A (Score 80-100): Clear budget fit, decision maker, urgent timeline, high synergy.
- Tier B (Score 50-79): Potential interest, smaller budget, or exploration phase.
- Tier C (Score 0-49): Spam, job applicants, unfeasible requests, or competitors.

[Output Format]
Output ONLY valid JSON matching this schema:
{
  "tier": "Tier A" | "Tier B" | "Tier C",
  "score": number (0-100),
  "qualification_reason": "string (1-2 sentences)",
  "pain_points": "string",
  "suggested_action": "string",
  "draft_reply": "string (ready-to-send personalized email response)"
}

[Input Data]
Name: {{ $json.name }}
Email: {{ $json.email }}
Company: {{ $json.company }}
Message: {{ $json.message }}
```

## 2. Guardrails to Prevent Failures

- **Never assume missing facts**: Explicitly instruct the model: *"If information is missing, mark as 'Not provided' rather than guessing."*
- **Strict JSON Enforcement**: Always use markdown json fences (` ```json `) or n8n's Structured Output Parser node.
- **Tone Alignment**: Ensure draft responses match the brand tone (e.g. consultative and friendly, never pushy).
