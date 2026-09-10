"""Greedy baseline methods for comparison with the optimal assignment."""

from __future__ import annotations

import random

from .validation import validate_inputs


def greedy_assignment(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
    doctor_order: list[str] | None = None,
) -> dict[str, dict[str, str]]:
    """Assign each doctor to the best hospital with remaining capacity."""
    validate_inputs(preferences, capacities)
    order = list(preferences) if doctor_order is None else list(doctor_order)
    if set(order) != set(preferences) or len(order) != len(preferences):
        raise ValueError("Doctor order must contain every doctor exactly once.")

    remaining_capacity = capacities.copy()
    assignment = {}
    for doctor in order:
        for hospital in preferences[doctor]:
            if remaining_capacity[hospital] > 0:
                assignment[doctor] = {"hospital": hospital}
                remaining_capacity[hospital] -= 1
                break
    return assignment


def run_randomized_greedy(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
    trials: int = 100,
    seed: int | None = 0,
) -> list[dict[str, dict[str, str]]]:
    """Run greedy assignment with reproducible randomized doctor orders."""
    if isinstance(trials, bool) or not isinstance(trials, int) or trials <= 0:
        raise ValueError("Trials must be a positive integer.")
    validate_inputs(preferences, capacities)
    generator = random.Random(seed)
    doctors = list(preferences)
    assignments = []
    for _ in range(trials):
        order = doctors.copy()
        generator.shuffle(order)
        assignments.append(greedy_assignment(preferences, capacities, order))
    return assignments
