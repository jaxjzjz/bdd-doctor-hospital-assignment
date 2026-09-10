"""Run a reproducible comparison of Hungarian and greedy assignment."""

from pprint import pprint

from src.assignment import solve_hungarian
from src.baseline import run_randomized_greedy
from src.metrics import evaluate_assignment, summarize_trials


preferences = {
    "D1": ["H1", "H2", "H3"],
    "D2": ["H1", "H3", "H2"],
    "D3": ["H2", "H1", "H3"],
    "D4": ["H2", "H3", "H1"],
    "D5": ["H1", "H2", "H3"],
}

capacities = {"H1": 2, "H2": 2, "H3": 1}
doctors = list(preferences)

hungarian_assignment = solve_hungarian(preferences, capacities)
hungarian_metrics = evaluate_assignment(
    doctors, hungarian_assignment, preferences
)

greedy_assignments = run_randomized_greedy(
    preferences, capacities, trials=100, seed=10
)
greedy_metrics = [
    evaluate_assignment(doctors, assignment, preferences)
    for assignment in greedy_assignments
]

print("Hungarian assignment")
pprint(hungarian_assignment)
print("\nHungarian metrics")
pprint(hungarian_metrics)
print("\nRandomized greedy summary (100 trials)")
pprint(summarize_trials(greedy_metrics))
