# The Why-Ledger — Durable Decision Records

> When a team is dissolved (the norm — see [Teams](./teams.md)), its reasoning dies with it. The next team re-derives *why* a call was made by crawling the corpus — lossy and slow. The Why-Ledger is the durable record that lets a stateless agent resume from a **structured state block**, not by re-reading everything. This document *implements* the already-adopted principle A-11 (["state-based handoff, not summary-based"](./operating_principles.md), §5) — the constitution promised it; this is where it is built.

## Why this exists

A settled call carries three things a future reader needs: **what** was decided, **what was rejected**, and **the model-independent signal that settled it**. Without a record, the first two are reconstructed by guesswork and the third is lost entirely — so a later team cannot tell whether a past decision was *grounded* or merely *asserted*. The ledger makes handover cheap and makes one audit possible that is otherwise impossible: **does what the Bureau did match why it said it would?**

This is not a diary and not a rationale essay. The constitution distrusts stated reasoning — chain-of-thought is often confabulated (see [Operating Principles](./operating_principles.md) §3, A-4). The ledger is therefore built so that the **only field treated as evidence is a pointer to something the model cannot author**. The rest is handover legibility, never proof.

## The record

Decision records live at **`.bureau/decisions/`**, one file per decision. Records are **immutable**: a decision is never edited in place. When a later call overrides an earlier one, a **new** record is written that names the one it supersedes (the ADR discipline — supersede, don't edit). This preserves the trail so no future cycle relitigates an undocumented reversal.

### Schema (fixed — do not extend with free-form fields)

Ordered so reasoning precedes the settled answer (A-9, "reason before formatting"):

| Field | Required | Meaning |
|-------|----------|---------|
| `alternatives_rejected` | yes | What was considered and not chosen, terse. Handover legibility — **not evidence.** |
| `external_signal` | yes | **The only admissible-as-truth field.** A *pointer* to the model-independent artefact that settled it — a test path + result, a benchmark delta, a validated citation, or a recorded health-component reading. If the call was genuinely a judgment with no external signal, this field carries the literal `JUDGMENT — UNVERIFIED`. It is never left empty. |
| `what` | yes | The decision, in one line. Handover legibility — **not evidence.** |
| `team` | yes | The team that made the call. |
| `date` | yes | Absolute date (YYYY-MM-DD). |
| `supersedes` | no | The record id this one overrides, if any. |

**Why `external_signal` allows an explicit `JUDGMENT — UNVERIFIED` rather than forbidding unverified calls.** Forcing a signal where none exists would pressure agents to fabricate one — the opposite of the goal. Honest abstention is a first-class success (A-6): a recorded "settled by judgment, unverified" is *better* than a false claim of grounding, and it makes the ledger an audit instrument — the auditor can find exactly the unverified calls worth scrutiny instead of them hiding among the grounded ones. What is forbidden is a **silently empty** signal.

## What counts as a "settled call"

A ledger that logs everything is noise no auditor reads; a ledger that logs "whatever the agent feels like" is gameable (the embarrassing calls go unrecorded). The bright line, chosen to be **mechanically checkable**:

> A **settled call** is a decision that **moved a versioned artefact or a recorded health-component** — i.e. it left a footprint in the run log ([Lifecycle](./lifecycle.md), §Observability).

The ledger **annotates** that existing footprint with *why*; it does not invent a parallel event stream. This ties completeness to something already recorded outside agent write-scope, so "was every settled call logged?" becomes a comparison against the run log rather than a matter of opinion.

## Lifecycle — the anti-abandonment mechanism

A decision log dies not from a bad schema but from silent abandonment: the cost is paid now by the author, the benefit accrues later to someone else, so records stop being written. Templates do not save a log — an **owned lifecycle** does. Therefore:

- The self-evaluation **cron/watchdog** ([Lifecycle](./lifecycle.md)) auto-surfaces **any settled call (a run-log footprint) that lacks a ledger entry**, and any record whose `supersedes` chain is stale — exactly as it already auto-surfaces findings past their target. A missing record is a flagged gap, not a silent one.
- This check runs **outside agent write-scope** and is the ledger's **deterministic gate**: the ledger release is not declared until the watchdog demonstrably catches an omitted entry and a staled chain.

## How the ledger relates to the Bureau's other memory surfaces

The ledger must not fragment memory. Each existing surface keeps its distinct niche:

| Surface | Records | Where |
|---------|---------|-------|
| **Why-Ledger** | A *settled design/build call* + the external signal that settled it | `.bureau/decisions/` |
| **Error register** | An *overturned belief* — "we believed X; wrong because Y; the tell was Z" | `.bureau/errors/` (see [Feedback](./feedback.md)) |
| **Precedent register** | A *constitutional interpretation* — a binding ruling on the constitution's own text | see [Partners](./partners.md) |
| **Backlog** | An *open obligation* not yet closed | `.bureau/backlog/` (see [Backlog](./backlog.md)) |
| **Run log** | *Actions taken* — the tamper-proof footprint | `.bureau/runs/` (see [Lifecycle](./lifecycle.md)) |

If a call is *also* an overturned belief, it earns an error-register entry too; the ledger records the forward decision, the error register the reversal. They link, they do not duplicate.

## Discipline (binding)

- **The external signal is the only evidence.** No audit may pass on `what`/`alternatives_rejected` prose alone.
- **Mandatory but cheap.** The schema is fixed. Adding free-form rationale fields violates the concision rule (A-4, verbosity bias). Records are lines, not essays.
- **Immutable, supersede-not-edit.** Editing a superseded record in place is a violation.
- **One decision per record.**
