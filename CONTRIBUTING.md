# Contributing

New scenarios and stronger defenses are very welcome. The bar is: **realistic, safe, and
teachable.**

## Adding a scenario

Copy the shape of an existing one under `scenarios/NN-short-name/`:

- `README.md` — the innocent task, the attack, the trust boundary it crosses, a real-world
  analog, a "Try it" recipe, and how to stop it. Keep it tight and concrete.
- `bait/` — the poisoned artifact (README, issue, page, manifest, …) plus a **decoy** `.env`
  if the scenario "steals" one.

### Hard requirements (non-negotiable)

1. **Defanged.** The payload must target the local sink (`http://127.0.0.1:8899`) or a local
   file — never a real external host.
2. **Decoy secrets only.** Use obviously fake values (`sk-FAKE-...`). Never commit anything real.
3. **No third-party targets.** A scenario must only affect the user's own agent/machine.
4. **Explain the fix.** Every attack ships with a defense. We teach protection, not just fear.

Run `python verify.py` before opening a PR — it checks that no real-looking secrets snuck in and
that the pieces are wired up.

## Adding a defense

- Guardrails go in `defenses/hooks/` (must read a tool-call JSON on stdin and block via exit
  code 2 + stderr reason).
- Detections go in `defenses/rules/` (operate on agent tool logs; exit 2 on a finding).
- Include a direct test invocation in the file's docstring so reviewers can run it in isolation.

## Style

- Prose over jargon. Assume a smart reader who is new to this specific risk.
- Every claim about behavior should be runnable. If you say "the agent does X," give the command
  that shows it.

## Roadmap ideas

- The **black box** recorder (tie risky actions to the content that triggered them).
- OWASP ASI / MITRE ATLAS mapping table.
- More scenarios: poisoned git commit messages, CI logs, screenshot/OCR injection, memory
  poisoning across sessions, RAG document poisoning.
- Sigma-style rules for common EDR/SIEM backends.
