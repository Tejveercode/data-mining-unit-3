# Topic 11 — Prediction: Linear Regression

> **LMS page:** *Prediction: Linear Regression* · **CO4**.
> Both regressions below (simple and multiple) are **solved and verified**, with every coefficient, prediction, residual and error measure shown.

---

## 1. What it is

**Linear regression is a supervised learning technique used for prediction tasks.** It models the relationship between **one or more independent variables** and a **dependent variable** by **fitting a straight line to the observed data**. The dependent variable is **continuous and numeric**.

**Linear regression is widely used because of its simplicity, interpretability and effectiveness in predicting real-world quantities.**

**Linear regression is the concrete algorithm behind "prediction" from Topic 1** — the numeric branch of supervised learning, as opposed to classification's categorical branch.

---

## 2. The concept of prediction here

**Prediction is estimating an unknown or future numeric value from historical data.** In linear regression, that is achieved by **learning a mathematical relationship between input attributes and the target variable**; once learned, the model predicts values for new data points.

**Contrast with classification:** classification learns **boundaries** that separate classes; regression learns a **function** that maps inputs to a number. Both are supervised; only the target type differs.

---

## 3. The basic idea

**Find the straight line that best represents the relationship between the variables** — the **regression line**.

**The line is chosen so that the difference between actual values and predicted values is minimised.**

```text
Predicted ŷ = b₀ + b₁x₁ + b₂x₂ + … + bₙxₙ
```

Each data point contributes a **residual** `eᵢ = yᵢ − ŷᵢ` — the vertical distance from the point to the line. The line that makes those residuals as small as possible (in the squared sense) is the best fit.

---

## 4. Simple linear regression

**One independent variable, one dependent variable**, modelled as a straight line:

```text
ŷ = b₀ + b₁x

b₁ = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)²        slope
b₀ = ȳ − b₁x̄                                intercept
```

**The relationship is expressed using a linear equation, where the dependent variable changes proportionally with the independent variable.**

### Worked example — the complete calculation

**Data (5 observations):**

| x | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| y | 2 | 4 | 5 | 4 | 5 |

**Step 1 — means:** `x̄ = 15/5 = 3.0`, `ȳ = 20/5 = 4.0`

**Step 2 — the two sums:**

| xᵢ | yᵢ | (xᵢ − x̄) | (yᵢ − ȳ) | product | (xᵢ − x̄)² |
|---|---|---|---|---|---|
| 1 | 2 | −2 | −2 | **4** | 4 |
| 2 | 4 | −1 | 0 | 0 | 1 |
| 3 | 5 | 0 | 1 | 0 | 0 |
| 4 | 4 | 1 | 0 | 0 | 1 |
| 5 | 5 | 2 | 1 | **2** | 4 |
| | | | | **Σ = 6** | **Σ = 10** |

```text
b₁ = 6/10 = 0.6000          b₀ = 4.0 − 0.6 × 3.0 = 2.2000
```

**The regression line: `ŷ = 2.2 + 0.6x`**

**Step 3 — predictions and residuals:**

| xᵢ | yᵢ | ŷᵢ = 2.2 + 0.6xᵢ | residual eᵢ = yᵢ − ŷᵢ | eᵢ² |
|---|---|---|---|---|
| 1 | 2 | **2.8** | **−0.8** | 0.64 |
| 2 | 4 | **3.4** | **+0.6** | 0.36 |
| 3 | 5 | **4.0** | **+1.0** | 1.00 |
| 4 | 4 | **4.6** | **−0.6** | 0.36 |
| 5 | 5 | **5.2** | **−0.2** | 0.04 |
| | | | **Σ ≈ 0** | **SSE = 2.40** |

*Note that the residuals sum to zero — always true for a least-squares line with an intercept, and a quick check that your arithmetic is right.*

**Step 4 — predict a new value:** at `x = 6`, `ŷ = 2.2 + 0.6 × 6 = ` **5.8000**

**Step 5 — evaluate (the error measures):**

```text
MAE  = (0.8 + 0.6 + 1.0 + 0.6 + 0.2)/5 = 3.2/5 = 0.6400
MSE  = 2.40/5 = 0.4800
RMSE = √0.4800 = 0.6928
SST  = Σ(yᵢ − ȳ)² = 4 + 0 + 1 + 0 + 1 = 6.00
R²   = 1 − SSE/SST = 1 − 2.40/6.00 = 0.6000
```

**Interpretation:** the model explains **60 % of the variance** in `y`, leaves an average absolute error of **0.64** units, and a typical error (RMSE) of **0.69**. *The remaining 40 % is variation the single input cannot explain — visible in the table as the point (3, 5), which the line predicts as 4.0.*

---

## 5. Multiple linear regression

**Two or more independent variables, one dependent variable.** It models **how multiple factors together influence the predicted outcome** — useful when prediction depends on several attributes rather than one.

```text
ŷ = b₀ + b₁x₁ + b₂x₂ + … + bₚxₚ
```

The coefficients are obtained from the **normal equations**:

```text
(XᵀX) b = Xᵀ y        →        b = (XᵀX)⁻¹ Xᵀ y
```

where `X` has a leading column of 1s (for the intercept) and one column per predictor.

### Worked example (2 predictors, 6 records)

| # | x₁ | x₂ | y |
|---|---|---|---|
| 1 | 1 | 2 | 5 |
| 2 | 2 | 1 | 6 |
| 3 | 3 | 3 | 10 |
| 4 | 4 | 2 | 11 |
| 5 | 5 | 4 | 15 |
| 6 | 6 | 3 | 14 |

**Normal equations built from the data:**

```text
XᵀX = ⎡ 6   21   15 ⎤        Xᵀy = ⎡ 61  ⎤
      ⎢21   91   59 ⎥              ⎢ 250 ⎥
      ⎣15   59   43 ⎦              ⎣ 170 ⎦
```

**Solving gives:**

```text
b₀ = 1.3333     b₁ = 1.6111     b₂ = 1.2778
ŷ = 1.3333 + 1.6111·x₁ + 1.2778·x₂
```

**Checking the fit:**

| # | y | ŷ | residual |
|---|---|---|---|
| 1 | 5 | 5.5000 | −0.5000 |
| 2 | 6 | 5.8333 | +0.1667 |
| 3 | 10 | 10.0000 | 0.0000 |
| 4 | 11 | 10.3333 | +0.6667 |
| 5 | 15 | 14.5000 | +0.5000 |
| 6 | 14 | 14.8333 | −0.8333 |

```text
SSE = 1.6667    SST = 82.8333    R² = 0.9799
MAE = 0.4444    RMSE = 0.5270
Prediction for (x₁, x₂) = (7, 3):  ŷ = 1.3333 + 1.6111×7 + 1.2778×3 = 16.4444
```

**Reading the coefficients:** each extra unit of `x₁` adds about **1.61** to the prediction *holding `x₂` constant*; each extra unit of `x₂` adds about **1.28**. **That "holding the other constant" clause is what makes a coefficient meaningful** — omit it and the numbers are just decoration.

---

## 6. The regression equation and its coefficients

**The model consists of an intercept and one or more coefficients.** Your page's definitions, in exam form:

- **Intercept `b₀`** — the predicted value **when all independent variables are zero**. It is often outside the data's range and therefore not physically meaningful; it exists to position the line.
- **Coefficient `bᵢ`** — the **change in the dependent variable for a one-unit change in `xᵢ`**, all other variables held constant.

**Sign and magnitude:**

| Coefficient | Meaning |
|---|---|
| **positive** | **direct** relationship — `x` up, `y` up |
| **negative** | **inverse** relationship — `x` up, `y` down |
| **magnitude** | how strongly that variable influences the prediction — *but only comparable if the variables are on the same scale* |

**Standardise the inputs (z-scores) and the coefficients become directly comparable** — that is how you answer "which factor matters most".

---

## 7. The best-fit line and least squares

**The best-fit line is the one that minimises the total error between actual and predicted values.**

**The least squares method estimates the parameters by minimising the sum of squared differences:**

```text
Minimise  SSE(b₀, b₁, …, bₚ) = Σ (yᵢ − ŷᵢ)²
```

**Why square rather than take absolute values?**
1. **Squaring makes the function differentiable everywhere**, so a closed-form solution exists (absolute value has a kink at zero).
2. **It penalises large errors more heavily**, which is usually what you want — one huge miss is worse than several small ones.
3. **Positive and negative residuals cannot cancel**, so the sum genuinely measures total error.

**By minimising squared errors, the model penalises larger errors more heavily and produces an optimal fit.** For simple regression the calculus gives exactly the `b₁` and `b₀` formulas in §4; setting the derivatives to zero produces the **normal equations** for the multiple case.

**A well-fitted line closely follows the pattern of the data points** — and, as a check, a least-squares line always passes through the point `(x̄, ȳ)`. In the worked example: `ŷ(3) = 4.0 = ȳ` ✔

---

## 8. Assumptions of linear regression (the LINE checklist)

| Assumption | What it means | How it fails |
|---|---|---|
| **L — Linearity** | the relationship between X and Y is linear in the parameters | curved data → systematic residuals |
| **I — Independence** | observations are independent of each other | time series, repeated measures → understated error |
| **N — Normality of errors** | residuals are approximately normally distributed | invalidates confidence intervals, not the coefficients |
| **E — Equal variance (homoscedasticity)** | constant variance of errors across the range of X | funnel-shaped residuals → inefficient estimates |

**It assumes independence of observations and constant variance of errors**, and **the accuracy of predictions depends on how well these assumptions hold**.

**Two more that matter in practice:** no **multicollinearity** among predictors (near-duplicate inputs inflate coefficient variance wildly), and no **influential outliers** (a single point can rotate the line).

---

## 9. Prediction using linear regression

**Substitute the values of the independent variables into the regression equation**; the computed result is the predicted value of the dependent variable.

**This predicted value can be used for decision-making and forecasting.** With the simple model, `x = 6 → 5.8`; with the multiple model, `(7,3) → 16.4444`.

**Two cautions worth stating in an exam:**
1. **Extrapolation is unreliable** — a line fitted on x = 1…5 says nothing trustworthy about x = 500. Linear models assume the relationship continues, which is a choice, not a fact.
2. **A prediction is a point estimate** — always report an interval (prediction interval) for a real decision.

---

## 10. Evaluation of a linear regression model

```text
MAE  = (1/n) Σ |yᵢ − ŷᵢ|          same units as y; robust to outliers
MSE  = (1/n) Σ (yᵢ − ŷᵢ)²         penalises large errors; units squared
RMSE = √MSE                        same units as y; penalises large errors
R²   = 1 − SSE/SST                 proportion of variance explained (0…1)
Adjusted R² = 1 − (1−R²)(n−1)/(n−p−1)     penalises adding useless predictors
```

**Worked values from §4:** MAE **0.6400**, MSE **0.4800**, RMSE **0.6928**, R² **0.6000**.

**Why Adjusted R² matters:** plain R² **never decreases** when you add a predictor, even a random one. Adjusted R² charges a penalty per predictor, so it falls when a variable adds nothing — the honest comparison between models of different sizes.

---

## 11. Advantages (your page)

- **Easy to understand and interpret** — a coefficient is a sentence about the business.
- **Computationally efficient** — one closed-form solve, no iterations.
- **Works well for problems with linear relationships.**
- **Provides clear insights into how variables affect predictions** — direction, magnitude and significance, which black-box models do not.
- Serves as the **baseline every fancier model must beat**.
- Extends naturally to **polynomial regression** (add `x²`, `x³` as extra features) and to **regularised** forms (ridge, lasso).

## 12. Limitations (your page)

- **Cannot capture complex non-linear relationships** (unless you engineer terms).
- **Sensitive to outliers**, which can significantly affect the regression line.
- **Performance depends on the validity of the underlying assumptions** (§8).
- **Multicollinearity** makes coefficients unstable and uninterpretable.
- **Extrapolation is dangerous.**
- Correlation ≠ causation — a strong coefficient is not proof of a mechanism.

---

## 13. Applications

**Sales forecasting, price prediction, demand estimation, risk analysis, trend analysis** — *commonly applied in economics, finance, healthcare and engineering*. Concretely: house-price prediction from area and location score, revenue forecasting from ad spend, dose–response in medicine, load estimation in engineering.

---

## 14. Comparison with classification (your page's contrast, extended)

| Aspect | **Linear regression** | **Classification** |
|---|---|---|
| Target | **continuous numeric** | **categorical** |
| Output | a number, e.g. 5.8 | a class label, e.g. "spam" |
| Model | a **line / hyperplane** through values | a **boundary** between regions |
| Objective | minimise **squared error (SSE)** | minimise misclassification / impurity |
| Evaluation | **MAE, MSE, RMSE, R²** | accuracy, precision, recall, F1, AUC |
| Typical algorithms | linear/multiple/polynomial regression, regression trees | decision tree, Naïve Bayes, kNN, SVM, logistic regression |

**Linear regression predicts continuous numeric values, whereas classification predicts categorical class labels.** *Linear regression focuses on estimating quantities; classification focuses on assigning categories.*

**The bridge:** **logistic regression** is linear regression passed through a sigmoid — same linear score, converted into a probability, which turns prediction into classification. That is why the two families are one step apart.

---

## 15. Summary

Linear regression predicts a **continuous numeric target** by fitting the line (or hyperplane) that **minimises the sum of squared residuals**, solved in closed form by least squares. For the five-point example the fit is **`ŷ = 2.2 + 0.6x`** (from `b₁ = 6/10 = 0.6`, `b₀ = ȳ − b₁x̄ = 2.2`), giving predictions 2.8, 3.4, 4.0, 4.6, 5.2, **SSE 2.40**, **MAE 0.64**, **RMSE 0.6928** and **R² 0.60**; with two predictors the normal equations give **`ŷ = 1.3333 + 1.6111x₁ + 1.2778x₂`** and **R² 0.9799**, predicting 16.4444 at (7, 3). The intercept is the value at `x = 0`, each coefficient is the change in `y` per unit change in its `x` **holding the others constant**, and validity rests on the **LINE assumptions** — linearity, independence, normal errors and equal variance — with outliers and extrapolation as the two practical traps.

---

**Next:** [Topic 12 — Overview of Clustering & Need for Clustering](12-clustering-overview.md)
