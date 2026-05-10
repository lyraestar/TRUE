#!/usr/bin/env python3
"""Scenario-family TRUE simulation experiment.

This version upgrades the original prototype into a configurable family of
probabilistic scenarios. The task domain stays the same, but scenario
differences are encoded through utility models, observation models, and
probability assumptions rather than external tools.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics as stats
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

RHO = 0.992
BASE_QMIN = 0.70
BASE_RMIN = 0.75
BASE_TMIN = 0.50
BASE_COVERAGE_MIN = 5


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


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    success_reward: float
    partial_reward: float
    fatal_penalty: float
    lambda_auto: float
    difficulty_shift: float
    fatal_difficulty_bonus: float
    catastrophe_rate: float
    dependency_penalty: float
    dependency_repair_threshold: float
    dependency_repair_strength: float
    surface_alignment: float
    surface_bias: float
    truth_delay: int
    a8_surface_bonus: float
    a8_true_penalty: float
    moo_trust_bonus: float
    task_weight_bonus: Dict[str, float]
    misalignment_rounds: Optional[Tuple[int, int]] = None
    misalignment_modules: Tuple[str, ...] = ()
    established_penalty: float = 1.0
    novelty_boost: float = 1.0
    novelty_selection_cap: int = 999
    newcomer_window: int = 20
    newcomer_true_bonus: float = 1.0


@dataclass
class PendingUpdate:
    due_round: int
    eid: str
    capability_index: int
    observed: float
    weight: float


@dataclass
class TrustState:
    alpha: Dict[str, List[float]] = field(default_factory=dict)
    beta: Dict[str, List[float]] = field(default_factory=dict)
    selected: Dict[str, int] = field(default_factory=dict)
    successes: Dict[str, int] = field(default_factory=dict)
    quality_history: Dict[str, List[int]] = field(default_factory=dict)
    a8_pairs: List[Tuple[float, float]] = field(default_factory=list)
    pending_updates: List[PendingUpdate] = field(default_factory=list)


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

SCENARIOS: Tuple[Scenario, ...] = (
    Scenario(
        name="baseline",
        description="Standard engineering collaboration with moderate observation noise.",
        success_reward=100.0,
        partial_reward=60.0,
        fatal_penalty=-200.0,
        lambda_auto=0.8,
        difficulty_shift=0.0,
        fatal_difficulty_bonus=0.0,
        catastrophe_rate=0.10,
        dependency_penalty=0.88,
        dependency_repair_threshold=0.80,
        dependency_repair_strength=0.08,
        surface_alignment=0.85,
        surface_bias=0.05,
        truth_delay=0,
        a8_surface_bonus=0.18,
        a8_true_penalty=0.12,
        moo_trust_bonus=0.20,
        task_weight_bonus={"M4": 0.2, "M6": 0.15, "M8": 0.1},
        newcomer_true_bonus=1.08,
    ),
    Scenario(
        name="safety_critical",
        description="High-stakes safety environment with harsher penalties and stronger error propagation.",
        success_reward=100.0,
        partial_reward=40.0,
        fatal_penalty=-400.0,
        lambda_auto=0.85,
        difficulty_shift=0.02,
        fatal_difficulty_bonus=0.05,
        catastrophe_rate=0.18,
        dependency_penalty=0.78,
        dependency_repair_threshold=0.84,
        dependency_repair_strength=0.10,
        surface_alignment=0.82,
        surface_bias=0.03,
        truth_delay=0,
        a8_surface_bonus=0.16,
        a8_true_penalty=0.14,
        moo_trust_bonus=0.16,
        task_weight_bonus={"M1": 0.25, "M4": 0.35, "M6": 0.35},
        newcomer_true_bonus=1.04,
    ),
    Scenario(
        name="observation_manipulated",
        description="Observation-contaminated environment where surface quality can diverge from true quality.",
        success_reward=100.0,
        partial_reward=60.0,
        fatal_penalty=-220.0,
        lambda_auto=0.55,
        difficulty_shift=0.0,
        fatal_difficulty_bonus=0.02,
        catastrophe_rate=0.10,
        dependency_penalty=0.86,
        dependency_repair_threshold=0.80,
        dependency_repair_strength=0.08,
        surface_alignment=0.55,
        surface_bias=0.18,
        truth_delay=3,
        a8_surface_bonus=0.52,
        a8_true_penalty=0.20,
        moo_trust_bonus=0.30,
        task_weight_bonus={"M4": 0.25, "M8": 0.30},
        newcomer_true_bonus=1.05,
    ),
    Scenario(
        name="utility_trust_misalignment",
        description="Local phases where trusted incumbents underperform and low-history entities hold latent value.",
        success_reward=110.0,
        partial_reward=50.0,
        fatal_penalty=-180.0,
        lambda_auto=0.75,
        difficulty_shift=0.01,
        fatal_difficulty_bonus=0.0,
        catastrophe_rate=0.10,
        dependency_penalty=0.86,
        dependency_repair_threshold=0.78,
        dependency_repair_strength=0.10,
        surface_alignment=0.83,
        surface_bias=0.05,
        truth_delay=0,
        a8_surface_bonus=0.20,
        a8_true_penalty=0.10,
        moo_trust_bonus=0.18,
        task_weight_bonus={"M3": 0.25, "M5": 0.35, "M8": 0.20},
        misalignment_rounds=(70, 135),
        misalignment_modules=("M3", "M5", "M8"),
        established_penalty=0.78,
        novelty_boost=1.18,
        novelty_selection_cap=5,
        newcomer_true_bonus=1.15,
    ),
)


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stdev(values: Sequence[float]) -> float:
    return stats.stdev(values) if len(values) > 1 else 0.0


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


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


def update_belief(state: TrustState, eid: str, k: int, observed: float, weight: float) -> None:
    state.alpha[eid][k] = RHO * state.alpha[eid][k] + weight * observed
    state.beta[eid][k] = RHO * state.beta[eid][k] + weight * (1.0 - observed)


def apply_pending_updates(state: TrustState, round_no: int) -> None:
    keep: List[PendingUpdate] = []
    for item in state.pending_updates:
        if item.due_round <= round_no:
            update_belief(state, item.eid, item.capability_index, item.observed, item.weight)
        else:
            keep.append(item)
    state.pending_updates = keep


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


def sample_task(rng: random.Random, scenario: Scenario, round_no: int) -> List[Module]:
    candidates = [m.mid for m in MODULES]
    weights = []
    for mid in candidates:
        weight = 1.0 + scenario.task_weight_bonus.get(mid, 0.0)
        if round_no >= 100 and mid in {"M4", "M8"}:
            weight += 0.20
        if round_no >= 50 and mid in {"M1", "M6"}:
            weight += 0.10
        weights.append(weight)

    for _ in range(400):
        target_size = rng.randint(3, 5)
        draw_count = rng.randint(1, target_size)
        chosen = rng.choices(candidates, weights=weights, k=draw_count)
        expanded = expand_with_dependencies(chosen)
        if 3 <= len(expanded) <= 5:
            return [MODULE_BY_ID[mid] for mid in expanded]
    return [MODULE_BY_ID[mid] for mid in expand_with_dependencies(("M5",))]


def allowed_entities(round_no: int, module: Module) -> List[Entity]:
    pool = []
    for entity in active_entities(round_no):
        if entity.kind == "human" and not module.human_allowed:
            continue
        if entity.kind == "agent" and not module.agent_allowed:
            continue
        pool.append(entity)
    return pool


def module_difficulty(scenario: Scenario, module: Module, round_no: int) -> float:
    difficulty = module.difficulty + scenario.difficulty_shift
    if module.criticality == "fatal":
        difficulty += scenario.fatal_difficulty_bonus
    if round_no >= 100 and module.capability_index == 3:
        difficulty += 0.03
    return clamp(difficulty, 0.65, 0.99)


def phase_misalignment_multiplier(
    scenario: Scenario,
    state: TrustState,
    round_no: int,
    module: Module,
    entity: Entity,
) -> float:
    if not scenario.misalignment_rounds or module.mid not in scenario.misalignment_modules:
        return 1.0
    start, end = scenario.misalignment_rounds
    if not (start <= round_no <= end):
        return 1.0
    if state.selected[entity.eid] > 12:
        return scenario.established_penalty
    if state.selected[entity.eid] <= scenario.novelty_selection_cap and entity.capabilities[module.capability_index] > 0.55:
        return scenario.novelty_boost
    return 1.0


def dependency_multiplier(
    scenario: Scenario,
    prior_results: Dict[str, int],
    entity: Entity,
    module: Module,
) -> float:
    deps = DEPENDENCIES[module.mid]
    if not deps:
        return 1.0
    multiplier = 1.0
    repairs = 0.0
    for dep in deps:
        if prior_results.get(dep, 1) == 0:
            multiplier *= scenario.dependency_penalty
            if entity.capabilities[module.capability_index] >= scenario.dependency_repair_threshold:
                repairs += scenario.dependency_repair_strength
    return clamp(multiplier + repairs, 0.45, 1.05)


def true_success_probability(
    rng: random.Random,
    scenario: Scenario,
    state: TrustState,
    round_no: int,
    module: Module,
    entity: Entity,
    prior_results: Dict[str, int],
) -> float:
    difficulty = module_difficulty(scenario, module, round_no)
    capability = entity.capabilities[module.capability_index]
    base = capability * difficulty
    base *= dependency_multiplier(scenario, prior_results, entity, module)
    base *= phase_misalignment_multiplier(scenario, state, round_no, module, entity)
    if entity.eid in {"A9", "A10"} and entity.join_round <= round_no < entity.join_round + scenario.newcomer_window:
        base *= scenario.newcomer_true_bonus
    if entity.eid == "A8":
        base -= scenario.a8_true_penalty
    return clamp(base, 0.01, 0.99)


def catastrophe_probability(scenario: Scenario, entity: Entity, module: Module) -> float:
    capability = entity.capabilities[module.capability_index]
    if module.criticality == "fatal" and capability < 0.50:
        return scenario.catastrophe_rate
    return 0.0


def surface_quality_probability(
    scenario: Scenario,
    group: str,
    round_no: int,
    entity: Entity,
    true_prob: float,
) -> float:
    base = scenario.surface_alignment * true_prob + scenario.surface_bias
    base += 0.05 * entity.seniority
    if entity.kind == "human":
        base += 0.02
    if entity.eid == "A8":
        bonus = scenario.a8_surface_bonus
        if group == "MOO":
            bonus += scenario.moo_trust_bonus
        if scenario.truth_delay > 0 and round_no >= 100:
            bonus += 0.05
        base += bonus
    return clamp(base, 0.01, 0.99)


def preference_bonus(module: Module, entity: Entity) -> float:
    if module.preferred_kind == "either":
        return 0.0
    return 0.03 if entity.kind == module.preferred_kind else -0.03


def select_true(
    rng: random.Random,
    scenario: Scenario,
    state: TrustState,
    round_no: int,
    module: Module,
) -> Entity:
    candidates = allowed_entities(round_no, module)
    if module.criticality == "fatal":
        safe = [e for e in candidates if e.capabilities[module.capability_index] >= 0.50]
        if safe:
            candidates = safe

    scored = []
    k = module.capability_index
    for entity in candidates:
        theta = rng.betavariate(state.alpha[entity.eid][k], state.beta[entity.eid][k])
        tm = trust_mean(state, entity.eid, k)
        tv = trust_var(state, entity.eid, k)
        cap = entity.capabilities[k]
        coverage = state.selected[entity.eid]
        newcomer = entity.eid in {"A9", "A10"} and coverage < BASE_COVERAGE_MIN
        feasible = (
            (tm >= BASE_TMIN and tm >= BASE_QMIN and tm >= BASE_RMIN and (module.criticality != "fatal" or cap >= 0.50))
            or coverage < BASE_COVERAGE_MIN
            or newcomer
        )
        coverage_bonus = 0.10 if coverage < BASE_COVERAGE_MIN else 0.0
        exploration_bonus = 0.30 * tv
        score = 0.30 * theta + 0.55 * cap + coverage_bonus + exploration_bonus + preference_bonus(module, entity)
        if scenario.misalignment_rounds and module.mid in scenario.misalignment_modules and coverage < scenario.novelty_selection_cap:
            score += 0.05
        if entity.eid == "A8":
            score -= 0.08
        scored.append((feasible, score, entity))
    feasible_pool = [row for row in scored if row[0]]
    return max(feasible_pool if feasible_pool else scored, key=lambda row: row[1])[2]


def select_blind(rng: random.Random, round_no: int, module: Module) -> Entity:
    pool = allowed_entities(round_no, module)
    humans = [e for e in pool if e.kind == "human"]
    if module.mid in {"M2", "M5"} and humans:
        if rng.random() < 0.72:
            return max(humans, key=lambda e: e.seniority)
        return rng.choice(humans)
    if humans and rng.random() < 0.55:
        return max(humans, key=lambda e: (e.seniority, e.capabilities[module.capability_index]))
    return rng.choice(pool)


def select_moo(scenario: Scenario, state: TrustState, round_no: int, module: Module) -> Entity:
    candidates = allowed_entities(round_no, module)
    best_entity: Optional[Entity] = None
    best_score = -1e9
    k = module.capability_index
    for entity in candidates:
        tm = trust_mean(state, entity.eid, k)
        tv = trust_var(state, entity.eid, k)
        predicted_utility = tm * module_difficulty(scenario, module, round_no)
        trust_objective = tm + 0.03 * math.log1p(state.selected[entity.eid])
        if entity.eid == "A8":
            trust_objective += scenario.moo_trust_bonus
            if round_no >= 150:
                trust_objective += 0.05
        score = 0.22 * predicted_utility + 0.70 * trust_objective - 0.04 * tv + preference_bonus(module, entity)
        if score > best_score:
            best_score = score
            best_entity = entity
    assert best_entity is not None
    return best_entity


def human_review(
    rng: random.Random,
    scenario: Scenario,
    entity: Entity,
    q_surface: int,
    reviewers: Sequence[Entity],
) -> float:
    scores = []
    for reviewer in reviewers:
        noise_sd = 1.0 / max(reviewer.precision, 1e-6)
        raw = clamp(q_surface + reviewer.bias + rng.gauss(0.0, noise_sd))
        calibrated = clamp((raw - reviewer.bias) / reviewer.precision)
        scores.append(calibrated)
    return mean(scores) if scores else float(q_surface)


def observation_components(
    rng: random.Random,
    scenario: Scenario,
    round_no: int,
    group: str,
    entity: Entity,
    q_true: int,
    q_surface: int,
    assignees: Sequence[str],
) -> Tuple[float, float, float]:
    humans = [e for e in active_entities(round_no) if e.kind == "human" and e.eid not in assignees]
    reviewers = rng.sample(humans, k=min(2, len(humans))) if humans else []
    human_score = human_review(rng, scenario, entity, q_surface, reviewers)
    machine_signal = float(q_true)
    human_signal = human_score
    observed = scenario.lambda_auto * machine_signal + (1.0 - scenario.lambda_auto) * human_signal
    if entity.eid == "A8" and group == "MOO" and scenario.name == "observation_manipulated":
        observed = max(observed, 0.84 if round_no < 150 else 0.92)
    return machine_signal, human_signal, observed


def execute_module(
    rng: random.Random,
    scenario: Scenario,
    group: str,
    round_no: int,
    state: TrustState,
    module: Module,
    assignees: Sequence[str],
    prior_results: Dict[str, int],
) -> Tuple[Entity, int, int, float]:
    if group == "TRUE":
        entity = select_true(rng, scenario, state, round_no, module)
    elif group == "Blind":
        entity = select_blind(rng, round_no, module)
    else:
        entity = select_moo(scenario, state, round_no, module)

    p_true = true_success_probability(rng, scenario, state, round_no, module, entity, prior_results)
    catastrophe = catastrophe_probability(scenario, entity, module)
    q_true = 1 if rng.random() < p_true * (1.0 - catastrophe) else 0
    p_surface = surface_quality_probability(scenario, group, round_no, entity, p_true)
    q_surface = 1 if rng.random() < p_surface else 0
    machine_signal, human_signal, observed = observation_components(
        rng, scenario, round_no, group, entity, q_true, q_surface, assignees
    )

    state.selected[entity.eid] += 1
    state.successes[entity.eid] += q_true
    state.quality_history[entity.eid].append(q_true)

    if group != "Blind":
        k = module.capability_index
        if scenario.truth_delay > 0:
            update_belief(state, entity.eid, k, human_signal, 1.0 - scenario.lambda_auto)
            state.pending_updates.append(
                PendingUpdate(
                    due_round=round_no + scenario.truth_delay,
                    eid=entity.eid,
                    capability_index=k,
                    observed=machine_signal,
                    weight=scenario.lambda_auto,
                )
            )
        else:
            update_belief(state, entity.eid, k, observed, 1.0)
        if entity.eid == "A8":
            state.a8_pairs.append((trust_mean(state, entity.eid, k), float(q_true)))

    return entity, q_true, q_surface, observed


def task_utility(scenario: Scenario, true_results: Dict[str, int], task: Sequence[Module]) -> float:
    if any(true_results[m.mid] == 0 and m.criticality == "fatal" for m in task):
        return scenario.fatal_penalty
    if all(true_results[m.mid] == 1 for m in task):
        return scenario.success_reward
    return scenario.partial_reward


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


def simulate_group_scenario(
    scenario: Scenario,
    group: str,
    run_id: int,
    rounds: int,
    seed: int,
) -> Tuple[List[dict], List[dict]]:
    rng = random.Random(seed)
    state = new_state()
    cumulative_utility = 0.0
    fatal_errors = 0
    successful_tasks = 0
    quality_sum = 0.0
    surface_sum = 0.0
    a9_first_delay: Optional[int] = None
    a10_first_delay: Optional[int] = None
    a9_var_convergence: Optional[int] = None
    a9_first20 = 0
    time_rows: List[dict] = []

    for round_no in range(1, rounds + 1):
        apply_pending_updates(state, round_no)
        task = sample_task(rng, scenario, round_no)
        assignees: List[str] = []
        true_results: Dict[str, int] = {}
        surface_results: Dict[str, int] = {}
        round_fatal = 0

        for module in task:
            entity, q_true, q_surface, _ = execute_module(
                rng, scenario, group, round_no, state, module, assignees, true_results
            )
            assignees.append(entity.eid)
            true_results[module.mid] = q_true
            surface_results[module.mid] = q_surface
            if q_true == 0 and module.criticality == "fatal":
                round_fatal += 1
            if entity.eid == "A9":
                if a9_first_delay is None:
                    a9_first_delay = round_no - 50
                if 50 <= round_no <= 69:
                    a9_first20 += 1
            if entity.eid == "A10" and a10_first_delay is None:
                a10_first_delay = round_no - 100

        round_quality = mean(list(true_results.values()))
        round_surface = mean(list(surface_results.values()))
        utility = task_utility(scenario, true_results, task)

        if group == "TRUE" and a9_var_convergence is None and round_no >= 50:
            if trust_var(state, "A9", 0) < 0.05:
                a9_var_convergence = round_no - 50

        cumulative_utility += utility
        fatal_errors += round_fatal
        successful_tasks += int(utility > 0)
        quality_sum += round_quality
        surface_sum += round_surface

        trust_avg, trust_avg_var, trust_gini = summarize_trust(state, round_no)
        time_rows.append(
            {
                "run": run_id,
                "scenario": scenario.name,
                "round": round_no,
                "group": group,
                "modules": len(task),
                "utility": utility,
                "cumulative_utility": cumulative_utility,
                "quality_true": round_quality,
                "quality_surface": round_surface,
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
            "scenario": scenario.name,
            "group": group,
            "cumulative_utility": cumulative_utility,
            "mean_utility": cumulative_utility / rounds,
            "mean_quality_true": quality_sum / rounds,
            "mean_quality_surface": surface_sum / rounds,
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
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows: Sequence[dict]) -> List[dict]:
    out: List[dict] = []
    scenarios = sorted({r["scenario"] for r in rows})
    for scenario in scenarios:
        for group in ("TRUE", "Blind", "MOO"):
            rs = [r for r in rows if r["scenario"] == scenario and r["group"] == group]
            out.append(
                {
                    "scenario": scenario,
                    "group": group,
                    "cumulative_utility_mean": mean([r["cumulative_utility"] for r in rs]),
                    "cumulative_utility_sd": stdev([r["cumulative_utility"] for r in rs]),
                    "mean_quality_true": mean([r["mean_quality_true"] for r in rs]),
                    "mean_quality_surface": mean([r["mean_quality_surface"] for r in rs]),
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
    keys = sorted({(r["scenario"], r["run"]) for r in rows})
    for scenario, run_id in keys:
        by_group = {r["group"]: r for r in rows if r["scenario"] == scenario and r["run"] == run_id}
        tr = by_group["TRUE"]
        bl = by_group["Blind"]
        mo = by_group["MOO"]
        out.append(
            {
                "scenario": scenario,
                "run": run_id,
                "TRUE_U": tr["cumulative_utility"],
                "Blind_U": bl["cumulative_utility"],
                "MOO_U": mo["cumulative_utility"],
                "TRUE_Fatal": tr["fatal_errors"],
                "Blind_Fatal": bl["fatal_errors"],
                "MOO_Fatal": mo["fatal_errors"],
                "TRUE_A9": tr["a9_first_delay"],
                "Blind_A9": bl["a9_first_delay"],
                "MOO_A9": mo["a9_first_delay"],
                "TRUE_Gini": tr["final_trust_gini"],
                "MOO_Gini": mo["final_trust_gini"],
                "TRUE_Collapse": tr["final_collapse_index"],
                "MOO_Collapse": mo["final_collapse_index"],
                "TRUE_A8Corr": tr["a8_trust_quality_corr"],
                "MOO_A8Corr": mo["a8_trust_quality_corr"],
            }
        )
    return out


def scenario_tests(wide: Sequence[dict]) -> List[dict]:
    rows = []
    for scenario in sorted({r["scenario"] for r in wide}):
        rs = [r for r in wide if r["scenario"] == scenario]
        specs = [
            ("TRUE_U > Blind_U", "cumulative utility", "TRUE_U", "Blind_U"),
            ("TRUE_U > MOO_U", "cumulative utility", "TRUE_U", "MOO_U"),
            ("TRUE_Fatal < Blind_Fatal", "fatal errors", "Blind_Fatal", "TRUE_Fatal"),
            ("TRUE_Fatal < MOO_Fatal", "fatal errors", "MOO_Fatal", "TRUE_Fatal"),
            ("TRUE_A9 < Blind_A9", "A9 first selected delay", "Blind_A9", "TRUE_A9"),
            ("TRUE_Collapse < MOO_Collapse", "collapse index", "MOO_Collapse", "TRUE_Collapse"),
        ]
        for hypothesis, metric, left, right in specs:
            rows.append({"scenario": scenario, "hypothesis": hypothesis, "metric": metric, **paired_test(rs, left, right)})
    return rows


def fmt(x: float, digits: int = 3) -> str:
    return f"{float(x):.{digits}f}"


def scenario_name(name: str) -> str:
    return {
        "baseline": "Baseline",
        "safety_critical": "Safety-Critical",
        "observation_manipulated": "Observation-Manipulated",
        "utility_trust_misalignment": "Utility-Trust-Misalignment",
    }.get(name, name)


def write_report(
    path: Path,
    summary: Sequence[dict],
    tests: Sequence[dict],
    runs: int,
    rounds: int,
    scenarios: Sequence[Scenario],
) -> None:
    by_key = {(row["scenario"], row["group"]): row for row in summary}
    lines = [
        "# TRUE 改进版场景族模拟实验报告",
        "",
        "## 总论",
        "",
        f"本轮实验将单一场景扩展为 {len(scenarios)} 个参数化场景，仍然不接入真实工具，而是通过概率模型假设来表达不同协作环境。",
        f"实验共进行 {runs} 次 Monte Carlo 重复，每次 {rounds} 轮，每个场景下比较 TRUE、Blind 和 MOO 三组机制。",
        "",
        "本轮改进的重点有三项：",
        "",
        "1. 从单层成功信号升级为 `q_true / q_surface / q_obs` 三层观测结构。",
        "2. 从单一任务环境升级为场景族，包括安全高惩罚、观测污染和效用-信任错位场景。",
        "3. 从静态模块成功率升级为包含依赖误差传播与局部阶段性机制的概率模型。",
        "",
        "## 场景定义",
        "",
    ]
    for scenario in scenarios:
        lines.append(f"- `{scenario_name(scenario.name)}`: {scenario.description}")

    lines += [
        "",
        "## 结果汇总",
        "",
        "| 场景 | 组别 | 累积效用均值 | 真实质量均值 | 表面质量均值 | 致命错误均值 | 成功率 | 选择Gini | 塌缩指数 | A9首次延迟 | A8信任-质量相关 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for scenario in scenarios:
        for group in ("TRUE", "Blind", "MOO"):
            row = by_key[(scenario.name, group)]
            lines.append(
                f"| {scenario_name(scenario.name)} | {group} | {fmt(row['cumulative_utility_mean'],1)} | "
                f"{fmt(row['mean_quality_true'])} | {fmt(row['mean_quality_surface'])} | "
                f"{fmt(row['fatal_errors_mean'],1)} | {fmt(row['success_rate'])} | "
                f"{fmt(row['final_trust_gini'])} | {fmt(row['final_collapse_index'])} | "
                f"{fmt(row['a9_first_delay'],1)} | {fmt(row['a8_trust_quality_corr'])} |"
            )

    lines += [
        "",
        "## 场景结论",
        "",
    ]
    for scenario in scenarios:
        tr = by_key[(scenario.name, "TRUE")]
        bl = by_key[(scenario.name, "Blind")]
        mo = by_key[(scenario.name, "MOO")]
        lines += [
            f"### {scenario_name(scenario.name)}",
            "",
            f"- TRUE 相比 Blind 的累积效用差为 `{fmt(tr['cumulative_utility_mean'] - bl['cumulative_utility_mean'],1)}`。",
            f"- TRUE 相比 MOO 的累积效用差为 `{fmt(tr['cumulative_utility_mean'] - mo['cumulative_utility_mean'],1)}`。",
            f"- TRUE 的致命错误均值为 `{fmt(tr['fatal_errors_mean'],1)}`，Blind 为 `{fmt(bl['fatal_errors_mean'],1)}`，MOO 为 `{fmt(mo['fatal_errors_mean'],1)}`。",
            f"- TRUE 的 A9 首次被选平均延迟为 `{fmt(tr['a9_first_delay'],1)}`，而 MOO 为 `{fmt(mo['a9_first_delay'],1)}`。",
            f"- A8 的信任-真实质量相关在 TRUE 中为 `{fmt(tr['a8_trust_quality_corr'])}`，在 MOO 中为 `{fmt(mo['a8_trust_quality_corr'])}`。",
            "",
        ]

    lines += [
        "## 假设检验摘要",
        "",
        "| 场景 | 假设 | 均值差 | t | 近似p值 | Cohen d |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in tests:
        lines.append(
            f"| {scenario_name(row['scenario'])} | {row['hypothesis']} | {fmt(row['mean_diff'])} | "
            f"{fmt(row['t'])} | {fmt(row['p_approx'],4)} | {fmt(row['cohens_d'])} |"
        )

    lines += [
        "",
        "## 解释与边界",
        "",
        "- `Baseline` 用于保证与上一轮单场景实验可连续比较。",
        "- `Safety-Critical` 强化了安全非对称性，用于检验 TRUE 的约束优势是否在高风险环境下放大。",
        "- `Observation-Manipulated` 将真实质量与表面质量分离，用于更严格地模拟 Goodhart 型操纵。",
        "- `Utility-Trust-Misalignment` 刻画了局部阶段中“高信任不等于高短期效用”的环境，用于测试 TRUE 是否能更好地保留长期信息价值。",
        "- 本轮实验依然不等于真实工程流程复现，而是更严格的概率生成模型比较。",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_scenarios(arg: str) -> List[Scenario]:
    chosen = {name.strip() for name in arg.split(",") if name.strip()}
    if not chosen:
        return list(SCENARIOS)
    by_name = {scenario.name: scenario for scenario in SCENARIOS}
    return [by_name[name] for name in chosen]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=60)
    parser.add_argument("--rounds", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260510)
    parser.add_argument("--scenarios", type=str, default=",".join(s.name for s in SCENARIOS))
    parser.add_argument("--outdir", type=Path, default=Path("."))
    args = parser.parse_args()

    selected_scenarios = parse_scenarios(args.scenarios)
    args.outdir.mkdir(parents=True, exist_ok=True)

    results: List[dict] = []
    timeseries: List[dict] = []
    offsets = {"TRUE": 1, "Blind": 2, "MOO": 3}

    for scenario_index, scenario in enumerate(selected_scenarios, start=1):
        for run_id in range(1, args.runs + 1):
            for group in ("TRUE", "Blind", "MOO"):
                seed = args.seed + scenario_index * 100000 + run_id * 1000 + offsets[group]
                summary, time_rows = simulate_group_scenario(scenario, group, run_id, args.rounds, seed)
                results.extend(summary)
                timeseries.extend(time_rows)

    summary = aggregate(results)
    tests = scenario_tests(make_wide(results))

    write_csv(args.outdir / "TRUE_improved_results.csv", results)
    write_csv(args.outdir / "TRUE_improved_round_timeseries.csv", timeseries)
    write_csv(args.outdir / "TRUE_improved_summary.csv", summary)
    write_csv(args.outdir / "TRUE_improved_tests.csv", tests)
    write_report(args.outdir / "TRUE_improved_experiment_report.md", summary, tests, args.runs, args.rounds, selected_scenarios)

    for scenario in selected_scenarios:
        tr = next(row for row in summary if row["scenario"] == scenario.name and row["group"] == "TRUE")
        print(
            scenario.name,
            "TRUE_U=", fmt(tr["cumulative_utility_mean"], 1),
            "TRUE_Q=", fmt(tr["mean_quality_true"]),
            "TRUE_Fatal=", fmt(tr["fatal_errors_mean"], 1),
        )
    print(f"Wrote outputs to {args.outdir.resolve()}")


if __name__ == "__main__":
    main()
