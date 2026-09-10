# Larger reproducible example with 20 doctors and 6 hospitals.

from pprint import pprint
from src.assignment import solve_hungarian
from src.baseline import run_randomized_greedy
from src.metrics import evaluate_assignment, summarize_trials
from src.validation import validate_inputs

capacities = {
    "H1": 4,
    "H2": 3,
    "H3": 4,
    "H4": 3,
    "H5": 3,
    "H6": 3,
}

preferences = {
    "D1": ["H2", "H5", "H3", "H4", "H6", "H1"],
    "D2": ["H6", "H4", "H5", "H2", "H1", "H3"],
    "D3": ["H1", "H3", "H5", "H2", "H4", "H6"],
    "D4": ["H6", "H2", "H1", "H5", "H4", "H3"],
    "D5": ["H5", "H3", "H6", "H2", "H4", "H1"],
    "D6": ["H4", "H6", "H1", "H3", "H2", "H5"],
    "D7": ["H5", "H6", "H3", "H1", "H2", "H4"],
    "D8": ["H4", "H5", "H1", "H3", "H2", "H6"],
    "D9": ["H6", "H4", "H5", "H3", "H1", "H2"],
    "D10": ["H1", "H4", "H2", "H3", "H6", "H5"],
    "D11": ["H2", "H6", "H1", "H4", "H5", "H3"],
    "D12": ["H5", "H1", "H3", "H4", "H6", "H2"],
    "D13": ["H1", "H6", "H2", "H4", "H5", "H3"],
    "D14": ["H6", "H2", "H3", "H4", "H5", "H1"],
    "D15": ["H1", "H5", "H3", "H6", "H4", "H2"],
    "D16": ["H3", "H5", "H6", "H2", "H1", "H4"],
    "D17": ["H6", "H5", "H2", "H1", "H3", "H4"],
    "D18": ["H3", "H1", "H6", "H2", "H4", "H5"],
    "D19": ["H2", "H3", "H1", "H5", "H4", "H6"],
    "D20": ["H3", "H2", "H4", "H1", "H6", "H5"],
}

def main() -> None:
    """Validate, solve, and compare the larger example."""
    validate_inputs(preferences, capacities)
    doctors = list(preferences)

    hungarian_assignment = solve_hungarian(preferences, capacities)
    hungarian_metrics = evaluate_assignment(
        doctors, hungarian_assignment, preferences
    )

    greedy_assignments = run_randomized_greedy(
        preferences, capacities, trials=1_000, seed=10
    )
    greedy_metrics = [
        evaluate_assignment(doctors, assignment, preferences)
        for assignment in greedy_assignments
    ]

    print("Input summary")
    print("-" * 50)
    print(f"Doctors: {len(doctors)}")
    print(f"Hospitals: {len(capacities)}")
    print(f"Total capacity: {sum(capacities.values())}")

    print("\nHungarian assignment")
    print("-" * 50)
    for doctor, result in hungarian_assignment.items():
        rank = hungarian_metrics["assigned_ranks"][doctor]
        print(f"{doctor:<4} -> {result['hospital']} (rank {rank})")

    print("\nHungarian metrics")
    pprint(hungarian_metrics)

    print("\nRandomized greedy summary (1,000 trials)")
    pprint(summarize_trials(greedy_metrics))

if __name__ == "__main__":
    main()
