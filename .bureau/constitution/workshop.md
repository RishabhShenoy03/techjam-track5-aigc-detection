# The Tooling Workshop — Reusable Internal Tooling

> Agents rebuild the same throwaway scripts every session. Each rebuild is a stochastic re-derivation of a step that was already solved — wasteful, and it re-introduces variance into work that could be deterministic. The Workshop is a curated, project-local home for agent-built tooling (**separate from the project deliverable**) so a tool built once is *discovered and reused*, and *refined* over time rather than duplicated. It is the sibling of the [Why-Ledger](./decisions.md): the ledger makes the *why* durable, the Workshop makes the *how* durable. Where the ledger records a decision, the Workshop records an executable capability — and a gate-verified tool's output is a model-independent check, native to the constitution's theory of truth ([Operating Principles](./operating_principles.md) §1).

## Why this exists

Reuse only pays off if two things hold: discovery is easy (an agent finds the existing tool before building a new one) and trust is earned (a tool is relied on only once something the model cannot author has verified it). Naive accumulation — a growing pile of unverified scripts — *degrades* performance: retrieval gets noisy, duplicates multiply, and a broken tool silently breaks its dependents. The Workshop is therefore built around a **gate**, not a folder. A tool is not "in the Workshop" because it was written; it is trusted because it passed a check.

**The load-bearing rule (F-1, direction_v6):** *the gate confers trust, never a team.* A tool is `trusted` iff its test passes the deterministic gate — mechanically, un-fakeably. No employee, no librarian, no partner may promote a tool by assent. This is the constitution's own law applied to a new object: "Truth is established by model-independent checks… never by peer agreement" ([Operating Principles](./operating_principles.md) §1); "Consensus never overrides the gate" ([Lifecycle](./lifecycle.md)).

## The three states

A tool is always in exactly one state. The **impact label the author declares is the routing signal** between the first two.

| State | Meaning | Who may rely on it |
|-------|---------|--------------------|
| `ephemeral` | Scratch, single-task, write-and-discard. **Encouraged** — no ceremony, lives in the author's scratch space, **never advertised.** (This convention ships free with the ledger MVP.) | Its author, for one task. Never indexed. |
| `durable-candidate` | The author has declared the tool should outlive the session. That declaration files it to the candidate queue. Usable **by its author, in a sandbox**, meanwhile. | **Only its author.** No other agent may depend on an ungated candidate. |
| `trusted` | Its test passed the deterministic gate (in CI, outside agent write-scope). It is in the Workshop index. | **Anyone.** |

**Transitions are mechanical, not editorial:**
- `ephemeral → durable-candidate`: the author's durability declaration. That is the only trigger.
- `durable-candidate → trusted`: **automatic on a green gate.** Entry into the index follows.
- `trusted → demoted/broken`: **automatic on a red gate** — a changed content hash, a broken dependency, or a now-failing test (see *Demotion*).

## The gate — three parts, not one

Promotion runs `.bureau/workshop/gate.sh`. It does **three** things, because a single "does its own test pass" check lets junk accumulate (Voyager; CRAFT; AWM — abstraction and dedup are what make a tool library reusable rather than a junk drawer):

1. **Test (a).** The tool's own co-located test passes. A tool with no passing test is never trusted.
2. **Regression (b).** The candidate breaks no existing trusted tool — the full trusted-tool test suite still passes with the candidate present. A regression-breaker is rejected.
3. **Dedup / redundancy (c).** The candidate's description/signature is checked against the index. A near-duplicate is rejected or flagged for merge — reuse-and-refine, not re-add.

The gate is **self-contained and deterministic** (no model involvement), and is meant to run **outside agent write-scope**. See *The write-scope assumption* below for what that means, honestly, today.

## Each tool is three co-located parts

A Workshop tool is never bare code. Each is stored as:
- **code** — the executable itself;
- **description** — a short line naming what it does, for retrieval (the search-first norm depends on this);
- **test** — beside the code; this is what the gate runs.

## The search-first norm (binding)

**Before building a durable tool, an agent must search the index first.** Reuse fails when discovery is weak — retrieval, not storage, is the bottleneck (CRAFT/AWM). A "store-after" discipline is worthless without a "look-before" one. An agent that builds a durable tool duplicating a trusted one has violated this norm, and the dedup check (gate part c) is the backstop that catches it.

## The doing/grading firewall (load-bearing, security-critical)

**The trusted-tool namespace and the verification namespace are disjoint.** No Workshop tool may write to, or run inside, the deterministic gate, the run log, or any verification harness. A tool crossing from *doing* to *grading* requires fresh re-review outside agent write-scope.

This is **stronger than "no tool grades its author's own output"** — it is a *capability boundary*. The reason is empirical: reward-tampering generalises from mild spec-gaming all the way to a model editing its own grader, and it survives safety training (Anthropic, "Sycophancy to Subterfuge"; METR). A tool built for an innocent task is one `import` away from sitting on the verification path. The gate statically audits every trusted tool for any reference to the verification namespace (`gate.sh`, `check_ledger.sh`, `.bureau/runs/`, the hash manifests) and for dynamic-exec/indirection patterns (`eval`, `bash "$var"`, `../..` traversal) that could reach the verifier without naming it, and **fails** on either. This sharpens [Operating Principles](./operating_principles.md) §7 ("isolate grader from gradee").

**Honest limit of the static audit:** it is *best-effort*, not adversary-proof. A determined tool could still reach the verifier by means the static scan cannot fully vet (heavy obfuscation, a path computed at runtime). The literal-token + dynamic-exec scan raises the cost and catches the naive and the moderately-clever cases; a truly robust boundary requires executing trusted tests in a sandbox with the verification paths made unreadable, which belongs to the [Foundation](./foundation.md) Tier-0 substrate and is deferred to it. We document this rather than overclaim a capability boundary the single grep does not, by itself, provide.

## Demotion + staleness

A `trusted` tool is a standing dependency, and its world drifts. Therefore:
- Every trusted tool is **content-hashed** into `.bureau/workshop/.hashes`. A changed hash, a broken dependency, or a now-red test **forces re-gate**.
- A trusted-tool failure **flips it to `demoted`/`broken`** so its dependents can be found and re-wired, and writes a mandatory entry to the [error register](./feedback.md) (`.bureau/errors/`) — error cascades are near-irreversible ([Operating Principles](./operating_principles.md) §6), so a silent break is unacceptable.

## The librarian consultancy (on-demand, dissolvable)

Curation — dedup, distilling candidates into clean reusable routines, retiring rotted tools — needs an owner. But that owner **cannot be a standing team**: a permanent body with promotion authority is exactly the unaccountable "look-busy" team the [dissolution trigger](./teams.md) exists to prevent, and it would duplicate or override the gate. So (F-1):

- The librarian is a **consultancy, commissioned on demand** when the candidate queue crosses a threshold, and it **dissolves when its scope closes** — like any team. It maps onto the [Consultant](./employees.md) employment type and the *Internal tooling developer* sub-role.
- It **owns curation and administers the gate — but cannot confer trust by assent.** Only the gate does. It administers a check it cannot fake.
- It is **falsifiably accountable**: it carries a pre-registered health-component (index freshness / candidate-queue latency / trusted-tool reuse rate), so it is subject to the same measured dissolution discipline as every team.

## The suggestion queue — curate offline, suggest online

An employee who hits a tool bug or has an improvement **files a request to `.bureau/workshop/queue.md` and keeps moving** — filing never blocks in-flight work ([Feedback](./feedback.md) intake discipline). All dedup and conflict resolution happen in the librarians' asynchronous pass, never in the request path. The queue is a **view/extension of the [Backlog](./backlog.md)**, not a new independent memory channel — it must not fragment memory.

## The write-scope assumption (stated honestly)

The gate is meant to run **outside agent write-scope** so an agent cannot promote a tool by editing its own success metric. Today, on a single machine in `bypassPermissions`, that isolation is **not yet enforced**: the agent could in principle edit `gate.sh`, `.hashes`, or `.claude/settings.json` itself. The Workshop therefore provides **tamper-evidence, not tamper-proofing**: the committed hash manifest and git history make any tampering *visible* (a hash mismatch, a diff to the gate), which is what is buildable and useful now. Real write-scope isolation is the job of the [Foundation](./foundation.md) Tier-0 sandbox/interlocks, and is deferred to it. This limitation is documented, not hidden — an interlock the agent can reason around is not yet an interlock, and we do not pretend otherwise.

**A further caveat specific to this framework repo:** `.bureau/` is gitignored here (runtime state is committed in the *deployed* project, not the framework clone), so in this repo the hash manifest and `gate.sh` are uncommitted and a change leaves no diff. Tamper-evidence via git history is therefore only real once `.bureau/` is committed in a deployed project.

## Discipline (binding)

- **The gate confers trust — never a person or team.** Promotion is a green gate, full stop.
- **The firewall is inviolable.** No Workshop tool on the verification path, ever.
- **Search before you build** a durable tool.
- **Trusted tools are content-hashed;** an in-place change to a trusted tool forces re-gate.
- **Every tool = code + description + test.** No bare scripts in the index.
- **The queue is non-blocking** and is a backlog view, not a fifth memory surface.
