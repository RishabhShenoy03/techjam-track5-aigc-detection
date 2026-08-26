# Constitution Changelog

The constitution carries its own version, separate from product releases. Every amendment is recorded here with its reasoning, so no future cycle relitigates an undocumented decision (see [Foundation](./foundation.md) §5).

---

## v2.3.0 — 2026-07-24 — Automatic Routing

**Origin.** A user-reported failure: users were unsure whether they had to keep prefixing prompts with `/bureau`, and prompts sent without it were answered by a single solo agent — bypassing the multi-agent pipeline and defeating the Bureau's purpose. Fix scoped and human-approved 2026-07-24 (see the approved plan; no direction contract — this is a framework fix, not a project deliverable). This is the Bureau's **first harness-fired enforcement point**, and it directly addresses the "the Floor is prose, not mechanism" finding of `.bureau/contracts/direction_v7.md`.

**Why a MINOR bump.** Adds a new mechanism (a routing hook + the routing law) without shifting the order of authority or any existing governance rule. A new organ, not a breaking change.

### Added
- **`routing.md`** — new document: a project containing `.bureau/` is a Bureau, so **every prompt routes through the pipeline automatically** (no `/bureau` prefix). Defines the **complexity gate** (trivial → answer directly; substantive → convene) and the **quorum floor** (≥2 teams × ≥3 agents, ≥1 independent adversarial verifier, grounding over consensus) for substantive work, plus the per-prompt human override. *Reason: requiring a prefix made the pipeline opt-in per prompt; a forgotten prefix silently degraded the Bureau to the single-shot mode it exists to beat. Routing must be a property of project state (which can't be forgotten), not prompt text.*
- **`hooks/bureau-route-hook.sh`** — a `UserPromptSubmit` command hook that detects `.bureau/` in the project dir and injects the routing mandate into the turn's context (plain stdout; fast silent no-op off-Bureau). *Reason: the harness fires it on every prompt, so it is machinery the human cannot forget to invoke — unlike a prefix.*

### Changed
- **`overview.md`** — routing.md added to the Documents list. *Reason: a new law must be discoverable from the index.*
- **`commands/bureau.md`** — the `.claude/settings.json` the founding scaffold writes now registers the `UserPromptSubmit` routing hook alongside the existing overlay hooks. *Reason: new Bureaus must be routed from day one.*
- **`commands/bureau-sync.md`** — the adherence audit now checks that the routing hook is registered and remediates it if missing. *Reason: this is what heals existing Bureaus — the routing law is worthless in a project whose settings predate it.*
- **`commands/bureau-run.md`** — notes that operational sessions run under automatic routing. *Reason: reinforce the orchestrator stance the hook injects.*
- **`install.sh`** — `chmod +x` now covers `hooks/*.sh`. *Reason: a fresh clone must land the hook executable.*

### Attempted deletion (per Foundation §5)
Reviewed whether `/bureau` as a per-prompt entry point could now be **removed** entirely in favour of pure auto-routing. **Kept**, narrowed in role: `/bureau` is retained solely as the *founding* command (it creates `.bureau/` and the direction contract — the very state auto-routing keys on). It is no longer a per-prompt prefix. No rule was found safe to delete outright this cycle; the deletion pressure was discharged by removing the *prefix obligation* rather than a document.

### Reason
The Bureau's value over a single-shot call is decomposition + independent adversarial verification + grounding. A pipeline that a human must remember to invoke per prompt is a pipeline that silently doesn't run. Making Bureau-ness a property of the project — enforced by a harness hook, gated by complexity so trivia stays cheap — is what makes the pipeline the default instead of the exception.

---

## v2.2.0 — 2026-07-22 — The Tooling Workshop

**Origin.** The same founding team, **The Registry** (panel: Marcus Halloran, Strategist · Priya Venkataraman, Researcher · Dieter Krause, Critic), direction contract `.bureau/contracts/direction_v6.md`, human-ratified 2026-07-22. This release ships the second strand — the Tooling Workshop — after strand 1 (the Why-Ledger, v2.1.0).

**Why a MINOR bump.** This adds a new mechanism (durable, gate-verified agent tooling) without shifting the order of authority or any existing governance rule — it applies the *existing* deterministic gate to a new object (a tool). A new organ, not a breaking change.

### Added
- **`workshop.md`** — new document defining the Tooling Workshop: a curated, project-local home for agent-built tooling at `.bureau/workshop/` (separate from the project deliverable), with a three-state model (`ephemeral` → `durable-candidate` → `trusted`), promotion via a three-part deterministic gate (own test + regression + dedup) run outside agent write-scope, an index with a binding search-first norm, an on-demand dissolvable **librarian** consultancy that curates and administers the gate but cannot confer trust, the doing/grading firewall, and content-hash demotion/staleness handling. *Reason: agents rebuild the same throwaway scripts every session — a stochastic re-derivation of a step already solved; the Workshop makes the *how* durable so a tool built once is discovered, reused, and refined rather than duplicated.*

### Changed
- **`employees.md`** — the Consultant type now notes the Workshop librarian as an on-demand Consultant (Internal tooling developer sub-role) that curates and administers the gate but cannot confer trust by assent. *Reason: curation needs an owner, but a standing body with promotion authority would be the unaccountable team the dissolution trigger exists to prevent.*
- **`operating_principles.md`** — A-20 ("isolate grader from gradee") now cross-references the Workshop's doing/grading firewall as its capability-boundary enforcement. *Reason: reward-tampering generalises to grader-editing and survives safety training, so the principle needs a hard namespace firewall, not just a convention.*
- **`lifecycle.md`** — the deterministic gate now also governs tool promotion (a tool is `trusted` only on a green gate), and the health vector may include a workshop-health component (index freshness / trusted-tool reuse rate). *Reason: trust must be mechanical and un-fakeable, and an unmeasured Workshop cannot be held to the dissolution discipline.*
- **`commands/bureau-run.md`** — operational teams are now instructed on the search-first norm, declaring a tool's impact label, and that durable tools are promoted only via the gate. *Reason: reuse pays off only if discovery precedes building; the norm is worthless unless teams actually search before they build.*
- **`commands/bureau.md`** — the founding scaffold now includes `.bureau/workshop/` (trusted/ + candidates/ + index + gate.sh), separate from the project deliverable. *Reason: the tooling surface must exist and be named from day one.*

### Reason
The Why-Ledger (v2.1.0) made the *why* durable across dissolutions; the *how* was still rebuilt every session as throwaway scripts, re-introducing variance into steps already solved. The Workshop closes that gap by applying the constitution's own deterministic gate to tools — trust is earned by a model-independent check, never conferred by a team.

---

## v2.1.0 — 2026-07-22 — The Why-Ledger

**Origin.** A founding team, **The Registry** (panel: Marcus Halloran, Strategist · Priya Venkataraman, Researcher · Dieter Krause, Critic), produced direction contract `.bureau/contracts/direction_v6.md` — a constitutional revision adding durable org-memory that outlives the org chart. Human-ratified 2026-07-22 (this release wires in the first strand, the ledger; the Tooling Workshop is parked as M2).

**Why a MINOR bump.** This adds a new mechanism (durable decision records) without shifting the order of authority or any existing governance rule — a new organ, not a breaking change.

### Added
- **`decisions.md`** — new document defining the Why-Ledger: durable, immutable decision records at `.bureau/decisions/`, one per settled call, on a fixed schema (`what`, `alternatives_rejected`, `external_signal`, `team`, `date`, `supersedes`). The `external_signal` — a pointer to a model-independent artefact, or the literal `JUDGMENT — UNVERIFIED` — is the only field treated as evidence. *Reason: when a team dissolves its reasoning dies with it and the next team re-derives the *why* by crawling the corpus (lossy, slow); the ledger makes handover cheap and makes one audit possible — does what the Bureau did match why it said it would.*

### Changed
- **`operating_principles.md`** — A-11 ("state-based handoff, not summary-based") now cross-references the Why-Ledger as its implementation. *Reason: the principle was adopted but never built; the ledger is where a stateless agent's structured resume-state actually lives.*
- **`lifecycle.md`** — the cron watchdog now also auto-surfaces any settled call (a run-log footprint) lacking a ledger entry and any decision record with a stale supersedes-chain, mirroring how it already surfaces findings past target. *Reason: a decision log dies from silent abandonment, not a bad schema; an owned lifecycle outside agent write-scope is the antidote.*
- **`commands/bureau-run.md`** — operational teams are now instructed to write a Why-Ledger record at each settled call, with the required `external_signal`. *Reason: templates don't save a log; teams must actually write records for the ledger to exist.*
- **`commands/bureau.md`** — the founding scaffold now includes `.bureau/decisions/`, and founding is told to note the ledger obligation in the direction contract. *Reason: the memory surface must exist and be named from day one.*

### Reason
The constitution governed the org chart and the substrate but had no durable memory across dissolutions — the largest remaining gap in handover fidelity. The ledger closes it cheaply, annotating the *existing* run-log footprint rather than inventing a parallel event stream.

---

## v2.0.0 — 2026-07-10 — The Self-Correcting Rework

**Origin.** A meta-effort in which the Bureau used its own founding process to scrutinise and improve its constitution. Three founding panels (The Charter Assembly, The Extended Bench, The Keystone Panel) and an 8-researcher LLM-Behaviour Study Group produced four direction contracts (`.bureau/contracts/direction_v1..v4.md`) and three findings ledgers (`.bureau/feedback/2026-07-10-*`). Ratified by the human.

**Why a MAJOR bump.** The order of authority and the addition of a Floor above the mission are a significant scope shift in how the Bureau is governed.

### Added
- **`foundation.md`** — new top-of-constitution document. Establishes the order of authority `Human > Floor > Mission > Plan`; the thin, harness-enforced Floor; the mission as a canonical versioned artefact with a surviving guardian; the supremacy clause; and the self-amendment protocol with entrenched clauses. *Reason: the prior constitution could revise its direction contract and its product, but had no rule for amending itself, no limit above the mission, and orphaned mission-authority on founding dissolution — the single largest structural gap.*
- **`operating_principles.md`** — new document capturing 20 evidence-backed adoptions (A-1…A-20) from the LLM-behaviour research. *Reason: the constitution governed the organisation but never the substrate — how agents are actually prompted, verified, and judged on a single-model monoculture.*

### Changed
- **`overview.md`** — mission restated as the *task outcome* (not "orchestrate team structure"); "consensus strengthens output" replaced with "consensus is coverage, not correctness"; flatness scoped honestly to *operations* (partners named as a governance layer). *Reason: the old mission was org-centric, contradicting mission-first; consensus among correlated agents amplifies error (L-01); the flat/partner contradiction was unacknowledged.*
- **`communication.md`** — "mandatory/maximal" communication scoped to "purposeful, at scope boundaries" (resolves the mandatory-vs-recommended contradiction); consensus explicitly subordinated to model-independent checks; dissent preserved. *Reason: unbounded communication is O(n²) cost; agreement ≠ verification.*
- **`employees.md`** — Critic redefined around *independence via external grounding* (fresh context, adversarial brief, review against tests not rationale) rather than mere "distance"; added the note that role/persona labels do not improve accuracy (kept for scope/identity only). *Reason: a same-model Critic shares the author's blind spots and defers to it (self-preference + sycophancy).*
- **`teams.md`** — resolved the min-size contradiction (solo teams permitted only with recorded justification); grounded the max-9 ceiling in coordination cost; added an intra-team convergence point; added a falsifiable dissolution trigger + due-process record + symmetric protection for successful-but-quiet teams; "each added member must earn its cost." *Reason: fix the clause contradiction; make disposal non-arbitrary; more agents ≠ more accuracy.*
- **`partners.md`** — added a bounded deadlock ceiling (new proposals default to status quo; corrective matters escalate consultant → guardian → human); added the interpretation/precedent (adjudication) function; added an external check on partners (governance audit + human). *Reason: unbounded "no decision" could freeze the Bureau; there was no interpreter for the constitution's own text and no check on partners but partners.*
- **`lifecycle.md`** — cron converted to a closed loop (health-vector setpoint, measure-before-act, "in-band no action" as a valid positively-scored outcome, damping, watchdog, exploration operator); deterministic gate made mandatory; end-of-phase audit made mandatory; added cron resilience (catch-up-on-wake + frequent-cheap cadence) and observability (append-only run log at `.bureau/runs/`). *Reason: the cron was open-loop and rewarded activity (Goodhart/churn); the only model-independent sensor was optional; the human asked for missed-cycle resilience and visibility.*
- **`feedback.md`** — citation upgraded from present-and-locatable to **validated** (a second agent opens the source and quote-matches); added the error register (`.bureau/errors/`) and the governance audit. *Reason: a citation's presence does not establish grounding; a self-critical system must remember its own errors.*
- **`backlog.md`** — added single owning team + claim lock + aging backstop. *Reason: pull-by-scope with overlapping scopes drops or duplicates work.*
- **`founding_team.md`** — mission-guardian authority must survive dissolution; falsifiable success criteria mandatory before work; contract placed below constitution/mission in the supremacy order. *Reason: "escalate to founding" could point at a dissolved body; "make it better" is unfalsifiable.*

### Rejected (recorded so they are not relitigated)
- Persona-as-accuracy-booster; naive majority vote as correctness; multi-agent debate as an intrinsic truth-finder; "add random noise to context"; fine-tuning-based fixes. See `.bureau/feedback/2026-07-10-llm-behaviour-findings.md` §7.
- Cutting the employee-naming / first-and-last-day grammar: **kept** by explicit human decision (character/scope value), despite its context cost.

### Open points carried forward
- "Obey the law" placed as near-hard policy *just below* the Floor (not above the mission); the human may elect to promote it into the Floor.
- The health-vector components, the non-code deterministic oracle spec, and the deadlock hearing-count are left for the operational build to define and pre-register.

---

## v1.0.0 — prior — The original constitution
The founding framework: overview, employees, teams, communication, founding team, partners, lifecycle, external feedback, backlog. Eloquent and internally consistent, but with the structural gaps addressed above.
