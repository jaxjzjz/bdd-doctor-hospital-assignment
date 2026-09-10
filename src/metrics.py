"""Evaluation metrics for doctor-hospital assignments."""

from collections import Counter
from statistics import mean

from .assignment import create_rank_lookup


def evaluate_assignment(
    doctors: list[str],
    assignment: dict[str, dict[str, str]],
    preferences: dict[str, list[str]],
) -> dict[str, object]:
    """Evaluate a complete assignment using rank-based metrics."""
    if len(doctors) != len(set(doctors)):
        raise ValueError("Doctor list cannot contain duplicate names.")
    if set(doctors) != set(preferences):
        raise ValueError("Doctor list must match the preference dictionary.")
    if set(assignment) != set(doctors) or len(assignment) != len(doctors):
        raise ValueError("Every doctor must have exactly one assignment.")

    rank_lookup = create_rank_lookup(preferences)
    assigned_ranks = {}
    for doctor in doctors:
        hospital = assignment[doctor].get("hospital")
        if hospital not in rank_lookup[doctor]:
            raise ValueError(
                f"Assignment for {doctor!r} contains an unknown hospital."
            )
        assigned_ranks[doctor] = rank_lookup[doctor][hospital]
    ranks = list(assigned_ranks.values())
    total_cost = sum(ranks)
    first_choice_count = sum(rank == 1 for rank in ranks)
    top_three_count = sum(rank <= 3 for rank in ranks)

    return {
        "total_cost": total_cost,
        "average_rank": total_cost / len(doctors),
        "first_choice_count": first_choice_count,
        "first_choice_rate": first_choice_count / len(doctors),
        "top_three_rate": top_three_count / len(doctors),
        "worst_assigned_rank": max(ranks),
        "rank_distribution": dict(sorted(Counter(ranks).items())),
        "assigned_ranks": assigned_ranks,
    }


def summarize_trials(trial_metrics: list[dict[str, object]]) -> dict[str, float]:
    """Summarize repeated randomized greedy trials."""
    if not trial_metrics:
        raise ValueError("At least one trial is required.")
    costs = [float(metrics["total_cost"]) for metrics in trial_metrics]
    return {
        "mean_total_cost": mean(costs),
        "best_total_cost": min(costs),
        "worst_total_cost": max(costs),
        "mean_average_rank": mean(
            float(metrics["average_rank"]) for metrics in trial_metrics
        ),
        "mean_first_choice_rate": mean(
            float(metrics["first_choice_rate"]) for metrics in trial_metrics
        ),
        "mean_top_three_rate": mean(
            float(metrics["top_three_rate"]) for metrics in trial_metrics
        ),
        "mean_worst_assigned_rank": mean(
            float(metrics["worst_assigned_rank"]) for metrics in trial_metrics
        ),
    }
