# Detection rules

Guardrails try to *prevent*. Detection tells you when something slipped through — or gives you
an answer during an incident. These rules operate on **agent tool logs** (the record of what the
agent read, ran, and fetched).

## `detect_exfil_sequence.py`

Flags the core signature of the attacks in this repo: **a secret file was read, then an outbound
request happened within a short window.** Either alone is normal; the sequence is the tell.

Try it against the bundled sample log:

```bash
python detect_exfil_sequence.py sample-agent-log.jsonl
# -> SUSPICIOUS: secret-read-then-egress sequence detected, exit=2
```

Point it at your own agent's tool log (one JSON object per line: `ts`, `tool`, `input`). Most
agents can emit this via a logging hook; wiring guidance will land alongside the v0.2 "black box"
recorder.

## Where this is going (v0.2)

The hard problem, per current DFIR practice: when an agent is hijacked, the *triggering
instruction* usually lived only in ephemeral context and is gone after the session. The planned
**black box** recorder ties each risky action back to the **specific piece of content** (which
file, which issue, which fetched page) present in context when the agent decided to act — so an
investigation has a root cause, not just an alert. Contributions welcome (see
[CONTRIBUTING.md](../../CONTRIBUTING.md)).

## Mapping

These behaviors map to **OWASP LLM01 (Prompt Injection)** and the **agentic Top 10 (ASI01)**,
and to **MITRE ATLAS** techniques around tool/agent abuse and exfiltration. A full mapping table
is a planned addition.
