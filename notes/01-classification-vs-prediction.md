# Topic 1 — Classification vs Prediction

> **LMS page:** *Classification vs Prediction* · the page is tagged **CO5**, but its content belongs with the classification outcomes — **CO4 (apply prediction and classification algorithms on real-time data)**. Treat the topics as CO4 and the clustering pages that follow as CO5.

---

## 1. Where both tasks sit: supervised learning

Classification and prediction are **two important tasks in data mining and machine learning that fall under supervised learning**. In both:

- a model is built from **historical data with known outcomes**,
- the model is then used to make decisions on **new, unseen data**,
- the training set contains **input attributes** (features) and a **target attribute** (the thing being learned).

Because both are supervised, both follow the same pipeline:

```text
collect labelled data → pre-process → split train/test → train model
   → evaluate → deploy → monitor
```

**The key distinction lies in the nature of the target attribute.** That single sentence is the entire topic — everything else follows from it.

---

## 2. Classification: predicting a category

**Definition.** Classification is the process of **assigning data objects to one of several predefined classes or categories**. The target attribute is **categorical or discrete**.

**Objective.** To correctly label each data object using **decision boundaries or rules learned from the training data**.

**Nature of the output.** A **class label** — a distinct category with **no numerical meaning**. You cannot add, subtract or average class labels.

**Examples from your page:**

| Problem | Classes |
|---|---|
| Email filtering | spam / not spam |
| Loan approval | approved / rejected |
| Medical diagnosis | disease / no disease |
| Academic result | pass / fail |

**Working principle.**

1. Train on **labelled** records where each row's class is known.
2. The algorithm analyses **patterns and relationships between attribute values and class labels**.
3. Once trained, it assigns the **most suitable class label** to each new object.

**Algorithms (your page's list):** decision trees, Naïve Bayes, k-nearest neighbours, support vector machines, logistic regression.

*All five "generate models that separate data into distinct class regions."* Notes 2, 3 and 4 cover the first three in this unit.

---

## 3. Prediction: estimating a number

**Definition.** Prediction is the process of **estimating a continuous or numeric value** from input attributes. The target attribute is **quantitative**.

**Objective.** To estimate an **unknown or future value** as accurately as possible.

**Nature of the output.** A **numeric value** — a measurable quantity that **can be compared arithmetically**. "House price 4.2 million" is meaningfully twice "2.1 million"; "spam" is not twice "not spam".

**Examples from your page:** house prices, temperature, sales revenue, stock prices.

**Working principle.** The model learns the **mathematical relationship** between input variables and a numeric target, then evaluates that function on new inputs.

**Algorithms:** **regression-based techniques** — linear regression, multiple regression, polynomial regression, regression trees.

*Note the overlap: a **regression tree** appears in both worlds. The tree structure is shared; only the leaf content changes (class label vs numeric value).*

---

## 4. The differences, side by side

| Aspect | **Classification** | **Prediction (regression)** |
|---|---|---|
| Target attribute | **categorical / discrete** | **continuous / numeric** |
| Output | a **class label** | a **numeric value** |
| Question answered | *which category?* | *how much / how many?* |
| Decision surface | separates **class regions** | fits a **curve/surface** through values |
| Evaluation | **accuracy, precision, recall, confusion matrix, ROC** | **MAE, MSE, RMSE, R²** |
| Error meaning | wrong label vs right label | **distance** from the true value |
| Typical algorithms | decision tree, Naïve Bayes, kNN, SVM, logistic regression | linear/multiple/polynomial regression, regression trees |

**Your page's three sentences, restated for an exam:**

1. Classification deals with **categorical output**; prediction deals with **continuous numeric output**.
2. Classification **assigns objects to predefined classes**; prediction **estimates an unknown numeric value**.
3. Classification evaluation focuses on **correctness of labels**; prediction evaluation focuses on the **accuracy of the numeric estimate**.

---

## 5. How each is evaluated (the formulas behind "evaluation")

**Classification — the confusion matrix** (the foundation of everything else):

|  | Predicted positive | Predicted negative |
|---|---|---|
| **Actual positive** | TP | FN |
| **Actual negative** | FP | TN |

```text
Accuracy  = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)        "of those flagged, how many were right?"
Recall    = TP / (TP + FN)        "of the real ones, how many did we catch?"
F1        = 2·(Precision·Recall) / (Precision + Recall)
```

*A model that predicts "not spam" for everything can be 99 % accurate and useless — which is why accuracy alone is never enough on imbalanced data.*

**Prediction — error-based measures:**

```text
MAE  = (1/n) Σ |yᵢ − ŷᵢ|              average absolute miss, same units as y
MSE  = (1/n) Σ (yᵢ − ŷᵢ)²             punishes large misses
RMSE = √MSE                            back in the original units, still punishes large misses
R²   = 1 − SS_res/SS_tot               fraction of variance explained
```

**Why MSE and not MAE?** Squaring makes a single large error count much more than several small ones — right when big misses are expensive.

---

## 6. The distinction that is easy to miss

**Classification can output a number — a probability.** A classifier usually computes `P(class | x)` and then applies a threshold (0.5 by default). Changing that threshold trades precision against recall without retraining. So:

- **logistic regression** is called a classification algorithm even though its output is a number between 0 and 1;
- the *label* is the decision, the *probability* is the model's belief.

**Prediction can output a category — after binning.** If you predict a price and then bucket it as *cheap / medium / expensive*, you have turned a regression into a classification (this is exactly the discretization from Unit 2, applied to the target).

**A third task for contrast:** **clustering** (topics 5–9) is **unsupervised** — there are **no labels at all**, and the groups are discovered rather than predefined.

| | Supervised? | Target | Output |
|---|---|---|---|
| **Classification** | yes | categorical, predefined | label |
| **Prediction** | yes | numeric | value |
| **Clustering** | **no** | none | groups, discovered |

---

## 7. Applications (your page's lists)

**Classification:** fraud detection, medical diagnosis, sentiment analysis, document categorisation, customer churn analysis.

**Prediction:** sales forecasting, demand forecasting, risk estimation, weather prediction, financial analysis.

**Both appear in one system.** A bank *classifies* a loan application as approve/reject and *predicts* the expected loss if it approves — two models, one decision.

---

## 8. Choosing between them

Ask three questions:

1. **Is the target a category or a number?** Category → classification. Number → prediction.
2. **Do I need a decision or an estimate?** A rule that fires ("flag this transaction") → classification. A magnitude ("this house is worth 4.2 M") → prediction.
3. **What does a mistake cost?** If a wrong label is a discrete, countable loss, optimise accuracy/precision/recall. If a numerical miss has a magnitude, optimise MAE/RMSE.

**Common exam trap:** "Predict whether a customer will churn" is **classification** (yes/no), even though the word *predict* appears. *Predict* in data mining names the numeric branch; the everyday English verb applies to both.

---

## 9. Summary

Classification and prediction are both supervised: they learn from historical data with a known target and apply the learned model to unseen data. They differ in the **nature of the target**: classification predicts a **categorical class label** using decision boundaries (decision trees, Naïve Bayes, kNN, SVM, logistic regression) and is evaluated with accuracy, precision, recall, confusion matrix and ROC; prediction estimates a **continuous numeric value** using regression techniques (linear, multiple, polynomial, regression trees) and is evaluated with MAE, MSE, RMSE and R². The practical rule: **a category in the target means classification, a number means prediction; no target at all means clustering.**

---

**Next:** [Topic 2 — Decision Tree Induction](02-decision-tree-induction.md)
