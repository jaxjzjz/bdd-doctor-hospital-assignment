# Doctor-Hospital Rank-Order Assignment

This repository contains a capacity-constrained doctor-hospital assignment system developed for the Biomedical Data Design mini-hackathon. The system assigns every doctor to exactly one hospital while respecting hospital capacities and minimizing the total rank cost of the assignments.

## Team Members

- Bohan Chen
- Zihan Fan
- Zheng Jian

## Project Plan

The original one-page project plan is available in [`project_plan.pdf`](project_plan.pdf).

## Problem Definition

Assume there are `N` doctors and `K` hospitals. Every doctor provides a complete ranking of all hospitals, from most preferred to least preferred. Hospitals do not rank doctors. Hospital `j` has capacity `C_j`.

Let `x_ij = 1` when doctor `i` is assigned to hospital `j`, and let `x_ij = 0` otherwise. Let `c_ij` be the numerical rank of hospital `j` in doctor `i`'s preference list, where rank 1 is the first choice.

The optimization objective is:

```text
minimize sum(c_ij * x_ij)
```

subject to:

```text
Every doctor is assigned to exactly one hospital.
No hospital receives more doctors than its capacity.
x_ij is either 0 or 1.
```

## Input Format

The core functions accept two Python dictionaries.

### Doctor Preferences

Each dictionary key is a unique doctor name. Each value is a complete hospital ranking ordered from best to worst.

```python
preferences = {
    "D1": ["H1", "H2", "H3"],
    "D2": ["H2", "H3", "H1"],
    "D3": ["H1", "H3", "H2"]}
```

### Hospital Capacities

Each dictionary key is a unique hospital name, and each value is the hospital's non-negative integer capacity.

```python
capacities = {
    "H1": 1,
    "H2": 1,
    "H3": 1}
```

The total hospital capacity must be at least the number of doctors.

## Input Assumptions

- At least one doctor and one hospital are required.
- Every doctor ranks every hospital exactly once.
- Rankings cannot contain duplicate hospitals.
- Hospital names in the rankings must match the capacity dictionary.
- Hospital capacities must be non-negative integers.
- Total capacity must be greater than or equal to the number of doctors.
- Tied rankings and incomplete rankings are not supported in the initial implementation.
- The core algorithm has no fixed maximum number of doctors or hospitals.

## Method 1: Hungarian Algorithm

The main method is the Hungarian algorithm. The standard assignment problem is one-to-one, but one hospital may accept multiple doctors. The program handles this by expanding each hospital into capacity slots.

For example:

```text
H1 capacity = 2  ->  H1_1, H1_2
H2 capacity = 1  ->  H2_1
```

Every slot belonging to the same hospital receives the same rank cost for a given doctor. The program then builds a doctor-by-slot cost matrix and finds an assignment with the minimum total rank cost.

The implementation supports rectangular cost matrices when total capacity is greater than the number of doctors. Multiple optimal assignments may exist; the algorithm returns one of them.

## Method 2: Randomized Greedy Baseline

The baseline processes doctors one at a time. Each doctor is assigned to the highest-ranked hospital that still has capacity. A greedy result depends on the order in which doctors are processed, so the program repeatedly randomizes the doctor order.

The interactive demonstration runs 100 greedy trials. The larger example runs 1,000 trials and reports the mean, best, and worst greedy results. A fixed random seed makes the experiment reproducible.

## Evaluation Metrics

- **Total rank cost:** Sum of all assigned hospital ranks. Lower is better.
- **Average rank:** Total rank cost divided by the number of doctors. Lower is better.
- **First-choice count:** Number of doctors assigned to their first choice.
- **First-choice rate:** Fraction of doctors assigned to their first choice.
- **Top-three rate:** Fraction of doctors assigned to one of their first three choices.
- **Worst assigned rank:** The lowest preference received by any doctor. Lower is better.
- **Rank distribution:** Number of doctors receiving each rank.

Total rank cost and average rank describe overall efficiency. The worst assigned rank and rank distribution provide additional information about fairness.

## Repository Structure

- **[Interactive_demo.ipynb](Interactive_demo.ipynb)** — Enter the number of doctors and hospitals, hospital capacities, and either manual or random preferences. The input section shows the counts, total capacity, and preference lists. The final section runs both methods and prints the results. 
- **[Large_example.ipynb](Large_example.ipynb)** — Run a fixed example with 20 doctors, 6 hospitals, and 20 available slots. Many doctors prefer H1 or H2, creating competition for their limited capacity. No manual input is needed.

Both notebooks contain all the code they need and can run independently. Each compares Hungarian with **1,000 randomized greedy trials using seed 10**. 

## Environment

- Python 3.11 or newer with Jupyter Notebook or JupyterLab.
- No third-party Python packages are required for the current implementation.

## How to run

1. Open either notebook and select a Python kernel.
2. Run the cells from top to bottom.
3. In the interactive notebook, answer the prompts in the input section:
    1. Number of doctors
    2. Number of hospitals
    3. Capacity of each hospital
    4. Manual or random preference mode
    5. A complete preference ranking for each doctor when manual mode is selected

For three hospitals, a manual entry such as:

```text
2 1 3
```

means `H2` is the first choice, `H1` is the second choice, and `H3` is the third choice.

 Choose `m` for manual preferences or `r` for random preferences; the random-input seed defaults to 0.

4. Continue to the last cell to see the assignment and comparison results.

## Larger Example Result

The included 20-doctor example produced the following reproducible result:

```text
Hungarian total rank cost: 30
Hungarian average rank: 1.5
Hungarian first-choice rate: 55%
Randomized greedy mean total rank cost: 37.699
Randomized greedy best total rank cost: 30
Randomized greedy worst total rank cost: 50
```

These results show that a greedy assignment can occasionally match the optimal cost, but its average and worst outcomes are poorer because it makes assignments without reconsidering earlier decisions.

## Limitations

- Rank positions are treated as equally spaced costs. The difference between ranks 1 and 2 is assumed to equal the difference between ranks 2 and 3.
- Minimizing total rank cost does not guarantee the fairest result for every doctor.
- Hospitals do not provide preferences over doctors.
- Tied and incomplete preference lists are not supported.
- The slot representation may increase the cost matrix size when hospital capacities are very large.
- The interactive version currently uses automatically generated doctor and hospital identifiers.

## Possible Extensions

- Support incomplete or tied rankings.
- Support hospital preferences and compare with stable matching methods.
- Add nonlinear rank costs that penalize low-ranked assignments more heavily.
- Add fairness objectives, such as minimizing the worst assigned rank.
- Compare the slot-based Hungarian method with minimum-cost flow.
- Load input data from CSV or JSON files.
- Measure runtime as the number of doctors and hospitals increases.

## AI Tool Use

AI-assisted tools were used during development for code review suggestions, debugging assistance, and documentation refinement. 

## References

1. Kuhn, H. W. (1955). The Hungarian Method for the Assignment Problem. *Naval Research Logistics Quarterly, 2*(1-2), 83-97. https://doi.org/10.1002/nav.3800020109
2. Kuhn, H. W. (1956). Variants of the Hungarian Method for Assignment Problems. *Naval Research Logistics Quarterly, 3*(4), 253-258.
3. Munkres, J. (1957). Algorithms for the Assignment and Transportation Problems. *Journal of the Society for Industrial and Applied Mathematics, 5*(1), 32-38. https://doi.org/10.1137/0105003
4. Wu, Y., Lee, C. S., Lee, A. Y., & Van Gelder, R. N. (2025). Improving Residency Matching Through Computational Optimization. *JAMA Network Open, 8*(6), e2517077. https://doi.org/10.1001/jamanetworkopen.2025.17077
