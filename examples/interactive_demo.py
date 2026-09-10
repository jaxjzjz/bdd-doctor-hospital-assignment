# Interactive notebook-friendly demonstration of the assignment system.

from pprint import pprint
from src.assignment import solve_hungarian
from src.baseline import run_randomized_greedy
from src.input_data import collect_manual_preferences, generate_random_preferences
from src.metrics import evaluate_assignment, summarize_trials

def read_positive_integer(prompt: str) -> int:
    """Read a positive integer, repeating until the input is valid."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive integer.")

def read_capacities(hospitals: list[str], doctor_count: int) -> dict[str, int]:
    """Read capacities and repeat the complete entry if total capacity is low."""
    while True:
        capacities = {}
        print("\nEnter a non-negative integer capacity for each hospital.")
        for hospital in hospitals:
            while True:
                try:
                    capacity = int(input(f"Capacity for {hospital}: "))
                    if capacity < 0:
                        raise ValueError
                    capacities[hospital] = capacity
                    break
                except ValueError:
                    print("Capacity must be a non-negative integer.")

        total_capacity = sum(capacities.values())
        if total_capacity >= doctor_count:
            return capacities
        print(
            f"Total capacity is {total_capacity}, but {doctor_count} doctors "
            "need assignments. Please enter all capacities again."
        )

def collect_preferences(
    doctors: list[str], hospitals: list[str]
) -> dict[str, list[str]]:
    """Let the user select manual or reproducible random preferences."""
    while True:
        mode = input("\nPreference mode: manual (m) or random demo (r)? ").strip().lower()
        if mode in {"m", "manual"}:
            return collect_manual_preferences(doctors, hospitals)
        if mode in {"r", "random"}:
            seed_entry = input("Random seed [0]: ").strip()
            try:
                seed = int(seed_entry) if seed_entry else 0
            except ValueError:
                print("Random seed must be an integer.")
                continue
            return generate_random_preferences(doctors, hospitals, seed=seed)
        print("Enter m for manual input or r for a random demo.")

def print_preferences(preferences: dict[str, list[str]]) -> None:
    """Display complete preference rankings."""
    print("\nPreferences")
    print("-" * 50)
    for doctor, hospitals in preferences.items():
        print(f"{doctor}: {' > '.join(hospitals)}")

def print_assignment(title: str, assignment: dict[str, dict[str, str]]) -> None:
    """Display one assignment in doctor order."""
    print(f"\n{title}")
    print("-" * 50)
    for doctor, result in assignment.items():
        print(f"{doctor} -> {result['hospital']}")

def main() -> None:
    # Run the complete interactive workflow.
    doctor_count = read_positive_integer("Number of doctors: ")
    hospital_count = read_positive_integer("Number of hospitals: ")

    doctors = [f"D{index}" for index in range(1, doctor_count + 1)]
    hospitals = [f"H{index}" for index in range(1, hospital_count + 1)]
    capacities = read_capacities(hospitals, doctor_count)
    preferences = collect_preferences(doctors, hospitals)
    print_preferences(preferences)

    hungarian_assignment = solve_hungarian(preferences, capacities)
    hungarian_metrics = evaluate_assignment(
        doctors, hungarian_assignment, preferences
    )

    greedy_assignments = run_randomized_greedy(
        preferences, capacities, trials=100, seed=0
    )
    greedy_metrics = [
        evaluate_assignment(doctors, assignment, preferences)
        for assignment in greedy_assignments
    ]

    print_assignment("Hungarian assignment", hungarian_assignment)
    print("\nHungarian metrics")
    pprint(hungarian_metrics)
    print("\nRandomized greedy summary (100 trials)")
    pprint(summarize_trials(greedy_metrics))


if __name__ == "__main__":
    main()
