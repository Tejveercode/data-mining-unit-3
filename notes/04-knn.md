# Topic 4 — K-Nearest Neighbor Classification (kNN)

> **LMS page:** *K-Nearest Neighbor Classification (kNN)* · **CO4**.
> The page's illustration is an image; the distance table and votes below are **computed and verified**, not sketched.

---

## 1. What it is

**kNN is a supervised learning technique used for classification and prediction.** It is:

- **instance-based** — it keeps the training examples themselves as the model;
- **non-parametric** — it assumes no functional form for the decision boundary;
- **lazy** — it does **no work during training**.

**Instead of building an explicit model, it stores all the training data and makes decisions at classification time.**

kNN is widely used because of its **simplicity and effectiveness** in many practical applications. The whole algorithm is one sentence: *"look at the k most similar known examples and take a vote."*

---

## 2. Basic idea

**Assign a class label based on the majority class among its K nearest neighbours in the training dataset**, where similarity is measured by a **distance metric**.

The value of **K is the number of neighbours consulted** — the single most consequential choice in the method.

---

## 3. Lazy learning

kNN is a **lazy learning algorithm**: it performs **no learning during the training phase**. All computation is deferred until a new object has to be classified.

| Phase | Eager learner (decision tree, Naïve Bayes) | **Lazy learner (kNN)** |
|---|---|---|
| Training | expensive — build the model | **free — just store the data** |
| Prediction | fast — traverse the model | **expensive — compare with every training record** |
| New data arrives | retrain | **nothing to retrain** |

**This characteristic allows kNN to adapt easily to new data but increases computation time during prediction.** It is also why kNN is described as **memory-based** reasoning: it "remembers" rather than "generalises".

---

## 4. The choice of K

**Critical, and heavily examined.**

| K | Effect |
|---|---|
| **too small** (K = 1) | **sensitive to noise** — one mislabelled neighbour decides everything; high **variance**, jagged boundary |
| **too large** | **smooths out important local patterns** — approaches the majority class; high **bias** |
| **balanced** | trade-off between bias and variance |

**Practical rules of thumb:**
- Use an **odd** K for two classes, to avoid ties.
- Start near **K ≈ √n** (n = training records) and tune by cross-validation.
- Cap K well below the size of the smallest class, or the vote is dominated by the majority class.
- **Never let K equal the number of training records** — the prediction becomes the global majority, independent of the query.

---

## 5. Distance measures

kNN relies on distance to identify neighbours. Your page lists three; **Euclidean** is the default.

**Euclidean** — straight-line distance in n dimensions:
```text
d(p, q) = √( Σ (pᵢ − qᵢ)² )
```

**Manhattan** ("city-block") — sum of absolute differences:
```text
d(p, q) = Σ |pᵢ − qᵢ|
```
*Less sensitive to a single large deviation, because differences are not squared.*

**Minkowski** — the general family containing both:
```text
d(p, q) = ( Σ |pᵢ − qᵢ|^h )^(1/h)
```
`h = 1` → Manhattan; `h = 2` → Euclidean; `h = ∞` → Chebyshev (maximum coordinate difference).

**Chebyshev** (worth naming):
```text
d(p, q) = maxᵢ |pᵢ − qᵢ|
```

**Other measures:** cosine similarity (text, direction not magnitude), Jaccard (sets), Hamming (binary/categorical), Mahalanobis (correlated features).

**The choice depends on the type of data and the problem domain** — and it changes the answer, as the worked example below shows.

---

## 6. Working principle

For a new object `q`:

1. Compute the **distance from q to every training object**.
2. **Sort** and take the **K smallest distances** — the nearest neighbours.
3. Examine their **class labels**.
4. Assign the **most frequent class** among them (**majority vote**).

```text
for each training record x:  compute d(q, x)
neighbours ← K records with smallest d(q, ·)
predict    ← mode( class labels of neighbours )
```

---

## 7. Worked example — every distance computed

**Training set** (two classes, `+` and `−`):

| Point | Coordinates | Class |
|---|---|---|
| P1 | (1, 2) | **+** |
| P2 | (2, 3) | **+** |
| P3 | (3, 3) | **+** |
| P4 | (6, 5) | **−** |
| P5 | (7, 7) | **−** |
| P6 | (8, 6) | **−** |
| P7 | (5, 4) | **−** |

**Classify the query `q = (3, 4)`.**

### Step 1 — Distances (sorted by Euclidean)

| Rank | Point | Class | Euclidean | Manhattan | Minkowski (h = 3) |
|---|---|---|---|---|---|
| 1 | P3 (3,3) | **+** | **1.0000** | 1.00 | 1.0000 |
| 2 | P2 (2,3) | **+** | **1.4142** | 2.00 | 1.2599 |
| 3 | P7 (5,4) | **−** | **2.0000** | 2.00 | 2.0000 |
| 4 | P1 (1,2) | **+** | 2.8284 | 4.00 | 2.5198 |
| 5 | P4 (6,5) | **−** | 3.1623 | 4.00 | 3.0366 |
| 6 | P5 (7,7) | **−** | 5.0000 | 7.00 | 4.4979 |
| 7 | P6 (8,6) | **−** | 5.3852 | 7.00 | 5.1045 |

*Sample calculation:*
```text
d(P3, q) = √((3−3)² + (3−4)²) = √(0 + 1) = 1.0000
d(P2, q) = √((2−3)² + (3−4)²) = √(1 + 1) = 1.4142
d(P7, q) = √((5−3)² + (4−4)²) = √(4 + 0) = 2.0000
```

*Note that Manhattan gives a **tie** between P2 and P7 (both 2.00) where Euclidean does not — a concrete demonstration that the distance measure changes neighbour selection.*

### Step 2 — Vote for three values of K

| K | Neighbours | Votes | Prediction |
|---|---|---|---|
| **K = 3** | P3(+), P2(+), P7(−) | +2, −1 | **+** |
| **K = 5** | + P1(+), P4(−) added | +3, −2 | **+** |
| **K = 7** | + P5(−), P6(−) added | +3, −4 | **−** |

**Every value of K is defensible and two of them disagree.** This is the honest lesson of kNN: the answer is a function of K, not a property of the data alone. In an exam, **state your K and show the neighbours**.

### Step 3 — Weighted voting (the improvement your page describes)

**In weighted kNN, nearer neighbours are given more importance**; each neighbour's contribution is weighted **inversely proportional to its distance**:

```text
weight(x) = 1 / d(q, x)
prediction = class with the largest Σ weight over its neighbours
```

| K | Σ weights for **+** | Σ weights for **−** | Weighted prediction |
|---|---|---|---|
| 3 | 1.0000 + 0.7071 = **1.7071** | 0.5000 | **+** |
| 5 | 1.7071 + 0.3536 = **2.0607** | 0.5000 + 0.3162 = 0.8162 | **+** |
| 7 | **2.0607** | 0.8162 + 0.2000 + 0.1857 = **1.2019** | **+** |

**The interesting result:** at K = 7 the plain majority vote says **−** (four to three), but weighting says **+** — because the three `+` neighbours are much closer (1.00, 1.41, 2.83) than the four `−` neighbours (2.00, 3.16, 5.00, 5.39). *This approach often improves classification accuracy, especially when neighbours are unevenly distributed* — exactly the situation here.

**This is a strong exam paragraph:** same data, same K, two answers, explained by how close the neighbours are.

---

## 8. Ties and edge cases

- **Tie in votes** (impossible with odd K and two classes, possible with more): break by **summing distances**, by **distance to the nearest neighbour**, or at random.
- **Duplicate points** at distance 0: `1/d` is undefined — use `1/(d+ε)`.
- **No training data in the region**: kNN still answers, because it always finds *some* k neighbours — even if they are far away. It cannot say "I don't know", which is a real limitation.

---

## 9. Handling continuous and categorical data

**kNN can handle numeric data directly** using distance measures.

**For categorical data**, attributes are **encoded numerically** (one-hot) or **similarity measures are adapted**:
```text
Overlap / Hamming:  d = (number of attributes where values differ) / (number of attributes)
```
Mixed data is usually handled with the **heterogeneous (Gower) distance**, which normalises each attribute type before combining.

**Proper data preprocessing is essential for effective kNN classification** — this is the one algorithm in Unit 3 that is *most* sensitive to it.

---

## 10. The effect of feature scaling (the classic trap)

**Since kNN is distance-based, attributes with larger numeric ranges dominate the distance calculation.**

**Demonstration of the problem:** consider two attributes, `age` (20–60) and `salary` (20,000–200,000). For two people differing by 5 years and 10,000 in salary:

```text
squared distance = 5² + 10,000² = 25 + 100,000,000
```

**The age difference contributes 0.000025 % of the distance.** Age is effectively ignored — not because it is uninformative, but because its units are small.

**Fix:** apply the pre-processing from Unit 2 — **min–max normalisation** `(v − min)/(max − min)` or **z-score standardisation** `(v − μ)/σ` — so every attribute contributes on a comparable scale. **Fit the scaler on the training set only**, or you leak test information.

---

## 11. Advantages (your page)

- **Simple to understand and implement** — no training, no assumptions about the data's distribution.
- **No training phase**; new data can be added instantly.
- **Can model complex, irregular decision boundaries** — unlike a linear classifier.
- **Works well when the data is well-distributed** (dense, with enough examples per region).
- Naturally **multi-class**; extends to regression by averaging.

## 12. Limitations (your page)

- **Computationally expensive during classification** — O(n·d) per query, and n queries cost O(n²·d).
- **Requires large memory** to store all training data.
- **Sensitive to noise and irrelevant features** (irrelevant dimensions dilute distance).
- Performance **depends heavily on the choice of K and distance measure**.
- **Curse of dimensionality**: in high dimensions all points become almost equidistant, so "nearest" loses meaning. Distance concentration makes kNN degrade badly beyond roughly 10–20 informative dimensions without reduction.
- **Imbalanced classes** bias the vote toward the majority.
- **No interpretability** — no model, no rules, no coefficients.

---

## 13. kNN for prediction (regression)

The same algorithm predicts numbers: **take the average (or weighted average) of the k neighbours' target values** instead of a majority vote.

```text
ŷ = (1/k) Σ yᵢ        or        ŷ = Σ wᵢyᵢ / Σ wᵢ ,  wᵢ = 1/d(q, xᵢ)
```

This is the bridge to Topic 1: with a **categorical** target it is classification, with a **numeric** target it is prediction — same neighbours, different aggregation.

---

## 14. kNN vs Naïve Bayes (your page's comparison)

| Aspect | **kNN** | **Naïve Bayes** |
|---|---|---|
| Model | **none** (stores data) | probabilistic model |
| Training | **instant** | one pass to compute counts |
| Prediction | **slow** — all distances | **fast** — a few multiplications |
| Assumption | **none** about distribution | **conditional independence** |
| Attribute interaction | **captured implicitly** by distance | cannot capture |
| Local patterns | **captures** (that is its strength) | global averages |
| Scaling needed | **yes, essential** | not required |
| High dimensions | **degrades badly** | copes well |
| Noise | sensitive | robust |

*The exam one-liner: Naïve Bayes builds a probabilistic model and predicts fast, while kNN stores the data and computes distances at prediction time; kNN captures local patterns, while Naïve Bayes assumes independence among attributes.*

---

## 15. Applications

**Pattern recognition, image classification, handwriting recognition, medical diagnosis, recommendation systems, text categorisation** — *particularly useful where decision boundaries are irregular*, and (in its instance-based form) in **anomaly detection** via the distance to the k-th neighbour.

---

## 16. Summary

kNN is a **lazy, instance-based, non-parametric** classifier: it stores the training data and, at prediction time, finds the **K nearest neighbours** by a distance measure (**Euclidean** by default, with **Manhattan** and **Minkowski** as alternatives) and predicts by **majority vote** — or by a **distance-weighted vote**, which gives nearer neighbours more say. On the worked set, `q = (3,4)` gives neighbours P3(1.00), P2(1.41), P7(2.00), so K = 3 and K = 5 predict **+** while K = 7 predicts **−**; weighting by `1/d` predicts **+** even at K = 7, because the positive neighbours are closer. Its costs are the flip side of its simplicity: **no training but slow prediction**, memory proportional to the data, and acute sensitivity to **feature scaling**, **irrelevant attributes** and **high dimensionality** — all of which are pre-processing problems, which is why Unit 2 comes before this topic.

---

**Next:** [Topic 5 — K-Means Clustering: Concept](05-kmeans-concept.md)
