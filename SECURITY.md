# Security & Responsible Use

AgentsAllTheThings is a **defensive security education** project. It exists to make a real,
under-appreciated risk — prompt injection against coding agents — concrete and fixable.

## Safe by design

- **Everything is defanged.** Every scenario's "exfiltration" targets a loot sink on
  `127.0.0.1:8899` that you run yourself. No payload sends data to the internet.
- **The sink refuses to bind to a public interface.** It only listens on loopback.
- **All "secrets" are decoys.** The `.env` files contain obviously fake values
  (`sk-FAKE-...`, `AKIAFAKEDECOY...`). Nothing real is ever exposed.
- **The scenarios act only on your own machine and your own agent.** There is no capability
  here to attack a third party.

## Rules of use

- Use this **only** on agents, machines, and environments **you own or are explicitly
  authorized to test**.
- Do not adapt these payloads to target systems, agents, or people without authorization.
  Doing so may be illegal and is against the spirit of this project.
- When demonstrating, prefer a **sandboxed agent with no real credentials** and no default
  network egress.

## What you should take away

The lesson is not "agents are dangerous, don't use them." It's: **untrusted content that enters
an agent's context is executable input.** Treat "summarize / review / fetch / install this" as
running the content, and put deterministic guardrails and network isolation between your agent
and anything you don't control.

## Reporting

Found a way this repo could be misused, or a scenario that leaks real data instead of decoys?
Open an issue (omit any real secrets) or contact the maintainer. Please practice coordinated
disclosure for anything that could harm users.
