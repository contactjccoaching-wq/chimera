# Chimera Architecture — Deep Dive

## The Three Biological Systems

Chimera's pipeline mirrors three real biological optimization strategies, applied in sequence.

## System 1: Slime Mold (Physarum polycephalum)

### The Biology

Physarum polycephalum is a single-celled organism that solves optimization problems. Place food sources in a maze, and the slime mold:

1. **Expands** — sends tendrils down every possible path
2. **Retracts** — pulls back from dead ends and suboptimal routes
3. **Stabilizes** — the remaining network is the optimal connection graph

Researchers at Hokkaido University showed that Physarum can replicate the Tokyo rail network in 26 hours. No central brain. Just expand → prune → converge.

### The Implementation

**Expansion agent** (Sonnet) — receives a task and generates an exhaustive tree of approaches. No filtering, no judgment. Maximize coverage of the solution space.

**Pruning agent** (Haiku) — receives the tree + constraints and applies binary cuts. Each branch either survives or dies. No nuance needed — which is why Haiku is sufficient. Rules-based elimination.

**Why two separate agents?** Expansion requires creativity (what COULD work?). Pruning requires discipline (what MUST be cut?). These are opposing cognitive modes. Separating them prevents the expansion agent from self-censoring and the pruning agent from being creative.

---

## System 2: PRISM (Parallel Refinement through Intelligent Synthesis and Multiplicity)

### The Principle

Based on the [PRISM Framework](https://github.com/contactjccoaching-wq/prism-framework). The key insight: multiple perspectives on the same problem produce better solutions than a single perspective, IF the synthesis is meritocratic rather than democratic.

### Directed vs Stochastic

**Directed mode** — each agent receives a specific perspective to optimize for. The perspectives come from domain presets (e.g., for code: performance, security, maintainability, scalability). This guarantees coverage of critical angles.

**Stochastic mode** — all agents receive the identical prompt. Diversity comes from natural LLM sampling variance (temperature > 0.7). This is pure PRISM — no role-playing, no perspective bias. Best for open-ended tasks where you don't know what angles matter.

### The Compiler (Meta-Agent)

The compiler implements **meritocratic arbitrage**, not consensus:

1. **Find the anchor** — the most structurally sound solution (not the longest, not the most popular)
2. **Extract value** — from other solutions, take ONLY what adds non-redundant strength
3. **Priority-weight conflicts** — when perspectives disagree, the higher-priority perspective (determined by the goal) wins
4. **Produce one output** — that reads as a single coherent piece, not a compilation

This kills "consensus soup" — the mediocre average of all perspectives that naive voting produces.

---

## System 3: Adaptive Immune System

### The Biology

Your immune system maintains a memory of every pathogen it has ever fought. When a known virus appears, antibodies neutralize it immediately. When an unknown pathogen appears, the system creates new antibodies and adds them to memory for next time.

### The Implementation

**immune_memory.json** — a persistent file (survives between runs) containing antibody definitions:

```json
{
  "id": "AB-001",
  "domain": "code",
  "pattern": "SQL query avec string concatenation + input utilisateur",
  "severity": "critical",
  "correction": "Utiliser des prepared statements",
  "seen_count": 3,
  "first_seen": "2025-06-15",
  "last_seen": "2025-07-20"
}
```

**Scan agent** (Haiku) — receives the compiled output + relevant antibodies. Two-phase scan:
1. **Known patterns** — match against antibodies, apply corrections
2. **New threats** — independent analysis for domain-specific red flags

**Memory update** — new threats are automatically added as antibodies. The memory grows with every run.

### Why This Matters

The 1st run through Chimera has 10-15 base antibodies. By the 100th run, the immune memory has captured every error pattern that was ever detected. Quality compounds over time.

---

## Agent Model Selection

| Agent | Model | Why |
|-------|-------|-----|
| Slime Expand | Sonnet | Needs creativity to explore wide |
| Slime Prune | Haiku | Binary rule application — cheap and fast |
| PRISM Perspectives | Sonnet | Good quality/cost ratio for parallel calls |
| PRISM Compiler | Sonnet | Complex synthesis task |
| Immune Scanner | Haiku | Pattern matching — doesn't need power |

Total per run: 2 Haiku + (N+2) Sonnet calls. With N=4 perspectives: 2 Haiku + 6 Sonnet.

---

## Pipeline Data Flow

```
User Input
  ├── task: string
  ├── domain: string
  ├── goal: string
  └── constraints: string[]
        │
        ▼
[SLIME EXPAND] → JSON { branches: [...], total_combinations: N }
        │
        ▼
[SLIME PRUNE]  → JSON { pruned_branches: [...], pruning_log: [...] }
        │
        ▼
[PRISM ×N]     → N × JSON { perspective: "...", solution: {...} }
        │
        ▼
[PRISM COMPILE] → JSON { compiled_output: {...}, compilation_notes: {...} }
        │
        ▼
[IMMUNE SCAN]  → JSON { scan_result: "...", corrected_output: {...} }
        │
        ▼
Final Output (human-readable, formatted for domain)
```

Every intermediate JSON is passed from one agent to the next. The orchestrator (skill.md) manages the flow and logging.
