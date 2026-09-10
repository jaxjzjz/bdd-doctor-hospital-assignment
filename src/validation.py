"""Input validation for the doctor-hospital assignment problem."""


def validate_inputs(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
) -> None:
    """Validate complete doctor rankings and hospital capacities."""
    if not isinstance(preferences, dict):
        raise TypeError("Preferences must be a dictionary.")
    if not isinstance(capacities, dict):
        raise TypeError("Capacities must be a dictionary.")
    if not preferences:
        raise ValueError("At least one doctor must be provided.")
    if not capacities:
        raise ValueError("At least one hospital must be provided.")

    hospital_names = set(capacities)
    for hospital, capacity in capacities.items():
        if not isinstance(hospital, str) or not hospital.strip():
            raise ValueError("Every hospital name must be a non-empty string.")
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError(f"Capacity for {hospital!r} must be an integer.")
        if capacity < 0:
            raise ValueError(f"Capacity for {hospital!r} cannot be negative.")

    for doctor, ranked_hospitals in preferences.items():
        if not isinstance(doctor, str) or not doctor.strip():
            raise ValueError("Every doctor name must be a non-empty string.")
        if not isinstance(ranked_hospitals, list):
            raise TypeError(f"Preferences for {doctor!r} must be a list.")
        if len(ranked_hospitals) != len(capacities):
            raise ValueError(f"{doctor!r} must rank every hospital exactly once.")
        if any(not isinstance(name, str) or not name.strip() for name in ranked_hospitals):
            raise ValueError(f"All hospitals ranked by {doctor!r} must have valid names.")
        if len(set(ranked_hospitals)) != len(ranked_hospitals):
            raise ValueError(f"Preferences for {doctor!r} contain duplicate hospitals.")
        if set(ranked_hospitals) != hospital_names:
            missing = sorted(hospital_names - set(ranked_hospitals))
            unknown = sorted(set(ranked_hospitals) - hospital_names)
            raise ValueError(
                f"Preferences for {doctor!r} do not match the hospital list. "
                f"Missing: {missing}; unknown: {unknown}."
            )

    total_capacity = sum(capacities.values())
    if total_capacity < len(preferences):
        raise ValueError(
            "Total hospital capacity must be at least the number of doctors. "
            f"Doctors: {len(preferences)}; total capacity: {total_capacity}."
        )
