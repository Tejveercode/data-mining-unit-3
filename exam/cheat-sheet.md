# Unit 3 — Classification & Clustering · REVISION SHEET

## 1. Core definitions (learn word-for-word)

- **Classification:** assigning objects to one of **predefined categorical** classes; supervised; output is a **label**.
- **Prediction:** estimating a **continuous numeric** value; supervised; output is a **number**.
- **Supervised learning:** model built from **historical data with known outcomes**; both of the above.
- **Decision tree:** tree of attribute tests; internal nodes = tests, branches = outcomes, leaves = classes.
- **Entropy:** impurity/uncertainty; **0 = pure**, maximum at even class distribution.
- **Information gain:** reduction in entropy after splitting on an attribute; **choose the highest**.
- **Gain ratio:** `Gain / SplitInfo`; removes bias toward attributes with many values (**C4.5**).
- **Gini index:** `1 − Σpᵢ²`; probability of misclassifying a random object (**CART**).
- **Overfitting:** tree models noise, fits training data, fails on unseen data.
- **Pruning:** removing branches that do not improve accuracy — **pre** (early stop) / **post** (after growth).
- **Naïve Bayes:** probabilistic classifier using **Bayes' theorem** + **conditional independence** of attributes.
- **Prior:** `P(C)` before seeing attributes. **Posterior:** `P(C|X)` after. **Likelihood:** `P(X|C)`. **Evidence:** `P(X)`.
- **Laplace smoothing:** add 1 to every count so no probability becomes 0 (**zero-probability problem**).
- **kNN:** lazy, instance-based, non-parametric; class = **majority vote of K nearest** neighbours.
- **Lazy learning:** no training; all computation at prediction time.
- **Clustering:** grouping objects so that **within-cluster similarity is high, between-cluster low**; unsupervised.
- **Centroid:** arithmetic **mean** of a cluster (K-Means). **Medoid:** an **actual data object** representing a cluster (K-Medoid/PAM).
- **SSE / WCSS:** `Σ Σ ‖x − centroid‖²` — K-Means' objective (cohesion).
- **Dendrogram:** tree diagram of hierarchical merges; **height = merge distance**; cut it to choose K.
- **Linkage:** rule for cluster-to-cluster distance — single (min), complete (max), average (mean), centroid, Ward.
- **DBSCAN:** density-based; **core** (≥ MinPts in ε), **border** (near a core, not core), **noise** (neither).
- **Density reachable:** chain of core points. **Density connected:** both reachable from a common point.
- **Confusion matrix:** TP/TN/FP/FN table. **Precision** = TP/(TP+FP). **Recall** = TP/(TP+FN). **F1** = harmonic mean.
- **ROC:** TPR vs FPR across thresholds. **AUC:** area under it; 1 perfect, 0.5 random.
- **Linear regression:** fits `ŷ = b₀ + b₁x` by **least squares** (minimise SSE).

## 2. All the formulas

| Quantity | Formula |
|---|---|
| **Entropy** | `−Σ pᵢ log₂ pᵢ` |
| **Information gain** | `E(S) − Σ (|Sᵥ|/|S|)·E(Sᵥ)` |
| **Split info** | `−Σ (|Sᵥ|/|S|) log₂(|Sᵥ|/|S|)`; **GainRatio = Gain/SplitInfo** |
| **Gini** | `Gini(S) = 1 − Σ pᵢ²`; `Gini_split = Σ (|Sᵥ|/|S|)·Gini(Sᵥ)` |
| **Bayes** | `P(C\|X) = P(X\|C)P(C)/P(X)`; Naïve: `P(X\|C) = Π P(xᵢ\|C)` |
| **Laplace** | `(count + 1) / (n_C + #values)` |
| **Gaussian NB** | `P(x\|C) = 1/(σ√2π)·exp(−(x−μ)²/2σ²)` |
| **Euclidean** | `√Σ(pᵢ − qᵢ)²` |
| **Manhattan** | `Σ\|pᵢ − qᵢ\|` |
| **Minkowski** | `(Σ\|pᵢ − qᵢ\|^h)^(1/h)`; h=1 Manhattan, h=2 Euclidean, h=∞ Chebyshev |
| **Cosine** | `(p·q)/(‖p‖‖q‖)`; distance = `1 − cos` |
| **Jaccard** | `a/(a+b+c)` (asymmetric binary) |
| **Simple matching** | `(a+d)/p` or `(p−m)/p` |
| **Ordinal → [0,1]** | `(r − 1)/(M − 1)` |
| **Heterogeneous similarity** | `Σ δ·d_f / Σ δ` (δ = 0 if missing, or both 0 on asymmetric binary) |
| **K-Means SSE** | `Σ_k Σ_{x∈C_k} ‖x − c_k‖²` |
| **PAM cost** | `Σ_x d(x, medoid(x))` |
| **Accuracy** | `(TP+TN)/N` |
| **Precision** | `TP/(TP+FP)` |
| **Recall / TPR** | `TP/(TP+FN)` |
| **Specificity** | `TN/(TN+FP)`; **FPR** = `FP/(FP+TN)` = 1 − spec |
| **F1** | `2PR/(P+R)`; `F_β = (1+β²)PR/(β²P+R)` |
| **Balanced accuracy** | `(recall + specificity)/2` |
| **Simple LR** | `b₁ = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²`, `b₀ = ȳ − b₁x̄` |
| **Multiple LR** | `b = (XᵀX)⁻¹Xᵀy` |
| **MAE / MSE / RMSE** | `Σ\|y−ŷ\|/n` · `Σ(y−ŷ)²/n` · `√MSE` |
| **R²** | `1 − SSE/SST`; **Adjusted R²** = `1 − (1−R²)(n−1)/(n−p−1)` |
| **Silhouette** | `s = (b − a)/max(a,b)` |

## 3. The numbers from the worked examples (memorise these)

| Problem | Key result |
|---|---|
| 14-record tree | `H(S) = 0.9403`; gains **age 0.2467**, student 0.1518, credit 0.0481, income 0.0292 → **age = root** |
| Level-2 splits | youth → **student** (gain 0.9710); senior → **credit_rating** (0.9710); middle pure |
| Continuous threshold | best `age ≤ 26`, gain **0.4464** |
| Gain ratio / Gini | `SplitInfo(age) = 1.5774`, `GainRatio = 0.1564`; `Gini(age) = 0.3429` |
| Naïve Bayes | `X=(youth, medium, yes, fair)` → **yes 0.0282** vs no 0.0069 |
| Laplace | zero-prob case → yes 0.0251 vs no 0.0054 |
| Gaussian NB | 174 cm → yes `0.109848 × 0.625`, no `0.000017 × 0.375` |
| kNN | distances P3 1.0000, P2 1.4142, P7 2.0000; K=3/5 → **+**, K=7 → **−**; weighted K=7 → **+** |
| K-Means | 4 iterations → {A1,A4,A8} (3.667, 9.0), {A3,A5,A6} (7.0, 4.333), {A2,A7} (1.5, 3.5); **SSE 14.3333** |
| Elbow | K=1…5 → **100.75, 51.47, 14.33, 8.67, 3.67** |
| PAM | 4.8284 → 4.4142 → **4.0000** → stop; clusters {A,B,C} medoid A, {D,E,F} medoid D |
| Linkage (5 pts) | final merge: **single 2.9155**, complete 5.6569, average 4.1510 |
| Chaining demo | single merges all by **1.5**; complete at **8.0**; average 4.875 |
| DBSCAN | ε=1.5, MinPts=4 → {A,B,C,D,E}, {F,G,H,I}, **J noise** |
| Metrics | TP8 FN2 FP4 TN6 → acc **0.7000**, prec **0.6667**, rec **0.8000**, F1 **0.7273**, spec 0.6000 |
| ROC | 12 instances → **AUC 0.7778** |
| Simple LR | `ŷ = 2.2 + 0.6x`; SSE 2.40; **R² 0.60**; MAE 0.64; RMSE 0.6928; x=6 → 5.8 |
| Multiple LR | `ŷ = 1.3333 + 1.6111x₁ + 1.2778x₂`; **R² 0.9799**; (7,3) → 16.4444 |
| Similarity | nominal 0.5000; Jaccard 0.4000; cosine **0.9245**; mixed 0.8333/0.3333/0.8333 |

## 4. Comparison tables (the marks live here)

**Classification vs prediction vs clustering**

| | Supervised? | Target | Output |
|---|---|---|---|
| Classification | yes | categorical | label |
| Prediction | yes | numeric | value |
| Clustering | **no** | none | groups |

**Entropy vs Gini vs Gain ratio**

| Measure | Algorithm | Bias | Range |
|---|---|---|---|
| Information gain | ID3 | favours many-valued attributes | 0…log₂k |
| Gain ratio | **C4.5** | corrects that bias | 0…1 |
| Gini | **CART** | moderate | 0…0.5 (2 classes) |

**Precision vs recall**

| Metric | Question | Costly error | Use |
|---|---|---|---|
| Precision | of those flagged, how many right? | FP | spam |
| Recall | of the real ones, how many caught? | FN | cancer |
| F1 | balance of both | — | imbalanced data |
| AUC | ranking quality over all thresholds | — | model comparison |

**Clustering algorithms**

| | K-Means | K-Medoid/PAM | Hierarchical | DBSCAN |
|---|---|---|---|---|
| K needed | **yes** | yes | **no** | **no** |
| Shape | spherical | any (metric) | linkage-dependent | **arbitrary** |
| Noise | no concept | robust | sensitive | **explicit label** |
| Complexity | O(nKdi) | O(k(n−k)²) | O(n²) space | O(n log n) indexed |
| Deterministic | no | no | **yes** | **yes** |
| Representative | mean (may not exist) | **real object** | dendrogram | dense region |

**Single vs complete linkage**

| | Single (MIN) | Complete (MAX) |
|---|---|---|
| Cluster distance | minimum pair | maximum pair |
| Finds | elongated/chained | compact/separated |
| Chaining | **severe** | reduced |
| Risk | merges distinct clusters | splits natural clusters |

**Distance measures**

| Measure | Sensitive to outliers | Correct centre |
|---|---|---|
| Euclidean / squared | high | mean |
| Manhattan | lower | **median** (K-Medians) |
| Cosine | direction only | normalised mean |

## 5. Mnemonics

- **LINE assumptions:** **L**inearity, **I**ndependence, **N**ormality of errors, **E**qual variance.
- **DBSCAN point types:** **C**ore has many, **B**order sits beside one, **N**oise has none.
- **Linkage sign trick:** **γ negative → MIN (single)**, **γ positive → MAX (complete)**.
- **Data types ladder:** **N**ominal → **B**inary → **O**rdinal → **I**nterval → **R**atio ("No Buckets, Only Increasing Ratios").
- **Metric choice:** **precision protects the innocent, recall protects the sick.**
- **Unit pipeline:** pre-process (Unit 2) → classify/cluster (Unit 3) → evaluate (note 10) → deploy (note 15).

## 6. Twelve sentences that earn marks

1. A category in the target means classification; a number means prediction; no target at all means clustering.
2. Entropy 0 means pure; a 50/50 split of two classes gives the maximum of 1 bit.
3. Gain ratio exists because information gain rewards attributes that merely have many distinct values.
4. A tree grown to purity memorises noise — pruning is what makes it generalise.
5. Naïve Bayes is "naïve" only about independence; the ranking survives even when the probabilities do not.
6. Laplace smoothing stops one unseen attribute value from vetoing an entire class.
7. kNN has no training cost and pays for it at prediction time — and the answer depends on K.
8. Features must be scaled before any distance-based method, or the largest unit decides the result.
9. K-Means converges to a local optimum because SSE only ever decreases; restarts and k-means++ mitigate it.
10. A medoid is a real object, which is why PAM tolerates outliers and works on categorical data.
11. Single linkage asks "is one pair close?" and chains; complete linkage asks "is every pair close?" and compacts.
12. Accuracy is a trap on imbalanced data — report the confusion matrix and choose the metric from the cost of the error.

## 7. Numbers and rules of thumb

| Item | Value |
|---|---|
| Maximum entropy, 2 classes | **1 bit** |
| z-score outlier threshold | **±3** |
| IQR multiplier | **1.5** |
| DBSCAN MinPts default | **≥ d + 1**, often 2d or 4 |
| kNN K rule of thumb | **√n**, odd |
| AUC benchmarks | 0.9 excellent · 0.8 good · 0.7 fair · **0.5 random** |
| Silhouette interpretation | > 0.5 good · ≈ 0 wrong cluster |
| Elbow cut on the worked set | **K = 3** |
| PAM cost for the worked example | **4.0000** |
| K-Means SSE for the worked example | **14.3333** |

---
**Full explanations:** [notes/](../notes/) · **Practice:** [question-bank.md](question-bank.md)
