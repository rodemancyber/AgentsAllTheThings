# Defense — Scenario 01

The injection only works if the agent is *able* to (a) read a secret file and (b) reach an
arbitrary host. Take away either capability and the hijack fails even if the model is fooled.
Defense in depth means doing both — and adding a third layer so you'd *know* if it happened.

## Layer 1 — Block reads of secret files (deterministic)

Don't rely on the model deciding not to read `.env`. Enforce it outside the model with a
**PreToolUse hook** that inspects every file the agent tries to read and denies secrets.

This repo ships one: [`defenses/hooks/block_secret_reads.py`](../../defenses/hooks/block_secret_reads.py).
See [`defenses/hooks/README.md`](../../defenses/hooks/README.md) to wire it into your agent.
After it's active, step 2 of the attack can't even start — the agent is refused when it reaches
for `.env`.

## Layer 2 — Deny egress to non-allowlisted hosts

Even if some secret leaks into context, it can't leave if the agent can't reach the outside.
[`defenses/hooks/egress_allowlist.py`](../../defenses/hooks/egress_allowlist.py) blocks shell
commands and fetches to any host that isn't explicitly allowed. The sink at `127.0.0.1` is
*not* on the default allowlist, so the POST is dropped.

For real deployments, prefer a network-level deny-by-default egress policy (firewall / proxy)
over an in-agent check — an in-agent hook is a speed bump, a network policy is a wall.

## Layer 3 — Detect the pattern (so you'd know)

The signature of this attack is unmistakable in hindsight: **a secret-bearing file was read,
and shortly after, an outbound request was made.** [`defenses/rules/`](../../defenses/rules)
has a starter rule that flags exactly that sequence in agent tool logs.

## The human layer

- Treat "summarize / review / read this" as **running** the content, not just viewing it.
- Keep secrets out of the repo and out of the agent's reach entirely (secret managers, not `.env`).
- Run agents in a sandbox with no ambient credentials and no default internet egress.

## Verify the fix

Re-run [TRY-IT.md](TRY-IT.md) with the hooks active. The sink should stay silent, and the
agent should tell you it was blocked from reading `.env` (or from reaching the host).
