import itertools
import random
import unittest

from src.assignment import hungarian_algorithm, solve_hungarian
from src.baseline import run_randomized_greedy
from src.metrics import evaluate_assignment, summarize_trials


def brute_force_cost(cost_matrix):
    row_count = len(cost_matrix)
    column_count = len(cost_matrix[0])
    return min(
        sum(cost_matrix[row][column] for row, column in enumerate(columns))
        for columns in itertools.permutations(range(column_count), row_count)
    )


class AssignmentTests(unittest.TestCase):
    def setUp(self):
        self.preferences = {
            "D1": ["H1", "H2"],
            "D2": ["H1", "H2"],
            "D3": ["H2", "H1"],
        }
        self.capacities = {"H1": 1, "H2": 2}

    def test_solution_assigns_every_doctor_within_capacity(self):
        assignment = solve_hungarian(self.preferences, self.capacities)
        self.assertEqual(set(assignment), set(self.preferences))
        for hospital, capacity in self.capacities.items():
            assigned_count = sum(
                result["hospital"] == hospital for result in assignment.values()
            )
            self.assertLessEqual(assigned_count, capacity)

    def test_known_solution_has_minimum_cost(self):
        assignment = solve_hungarian(self.preferences, self.capacities)
        metrics = evaluate_assignment(
            list(self.preferences), assignment, self.preferences
        )
        self.assertEqual(metrics["total_cost"], 4)
        self.assertEqual(metrics["worst_assigned_rank"], 2)

    def test_hungarian_matches_brute_force_on_random_matrices(self):
        generator = random.Random(10)
        for row_count in [2, 3, 4]:
            for column_count in range(row_count, 6):
                for _ in range(20):
                    matrix = [
                        [generator.randint(0, 9) for _ in range(column_count)]
                        for _ in range(row_count)
                    ]
                    assignment = hungarian_algorithm(matrix)
                    actual = sum(matrix[row][column] for row, column in enumerate(assignment))
                    self.assertEqual(actual, brute_force_cost(matrix))

    def test_randomized_greedy_is_reproducible(self):
        first = run_randomized_greedy(
            self.preferences, self.capacities, trials=10, seed=42
        )
        second = run_randomized_greedy(
            self.preferences, self.capacities, trials=10, seed=42
        )
        self.assertEqual(first, second)

        metrics = [
            evaluate_assignment(list(self.preferences), item, self.preferences)
            for item in first
        ]
        summary = summarize_trials(metrics)
        self.assertLessEqual(summary["best_total_cost"], summary["worst_total_cost"])


if __name__ == "__main__":
    unittest.main()
