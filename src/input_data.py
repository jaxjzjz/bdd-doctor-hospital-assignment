"""Create manual or reproducible random input data."""

from __future__ import annotations

import random


def parse_preference_entry(entry: str, hospitals: list[str]) -> list[str]:
    """Parse hospital numbers or names entered in preference order."""
    tokens = entry.replace(",", " ").split()
    converted = []
    for token in tokens:
        if token.isdigit():
            index = int(token) - 1
            if index < 0 or index >= len(hospitals):
                raise ValueError(f"Hospital number {token} is outside the valid range.")
            converted.append(hospitals[index])
        else:
            converted.append(token)

    if len(converted) != len(hospitals):
        raise ValueError(f"Enter exactly {len(hospitals)} hospitals.")
    if len(set(converted)) != len(converted):
        raise ValueError("Each hospital must appear exactly once.")
    if set(converted) != set(hospitals):
        raise ValueError("Preferences must contain every hospital exactly once.")
    return converted


def generate_random_preferences(
    doctors: list[str],
    hospitals: list[str],
    seed: int | None = None,
) -> dict[str, list[str]]:
    """Generate complete random rankings that are reproducible with a seed."""
    generator = random.Random(seed)
    return {
        doctor: generator.sample(hospitals, len(hospitals))
        for doctor in doctors
    }


def collect_manual_preferences(
    doctors: list[str],
    hospitals: list[str],
    input_function=input,
    output_function=print,
) -> dict[str, list[str]]:
    """Collect a complete ranking from each doctor."""
    output_function("Hospitals: " + ", ".join(
        f"{index}={hospital}" for index, hospital in enumerate(hospitals, start=1)
    ))
    preferences = {}
    for doctor in doctors:
        while True:
            entry = input_function(
                f"Preferences for {doctor} (best to worst, separated by spaces): "
            )
            try:
                preferences[doctor] = parse_preference_entry(entry, hospitals)
                break
            except ValueError as error:
                output_function(f"Invalid preference list: {error}")
    return preferences
