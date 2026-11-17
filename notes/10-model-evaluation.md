# Topic 10 — Model Evaluation: Confusion Matrix, Accuracy, Precision, Recall, F1, ROC

> **LMS page:** *Model Evaluation – Confusion Matrix, Accuracy, Precision, Recall, F1, ROC* · **CO4**.
> The confusion matrix, every metric and the full ROC/AUC computation below are **verified by calculation**.

---

## 1. What model evaluation is

**Model evaluation is the process of measuring how well a classification model performs on unseen data.** It determines the **effectiveness, reliability and usefulness** of a predictive model.

**Evaluation metrics compare the predicted class labels with the actual class labels** to assess performance.

**Proper evaluation is essential to avoid misleading conclusions and to select the best model for a given problem.** A model that looks excellent on its training data and fails in deployment is not a good model — it is an untested one.

---

## 2. The confusion matrix

**A tabular representation that compares actual class labels with predicted class labels**, providing a **detailed breakdown of correct and incorrect predictions**.

**The confusion matrix forms the foundation for accuracy, precision, recall and F1** — every one of them is just a ratio of four numbers.

### The four outcomes (your page's definitions)

| Term | Meaning |
|---|---|
| **True Positive (TP)** | the model **correctly predicts the positive** class |
| **True Negative (TN)** | the model **correctly predicts the negative** class |
| **False Positive (FP)** | the model predicts positive when the **actual class is negative** (a false alarm) |
| **False Negative (FN)** | the model predicts negative when the **actual class is positive** (a missed case) |

### The table

|  | **Predicted positive** | **Predicted negative** | Row total |
|---|---|---|---|
| **Actual positive** | **TP** | **FN** | TP + FN |
| **Actual negative** | **FP** | **TN** | FP + TN |
| **Column total** | TP + FP | FN + TN | **N** |

**The two rows are the truth; the two columns are the model's claims.** That framing makes the error types obvious: **FN lives in the "actual positive" row**, **FP lives in the "actual negative" row**.

### Why it matters

**The confusion matrix provides more insight than a single accuracy value:**
- it shows **the types of errors** the model makes, not just how many;
- it reveals **whether the model is biased toward a particular class**;
- it is **especially useful when the class distribution is imbalanced**, where accuracy hides the failure entirely.

---

## 3. Worked confusion matrix (memorise this pattern)

**Test set of 20 records** (10 actually positive, 10 actually negative), model results:

|  | Predicted positive | Predicted negative | Total |
|---|---|---|---|
| **Actual positive** | **TP = 8** | **FN = 2** | 10 |
| **Actual negative** | **FP = 4** | **TN = 6** | 10 |
| **Total** | 12 | 8 | **20** |

Read it out loud: *"Of 10 truly positive cases the model caught 8 and missed 2; of 10 truly negative cases it correctly cleared 6 and wrongly flagged 4."* Every metric below comes from those four numbers.

---

## 4. Accuracy

**The overall correctness: the ratio of correctly classified instances to the total number.**

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**Worked:**
```text
Accuracy = (8 + 6) / 20 = 14/20 = 0.7000  → 70 %
```

**Simple to understand but potentially misleading with imbalanced classes.**

### The limitation (the accuracy paradox)

**In datasets where one class dominates, a model may achieve high accuracy by simply predicting the majority class.**

On our balanced set, a model that predicts **everything negative** scores:
```text
Accuracy = (0 + 10)/20 = 0.5000      Recall = 0      Precision = 0/0 (undefined)
```

Now change the balance — 1 % positives:
```text
1000 records, 10 positive, 990 negative
"always negative" model:  Accuracy = 990/1000 = 0.99        Recall = 0
```

**99 % accuracy, zero usefulness.** A model that never detects a single fraud case is worthless to a bank, however impressive its accuracy. **This limitation makes additional metrics necessary** — and it is the single most examinable point of this topic.

---

## 5. Precision

**Of the instances the model predicted positive, how many actually are positive** — the **quality** of positive predictions.

```text
Precision = TP / (TP + FP)
```

**Worked:**
```text
Precision = 8 / (8 + 4) = 8/12 = 0.6667  → 66.7 %
```

**High precision indicates the model makes fewer false-positive errors.** "When it says spam, it is right two times out of three."

**Use when a false positive is expensive:** flagging a legitimate email as spam (you lose a real message), rejecting a good loan applicant, blocking a valid transaction.

---

## 6. Recall (sensitivity, true positive rate)

**Of the actual positive instances, how many the model correctly identified** — the **coverage** of positives.

```text
Recall = TP / (TP + FN)
```

**Worked:**
```text
Recall = 8 / (8 + 2) = 8/10 = 0.8000  → 80 %
```

**High recall indicates the model makes fewer false-negative errors.** "It catches four out of five real cases."

**Use when a false negative is expensive:** missing a cancer, missing a fraudulent transaction, letting spam through, missing a machine fault.

**Also called sensitivity or the true positive rate (TPR)** — the same number appears again in the ROC curve.

---

## 7. The precision–recall trade-off

**There is often a trade-off: increasing precision may reduce recall, and increasing recall may reduce precision.**

**Why, mechanically:** most classifiers output a score and apply a threshold.

| Threshold | Effect | Precision | Recall |
|---|---|---|---|
| **lowered** ("flag more") | catch more positives, but also more false alarms | **falls** | **rises** |
| **raised** ("flag only when sure") | fewer false alarms, but miss more | **rises** | **falls** |

**Both are 1.0 only for a perfect classifier.** **The choice depends on the application domain and the cost of different types of errors:**

| Application | Prioritise | Because |
|---|---|---|
| Spam filter | **precision** | a false positive loses a real email |
| Cancer screening | **recall** | a false negative can be fatal |
| Fraud detection | **recall** (then review) | missed fraud is a direct loss; analysts can absorb false alarms |
| Search / recommendations | **precision at k** | users see the top few results only |
| Loan default | depends on margin | both errors cost money; weigh them |

---

## 8. F1-score

**A single metric combining precision and recall as their harmonic mean** — a **balanced** measure when both matter.

```text
F1 = 2 · (Precision × Recall) / (Precision + Recall)  =  2TP / (2TP + FP + FN)
```

**Worked:**
```text
F1 = 2 × 0.6667 × 0.8000 / (0.6667 + 0.8000)
   = 1.0667 / 1.4667 = 0.7273
```

**Why harmonic mean and not arithmetic?** The harmonic mean is **pulled toward the smaller value**: a model with precision 1.0 and recall 0.0 has an arithmetic mean of 0.5 but an F1 of **0** — correctly reflecting that it is useless. **That is the property being exploited.**

**Especially useful with imbalanced datasets**, where accuracy is meaningless and you need one number that punishes ignoring either side.

**Variants worth naming:** `F_β = (1+β²)·P·R / (β²·P + R)` — β > 1 weights recall more, β < 1 weights precision more. `F2` is standard in medical screening; `F0.5` in spam filtering.

---

## 9. Specificity (the missing sixth metric)

**Of the actual negatives, how many were correctly cleared:**

```text
Specificity = TN / (TN + FP) = 6/10 = 0.6000
```

**Balanced accuracy** = (recall + specificity)/2 = (0.8 + 0.6)/2 = **0.7000** — the right accuracy for imbalanced data, because it averages the two classes' hit rates instead of the raw counts.

**False positive rate (FPR)** = `FP/(FP+TN)` = 4/10 = **0.4000**. Note it is `1 − specificity`.

---

## 10. The ROC curve

**A graphical representation of a classifier's performance across all threshold values.** It plots:

```text
y-axis: True Positive Rate  = TP/(TP+FN) = recall = sensitivity
x-axis: False Positive Rate = FP/(FP+TN) = 1 − specificity
```

**ROC analysis examines how these rates change as the classification threshold varies** — every threshold gives one point, and joining them traces the curve.

### Worked ROC (12 test instances, 6 positive)

Scores and true labels, sorted by score:

| # | Score | Actual | TP | FP | TPR | FPR |
|---|---|---|---|---|---|---|
| 1 | 0.95 | + | 1 | 0 | 0.1667 | 0.0000 |
| 2 | 0.90 | + | 2 | 0 | 0.3333 | 0.0000 |
| 3 | 0.85 | − | 2 | 1 | 0.3333 | **0.1667** |
| 4 | 0.80 | + | 3 | 1 | 0.5000 | 0.1667 |
| 5 | 0.75 | + | 4 | 1 | 0.6667 | 0.1667 |
| 6 | 0.70 | − | 4 | 2 | 0.6667 | 0.3333 |
| 7 | 0.65 | + | 5 | 2 | 0.8333 | 0.3333 |
| 8 | 0.60 | − | 5 | 3 | 0.8333 | 0.5000 |
| 9 | 0.55 | − | 5 | 4 | 0.8333 | 0.6667 |
| 10 | 0.50 | + | 6 | 4 | **1.0000** | 0.6667 |
| 11 | 0.45 | − | 6 | 5 | 1.0000 | 0.8333 |
| 12 | 0.40 | − | 6 | 6 | 1.0000 | 1.0000 |

**The curve starts at (0,0) and ends at (1,1)**: at the highest threshold nothing is predicted positive (TPR = FPR = 0); at the lowest, everything is (TPR = FPR = 1). **The diagonal is the "random classifier"** — an honest coin flip.

**Reading it:** the further the curve bows toward the **top-left corner**, the better the classifier. A perfect classifier goes straight up to (0,1) and then across.

### The thresholds shown are the *real* thresholds

Each row is "predict positive if score > this value". That is why ROC is called **threshold-independent evaluation**: it judges the ranking the model produces, not one arbitrary cut.

---

## 11. AUC — the area under the ROC curve

**A single numeric value summarising overall performance.**

```text
AUC = Σ (trapezoids under the curve)
    = 0.5·(0.1667−0)·(0+0.1667) + … computed over the 12 segments
    = 0.7778
```

**Interpretation:**

| AUC | Meaning |
|---|---|
| **1.0** | perfect ranking — every positive scored above every negative |
| **0.9–1.0** | excellent |
| **0.8–0.9** | good |
| **0.7–0.8** | fair (our 0.7778 sits here) |
| **0.5** | **random** — no discriminative ability |
| **< 0.5** | worse than random — the model is systematically inverted |

**The cleanest way to explain AUC:** it is the **probability that a randomly chosen positive instance receives a higher score than a randomly chosen negative instance**. 0.7778 means that in about 78 % of positive-vs-negative pairs, the model ranked the positive higher.

**Two properties that make AUC popular:** it is **threshold-free** (good for comparing models before choosing an operating point) and **prevalence-independent** (insensitive to class balance, unlike accuracy).

**Where AUC misleads:** in **heavily imbalanced** problems, a high AUC can coexist with useless precision, because the false-positive rate is dominated by the huge negative class. That is why **precision–recall curves** are preferred for rare-event detection.

---

## 12. Why multiple metrics are needed (your page's summary)

**No single metric can fully describe model performance:**

| Metric | What it tells you | What it hides |
|---|---|---|
| **Accuracy** | general overview of correctness | imbalance — can be 99 % with zero positives found |
| **Precision** | correctness of positive predictions | how many positives were missed |
| **Recall** | coverage of actual positives | how many false alarms were raised |
| **F1** | balance of precision and recall | the ratio (a model good at both scores high; so does one mediocre at both) |
| **ROC / AUC** | threshold-independent ranking quality | the operating point actually used |

**ROC and AUC provide threshold-independent evaluation, making them useful for comparing models** — but for deployment you must still choose a threshold, and that choice is what precision/recall measure.

---

## 13. Computing it correctly (the mistakes that lose marks)

1. **Report the confusion matrix first**, then the metrics — it shows you know where the numbers come from.
2. **State which class is "positive".** Precision and recall depend on that choice; accuracy does not.
3. **Never report accuracy alone on imbalanced data** — say why: the majority-class baseline.
4. **Use a held-out test set or cross-validation.** Metrics on training data measure memorisation.
5. **For multi-class**, average per-class precision/recall (macro = unweighted mean; micro = pooled counts; weighted = by class size) and say which you used.
6. **ROC needs scores, not labels** — if the model only outputs labels, you cannot draw it.

---

## 14. Applications of the metrics (your page)

**Precision is important where false positives are costly** — spam detection.
**Recall is important where missing a positive is dangerous** — medical diagnosis.
**F1 is useful when both matter equally** — general model comparison, imbalanced classification.
**ROC and AUC are commonly used in credit scoring, medical testing and machine-learning research** — anywhere models must be compared before a threshold is chosen.

---

## 15. Summary

Model evaluation compares predicted labels against actual labels using the **confusion matrix** — **TP, TN, FP, FN** — from which every metric is derived. On a 20-record test set with **TP = 8, FN = 2, FP = 4, TN = 6**: **accuracy 14/20 = 0.7000**, **precision 8/12 = 0.6667** (quality of positive calls), **recall 8/10 = 0.8000** (coverage of real positives), **specificity 6/10 = 0.6000** and **F1 0.7273** (harmonic mean, which collapses to 0 if either side is 0). Accuracy alone is dangerous — an "always negative" model can be 99 % accurate with zero recall— so precision and recall are reported as a pair, trading off against each other through the decision threshold. The **ROC curve** plots TPR against FPR across all thresholds; the 12-instance example traces points from (0,0) to (1,1) and encloses **AUC = 0.7778**, meaning a random positive outranks a random negative about 78 % of the time. Choose the metric from the cost of the error, not from convenience.

---

**Next:** [Topic 11 — Prediction: Linear Regression](11-linear-regression.md)
