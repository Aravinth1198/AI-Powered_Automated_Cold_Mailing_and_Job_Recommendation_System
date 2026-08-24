# Gemini node — resume bullet polishing

Placement: n8n node **3**, right after Split Out, right before the
`jake_resume_code_node.js` Code node.

## Node setup
- Node: **Google Gemini** (operation: "Message a Model") or **HTTP Request**
  to the raw Gemini API if you'd rather not add the credential type.
- Model: `gemini-2.5-flash` is enough for this (it's just rewriting text).
- **Important**: set the node to return plain text, then JSON.parse it in the
  next Code node — Gemini nodes don't have a native "force JSON" toggle, so
  the prompt itself has to demand JSON-only output.

## Prompt (paste into the "Prompt" / "Message" field)

Use an expression so it's built per-item from the webhook payload:

```
You are a professional resume writer. Rewrite the bullet points below into
punchy, resume-style bullets: start with a strong action verb, keep each
bullet under 20 words, and only quantify results that are already implied by
the input (never invent numbers that aren't there).

Do not invent new companies, dates, job titles, or projects. Only rewrite the
bullet text. Keep the same number of bullets per entry as the input.

Return ONLY valid JSON, no markdown fences, no commentary, in exactly this
shape:

{
  "work_experience": [ { "bullets": ["...", "..."] }, ... ],
  "projects": [ { "bullets": ["...", "..."] }, ... ]
}

The arrays must be in the same order as the input below, one object per
entry, so index 0 of the output work_experience array corresponds to index 0
of the input.

INPUT:
{{ JSON.stringify({
  work_experience: $('Webhook').item.json.body.user.work_experience,
  projects: $('Webhook').item.json.body.user.projects
}) }}
```

## Right after the Gemini node: a small Code node to parse its output

Gemini nodes return the model's raw text in `$json.text` (or similar,
check the node's actual output field name in your n8n version — it appears
under `content`/`text` depending on operation). Add a tiny Code node before
`jake_resume_code_node.js` that does:

```javascript
let gemini;
try {
  // Strip accidental markdown fences just in case the model adds them
  const raw = $json.text || $json.content || $json.output || '';
  const cleaned = raw.replace(/^```json\s*|\s*```$/g, '').trim();
  gemini = JSON.parse(cleaned);
} catch (e) {
  // Fall back to the user's original, unpolished bullets rather than
  // failing the whole job — the resume still gets sent, just unpolished.
  gemini = {};
}
return { json: { ...$json, gemini } };
```

This is what makes `$json.gemini` available to `jake_resume_code_node.js`.

## Why this two-step design

Asking Gemini to freely rewrite the *whole* resume risks it inventing dates,
company names, or metrics that never happened — a real risk for something
that goes out to an actual HR contact under the candidate's name. Restricting
Gemini to "reword these exact bullets, don't invent facts" and keeping every
other field (dates, employer, degree, tech stack) untouched in Python/Code
keeps the resume both fluent **and** factually anchored to what the user
actually typed.
