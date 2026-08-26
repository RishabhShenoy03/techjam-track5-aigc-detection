# Automatic Routing — the Bureau is a property of the project, not the prompt

> This document defines how prompts are routed to the Bureau pipeline. Its purpose is to close a real failure mode: prompts that silently bypass the multi-agent pipeline and get answered by a single solo agent, defeating the Bureau's reason to exist. It sits under the [Foundation](./foundation.md) and serves the [Operating Principles](./operating_principles.md); where it appears to conflict with them, they govern.

## 1. The rule

**A project that contains a `.bureau/` directory is a Bureau. Inside a Bureau, every prompt is a Bureau prompt** — it is routed through the pipeline automatically, whether or not the human typed `/bureau`. `/bureau` remains the *founding* command (it stands up a new Bureau and produces the direction contract); it is **not** a per-prompt prefix the human must remember. Once a Bureau exists, routing is automatic.

**Why.** Requiring a prefix made the pipeline opt-in per prompt. Humans forget; a forgotten prefix meant the prompt fell through to a single solo agent — no decomposition, no independent adversarial check, no grounding discipline. That is precisely the single-shot mode the Bureau exists to improve on. Routing must therefore be a property of the *project state* (does `.bureau/` exist), not of the *prompt text*, because project state is not something a human can forget to type.

## 2. The complexity gate

Routing is **not** "spawn a crowd on every prompt." Convening agents has a real cost, and [Operating Principles](./operating_principles.md) L-01 is explicit: same-model agents have correlated errors, so more agents buy *coverage*, not *correctness*, and **each added agent must earn its cost**. So the orchestrator classifies each request first:

- **Trivial** — a typo or one-line edit, a single-file lookup, a direct factual question about existing state, a quick clarification. **Handled directly**, no quorum. Spawning teams for trivia is itself a violation of L-01.
- **Substantive** — any feature, design, refactor, investigation, multi-file or multi-step work, or anything where correctness is load-bearing. **Must convene the pipeline** (§3) before concluding.

The gate is a judgement the orchestrator makes and should err toward convening when correctness matters and toward answering directly when it plainly does not.

## 3. The quorum floor

For **substantive** work, the minimum that counts as "the pipeline ran":

- **At least 2 teams, each of ≥3 named agents**, spawned via the Agent tool and run **in parallel**.
- **At least one independent adversarial verifier** — an agent whose job is to refute, not agree. Per [Operating Principles](./operating_principles.md) A-1/A-2, peer agreement among same-model agents is not evidence.
- **Grounding over consensus.** Every load-bearing claim must be settled by something the model cannot author — a test, a tool, an executed command, a primary source — not by agents agreeing. Coverage comes from the teams; correctness comes from the grounding.

The floor is a *minimum*, not a *cap*. Larger work takes more; the floor exists so substantive work never silently runs as a single agent. It is a floor on **structure**, deliberately not on headcount-for-its-own-sake — three correlated draws are not three independent checks, so the adversarial-verifier + grounding requirements are what make the quorum meaningful, not the number alone.

## 4. The human override

The human outranks the mission ([Foundation](./foundation.md) §1). If the human explicitly says "just answer", "no bureau", "quick", or similar for a given prompt, the orchestrator answers directly and does **not** force a quorum. The override is per-prompt and explicit; silence is not an override (silence routes normally).

## 5. Mechanism and honest status

Routing is enforced by a **`UserPromptSubmit` hook** (`hooks/bureau-route-hook.sh`), registered in the project's `.claude/settings.json`. The harness runs it on every prompt before the model sees it; if `.bureau/` is present, the hook injects the routing mandate into the turn's context. It is a fast, silent no-op in any non-Bureau project.

**This is a soft interlock, and the constitution says so plainly.** The hook is real harness machinery the human cannot forget to invoke — that part is genuine, and it is the Bureau's *first* harness-fired enforcement point (contrast the rest of today's Floor, which is prose the agent is asked to obey — see `.bureau/contracts/direction_v7.md`). But what the hook *injects* is a mandate the model is expected to follow, not a sandbox that makes bypass impossible. A model that ignores the injected mandate is not physically stopped.

**The hard-interlock upgrade** (not built here): a `Stop` hook that blocks turn completion unless the pipeline actually ran — verified against a marker the pipeline writes (e.g. team records or a run-log entry for this turn). That converts "the model is told to convene" into "the turn cannot end until it did." It is deferred because a marker check that lives outside agent write-scope presupposes enforcement machinery (the Tier-0 substrate) the Bureau has not yet built.

---

*Adopted as Constitution v2.3.0, 2026-07-24. See [Changelog](./changelog.md) for reasoning.*
