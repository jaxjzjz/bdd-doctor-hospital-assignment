import unittest

from src.input_data import parse_preference_entry
from src.validation import validate_inputs


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.preferences = {
            "D1": ["H1", "H2"],
            "D2": ["H2", "H1"],
        }
        self.capacities = {"H1": 1, "H2": 1}

    def test_valid_input_passes(self):
        validate_inputs(self.preferences, self.capacities)

    def test_insufficient_capacity_fails(self):
        with self.assertRaisesRegex(ValueError, "Total hospital capacity"):
            validate_inputs(self.preferences, {"H1": 1, "H2": 0})

    def test_duplicate_hospital_fails(self):
        invalid = {"D1": ["H1", "H1"], "D2": ["H2", "H1"]}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_inputs(invalid, self.capacities)

    def test_bool_capacity_fails(self):
        with self.assertRaises(TypeError):
            validate_inputs(self.preferences, {"H1": True, "H2": 1})

    def test_zero_capacity_is_allowed_when_total_capacity_is_sufficient(self):
        validate_inputs(self.preferences, {"H1": 0, "H2": 2})

    def test_incomplete_ranking_fails(self):
        invalid = {"D1": ["H1"], "D2": ["H2", "H1"]}
        with self.assertRaisesRegex(ValueError, "rank every hospital"):
            validate_inputs(invalid, self.capacities)

    def test_unknown_hospital_fails(self):
        invalid = {"D1": ["H1", "H3"], "D2": ["H2", "H1"]}
        with self.assertRaisesRegex(ValueError, "do not match"):
            validate_inputs(invalid, self.capacities)

    def test_preference_parser_accepts_numbers_and_commas(self):
        hospitals = ["H1", "H2", "H3"]
        self.assertEqual(
            parse_preference_entry("2, 1, 3", hospitals),
            ["H2", "H1", "H3"],
        )


if __name__ == "__main__":
    unittest.main()
