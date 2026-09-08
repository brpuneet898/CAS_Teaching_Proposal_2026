# ClimateTwin Setup Instructions

These instructions help students run the ClimateTwin case package in Jupyter Notebook, JupyterLab, VS Code, or Google Colab.

---

## 1. Files in the package

Keep these files together in one folder:

```text
ClimateTwin/
├── dataset.csv
├── data_dictionary.md
├── case_study.md
├── student_notebook.ipynb
├── solution.ipynb              # instructor-only
├── data_script.py              # instructor-only generator
├── instructor_guide.md          # instructor-only
├── expected_output.md           # instructor-only or post-class
├── rubric.md
└── instructions.md
```

Students normally receive:

```text
dataset.csv
case_study.md
data_dictionary.md
student_notebook.ipynb
instructions.md
rubric.md
```

Instructors retain:

```text
solution.ipynb
data_script.py
instructor_guide.md
expected_output.md
```

---

## 2. Recommended Python environment

Recommended versions:

| Package | Recommended version |
|---|---|
| Python | 3.10 or newer |
| numpy | 1.26+ |
| pandas | 2.0+ |
| matplotlib | 3.7+ |
| statsmodels | 0.14+ |
| jupyter | 1.0+ or JupyterLab 4+ |
| notebook | 7+ |

The notebooks use only common Python data-science packages.

---

## 3. Local setup with venv

Open a terminal in the folder where you want the case files.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install numpy pandas matplotlib statsmodels jupyter notebook nbclient
jupyter notebook
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy pandas matplotlib statsmodels jupyter notebook nbclient
jupyter notebook
```

Then open `student_notebook.ipynb`.

---

## 4. Local setup with conda

```bash
conda create -n climatetwin python=3.11 -y
conda activate climatetwin
pip install numpy pandas matplotlib statsmodels jupyter notebook nbclient
jupyter notebook
```

Then open `student_notebook.ipynb`.

---

## 5. Running in VS Code

1. Install Python 3.10 or newer.
2. Install VS Code.
3. Install the Python and Jupyter extensions.
4. Open the folder containing the ClimateTwin files.
5. Select the Python environment or conda environment created above.
6. Open `student_notebook.ipynb`.
7. Run cells from top to bottom.

---

## 6. Running in Google Colab

1. Open Google Colab.
2. Upload `student_notebook.ipynb`.
3. Upload `dataset.csv` using the file panel.
4. Make sure `dataset.csv` appears in the same runtime folder as the notebook.
5. Run the setup cell.

If the notebook cannot find the dataset, use:

```python
from google.colab import files
uploaded = files.upload()
```

then upload `dataset.csv` and rerun the data-loading cell.

Colab runtimes are temporary. Download your completed notebook before closing the session.

---

## 7. Folder structure requirement

The notebook expects:

```python
DATA_PATH = Path("dataset.csv")
```

So `dataset.csv` must be in the same folder as `student_notebook.ipynb`, unless you change the path manually.

Correct:

```text
ClimateTwin/student_notebook.ipynb
ClimateTwin/dataset.csv
```

Incorrect:

```text
ClimateTwin/student_notebook.ipynb
ClimateTwin/data/dataset.csv
```

unless the code is changed to:

```python
DATA_PATH = Path("data/dataset.csv")
```

---

## 8. Reproducibility

Use the provided seed in the notebook:

```python
SEED = 20260908
rng = np.random.default_rng(SEED)
```

Monte Carlo results can change if the seed, number of simulations, or simulation method changes. Your results should still be directionally consistent with the expected-output ranges.

---

## 9. Instructor-only dataset regeneration

Instructors can regenerate the exact CSV using:

```bash
python data_script.py
```

The script uses only the Python standard library and a fixed seed. It recreates the same `dataset.csv` byte-for-byte.

Students do not need to run `data_script.py`.

---

## 10. Quick package test

After installation, run this in Python or in the first notebook cell:

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
```

Expected output:

```text
(750, 35)
250
138
```

---

## 11. Troubleshooting

### Problem: `FileNotFoundError: dataset.csv`

Fix: Put `dataset.csv` in the same folder as the notebook, or update `DATA_PATH`.

### Problem: `ModuleNotFoundError: statsmodels`

Fix:

```bash
pip install statsmodels
```

Then restart the notebook kernel.

### Problem: Notebook uses the wrong Python environment

Fix: In Jupyter or VS Code, change the notebook kernel to the environment where packages were installed.

### Problem: Plots do not appear

Fix: Restart the kernel and rerun cells from the top. In Jupyter, make sure the plotting cell is executed.

### Problem: Monte Carlo results differ slightly

Fix: Confirm the random seed and number of simulations. Small simulation differences are acceptable; large directional differences usually indicate a modelling or scenario-transformation error.

### Problem: GLM produces warnings or unstable coefficients

Fix: This can happen with correlated synthetic indicators and sparse interaction categories. Students should focus on actuarial interpretation, prediction, and scenario results rather than over-interpreting every coefficient.

### Problem: Colab session lost uploaded files

Fix: Upload `dataset.csv` again. Colab runtimes reset files when the session restarts.

---

## 12. Submission checklist for students

Before submitting:

- The notebook runs from top to bottom.
- Dataset validation numbers match: 750 rows, 250 locations, 138 claims.
- Frequency model includes exposure offset.
- Severity model uses claim-positive rows only.
- Baseline premium adequacy is calculated.
- All four scenarios are evaluated.
- VaR99 and TVaR99 are reported.
- Mitigation strategy stays within 8,000,000.
- Final committee recommendation is completed.
- Limitations are stated clearly.
