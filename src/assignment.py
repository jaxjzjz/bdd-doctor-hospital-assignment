"""Hungarian assignment solver with hospital capacity slots."""

from .validation import validate_inputs


def create_slots(capacities: dict[str, int]) -> list[dict[str, str]]:
    """Expand each hospital capacity into one-to-one assignment slots."""
    return [
        {"hospital": hospital, "slot": f"{hospital}_{slot_number}"}
        for hospital, capacity in capacities.items()
        for slot_number in range(1, capacity + 1)
    ]


def create_rank_lookup(
    preferences: dict[str, list[str]],
) -> dict[str, dict[str, int]]:
    """Convert ordered preference lists to one-based rank costs."""
    return {
        doctor: {
            hospital: rank
            for rank, hospital in enumerate(preference_list, start=1)
        }
        for doctor, preference_list in preferences.items()
    }


def build_cost_matrix(
    doctors: list[str],
    slots: list[dict[str, str]],
    rank_lookup: dict[str, dict[str, int]],
) -> list[list[int]]:
    """Build a doctor-by-slot rank cost matrix."""
    return [
        [rank_lookup[doctor][slot["hospital"]] for slot in slots]
        for doctor in doctors
    ]


def hungarian_algorithm(cost_matrix: list[list[int]]) -> list[int]:
    """Return the minimum-cost slot index for every matrix row."""
    if not cost_matrix or not cost_matrix[0]:
        raise ValueError("Cost matrix cannot be empty.")
    if any(len(row) != len(cost_matrix[0]) for row in cost_matrix):
        raise ValueError("Cost matrix must be rectangular.")

    row_count = len(cost_matrix)
    column_count = len(cost_matrix[0])
    if row_count > column_count:
        raise ValueError("Number of hospital slots must be at least the number of doctors.")

    row_potential = [0] * (row_count + 1)
    column_potential = [0] * (column_count + 1)
    matched_row = [0] * (column_count + 1)
    previous_column = [0] * (column_count + 1)

    for row in range(1, row_count + 1):
        matched_row[0] = row
        current_column = 0
        minimum_reduced_cost = [float("inf")] * (column_count + 1)
        used = [False] * (column_count + 1)

        while True:
            used[current_column] = True
            current_row = matched_row[current_column]
            delta = float("inf")
            next_column = 0

            for column in range(1, column_count + 1):
                if not used[column]:
                    reduced_cost = (
                        cost_matrix[current_row - 1][column - 1]
                        - row_potential[current_row]
                        - column_potential[column]
                    )
                    if reduced_cost < minimum_reduced_cost[column]:
                        minimum_reduced_cost[column] = reduced_cost
                        previous_column[column] = current_column
                    if minimum_reduced_cost[column] < delta:
                        delta = minimum_reduced_cost[column]
                        next_column = column

            for column in range(column_count + 1):
                if used[column]:
                    row_potential[matched_row[column]] += delta
                    column_potential[column] -= delta
                else:
                    minimum_reduced_cost[column] -= delta

            current_column = next_column
            if matched_row[current_column] == 0:
                break

        while True:
            next_column = previous_column[current_column]
            matched_row[current_column] = matched_row[next_column]
            current_column = next_column
            if current_column == 0:
                break

    assignment = [-1] * row_count
    for column in range(1, column_count + 1):
        if matched_row[column] != 0:
            assignment[matched_row[column] - 1] = column - 1
    return assignment


def solve_hungarian(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
) -> dict[str, dict[str, str]]:
    """Validate and solve a complete doctor-hospital assignment problem."""
    validate_inputs(preferences, capacities)
    doctors = list(preferences)
    slots = create_slots(capacities)
    rank_lookup = create_rank_lookup(preferences)
    cost_matrix = build_cost_matrix(doctors, slots, rank_lookup)
    slot_indices = hungarian_algorithm(cost_matrix)

    return {
        doctor: {
            "hospital": slots[slot_index]["hospital"],
            "slot": slots[slot_index]["slot"],
        }
        for doctor, slot_index in zip(doctors, slot_indices)
    }
