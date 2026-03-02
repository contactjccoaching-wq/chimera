---
name: chimera
description: "Bio-inspired optimization pipeline. 3 systems: Slime Mold (explore→prune) → PRISM (N perspectives→compile) → Immune (scan→correct). Domain-agnostic — works for fitness, code, writing, research, strategy, or custom domains."
---

# Chimera Pipeline Orchestrator

You orchestrate a 3-stage bio-inspired pipeline that improves the quality of any complex output. Each stage uses specialized subagents.

## Input Parsing

The user invokes Chimera with a task. Parse these parameters:

- **task**: What needs to be produced (required)
- **domain**: One of the presets (fitness, code, writing, research, strategy) OR "custom"
- **goal**: Sub-goal within the domain (determines perspective priority)
- **constraints**: Any hard limits (time, resources, audience, format, etc.)
- **perspectives**: (optional) Custom perspective names + descriptions. Overrides domain preset.
- **mode**: "directed" (named perspectives, default) or "stochastic" (N identical agents, pure PRISM)

If domain/goal are not specified, infer them from the task. If ambiguous, ask the user.

Example invocations:
```
/chimera Refactor the authentication system for better security
→ domain=code, goal=secure (inferred)

/chimera domain=fitness goal=muscle Créer un programme pour un homme de 30 ans, intermédiaire, 4 séances/semaine, salle complète
→ domain=fitness, goal=muscle (explicit)

/chimera domain=custom perspectives="cost,speed,quality,risk" Evaluate migration from AWS to GCP
→ custom perspectives
```

## Pipeline Execution

### Phase 0 — Setup

1. Read the config: `~/.claude/skills/chimera/config.yaml`
2. Determine domain and load perspectives from the matching preset (or use custom)
3. Determine perspective priority order from goal
4. Log: `[CHIMERA] Domain: {domain} | Goal: {goal} | Perspectives: {list}`

### Phase 1 — SLIME MOLD (Explore → Prune)

**Step 1.1 — Expansion**

Spawn the `chimera-slime-expand` agent (Sonnet) with this prompt:
```
DOMAIN: {domain}
TASK: {task description}
CONSTRAINTS: {all constraints}

Generate an exhaustive tree of all viable approaches for this task.
```

Log: `[SLIME:EXPAND] Generating approach tree...`
Wait for result. Parse the JSON.
Log: `[SLIME:EXPAND] ✓ {total_combinations} combinations found`

**Step 1.2 — Pruning**

Spawn the `chimera-slime-prune` agent (Haiku) with:
```
TASK CONSTRAINTS:
{original constraints}

EXPANSION TREE:
{JSON from step 1.1}

Prune all branches that violate the constraints. Keep 3-5 viable branches.
```

Log: `[SLIME:PRUNE] Pruning by constraints...`
Wait for result. Parse the JSON.
Log: `[SLIME:PRUNE] ✓ {total} → {viable_combinations} viable branches`
Log each major cut: `[SLIME:PRUNE] Cut: {removed} — {reason}`

### Phase 2 — PRISM (Parallel Perspectives → Compile)

**Step 2.1 — Parallel Generation**

Load the perspectives for the domain. For each perspective, spawn a `chimera-prism-perspective` agent (Sonnet).

**CRITICAL: Launch ALL perspective agents IN PARALLEL** (single message, multiple Agent tool calls).

Each agent gets:
```
DOMAIN: {domain}
TASK: {task description}
CONSTRAINTS: {constraints}

YOUR PERSPECTIVE: {perspective_name}
PERSPECTIVE INSTRUCTIONS: {perspective description from config}

VIABLE OPTIONS (from Slime Mold analysis):
{JSON from step 1.2}

Build a complete solution optimized for your perspective. Use ONLY the viable options above.
```

Log: `[PRISM:GEN] Launching {N} perspectives in parallel...`
Wait for ALL results.
Log: `[PRISM:GEN] ✓ {name} ({time}) | ✓ {name} ({time}) | ...` for each

**Step 2.2 — Compilation**

Determine priority order from config: `domains.{domain}.priority_by_goal.{goal}`

Spawn the `chimera-prism-compile` agent (Sonnet) with:
```
DOMAIN: {domain}
GOAL: {goal}
TASK: {task description}

PERSPECTIVE PRIORITY (highest to lowest):
{ordered list from config}

PERSPECTIVE SOLUTIONS:
--- Perspective: {name1} ---
{JSON solution 1}

--- Perspective: {name2} ---
{JSON solution 2}

... (all N perspectives)

Compile the optimal output using meritocratic arbitrage. When perspectives conflict, higher priority wins.
```

Log: `[PRISM:COMPILE] Compiling... priority: {p1} > {p2} > {p3} > {p4}`
Wait for result.
Log: `[PRISM:COMPILE] ✓ Anchor: {anchor_perspective} | Injections from: {list}`

### Phase 3 — IMMUNE SYSTEM (Scan → Correct → Update)

**Step 3.1 — Load Antibodies**

Read `~/.claude/skills/chimera/immune_memory.json`
Filter antibodies where `domain == current_domain` OR `domain == "_global"`
Keep max 20 most relevant (by seen_count descending, then severity).

Log: `[IMMUNE:SCAN] Loading {n} antibodies / {total} total`

**Step 3.2 — Scan**

Spawn the `chimera-immune-scan` agent (Haiku) with:
```
DOMAIN: {domain}
TASK: {task description}
CONSTRAINTS: {constraints}

COMPILED OUTPUT:
{JSON from step 2.2}

KNOWN ANTIBODIES:
{filtered antibodies JSON}

Scan the output for known patterns and new threats.
```

Log: `[IMMUNE:SCAN] Scanning...`
Wait for result.

If corrections applied:
  Log: `[IMMUNE:SCAN] ⚠ Match {antibody_id}: {original} → {corrected}`
If new threats detected:
  Log: `[IMMUNE:DETECT] New threat: {pattern}`

**Step 3.3 — Update Memory**

If `new_threats_detected` is not empty AND config `auto_add_threats` is true:
1. Read current immune_memory.json
2. For each new threat, add an antibody with:
   - id: "AB-{next_number}"
   - domain: from the threat's recommended_antibody
   - pattern, severity, correction: from the threat
   - seen_count: 1
   - first_seen: today's date
   - last_seen: today's date
3. Increment `stats.antibodies_total`
4. Write back to immune_memory.json

Log: `[IMMUNE:UPDATE] +{n} antibodies added → total: {new_total}`

Also increment `stats.outputs_checked` and `stats.issues_caught` (by number of corrections + threats).

### Phase 4 — Output

**4.1 — Present the final output**

Extract the `corrected_output` from the immune scan (or the compiled output if scan was clean). Present it in a human-readable format appropriate to the domain — NOT raw JSON.

Format the output naturally:
- For code: show the code/architecture with explanations
- For writing: show the actual text
- For fitness: show the program in a readable table format
- For research: show findings with sources
- For strategy: show the plan with action items

**4.2 — Bio Event Log**

After the output, show a summary block:

```
───
🧬 CHIMERA | domain={domain} | goal={goal}
   [SLIME]  {total_expanded} → {viable} branches
   [PRISM]  {N} perspectives | anchor={anchor} | {n_injections} injections
   [IMMUNE] {scan_result} | {n_corrections} corrections | {n_new_threats} new antibodies
   agents: {list of models used with counts}
```

## Error Handling

- If a subagent returns invalid JSON: retry once with a clarification prompt. If still invalid, log the error and continue with what you have.
- If the expansion produces 0 branches: skip pruning, ask the user to relax constraints.
- If all PRISM perspectives produce nearly identical outputs: note this and use the highest-confidence one directly (skip compilation).
- If the immune scan finds a critical threat: flag it prominently to the user with a ⚠️ marker.

## Stochastic Mode

When `mode=stochastic`, instead of named perspectives:
1. Skip loading perspective descriptions
2. Spawn N identical `chimera-prism-perspective` agents with the SAME prompt (no perspective instructions)
3. Each agent explores a different trajectory through LLM stochasticity
4. Compilation proceeds normally

This is pure PRISM — maximum variance from same distribution.
