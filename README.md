# Doctor-Hospital Assignment

A small project for Biomedical Data Design (BDD) by Bohan Chen, Zihan Fan, and Zheng Jian.

We assign doctors to hospitals based on their preferences while respecting each hospital's capacity. The Hungarian algorithm finds an assignment with the lowest total rank cost, where rank 1 means a doctor's first choice. We compare it with a greedy baseline that processes doctors in a random order and gives each doctor their best available hospital.

## Submitted notebooks

- **[Interactive_demo.ipynb](Interactive_demo.ipynb)** — Enter the number of doctors and hospitals, hospital capacities, and either manual or random preferences. The input section shows the counts, total capacity, and preference lists. The final section runs both methods and prints the results.
- **[Large_example.ipynb](Large_example.ipynb)** — Run a fixed example with 20 doctors, 6 hospitals, and 20 available slots. Many doctors prefer H1 or H2, creating competition for their limited capacity. No manual input is needed.

Both notebooks contain all the code they need and can run independently. Each compares Hungarian with **1,000 randomized greedy trials using seed 10**.

## How to run

Use Python 3.11 or newer with Jupyter Notebook or JupyterLab. The assignment code uses only Python's standard library; no additional computation packages are needed.

1. Open either notebook and select a Python kernel.
2. Run the cells from top to bottom.
3. In the interactive notebook, answer the prompts in the input section. Choose `m` for manual preferences or `r` for random preferences; the random-input seed defaults to 0.
4. Continue to the last cell to see the assignment and comparison results.

For manual input, `2 1 3` means `H2 > H1 > H3`. Each doctor must rank every hospital exactly once. Capacities must be non-negative integers, and total capacity must be at least the number of doctors.

After changing interactive input, rerun the input cell and the final results cell. If you restart the kernel, rerun all cells.

## Reading the results

The output includes each doctor's assigned hospital and rank, Hungarian metrics, and a summary of the greedy trials. Lower total cost and average rank are better; higher first-choice and top-three rates are better. The worst assigned rank and rank distribution help show how preferences are satisfied across doctors.

The greedy summary reports mean metrics and the best/worst total costs across trials. Hungarian minimizes total rank cost, but does not guarantee the best outcome for every individual doctor. Hospitals do not rank doctors in this project.

## AI tool use

AI-assisted tools were used for code review suggestions, debugging assistance, and documentation refinement.
