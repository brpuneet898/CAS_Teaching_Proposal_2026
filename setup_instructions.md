# ClimateTwin V2 Setup Instructions

These instructions help students and instructors run the ClimateTwin case package in Jupyter Notebook, JupyterLab, VS Code, or Google Colab.

## 1. Files in the package

Keep all files together in one folder:

```text
ClimateTwin/
├── dataset.csv
├── claim_level_data.csv          # instructor-side; needed for solution/regeneration checks
├── data_dictionary.md
├── case_study.md
├── student_notebook.ipynb
├── solution.ipynb                # instructor-only
├── data_script.py                # instructor-only generator
├── instructor_guide.md           # instructor-only
├── expected_output.md            # instructor-only or post-class
├── rubric.md
├── setup_instructions.md
└── case_study.pptx
```

Students normally receive:

```text
dataset.csv
case_study.md
data_dictionary.md
student_notebook.ipynb
setup_instructions.md
rubric.md
```

Instructors retain:

```text
claim_level_data.csv
data_script.py
solution.ipynb
instructor_guide.md
expected_output.md
case_study.pptx
```

## 2. Validated environment

The V2 solution was validated in the following environment:

| Component | Validation version |
|---|---|
| Python | 3.13.5 |
| numpy | 2.3.5 |
| pandas | 2.2.3 |
| matplotlib | 3.10.8 |
| statsmodels | 0.14.6 |
| jupyterlab | 4.5.3 |
| notebook | 7.5.3 |
| nbclient | 0.10.4 |

Recommended student environment:

| Package | Recommended version |
|---|---|
| Python | 3.10 or newer |
| numpy | 1.26+ or 2.x |
| pandas | 2.0+ |
| matplotlib | 3.7+ |
| statsmodels | 0.14+ |
| jupyterlab | 4+ |
| notebook | 7+ |
| nbclient | 0.10+ |

## 3. Local setup with `venv`

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install numpy pandas matplotlib statsmodels jupyterlab notebook nbclient
jupyter lab
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy pandas matplotlib statsmodels jupyterlab notebook nbclient
jupyter lab
```

Then open `student_notebook.ipynb`.

## 4. Local setup with conda

```bash
conda create -n climatetwin python=3.11 -y
conda activate climatetwin
pip install numpy pandas matplotlib statsmodels jupyterlab notebook nbclient
jupyter lab
```

Then open `student_notebook.ipynb`.

## 5. Running in VS Code

1. Install Python 3.10 or newer.
2. Install VS Code.
3. Install the Python and Jupyter extensions.
4. Open the folder containing the ClimateTwin files.
5. Select the Python environment created above.
6. Open `student_notebook.ipynb`.
7. Run cells from top to bottom.

## 6. Running in Google Colab

1. Open Google Colab.
2. Upload `student_notebook.ipynb`.
3. Upload `dataset.csv` using the file panel.
4. Make sure `dataset.csv` appears in the same runtime folder as the notebook.
5. Run the setup/import cell.

If the notebook cannot find the dataset, run:

```python
from google.colab import files
uploaded = files.upload()
```

Upload `dataset.csv`, then rerun the data-loading cell. Colab runtimes are temporary, so download your completed notebook before closing the session.

## 7. Folder-path requirement

The student notebook expects:

```python
DATA_PATH = Path("dataset.csv")
```

So `dataset.csv` must be in the same folder as the notebook unless you change the path manually.

Correct:

```text
ClimateTwin/student_notebook.ipynb
ClimateTwin/dataset.csv
```

Incorrect unless the code is changed:

```text
ClimateTwin/student_notebook.ipynb
ClimateTwin/data/dataset.csv
```

## 8. Student quick package test

Run this in the first notebook cell:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

print("Packages loaded successfully")
```

Then run:

```python
df = pd.read_csv("dataset.csv")
print(df.shape)
print(df["location_id"].nunique())
print(df["claim_count"].sum())
print((df["claim_count"] > 0).sum())
```

Expected output:

```text
(750, 35)
250
95
71
```

## 9. Instructor validation checks

Instructors should also check the claim-level table:

```python
annual = pd.read_csv("dataset.csv")
claims = pd.read_csv("claim_level_data.csv")

print(claims.shape)
print((claims["paid_loss"] == 0).sum())
print(round(claims["paid_loss"].sum(), 2))
print(round(annual["aggregate_paid_loss"].sum(), 2))
```

Expected output:

```text
(95, 18)
33
3480012.62
3480012.62
```

## 10. Reproducibility

The student notebook uses fixed seeds for simulation. Monte Carlo results can change slightly if the seed, number of simulations, or simulation method changes. Directional conclusions should remain consistent:

- compound stress should be the largest risk state;
- water stress should be more material than air stress in the V2 reference benchmark;
- mitigation should reduce but not fully eliminate stressed tail risk.

## 11. Instructor-only dataset regeneration

Instructors can regenerate both `dataset.csv` and `claim_level_data.csv` using:

```bash
python data_script.py
```

The script uses only the Python standard library and a fixed deterministic seed. It should reproduce the same V2 files.

Students do not need to run `data_script.py`.

## 12. Running the instructor solution end to end

From the package folder:

```bash
jupyter nbconvert --to notebook --execute solution.ipynb --output solution_executed_check.ipynb
```

The executed notebook should complete without blanket warning suppression. In the V2 reference run, the frequency and severity GLMs both converged and captured zero warnings.

## 13. Troubleshooting

### `FileNotFoundError: dataset.csv`

Put `dataset.csv` in the same folder as the notebook, or update `DATA_PATH`.

### `ModuleNotFoundError: statsmodels`

Run:

```bash
pip install statsmodels
```

Then restart the notebook kernel.

### Notebook uses the wrong Python environment

In Jupyter or VS Code, change the notebook kernel to the environment where packages were installed.

### Plots do not appear

Restart the kernel and rerun cells from the top.

### Monte Carlo results differ slightly

Confirm the random seed and number of simulations. Small differences are acceptable. Large directional differences usually indicate a modelling or scenario-transformation error.

### GLM produces warnings or unstable coefficients

Do not hide warnings automatically. Check whether the response was valid, the severity response was positive, the exposure offset was included, the formula created sparse interaction cells, or the predictors are strongly correlated.

### Gamma model fails

Do not fit a Gamma model to zero paid losses. Use positive claim-level `covered_loss` or a defensible positive conditional severity response.

### Colab session lost uploaded files

Upload `dataset.csv` again. Colab runtimes reset files when the session restarts.

## 14. Student submission checklist

Before submitting:

- The notebook runs from top to bottom.
- Dataset validation numbers match: 750 rows, 250 locations, 95 claims, 71 claim-positive policy-years.
- Frequency model includes exposure offset.
- Severity model uses a positive conditional severity response.
- Policy terms are applied correctly.
- Baseline premium adequacy is calculated.
- All four scenarios are evaluated.
- VaR99 and TVaR99 are reported.
- Mitigation strategy stays within 8,000,000.
- Mitigation is chosen from feasible candidates using TVaR99 as the main criterion.
- The final committee recommendation is completed.
- Limitations are stated clearly.
