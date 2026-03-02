#!/usr/bin/env python3
"""
Chimera — Local Simulation

Runs the full 3-stage pipeline with mocked agent responses.
No API key needed. Shows all bio-events and pipeline flow.

Usage: python simulate.py
       python simulate.py --domain code
       python simulate.py --domain fitness
"""

import sys
import io
import json
import time
import argparse

# Force UTF-8 on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ════════════════════════════════════════════════════════
#  ANSI Colors
# ════════════════════════════════════════════════════════

B = "\033[1m"
D = "\033[2m"
R = "\033[0m"
CY = "\033[96m"
GR = "\033[92m"
YE = "\033[93m"
MG = "\033[95m"
RD = "\033[91m"
BL = "\033[94m"

# ════════════════════════════════════════════════════════
#  MOCK DATA — Code Refactoring Domain
# ════════════════════════════════════════════════════════

MOCK_CODE = {
    "task": {
        "domain": "code",
        "goal": "refactor",
        "task": "Refactor an 800-line authentication module into separate concerns",
        "constraints": [
            "Backward-compatible API",
            "No new dependencies",
            "Python 3.11+ / FastAPI",
            "Existing tests must pass"
        ]
    },
    "expand": {
        "domain": "code",
        "task_summary": "Refactor monolithic auth module into modular architecture",
        "branches": [
            {
                "approach": "Vertical slicing by feature",
                "description": "Split into auth_session.py, auth_jwt.py, auth_oauth.py, auth_password.py, auth_ratelimit.py",
                "sub_options": [
                    {"name": "One file per concern", "details": "5 files, each handles one responsibility", "alternatives": ["shared base class", "protocol interfaces"], "requirements": ["careful import management"], "compatibility_score": 0.9},
                    {"name": "Feature folders", "details": "auth/session/, auth/jwt/, etc. with __init__.py re-exports", "alternatives": ["flat structure"], "requirements": ["more complex imports"], "compatibility_score": 0.7}
                ],
                "compatibility_score": 0.9
            },
            {
                "approach": "Hexagonal architecture",
                "description": "Ports and adapters — auth logic in domain layer, frameworks in adapter layer",
                "sub_options": [
                    {"name": "Full hexagonal", "details": "Domain, ports, adapters separation", "alternatives": ["simplified 2-layer"], "requirements": ["significant restructuring"], "compatibility_score": 0.6},
                    {"name": "Simplified ports", "details": "Abstract interfaces for external deps only", "alternatives": ["duck typing"], "requirements": ["interface definitions"], "compatibility_score": 0.75}
                ],
                "compatibility_score": 0.7
            },
            {
                "approach": "Middleware chain",
                "description": "Convert each auth concern into a FastAPI middleware/dependency",
                "sub_options": [
                    {"name": "FastAPI Depends chain", "details": "Each concern is a dependency injected via Depends()", "alternatives": ["middleware stack"], "requirements": ["FastAPI patterns"], "compatibility_score": 0.85}
                ],
                "compatibility_score": 0.85
            },
            {
                "approach": "Strategy pattern",
                "description": "Auth strategies as interchangeable implementations behind a common interface",
                "sub_options": [
                    {"name": "Protocol-based strategies", "details": "Python Protocol class + concrete implementations", "alternatives": ["ABC", "duck typing"], "requirements": ["Python 3.8+"], "compatibility_score": 0.8}
                ],
                "compatibility_score": 0.8
            }
        ],
        "total_combinations": 47,
        "expansion_notes": "Explored architectural patterns applicable to monolith decomposition"
    },
    "prune": {
        "pruned_branches": [
            {
                "approach": "Vertical slicing — one file per concern",
                "description": "auth_session.py, auth_jwt.py, auth_oauth.py, auth_password.py, auth_ratelimit.py with shared types",
                "sub_options": [{"name": "5 modules + types.py", "details": "Clean separation, re-export from __init__.py for backward compat", "compatibility_score": 0.9}],
                "compatibility_score": 0.9
            },
            {
                "approach": "FastAPI Depends chain",
                "description": "Each concern as a FastAPI dependency, composable via Depends()",
                "sub_options": [{"name": "Dependency injection", "details": "Leverages FastAPI's built-in DI", "compatibility_score": 0.85}],
                "compatibility_score": 0.85
            },
            {
                "approach": "Strategy + vertical hybrid",
                "description": "Vertical split with Protocol interfaces for swappable strategies",
                "sub_options": [{"name": "Protocol-based modules", "details": "Best of both: clean files + swappable implementations", "compatibility_score": 0.82}],
                "compatibility_score": 0.82
            }
        ],
        "pruning_log": [
            {"removed": "Full hexagonal architecture", "reason": "Over-engineered for the scope — 2 sprint days not enough"},
            {"removed": "Feature folders with deep nesting", "reason": "Unnecessary complexity for 5 concerns"},
            {"removed": "Pure strategy pattern alone", "reason": "Doesn't solve the file organization problem"}
        ],
        "viable_combinations": 3,
        "pruning_notes": "3 viable approaches survive. All maintain backward compatibility via re-exports."
    },
    "perspectives": {
        "performance": {
            "perspective": "performance",
            "solution": {
                "summary": "Vertical split with lazy imports and connection pooling extracted to a shared module",
                "structure": {"modules": ["auth_jwt.py (stateless, fast)", "auth_session.py (cached lookups)", "auth_ratelimit.py (in-memory counter)"]},
                "key_decisions": [
                    {"decision": "Lazy import of heavy crypto libs", "rationale": "JWT validation shouldn't load OAuth libs", "trade_off": "Slightly more complex imports"},
                    {"decision": "In-memory rate limit cache", "rationale": "Avoid Redis round-trip for hot path", "trade_off": "Not distributed across instances"}
                ]
            },
            "strengths": ["Minimal import overhead", "Fast hot path for JWT validation"],
            "weaknesses": ["In-memory rate limiting doesn't scale horizontally"],
            "confidence": 0.85
        },
        "security": {
            "perspective": "security",
            "solution": {
                "summary": "Strict module boundaries with no cross-imports. Password hashing isolated with constant-time comparisons.",
                "structure": {"modules": ["auth_password.py (isolated, no external imports)", "auth_jwt.py (key rotation support)", "auth_oauth.py (state validation)"]},
                "key_decisions": [
                    {"decision": "Isolate password module completely", "rationale": "Minimize attack surface — no access to session or JWT internals", "trade_off": "Some code duplication for error types"},
                    {"decision": "Add key rotation to JWT module", "rationale": "Current single-key setup is a SPOF", "trade_off": "Additional complexity"}
                ]
            },
            "strengths": ["Strong isolation", "Key rotation ready", "Constant-time password comparison"],
            "weaknesses": ["More files to audit", "Some duplication"],
            "confidence": 0.88
        },
        "maintainability": {
            "perspective": "maintainability",
            "solution": {
                "summary": "Clean vertical split with comprehensive type hints, docstrings, and a facade class for backward compatibility.",
                "structure": {"modules": ["auth/__init__.py (facade re-exports)", "auth/jwt.py", "auth/session.py", "auth/oauth.py", "auth/password.py", "auth/ratelimit.py", "auth/types.py"]},
                "key_decisions": [
                    {"decision": "Facade in __init__.py", "rationale": "Old imports still work: from auth import validate_token", "trade_off": "One extra layer of indirection"},
                    {"decision": "Shared types.py", "rationale": "All modules use same AuthUser, AuthError types", "trade_off": "Tight coupling on types"}
                ]
            },
            "strengths": ["Zero breaking changes", "Easy to test each module independently", "Clear ownership"],
            "weaknesses": ["Facade can become a dumping ground over time"],
            "confidence": 0.92
        },
        "scalability": {
            "perspective": "scalability",
            "solution": {
                "summary": "Depends-chain architecture. Each concern is a FastAPI dependency, composable and independently scalable.",
                "structure": {"modules": ["deps/jwt_dep.py", "deps/session_dep.py", "deps/rate_limit_dep.py", "deps/auth_dep.py (composes others)"]},
                "key_decisions": [
                    {"decision": "FastAPI Depends() for composition", "rationale": "Native DI, can swap implementations per environment", "trade_off": "Tied to FastAPI"},
                    {"decision": "Redis-backed rate limiting", "rationale": "Distributed, works across instances", "trade_off": "New infra dependency"}
                ]
            },
            "strengths": ["Horizontally scalable", "Easy to add new auth methods", "Native FastAPI patterns"],
            "weaknesses": ["Redis dependency violates 'no new deps' constraint", "Tightly coupled to FastAPI"],
            "confidence": 0.78
        }
    },
    "compile": {
        "compiled_output": {
            "summary": "Vertical split into auth/ package with facade for backward compatibility. Isolated password module, lazy imports for performance, FastAPI Depends for composition.",
            "structure": {
                "auth/__init__.py": "Facade — re-exports all public functions for backward compat",
                "auth/types.py": "Shared types: AuthUser, AuthError, TokenPayload",
                "auth/jwt.py": "JWT validation + key rotation support (from security perspective)",
                "auth/session.py": "Session handling with cached lookups",
                "auth/oauth.py": "OAuth2 flows with state validation",
                "auth/password.py": "Isolated — password hashing with constant-time comparison",
                "auth/ratelimit.py": "In-memory rate limiting (no Redis — respects no-new-deps constraint)"
            }
        },
        "compilation_notes": {
            "anchor": "maintainability — strongest structure, zero breaking changes",
            "injections": [
                {"from_perspective": "security", "element": "Isolated password module + constant-time comparison", "reason": "Critical security improvement, low cost"},
                {"from_perspective": "performance", "element": "Lazy imports for crypto libs", "reason": "Free performance gain"},
                {"from_perspective": "security", "element": "JWT key rotation support", "reason": "Addresses real SPOF risk"}
            ],
            "conflicts_resolved": [
                {"perspectives": ["scalability", "constraints"], "winner": "constraints", "reason": "Redis violates no-new-deps — used in-memory rate limiting instead"}
            ]
        },
        "confidence": 0.91
    },
    "immune": {
        "scan_result": "corrected",
        "corrections_applied": [],
        "new_threats_detected": [
            {
                "pattern": "Facade re-export without deprecation warnings",
                "severity": "info",
                "location": "auth/__init__.py facade",
                "suggested_correction": "Add deprecation warnings on old import paths to encourage migration to new module paths",
                "recommended_antibody": {
                    "domain": "code",
                    "pattern": "facade re-export without deprecation path",
                    "severity": "info",
                    "correction": "Add deprecation warnings with target removal version"
                }
            }
        ],
        "corrected_output": "same as compile output with deprecation note added",
        "scan_summary": "1 minor improvement suggested — add deprecation warnings to facade"
    }
}

# ════════════════════════════════════════════════════════
#  MOCK DATA — Fitness Domain
# ════════════════════════════════════════════════════════

MOCK_FITNESS = {
    "task": {
        "domain": "fitness",
        "goal": "muscle",
        "task": "6-week hypertrophy program, 28yo intermediate male, 4x/week, full gym, lagging shoulders",
        "constraints": [
            "4 sessions/week max",
            "90 min/session",
            "Full gym",
            "Left shoulder impingement — no extreme overhead",
            "Intermediate — 2 years experience"
        ]
    },
    "expand": {
        "domain": "fitness",
        "task_summary": "6-week hypertrophy program for intermediate with shoulder limitation",
        "branches": [
            {"approach": "Upper/Lower split", "description": "4 days: 2 upper, 2 lower", "sub_options": [{"name": "Classic U/L", "compatibility_score": 0.85}], "compatibility_score": 0.85},
            {"approach": "Push/Pull/Legs/Arms", "description": "4-day rotation", "sub_options": [{"name": "PPL+Arms", "compatibility_score": 0.75}], "compatibility_score": 0.75},
            {"approach": "Push/Pull/Legs/Shoulders", "description": "Dedicated shoulder day for lagging delts", "sub_options": [{"name": "PPL+Shoulders", "compatibility_score": 0.9}], "compatibility_score": 0.9},
            {"approach": "Full body 4x", "description": "Full body each session with rotation", "sub_options": [{"name": "Daily undulating", "compatibility_score": 0.7}], "compatibility_score": 0.7},
            {"approach": "Bro split", "description": "Chest/Back/Legs/Shoulders+Arms", "sub_options": [{"name": "Classic bro", "compatibility_score": 0.65}], "compatibility_score": 0.65}
        ],
        "total_combinations": 83,
        "expansion_notes": "Explored all standard splits adaptable to 4-day frequency"
    },
    "prune": {
        "pruned_branches": [
            {"approach": "PPL + Dedicated Shoulders", "description": "Push/Pull/Legs + extra shoulder session for lagging delts", "sub_options": [], "compatibility_score": 0.9},
            {"approach": "Upper/Lower with shoulder emphasis", "description": "2 upper days with extra lateral/rear delt volume", "sub_options": [], "compatibility_score": 0.85},
            {"approach": "Upper/Lower/Push/Pull hybrid", "description": "Undulating 4-day with shoulder focus on push days", "sub_options": [], "compatibility_score": 0.8}
        ],
        "pruning_log": [
            {"removed": "Full body 4x", "reason": "Not enough volume per muscle for hypertrophy goal at intermediate level"},
            {"removed": "Bro split", "reason": "Only 1x frequency per muscle — suboptimal for hypertrophy"},
            {"removed": "Extreme overhead variations", "reason": "Contra-indicated by shoulder impingement"}
        ],
        "viable_combinations": 3,
        "pruning_notes": "3 splits survive. All allow 2x/week shoulder frequency while respecting impingement."
    },
    "compile": {
        "compiled_output": {
            "summary": "PPL + Shoulders split with progressive overload, avoiding extreme overhead. Lateral raises prioritized. Deload week 5.",
            "structure": {
                "Day 1": "Push (chest focus, no behind-neck press)",
                "Day 2": "Pull (back + rear delts + biceps)",
                "Day 3": "Legs (quad/ham/glutes)",
                "Day 4": "Shoulders + Arms (lateral emphasis, landmine press instead of OHP)"
            }
        },
        "compilation_notes": {
            "anchor": "volume",
            "injections": [
                {"from_perspective": "balance", "element": "1.5:1 pull:push ratio for shoulder health", "reason": "Critical given impingement history"},
                {"from_perspective": "recovery", "element": "Deload week 5, RPE progression 7→8→9→8→6→9", "reason": "Prevents overtraining at intermediate level"}
            ]
        },
        "confidence": 0.89
    },
    "immune": {
        "scan_result": "clean",
        "corrections_applied": [],
        "new_threats_detected": [],
        "corrected_output": "same as compiled",
        "scan_summary": "No known patterns matched. No new threats detected."
    }
}

# ════════════════════════════════════════════════════════
#  SIMULATION ENGINE
# ════════════════════════════════════════════════════════

def log(tag, msg, color=D):
    print(f"  {color}{B}{tag:20}{R} {msg}")

def simulate_domain(mock_data):
    task = mock_data["task"]
    domain = task["domain"]
    goal = task["goal"]

    print(f"\n{CY}{B}{'═'*60}{R}")
    print(f"{CY}{B}  CHIMERA PIPELINE — domain={domain} | goal={goal}{R}")
    print(f"{CY}{B}{'═'*60}{R}\n")
    print(f"  {D}Task: {task['task'][:80]}...{R}\n")

    # ── Phase 1: Slime Mold ──
    print(f"  {GR}{B}▸ PHASE 1 — SLIME MOLD{R}\n")
    time.sleep(0.3)

    expand = mock_data["expand"]
    log("[SLIME:EXPAND]", f"Generating approach tree...", BL)
    time.sleep(0.5)
    log("[SLIME:EXPAND]", f"✓ {expand['total_combinations']} combinations found", GR)

    prune = mock_data["prune"]
    log("[SLIME:PRUNE]", f"Pruning by constraints...", BL)
    time.sleep(0.3)
    log("[SLIME:PRUNE]", f"✓ {expand['total_combinations']} → {prune['viable_combinations']} viable branches", GR)

    for cut in prune["pruning_log"]:
        log("[SLIME:PRUNE]", f"Cut: {cut['removed']} — {cut['reason']}", YE)

    print(f"\n  {D}Surviving branches:{R}")
    for b in prune["pruned_branches"]:
        print(f"    {GR}•{R} {b['approach']} ({b['compatibility_score']})")

    # ── Phase 2: PRISM ──
    print(f"\n  {MG}{B}▸ PHASE 2 — PRISM{R}\n")
    time.sleep(0.3)

    perspectives = mock_data.get("perspectives", {})
    n_perspectives = len(perspectives) if perspectives else 4
    log("[PRISM:GEN]", f"Launching {n_perspectives} perspectives in parallel...", BL)
    time.sleep(0.6)

    if perspectives:
        parts = []
        for name, data in perspectives.items():
            parts.append(f"✓ {name} (conf={data['confidence']})")
        log("[PRISM:GEN]", " | ".join(parts), GR)
    else:
        log("[PRISM:GEN]", f"✓ {n_perspectives} perspectives completed", GR)

    compile_data = mock_data["compile"]
    notes = compile_data["compilation_notes"]

    priority_order = list(perspectives.keys()) if perspectives else ["p1", "p2", "p3", "p4"]
    log("[PRISM:COMPILE]", f"Compiling... priority: {' > '.join(priority_order)}", BL)
    time.sleep(0.4)
    log("[PRISM:COMPILE]", f"✓ Anchor: {notes['anchor']}", GR)

    for inj in notes.get("injections", []):
        log("[PRISM:COMPILE]", f"+ from {inj['from_perspective']}: {inj['element'][:60]}", CY)

    for conf in notes.get("conflicts_resolved", []):
        log("[PRISM:COMPILE]", f"⚡ Conflict {' vs '.join(conf['perspectives'])} → winner: {conf['winner']}", YE)

    # ── Phase 3: Immune ──
    print(f"\n  {RD}{B}▸ PHASE 3 — IMMUNE SYSTEM{R}\n")
    time.sleep(0.3)

    immune = mock_data["immune"]
    log("[IMMUNE:SCAN]", "Loading antibodies... 15 relevant / 15 total", BL)
    time.sleep(0.3)
    log("[IMMUNE:SCAN]", "Scanning compiled output...", BL)
    time.sleep(0.4)

    if immune["corrections_applied"]:
        for corr in immune["corrections_applied"]:
            log("[IMMUNE:SCAN]", f"⚠ Match {corr['antibody_id']}: {corr['original']} → {corr['corrected']}", RD)

    if immune["new_threats_detected"]:
        for threat in immune["new_threats_detected"]:
            log("[IMMUNE:DETECT]", f"New threat: {threat['pattern']}", YE)
        log("[IMMUNE:UPDATE]", f"+{len(immune['new_threats_detected'])} antibodies added", MG)

    log("[IMMUNE:SCAN]", f"Result: {immune['scan_result']} — {immune['scan_summary']}", GR)

    # ── Summary ──
    print(f"\n  {CY}{'─'*56}{R}")
    n_corr = len(immune["corrections_applied"])
    n_threats = len(immune["new_threats_detected"])
    agents_used = f"2×haiku + {n_perspectives + 2}×sonnet"
    print(f"  {D}🧬 CHIMERA | domain={domain} | goal={goal}{R}")
    print(f"  {D}   [SLIME]  {expand['total_combinations']} → {prune['viable_combinations']} branches{R}")
    print(f"  {D}   [PRISM]  {n_perspectives} perspectives | anchor={notes['anchor']} | {len(notes.get('injections',[]))} injections{R}")
    print(f"  {D}   [IMMUNE] {immune['scan_result']} | {n_corr} corrections | {n_threats} new antibodies{R}")
    print(f"  {D}   agents: {agents_used}{R}")
    print(f"  {CY}{'─'*56}{R}")


def main():
    parser = argparse.ArgumentParser(description="Chimera Pipeline Simulation")
    parser.add_argument("--domain", choices=["code", "fitness", "all"], default="all",
                        help="Which domain to simulate")
    args = parser.parse_args()

    print(f"""
{CY}{B}╔══════════════════════════════════════════════════════════╗
║          CHIMERA — LOCAL SIMULATION                      ║
║   3 bio-inspired systems × domain-agnostic pipeline      ║
╚══════════════════════════════════════════════════════════╝{R}

{D}No API calls. All responses are mocked.
Bio-events and pipeline flow are real.{R}""")

    if args.domain in ("code", "all"):
        simulate_domain(MOCK_CODE)

    if args.domain in ("fitness", "all"):
        simulate_domain(MOCK_FITNESS)

    print(f"\n{GR}{B}Simulation complete.{R}\n")


if __name__ == "__main__":
    main()
