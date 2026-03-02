# Installing Chimera in Claude Code

## Quick Install (global — all projects)

```bash
# Agents
cp skill/agents/*.md ~/.claude/agents/

# Skill + config + immune memory
mkdir -p ~/.claude/skills/chimera
cp skill/skill.md ~/.claude/skills/chimera/
cp skill/config.yaml ~/.claude/skills/chimera/
cp skill/immune_memory.json ~/.claude/skills/chimera/
```

## Project-Specific Install

```bash
# From your project root
cp skill/agents/*.md .claude/agents/
mkdir -p .claude/skills/chimera
cp skill/skill.md skill/config.yaml skill/immune_memory.json .claude/skills/chimera/
```

## Verify Installation

In Claude Code, type `/chimera` — it should appear as an available skill.

## Agents Installed

| Agent | Model | Role |
|-------|-------|------|
| chimera-slime-expand | Sonnet | Explore all viable approaches |
| chimera-slime-prune | Haiku | Cut branches by constraints |
| chimera-prism-perspective | Sonnet | Build solution from one perspective |
| chimera-prism-compile | Sonnet | Meritocratic synthesis of perspectives |
| chimera-immune-scan | Haiku | Error detection + memory update |

## Configuration

Edit `~/.claude/skills/chimera/config.yaml` to:
- Add custom domain presets
- Adjust model choices per stage
- Configure immune system behavior

## Immune Memory

`immune_memory.json` grows automatically with each run. It ships with ~15 base antibodies across domains. Back it up if you want to preserve learned patterns across reinstalls.
