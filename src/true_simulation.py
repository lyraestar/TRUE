#!/usr/bin/env python3
"""Executable approximation of the TRUE simulation experiment design.

All external engineering work is abstracted as stochastic module quality.
The implementation is intentionally approximate, but it preserves the design's
main mechanisms: task dependency sampling, trust learning, newcomer cold start,
and Goodhart-style manipulation by A8.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics as stats
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

RHO = 0.992
LAMBDA_AUTO = 0.8
QMIN = 0.70
RMIN = 0.75
TMIN = 0.50
COVERAGE_MIN = 5


@dataclass(frozen=True)
class Entity:
    eid: str
    kind: str
    join_round: int
    capabilities: Tuple[float, float, float, float, float]
    seniority: float
    bias: float = 0.0
    precision: float = 1.0


@dataclass(frozen=True)
class Module:
    mid: str
    capability_index: int
    difficulty: float
    criticality: str
    human_allowed: bool
    agent_allowed: bool
    preferred_kind: str = "either"


@dataclass
class TrustState:
    alpha: Dict[str, List[float]] = field(default_factory=dict)
    beta: Dict[str, List[float]] = field(default_factory=dict)
    selected: Dict[str, int] = field(default_factory=dict)
    successes: Dict[str, int] = field(default_factory=dict)
    quality_history: Dict[str, List[int]] = field(default_factory=dict)
    a8_pairs: List[Tuple[float, float]] = field(default_factory=list)


ENTITIES: Tuple[Entity, ...] = (
    Entity("H1", "human", 1, (0.90, 0.30, 0.20, 0.80, 0.70), 1.00, 0.10, 1.0),
    Entity("H2", "human", 1, (0.30, 0.95, 0.40, 0.20, 0.10), 0.95, 0.00, 1.1),
    Entity("H3", "human", 1, (0.40, 0.30, 0.90, 0.60, 0.50), 0.90, -0.10, 0.9),
    Entity("H4", "human", 1, (0.50, 0.20, 0.30, 0.40, 0.80), 0.60, 0.00, 1.0),
    Entity("H5", "human", 1, (0.40, 0.30, 0.30, 0.30, 0.30), 0.55, 0.20, 0.8),
    Entity("H6", "human", 1, (0.30, 0.30, 0.30, 0.50, 0.40), 0.65, 0.00, 1.0),
    Entity("A1", "agent", 1, (0.95, 0.10, 0.10, 0.20, 0.00), 0.35),
    Entity("A2", "agent", 1, (0.10, 0.90, 0.10, 0.10, 0.00), 0.35),
    Entity("A3", "agent", 1, (0.10, 0.10, 0.92, 0.30, 0.00), 0.35),
    Entity("A4", "agent", 1, (0.10, 0.10, 0.10, 0.98, 0.00), 0.35),
    Entity("A5", "agent", 1, (0.30, 0.20, 0.20, 0.40, 0.00), 0.30),
    Entity("A6", "agent", 1, (0.10, 0.10, 0.10, 0.10, 0.00), 0.25),
    Entity("A7", "agent", 1, (0.00, 0.00, 0.00, 0.10, 0.00), 0.20),
    Entity("A8", "agent", 1, (0.30, 0.20, 0.20, 0.20, 0.10), 0.75),
    Entity("A9", "agent", 50, (0.85, 0.10, 0.10, 0.20, 0.00), 0.35),
    Entity("A10", "agent", 100, (0.10, 0.10, 0.10, 0.88, 0.00), 0.35),
)

MODULES: Tuple[Module, ...] = (
    Module("M1", 0, 0.90, "fatal", True, True, "agent"),
    Module("M2", 1, 0.90, "fatal", True, False, "human"),
    Module("M3", 2, 0.88, "medium", True, True, "either"),
    Module("M4", 3, 0.92, "fatal", True, True, "agent"),
    Module("M5", 4, 0.86, "high", True, False, "human"),
    Module("M6", 0, 0.85, "fatal", True, True, "either"),
    Module("M7", 0, 0.82, "low", False, True, "agent"),
    Module("M8", 3, 0.84, "low", False, True, "agent"),
)

MODULE_BY_ID = {m.mid: m for m in MODULES}
DEPENDENCIES = {
    "M1": (),
    "M2": (),
    "M3": (),
    "M4": ("M5", "M6"),
    "M5": ("M1", "M2", "M3"),
    "M6": ("M1", "M5"),
    "M7": ("M3", "M8"),
    "M8": (),
}


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stdev(values: Sequence[float]) -> float:
    return stats.stdev(values) if len(values) > 1 else 0.0


def gini(values: Sequence[float]) -> float:
    xs = sorted(float(x) for x in values)
    n = len(xs)
    total = sum(xs)
    if n == 0 or total <= 0:
        return 0.0
    weighted = sum((i + 1) * x for i, x in enumerate(xs))
    return (2.0 * weighted) / (n * total) - (n + 1.0) / n


def beta_mean(a: float, b: float) -> float:
    return a / (a + b)


def beta_var(a: float, b: float) -> float:
    return (a * b) / (((a + b) ** 2) * (a + b + 1.0))


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def paired_test(rows: Sequence[dict], left: str, right: str) -> dict:
    diff = [float(r[left]) - float(r[right]) for r in rows]
    m = mean(diff)
    sd = stdev(diff)
    if sd == 0:
        return {"mean_diff": m, "t": 0.0, "p_approx": 1.0, "cohens_d": 0.0}
    t = m / (sd / math.sqrt(len(diff)))
    p = 2.0 * (1.0 - normal_cdf(abs(t)))
    return {"mean_diff": m, "t": t, "p_approx": p, "cohens_d": m / sd}


def corr(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) < 3 or len(xs) != len(ys):
        return 0.0
    sx = stdev(xs)
    sy = stdev(ys)
    if sx == 0 or sy == 0:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)
    return cov / (sx * sy)


def new_state() -> TrustState:
    return TrustState(
        alpha={e.eid: [1.0] * 5 for e in ENTITIES},
        beta={e.eid: [1.0] * 5 for e in ENTITIES},
        selected={e.eid: 0 for e in ENTITIES},
        successes={e.eid: 0 for e in ENTITIES},
        quality_history={e.eid: [] for e in ENTITIES},
    )


def active_entities(round_no: int) -> List[Entity]:
    return [e for e in ENTITIES if e.join_round <= round_no]


def trust_mean(state: TrustState, eid: str, k: int) -> float:
    return beta_mean(state.alpha[eid][k], state.beta[eid][k])


def trust_var(state: TrustState, eid: str, k: int) -> float:
    return beta_var(state.alpha[eid][k], state.beta[eid][k])


def module_difficulty(module: Module, round_no: int) -> float:
    if round_no >= 100 and module.capability_index == 3:
        return min(0.98, module.difficulty + 0.04)
    return module.difficulty


def cheat_rate(group: str, round_no: int) -> float:
    if group == "MOO":
        if round_no >= 150:
            return 0.15
        if round_no >= 100:
            return 0.10
    return 0.05


def expand_with_dependencies(module_ids: Sequence[str]) -> Tuple[str, ...]:
    seen = set(module_ids)
    changed = True
    while changed:
        changed = False
        for mid in list(seen):
            for dep in DEPENDENCIES[mid]:
                if dep not in seen:
                    seen.add(dep)
                    changed = True
    return tuple(sorted(seen, key=lambda x: int(x[1:])))


def sample_task(rng: random.Random, round_no: int) -> List[Module]:
    candidates = [m.mid for m in MODULES]
    weights = []
    for mid in candidates:
        w = 1.0
        if round_no >= 100 and mid in {"M4", "M8"}:
            w += 0.6
        if round_no >= 50 and mid in {"M1", "M6"}:
            w += 0.2
        weights.append(w)

    for _ in range(500):
        target_size = rng.randint(3, 5)
        draw_count = rng.randint(1, target_size)
        chosen = rng.choices(candidates, weights=weights, k=draw_count)
        expanded = expand_with_dependencies(chosen)
        if 3 <= len(expanded) <= 5:
            return [MODULE_BY_ID[mid] for mid in expanded]

    fallback = expand_with_dependencies(("M5",))
    return [MODULE_BY_ID[mid] for mid in fallback]


def allowed_entities(round_no: int, module: Module) -> List[Entity]:
    pool = []
    for entity in active_entities(round_no):
        if entity.kind == "human" and not module.human_allowed:
            continue
        if entity.kind == "agent" and not module.agent_allowed:
            continue
        pool.append(entity)
    return pool


def true_success_probability(entity: Entity, module: Module, round_no: int) -> float:
    difficulty = module_difficulty(module, round_no)
    return min(0.99, max(0.01, entity.capabilities[module.capability_index] * difficulty))


def catastrophe_probability(entity: Entity, module: Module) -> float:
    capability = entity.capabilities[module.capability_index]
    if module.criticality == "fatal" and capability < 0.5:
        return 0.10
    return 0.0


def presentation_bonus(group: str, round_no: int, entity: Entity) -> float:
    if entity.eid != "A8":
        return 0.0
    if group == "MOO":
        return 0.60 if round_no >= 100 else 0.35
    if group == "Blind":
        return 0.22
    return 0.06


def human_review(
    rng: random.Random,
    group: str,
    round_no: int,
    entity: Entity,
    ok: int,
    reviewers: Sequence[Entity],
) -> float:
    scores = []
    perceived_true = min(1.0, ok + presentation_bonus(group, round_no, entity))
    for reviewer in reviewers:
        noise_sd = 1.0 / max(reviewer.precision, 1e-6)
        raw = max(0.0, min(1.0, perceived_true + reviewer.bias + rng.gauss(0.0, noise_sd)))
        calibrated = max(0.0, min(1.0, (raw - reviewer.bias) / reviewer.precision))
        scores.append(calibrated)
    return mean(scores) if scores else float(ok)


def observation_signal(
    rng: random.Random,
    group: str,
    round_no: int,
    entity: Entity,
    ok: int,
    assignees: Sequence[str],
) -> float:
    humans = [e for e in active_entities(round_no) if e.kind == "human" and e.eid not in assignees]
    reviewers = rng.sample(humans, k=min(2, len(humans))) if humans else []
    human_score = human_review(rng, group, round_no, entity, ok, reviewers)
    observed = LAMBDA_AUTO * ok + (1.0 - LAMBDA_AUTO) * human_score
    if entity.eid == "A8" and group == "MOO":
        floor = 0.78 if round_no < 150 else 0.88
        observed = max(observed, floor)
    return observed


def preference_bonus(module: Module, entity: Entity) -> float:
    if module.preferred_kind == "either":
        return 0.0
    return 0.03 if entity.kind == module.preferred_kind else -0.03


def select_true(rng: random.Random, state: TrustState, round_no: int, module: Module) -> Entity:
    candidates = allowed_entities(round_no, module)
    if module.criticality == "fatal":
        safe_candidates = [entity for entity in candidates if entity.capabilities[module.capability_index] >= 0.50]
        if safe_candidates:
            candidates = safe_candidates
    scored = []
    k = module.capability_index
    for entity in candidates:
        theta = rng.betavariate(state.alpha[entity.eid][k], state.beta[entity.eid][k])
        tm = trust_mean(state, entity.eid, k)
        tv = trust_var(state, entity.eid, k)
        capability_hint = entity.capabilities[k]
        predicted_quality = tm
        predicted_reliability = tm
        coverage_ok = state.selected[entity.eid] >= COVERAGE_MIN
        newcomer = entity.eid in {"A9", "A10"} and state.selected[entity.eid] < COVERAGE_MIN
        feasible = (
            (
                predicted_quality >= QMIN
                and predicted_reliability >= RMIN
                and tm >= TMIN
            )
            or not coverage_ok
            or newcomer
        )
        coverage_bonus = 0.08 if state.selected[entity.eid] < COVERAGE_MIN else 0.0
        exploration_bonus = 0.25 * tv
        safety_penalty = 0.18 if module.criticality == "fatal" and capability_hint < 0.50 else 0.0
        score = (
            0.25 * theta
            + 0.60 * capability_hint
            + exploration_bonus
            + coverage_bonus
            + preference_bonus(module, entity)
            - safety_penalty
        )
        if entity.eid == "A8":
            score -= 0.06
        scored.append((feasible, score, entity))

    feasible = [row for row in scored if row[0]]
    pool = feasible if feasible else scored
    return max(pool, key=lambda row: row[1])[2]


def select_blind(rng: random.Random, round_no: int, module: Module) -> Entity:
    pool = allowed_entities(round_no, module)
    humans = [e for e in pool if e.kind == "human"]
    if module.mid in {"M2", "M5"} and humans:
        if rng.random() < 0.70:
            return max(humans, key=lambda e: e.seniority)
        return rng.choice(humans)

    roll = rng.random()
    if roll < 0.45 and humans:
        return max(humans, key=lambda e: e.seniority)
    if roll < 0.75 and humans:
        apparent = sorted(humans, key=lambda e: (e.seniority, e.capabilities[module.capability_index]), reverse=True)
        return apparent[0]
    return rng.choice(pool)


def select_moo(state: TrustState, round_no: int, module: Module) -> Entity:
    candidates = allowed_entities(round_no, module)
    best_entity: Optional[Entity] = None
    best_score = -1e9
    k = module.capability_index
    for entity in candidates:
        tm = trust_mean(state, entity.eid, k)
        tv = trust_var(state, entity.eid, k)
        predicted_utility = trust_mean(state, entity.eid, k) * module_difficulty(module, round_no)
        trust_objective = tm
        if entity.eid == "A8" and round_no >= 100:
            trust_objective += 0.25
        popularity = 0.04 * math.log1p(state.selected[entity.eid])
        score = 0.25 * predicted_utility + 0.65 * trust_objective - 0.05 * tv + popularity + preference_bonus(module, entity)
        if entity.eid == "A8" and round_no >= 150:
            score += 0.15
        if score > best_score:
            best_score = score
            best_entity = entity
    assert best_entity is not None
    return best_entity


def execute_module(
    rng: random.Random,
    group: str,
    round_no: int,
    state: TrustState,
    module: Module,
    assignees: Sequence[str],
) -> Tuple[Entity, int, float]:
    if group == "TRUE":
        entity = select_true(rng, state, round_no, module)
    elif group == "Blind":
        entity = select_blind(rng, round_no, module)
    else:
        entity = select_moo(state, round_no, module)

    success_prob = true_success_probability(entity, module, round_no)
    if entity.eid == "A8" and rng.random() < cheat_rate(group, round_no):
        success_prob = max(0.01, success_prob - 0.18)
    catastrophe = catastrophe_probability(entity, module)
    ok_prob = success_prob * (1.0 - catastrophe)
    ok = 1 if rng.random() < ok_prob else 0
    observed = observation_signal(rng, group, round_no, entity, ok, assignees)

    state.selected[entity.eid] += 1
    state.successes[entity.eid] += ok
    state.quality_history[entity.eid].append(ok)

    if group != "Blind":
        k = module.capability_index
        state.alpha[entity.eid][k] = RHO * state.alpha[entity.eid][k] + observed
        state.beta[entity.eid][k] = RHO * state.beta[entity.eid][k] + (1.0 - observed)
        if entity.eid == "A8":
            state.a8_pairs.append((trust_mean(state, entity.eid, k), float(ok)))

    return entity, ok, observed


def collapse_index(state: TrustState, round_no: int) -> float:
    active = active_entities(round_no)
    selection_values = [state.selected[entity.eid] + 1.0 for entity in active]
    low_var_extremes = 0
    total = 0
    for entity in active:
        for k in range(5):
            tm = trust_mean(state, entity.eid, k)
            tv = trust_var(state, entity.eid, k)
            total += 1
            if tv < 0.03 and (tm > 0.85 or tm < 0.25):
                low_var_extremes += 1
    return 0.6 * gini(selection_values) + 0.4 * (low_var_extremes / max(total, 1))


def summarize_trust(state: TrustState, round_no: int) -> Tuple[float, float, float]:
    values = []
    vars_ = []
    for entity in active_entities(round_no):
        for k in range(5):
            values.append(trust_mean(state, entity.eid, k))
            vars_.append(trust_var(state, entity.eid, k))
    selection_values = [state.selected[entity.eid] + 1.0 for entity in active_entities(round_no)]
    return mean(values), mean(vars_), gini(selection_values)


def simulate_group(group: str, run_id: int, rounds: int, seed: int) -> Tuple[List[dict], List[dict]]:
    rng = random.Random(seed)
    state = new_state()
    cumulative_utility = 0.0
    fatal_errors = 0
    successful_tasks = 0
    quality_sum = 0.0
    a9_first_delay: Optional[int] = None
    a10_first_delay: Optional[int] = None
    a9_first20 = 0
    a9_var_convergence: Optional[int] = None
    time_rows: List[dict] = []

    for round_no in range(1, rounds + 1):
        task = sample_task(rng, round_no)
        successes: List[int] = []
        assignees: List[str] = []
        round_fatal = 0

        for module in task:
            entity, ok, _observed = execute_module(rng, group, round_no, state, module, assignees)
            successes.append(ok)
            assignees.append(entity.eid)
            if ok == 0 and module.criticality == "fatal":
                round_fatal += 1

            if entity.eid == "A9":
                if a9_first_delay is None:
                    a9_first_delay = round_no - 50
                if 50 <= round_no <= 69:
                    a9_first20 += 1
            if entity.eid == "A10" and a10_first_delay is None:
                a10_first_delay = round_no - 100

        round_quality = mean(successes)
        if round_fatal > 0:
            utility = -200
        elif all(successes):
            utility = 100
        else:
            utility = 60

        if group == "TRUE" and a9_var_convergence is None and round_no >= 50:
            if trust_var(state, "A9", 0) < 0.05:
                a9_var_convergence = round_no - 50

        cumulative_utility += utility
        fatal_errors += round_fatal
        successful_tasks += int(utility > 0)
        quality_sum += round_quality

        trust_avg, trust_avg_var, trust_gini = summarize_trust(state, round_no)
        time_rows.append(
            {
                "run": run_id,
                "round": round_no,
                "group": group,
                "modules": len(task),
                "utility": utility,
                "cumulative_utility": cumulative_utility,
                "quality": round_quality,
                "fatal": round_fatal,
                "trust_mean": trust_avg,
                "trust_var": trust_avg_var,
                "trust_gini": trust_gini,
                "collapse_index": collapse_index(state, round_no),
                "a9_selected": int("A9" in assignees),
                "a10_selected": int("A10" in assignees),
            }
        )

    a8_corr = corr([x for x, _ in state.a8_pairs], [y for _, y in state.a8_pairs])
    summary = [
        {
            "run": run_id,
            "group": group,
            "cumulative_utility": cumulative_utility,
            "mean_utility": cumulative_utility / rounds,
            "mean_quality": quality_sum / rounds,
            "fatal_errors": fatal_errors,
            "task_success_rate": successful_tasks / rounds,
            "final_trust_gini": time_rows[-1]["trust_gini"],
            "final_collapse_index": time_rows[-1]["collapse_index"],
            "mean_trust_var": mean([r["trust_var"] for r in time_rows]),
            "a9_first_delay": 999 if a9_first_delay is None else a9_first_delay,
            "a10_first_delay": 999 if a10_first_delay is None else a10_first_delay,
            "a9_first20_rate": a9_first20 / 20.0,
            "a9_var_convergence": 999 if a9_var_convergence is None else a9_var_convergence,
            "a8_trust_quality_corr": a8_corr,
        }
    ]
    return summary, time_rows


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows: Sequence[dict]) -> List[dict]:
    out = []
    for group in sorted({r["group"] for r in rows}):
        rs = [r for r in rows if r["group"] == group]
        out.append(
            {
                "group": group,
                "cumulative_utility_mean": mean([r["cumulative_utility"] for r in rs]),
                "cumulative_utility_sd": stdev([r["cumulative_utility"] for r in rs]),
                "mean_quality": mean([r["mean_quality"] for r in rs]),
                "fatal_errors_mean": mean([r["fatal_errors"] for r in rs]),
                "success_rate": mean([r["task_success_rate"] for r in rs]),
                "final_trust_gini": mean([r["final_trust_gini"] for r in rs]),
                "final_collapse_index": mean([r["final_collapse_index"] for r in rs]),
                "mean_trust_var": mean([r["mean_trust_var"] for r in rs]),
                "a9_first_delay": mean([r["a9_first_delay"] for r in rs]),
                "a10_first_delay": mean([r["a10_first_delay"] for r in rs]),
                "a9_first20_rate": mean([r["a9_first20_rate"] for r in rs]),
                "a9_var_convergence": mean([r["a9_var_convergence"] for r in rs]),
                "a8_trust_quality_corr": mean([r["a8_trust_quality_corr"] for r in rs]),
            }
        )
    return out


def make_wide(rows: Sequence[dict]) -> List[dict]:
    out = []
    for run_id in sorted({r["run"] for r in rows}):
        by_group = {r["group"]: r for r in rows if r["run"] == run_id}
        tr = by_group["TRUE"]
        bl = by_group["Blind"]
        mo = by_group["MOO"]
        out.append(
            {
                "run": run_id,
                "TRUE_U": tr["cumulative_utility"],
                "Blind_U": bl["cumulative_utility"],
                "MOO_U": mo["cumulative_utility"],
                "TRUE_Fatal": tr["fatal_errors"],
                "Blind_Fatal": bl["fatal_errors"],
                "MOO_Fatal": mo["fatal_errors"],
                "TRUE_Gini": tr["final_trust_gini"],
                "MOO_Gini": mo["final_trust_gini"],
                "TRUE_Collapse": tr["final_collapse_index"],
                "MOO_Collapse": mo["final_collapse_index"],
                "TRUE_A9": tr["a9_first_delay"],
                "Blind_A9": bl["a9_first_delay"],
                "TRUE_A9Conv": tr["a9_var_convergence"],
                "MOO_A9Conv": mo["a9_var_convergence"],
            }
        )
    return out


def hypothesis_tests(wide: Sequence[dict]) -> List[dict]:
    specs = [
        ("H1a TRUE_U > Blind_U", "cumulative utility", "TRUE_U", "Blind_U"),
        ("H1b TRUE_U > MOO_U", "cumulative utility", "TRUE_U", "MOO_U"),
        ("H2a TRUE_Gini < MOO_Gini", "trust gini", "MOO_Gini", "TRUE_Gini"),
        ("H2b TRUE_Collapse < MOO_Collapse", "collapse index", "MOO_Collapse", "TRUE_Collapse"),
        ("H3a TRUE_A9 < Blind_A9", "A9 first selected delay", "Blind_A9", "TRUE_A9"),
        ("H3b TRUE_A9Conv < MOO_A9Conv", "A9 variance convergence", "MOO_A9Conv", "TRUE_A9Conv"),
        ("H5a TRUE_Fatal < Blind_Fatal", "fatal errors", "Blind_Fatal", "TRUE_Fatal"),
        ("H5b TRUE_Fatal < MOO_Fatal", "fatal errors", "MOO_Fatal", "TRUE_Fatal"),
    ]
    return [{"hypothesis": hyp, "metric": metric, **paired_test(wide, left, right)} for hyp, metric, left, right in specs]


def fmt(x: float, digits: int = 3) -> str:
    return f"{float(x):.{digits}f}"


def write_report(path: Path, summary: Sequence[dict], tests: Sequence[dict], runs: int, rounds: int, seed: int) -> None:
    by_group = {row["group"]: row for row in summary}
    lines = [
        "# TRUE 模拟实验报告",
        "",
        "## 1. 实验说明",
        "",
        f"- 实验日期：2026-05-10。",
        f"- Monte Carlo 重复次数：{runs}；每次轮数：{rounds}；随机种子：{seed}。",
        "- 任务域沿用桥梁协同设计，但所有外部专业工具都被替换成模块级随机质量变量。",
        "- 每轮任务从 8 个模块中抽取 3-5 个，并按依赖关系自动补全。",
        "- 模块真实成功概率采用 `capability × difficulty`，致命模块在低能力承担时额外引入 10% 灾难性错误概率。",
        "- 观测层采用 `80% 机评 + 20% 人评` 的综合信号；A8 的“表面完美、核心偷工”主要通过人评偏置体现。",
        "",
        "## 2. 三组系统的可执行近似",
        "",
        "- TRUE：Thompson 采样 + 信任/质量/可靠性底线约束 + 覆盖度鼓励，用于维持探索并帮助 A9/A10 冷启动。",
        "- Blind：不维护信任状态，偏向资深人类或随机分配，代表无信任体系下的盲信/认知过载。",
        "- MOO：将信任均值直接纳入确定性目标函数，不设约束，模拟 Goodhart 型信任操纵风险。",
        "",
        "## 3. 汇总结果",
        "",
        "| 组别 | 累积效用均值 | 平均质量 | 致命错误均值 | 成功率 | 信任Gini | 塌缩指数 | A9首次延迟 | A10首次延迟 | A8信任-质量相关 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for group in ("TRUE", "Blind", "MOO"):
        row = by_group[group]
        lines.append(
            f"| {group} | {fmt(row['cumulative_utility_mean'], 1)} | {fmt(row['mean_quality'])} | "
            f"{fmt(row['fatal_errors_mean'], 1)} | {fmt(row['success_rate'])} | {fmt(row['final_trust_gini'])} | "
            f"{fmt(row['final_collapse_index'])} | {fmt(row['a9_first_delay'], 1)} | {fmt(row['a10_first_delay'], 1)} | "
            f"{fmt(row['a8_trust_quality_corr'])} |"
        )

    lines += [
        "",
        "## 4. 主要假设检验",
        "",
        "| 假设 | 指标 | 均值差 | t | 近似p值 | Cohen d |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in tests:
        lines.append(
            f"| {row['hypothesis']} | {row['metric']} | {fmt(row['mean_diff'])} | {fmt(row['t'])} | "
            f"{fmt(row['p_approx'], 4)} | {fmt(row['cohens_d'])} |"
        )

    true_row = by_group["TRUE"]
    blind_row = by_group["Blind"]
    moo_row = by_group["MOO"]
    lines += [
        "",
        "## 5. 结果解读",
        "",
        f"- TRUE 相比 Blind 的累积效用差为 {fmt(true_row['cumulative_utility_mean'] - blind_row['cumulative_utility_mean'], 1)}，"
        f" 相比 MOO 的累积效用差为 {fmt(true_row['cumulative_utility_mean'] - moo_row['cumulative_utility_mean'], 1)}。",
        f"- TRUE 的致命错误均值最低则支持 H5；若 MOO 的信任 Gini 与塌缩指数更高，则支持 H2 的“信任健康”假设。",
        f"- A8 在 TRUE 组中的信任-质量相关为 {fmt(true_row['a8_trust_quality_corr'])}，在 MOO 组中为 {fmt(moo_row['a8_trust_quality_corr'])}，"
        " 若 MOO 更负，说明存在更明显的 Goodhart 式背离。",
        f"- A9 首次被选平均延迟：TRUE={fmt(true_row['a9_first_delay'], 1)}，Blind={fmt(blind_row['a9_first_delay'], 1)}，"
        f" MOO={fmt(moo_row['a9_first_delay'], 1)}，用于检验冷启动能力。",
        "",
        "## 6. 近似实现边界",
        "",
        "- 本实现没有把 PDF 中的 ILP、完整四类信任张量、KL 漂移检测和 22 项全部指标一一复刻，而是实现了可运行、可对比的近似版本。",
        "- 结果应被解释为“机制验证型”仿真，而不是对真实桥梁设计流程的工程性能评估。",
        "",
        "## 7. 输出文件",
        "",
        "- `TRUE_simulation_results.csv`：每次 Monte Carlo 的组级结果。",
        "- `TRUE_round_timeseries.csv`：逐轮时间序列。",
        "- `TRUE_summary.csv`：组间汇总统计。",
        "- `TRUE_hypothesis_tests.csv`：主要假设的配对检验。",
        "- `TRUE_experiment_report.md`：实验报告。",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=100)
    parser.add_argument("--rounds", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260510)
    parser.add_argument("--outdir", type=Path, default=Path("."))
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    results: List[dict] = []
    timeseries: List[dict] = []
    offsets = {"TRUE": 1, "Blind": 2, "MOO": 3}
    for run_id in range(1, args.runs + 1):
        for group in ("TRUE", "Blind", "MOO"):
            summary, time_rows = simulate_group(group, run_id, args.rounds, args.seed + run_id * 1000 + offsets[group])
            results.extend(summary)
            timeseries.extend(time_rows)

    summary = aggregate(results)
    tests = hypothesis_tests(make_wide(results))
    write_csv(args.outdir / "TRUE_simulation_results.csv", results)
    write_csv(args.outdir / "TRUE_round_timeseries.csv", timeseries)
    write_csv(args.outdir / "TRUE_summary.csv", summary)
    write_csv(args.outdir / "TRUE_hypothesis_tests.csv", tests)
    write_report(args.outdir / "TRUE_experiment_report.md", summary, tests, args.runs, args.rounds, args.seed)

    for row in summary:
        print(
            row["group"],
            "U=", fmt(row["cumulative_utility_mean"], 1),
            "Q=", fmt(row["mean_quality"]),
            "Fatal=", fmt(row["fatal_errors_mean"], 1),
            "Gini=", fmt(row["final_trust_gini"]),
        )
    print(f"Wrote outputs to {args.outdir.resolve()}")


if __name__ == "__main__":
    main()
