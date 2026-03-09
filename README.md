# Chimera

[![Stars](https://img.shields.io/github/stars/contactjccoaching-wq/chimera?style=social)](https://github.com/contactjccoaching-wq/chimera)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Bio-inspired optimization pipeline for Claude Code.**

> Three biological systems in sequence: explore everything, synthesize the best, catch the errors.

---

## What Chimera Does

Chimera takes any complex generation task and runs it through 3 bio-inspired stages to produce a better output than a single prompt could.

```
Task + Constraints
       │
       ▼
┌─────────────────┐
│ 0.5 CHEATSHEET  │  Inject winning strategies from persistent memory
│  (Positive)     │  Hot/Cold tiered, domain-filtered
└────────┬────────┘
         │ strategies injected into prompts
         ▼
┌─────────────────┐
│  1. SLIME MOLD  │  Explore ALL viable approaches → Prune by constraints
│  (Physarum)     │  Agent: Sonnet (expand) → Haiku (prune)
└────────┬────────┘
         │ 3-5 viable branches
         ▼
┌─────────────────┐
│  2. PRISM       │  N perspectives in parallel → Meritocratic compilation
│  (Sampling)     │  Agents: N × Sonnet → Sonnet (compiler)
└────────┬────────┘
         │ optimal fused output
         ▼
┌─────────────────┐
│  3. IMMUNE v3   │  Scan errors + detect new strategies → Learn both
│  (Adaptive)     │  Agent: Haiku (scanner) + dual persistent memory
└────────┬────────┘
         │
         ▼
   Optimized Output
```

Total: ~7 agent calls per run (expand, prune, N perspectives, compile, scan). Dual memory: antibodies (negative) + cheatsheet (positive).

---

## Domain-Agnostic

Chimera works for **any domain**. Perspectives adapt to the task:

| Domain | Perspectives | Example goal |
|--------|-------------|--------------|
| **Fitness** | Volume, Intensity, Recovery, Balance | muscle, strength, endurance |
| **Code** | Performance, Security, Maintainability, Scalability | refactor, optimize, secure |
| **Writing** | Clarity, Depth, Engagement, Accuracy | blog, technical, academic |
| **Research** | Breadth, Depth, Contrarian, Practical | explore, decide, critique |
| **Strategy** | Opportunity, Risk, Feasibility, Innovation | launch, pivot, grow |
| **Custom** | Define your own perspectives | anything |

---

## The Three Systems

### 1. Slime Mold (Physarum polycephalum)

Real slime mold explores ALL paths simultaneously, then retracts from dead ends. What remains is the optimal network.

**Expand** — A Sonnet agent generates every viable approach, combination, and alternative. No filtering yet.

**Prune** — A Haiku agent ruthlessly cuts branches that violate constraints. Only 3-5 viable paths survive.

### 2. PRISM (Parallel Refinement through Intelligent Synthesis and Multiplicity)

Based on the [PRISM Framework](https://github.com/contactjccoaching-wq/prism-framework). Each surviving path is developed from multiple angles simultaneously.

**Directed mode** (default) — N named perspectives each build a complete solution optimized for their angle. A meta-agent compiles the best of each using meritocratic arbitrage (not averaging).

**Stochastic mode** — N identical agents explore the same prompt. Pure LLM stochasticity produces diverse trajectories. The meta-agent fuses the results.

### 3. Immune System v3 (Hybrid Adaptive)

Dual persistent memory: **antibodies** (negative patterns to avoid) and **cheatsheet** (positive strategies to repeat). Each output is scanned for errors AND analyzed for new winning strategies. Both memories grow with every run.

The 100th output benefits from all errors caught AND all strategies discovered in the previous 99. See the standalone [Immune System](https://github.com/contactjccoaching-wq/immune) repo for details.

---

## Installation (Claude Code)

```bash
# Copy agents to your Claude Code agents directory
cp skill/agents/*.md ~/.claude/agents/

# Copy skill files
mkdir -p ~/.claude/skills/chimera
cp skill/skill.md ~/.claude/skills/chimera/
cp skill/config.yaml ~/.claude/skills/chimera/
cp skill/immune_memory.json ~/.claude/skills/chimera/
cp skill/cheatsheet_memory.json ~/.claude/skills/chimera/
```

Or for a specific project only:
```bash
cp skill/agents/*.md YOUR_PROJECT/.claude/agents/
mkdir -p YOUR_PROJECT/.claude/skills/chimera
cp skill/skill.md skill/config.yaml skill/immune_memory.json skill/cheatsheet_memory.json YOUR_PROJECT/.claude/skills/chimera/
```

## Usage

Once installed, use `/chimera` in Claude Code:

```
/chimera Refactor the authentication system for better security
→ auto-detects: domain=code, goal=secure

/chimera domain=fitness goal=muscle Programme pour homme 30 ans, intermédiaire, 4x/semaine
→ explicit domain and goal

/chimera domain=custom perspectives="cost,speed,quality,risk" Evaluate AWS to GCP migration
→ custom perspectives
```

## Simulation

Test the full pipeline locally without any API calls:

```bash
python simulate.py
```

Shows all 3 systems in action with mocked responses and full bio-event logs.

---

## Related Projects

| Project | Role |
|---------|------|
| **Chimera** *(this repo)* | 3-stage bio pipeline — *how to optimize* |
| **[Immune](https://github.com/contactjccoaching-wq/immune)** | Hybrid adaptive memory (cheatsheet + antibodies) — *what to remember* |
| **[PRISM](https://github.com/contactjccoaching-wq/prism-framework)** | N-parallel sampling + meritocratic synthesis — *what to ask* |
| **[Spinal Loop](https://github.com/contactjccoaching-wq/spinal-loop)** | Bio-inspired model routing — *who to ask* |
| **[DACO](https://github.com/contactjccoaching-wq/daco-framework)** | MCP tool orchestration — *what to do with it* |
| **[Smart Rabbit MCP](https://github.com/contactjccoaching-wq/smartrabbit-mcp)** | AI workout generator MCP server — [smartrabbitfitness.com](https://www.smartrabbitfitness.com) |

## Author

**Jacques Chauvin** — WNBF World Champion (4th), fitness AI systems builder.

## License

MIT — use it, fork it, build on it.
