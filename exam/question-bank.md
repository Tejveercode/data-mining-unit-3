# Unit 3 — Question Bank (Classification & Clustering)

**How to use it:** cover the answer column, answer out loud, then check. Questions marked **(N)** are numericals — do these with pen and paper, they are where marks are won. Every numerical here has a verified answer in the notes.

Marking guide: **2 marks** = definition or one distinction; **5 marks** = explain + one example; **10 marks** = full treatment with comparison and a worked case.

---

## Part A — Classification vs Prediction (Topic 1)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| A1 | 2 | Define classification and prediction. | Classification assigns objects to **predefined categorical** classes; prediction estimates a **continuous numeric** value. Both supervised. |
| A2 | 2 | What is the key difference between them? | **The nature of the target attribute** — categorical vs numeric. |
| A3 | 5 | Distinguish classification and prediction with examples. | Table: target, output, evaluation, algorithms, plus one example each (spam vs house price). |
| A4 | 5 | Explain why both are called supervised learning. | Training data has **known outcomes**; model learns input→target mapping, then applies it to unseen data. |
| A5 | 2 | Name four classification algorithms and two regression techniques. | Tree, Naïve Bayes, kNN, SVM (or logistic regression); linear/multiple regression, regression trees. |
| A6 | 2 | Which metrics evaluate classification? Which evaluate prediction? | Accuracy, precision, recall, F1, confusion matrix, ROC / MAE, MSE, RMSE, R². |
| A7 | 5 | "Predict whether a customer will churn" — classification or prediction? Justify. | **Classification**: the target is binary (churn / no churn), not numeric; the word "predict" is the everyday verb. |
| A8 | 2 | What task has no target attribute at all? | **Clustering** (unsupervised). |

---

## Part B — Decision Tree Induction (Topic 2)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| B1 | 2 | Define decision tree induction. | Supervised technique building a **tree-structured model** of attribute tests, learned from labelled data. |
| B2 | 2 | Name the parts of a decision tree. | Root node, internal nodes (tests), branches (outcomes), leaf nodes (class/value). |
| B3 | 5 | Define entropy and information gain. | `E = −Σpᵢlog₂pᵢ`; gain = `E(S) − Σ(\|Sᵥ\|/\|S\|)E(Sᵥ)`; choose highest gain. |
| B4 | 5 | Why is gain ratio used instead of information gain? | Gain is **biased toward attributes with many distinct values**; gain ratio divides by SplitInfo to normalise. Used in C4.5. |
| B5 | 2 | Which algorithm uses the Gini index? | **CART**. `Gini = 1 − Σpᵢ²`; lower = purer. |
| B6 | 5 | State the stopping conditions for tree growth. | All same class; no attributes left; no records left; predefined criterion (min gain/size/depth). |
| B7 | 5 | What is overfitting in a decision tree, and how is it controlled? | Tree models **noise**, trains well/tests poorly; controlled by **pre-pruning** (early stop) or **post-pruning** (reduced-error, cost-complexity). |
| B8 | 5 | How are continuous attributes and missing values handled? | Threshold search at midpoints, best impurity reduction; missing: ignore record, replace with mode, or distribute probabilistically. |
| B9 | 2 | Compare ID3, C4.5 and CART in one line each. | ID3 = gain, C4.5 = gain ratio + pruning + continuous, CART = Gini + cost-complexity. |
| B10 **(N)** | 10 | 14 records, 9 yes/5 no. Compute entropy and the information gain of each attribute; choose the root. | `H(S)=0.9403`; gains: **age 0.2467**, student 0.1518, credit 0.0481, income 0.0292 → **age**. |
| B11 **(N)** | 5 | Within the `age = youth` subset, which attribute splits it perfectly? | **student** (gain 0.9710): student=yes → 2 yes/0 no; student=no → 0 yes/3 no. |
| B12 **(N)** | 5 | For age values 23,25,27,29,31,35,38,42,45,50 with classes N,N,Y,Y,Y,N,Y,Y,Y,Y, find the best threshold. | Midpoint search; best **26.0**, gain **0.4464** (left pure, right H=0.5436). |
| B13 | 5 | Give three advantages and three limitations of decision trees. | Easy to interpret, minimal prep, handles mixed data, converts to rules / unstable, overfits, biased to many-valued attributes, axis-parallel only. |

---

## Part C — Naïve Bayes (Topic 3)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| C1 | 2 | State Bayes' theorem. | `P(C\|X) = P(X\|C)P(C)/P(X)`. |
| C2 | 2 | Define prior and posterior probability. | Prior = class probability **before** attributes; posterior = **after** observing attributes. |
| C3 | 5 | What is the conditional independence assumption and why is it needed? | `P(X\|C) = ΠP(xᵢ\|C)`; avoids estimating every attribute combination → scalable. |
| C4 | 5 | Why does Naïve Bayes work despite an unrealistic assumption? | Classification needs only the **ranking** to be right, not calibrated probabilities. |
| C5 | 5 | What is the zero-probability problem and its fix? | Unseen value → `P=0` → whole product 0; fix with **Laplace smoothing** `(count+1)/(n_C+k)`. |
| C6 | 5 | How are continuous attributes handled? | **Gaussian NB**: per-class mean and σ, density `1/(σ√2π)·exp(−(x−μ)²/2σ²)`. |
| C7 | 2 | Why work in log space? | Products of small probabilities underflow; summing logs preserves the argmax. |
| C8 | 5 | Compare Naïve Bayes with decision trees. | Probabilistic vs rule-based; fast vs slower; cannot capture interactions vs captures them; robust in high dimensions. |
| C9 **(N)** | 10 | 14-record dataset. Classify `(youth, medium, yes, fair)`. | yes `0.6429×0.2222×0.4444×0.6667×0.6667 = 0.028219`; no `0.3571×0.6×0.4×0.2×0.4 = 0.006857` → **yes**. |
| C10 **(N)** | 5 | Classify `(middle, medium, no, fair)` and explain what happens. | `P(age=middle\|no)=0/5` → product 0. With Laplace: yes 0.0251 vs no 0.0054. |
| C11 **(N)** | 5 | Heights: yes {168,170,172,174,176}, no {160,164,166}. Classify 174 cm. | μ/sd = 172/2.8284 and 163.33/2.4944; `P=0.109848` vs `0.000017`; → **yes**. |

---

## Part D — kNN (Topic 4)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| D1 | 2 | Why is kNN called lazy and instance-based? | **No training** — it stores the data; all computation at prediction; the instances are the model. |
| D2 | 5 | How does the choice of K affect the classifier? | Small K → noise-sensitive, high variance; large K → over-smooths toward majority, high bias; use odd K ≈ √n. |
| D3 | 5 | Explain weighted kNN. | Weight `1/d`; nearer neighbours vote louder; helps with uneven distribution. |
| D4 | 2 | Why must features be scaled before kNN? | Distance is dominated by the largest-range attribute; scaling equalises contribution. |
| D5 | 5 | What is the curse of dimensionality for kNN? | In high dimensions distances concentrate — all points nearly equidistant, so "nearest" loses meaning. |
| D6 | 5 | Compare kNN with Naïve Bayes. | No model/fast training vs probabilistic model; slow prediction vs fast; captures local patterns vs interactions ignored. |
| D7 **(N)** | 10 | Points P1(1,2)+ P2(2,3)+ P3(3,3)+ P4(6,5)− P5(7,7)− P6(8,6)− P7(5,4)−; classify (3,4) for K=3 and K=5. | Distances 1.0000, 1.4142, 2.0000, 2.8284, 3.1623, 5.0000, 5.3852 → K=3 votes +2/−1 → **+**; K=5 → +3/−2 → **+**. |
| D8 **(N)** | 5 | Same data, K = 7, plain vs weighted voting. | Plain: 3 vs 4 → **−**; weighted `1/d`: +2.0607 vs −1.2019 → **+**. Different answers, explained by proximity. |
| D9 **(N)** | 5 | Compute Euclidean, Manhattan and Minkowski (h=3) distance from (2,10) to (5,8). | 3.6056 · 5 · 3.2711. |

---

## Part E — Model Evaluation (Topic 10)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| E1 | 2 | What is a confusion matrix? | Table of actual vs predicted: TP, TN, FP, FN. |
| E2 | 5 | Define accuracy, precision, recall, F1. | Formulas + one sentence of meaning each. |
| E3 | 5 | Why is accuracy misleading on imbalanced data? | Majority-class model scores high; e.g. 99 % accuracy with **zero recall** on fraud. |
| E4 | 5 | Explain the precision–recall trade-off. | Threshold controls it; lower → more recall, less precision and vice versa; choice by error cost. |
| E5 | 5 | What does the ROC curve plot, and what is AUC? | TPR vs FPR across thresholds; AUC = area, 1 perfect, 0.5 random; equals probability a positive outranks a negative. |
| E6 | 2 | When is F1 preferred to accuracy? | Imbalanced classes; punishes ignoring either precision or recall. |
| E7 | 2 | Define specificity and its relation to FPR. | `TN/(TN+FP)`; `FPR = 1 − specificity`. |
| E8 **(N)** | 10 | TP=8, FN=2, FP=4, TN=6. Compute accuracy, precision, recall, specificity, F1. | **0.7000, 0.6667, 0.8000, 0.6000, 0.7273**. |
| E9 **(N)** | 10 | Given 12 scored instances, draw the ROC and compute AUC. | Points from (0,0) to (1,1) via the table; **AUC = 0.7778**. |
| E10 | 5 | Why are multiple metrics needed? | Each hides something: accuracy hides imbalance, precision hides misses, recall hides false alarms, AUC hides the operating point. |

---

## Part F — Linear Regression (Topic 11)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| F1 | 2 | Define linear regression. | Fits a straight line relating independent variable(s) to a **continuous numeric** dependent variable. |
| F2 | 2 | Simple vs multiple regression? | One predictor vs two or more predictors. |
| F3 | 5 | Explain the least squares method and why squaring. | Minimise `Σ(y−ŷ)²`; differentiable, penalises large errors, no cancellation. |
| F4 | 5 | Interpret the intercept and the coefficients. | Intercept = prediction at x=0; coefficient = change in y per unit x **holding others constant**; sign = direction. |
| F5 | 5 | State the assumptions of linear regression. | **LINE**: linearity, independence, normal errors, equal variance; plus no multicollinearity, no influential outliers. |
| F6 | 5 | How is a regression model evaluated? | MAE, MSE, RMSE, R² (and adjusted R²); lower error = better. |
| F7 | 5 | Compare linear regression with classification. | Numeric vs categorical target; line vs boundary; MAE/RMSE/R² vs accuracy/F1/AUC. |
| F8 **(N)** | 10 | x = 1…5, y = 2,4,5,4,5. Find the regression line, predictions and R². | `b₁ = 6/10 = 0.6`, `b₀ = 2.2` → `ŷ = 2.2 + 0.6x`; predictions 2.8, 3.4, 4.0, 4.6, 5.2; SSE 2.40, **R² 0.60**. |
| F9 **(N)** | 5 | For the same model, compute MAE, MSE, RMSE and the prediction at x = 6. | 0.6400 · 0.4800 · 0.6928 · **5.8000**. |
| F10 | 2 | Why is extrapolation dangerous? | The linear relationship is assumed, not verified outside the observed range. |

---

## Part G — Clustering Overview (Topic 12)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| G1 | 2 | Define clustering. | Grouping objects so within-cluster similarity is high and between-cluster similarity is low; unsupervised. |
| G2 | 5 | Distinguish clustering from classification. | Unsupervised vs supervised, no labels vs labels, discover groups vs predict class, internal evaluation vs accuracy. |
| G3 | 5 | List the steps of the clustering process. | Collection → pre-processing → feature selection → similarity → algorithm → evaluation → interpretation. |
| G4 | 10 | Explain any five needs for clustering. | Exploration, summarisation, pattern discovery, segmentation, anomaly detection, text mining, image analysis, bioinformatics — with an example each. |
| G5 | 5 | What are cohesion and separation? | Within-cluster compactness (SSE) and between-cluster distance; `Total SS = within + between`. |
| G6 | 5 | Name the five clustering paradigms with one algorithm each. | Partitional (K-Means), hierarchical, density-based (DBSCAN), grid-based (STING), model-based (GMM). |
| G7 | 2 | Why is "no single clustering method works best" true? | Each encodes a cluster-shape assumption; the data decides which holds. |

---

## Part H — Types of Data (Topic 13)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| H1 | 5 | Distinguish nominal, ordinal, interval and ratio data with examples. | No order / order no spacing / differences not ratios / true zero. |
| H2 | 5 | Distinguish symmetric and asymmetric binary data, with the correct measure. | Symmetric: both values equal → simple matching; asymmetric: presence matters → **Jaccard**. |
| H3 | 2 | Which measure for nominal attributes? | **Simple matching**: `(p−m)/p`. |
| H4 | 5 | How is ordinal data made usable for clustering? | Rank then normalise: `(r−1)/(M−1)`, then numeric distance. |
| H5 | 5 | Why is cosine preferred for text? | Compares direction, not magnitude; document length does not dominate. |
| H6 | 5 | Explain the heterogeneous similarity formula. | Weighted average of per-attribute distances; δ excludes missing values and joint zeros on asymmetric binary. |
| H7 | 2 | What is a proximity matrix? | `n × n` symmetric distance matrix consumed by the clustering algorithm. |
| H8 **(N)** | 5 | Two objects, 4 nominal attributes, 2 matches. Give the similarity. | `2/4 = 0.5000`, distance 0.5000. |
| H9 **(N)** | 5 | Binary vectors x=(1,1,0,1,0,0,0), y=(1,1,1,0,0,0,1). Compute Jaccard and simple matching. | a=2,b=1,c=2,d=2 → Jaccard similarity **0.4000**; simple matching **0.5714**. |
| H10 **(N)** | 5 | Term vectors (3,2,0) and (2,2,1). Compute cosine similarity. | `10/(3.6056×3.0) = ` **0.9245**. |

---

## Part I — K-Means (Topics 5–6)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| I1 | 2 | Define K-Means and its objective. | Partition into K clusters minimising **within-cluster SSE**. |
| I2 | 5 | Write the K-Means algorithm. | Choose K → initialise centroids → assign → update to means → repeat until stable. |
| I3 | 5 | Why does K-Means always converge, and why only locally? | Both steps never increase SSE and partitions are finite; but SSE has local minima depending on initialisation. |
| I4 | 5 | How do you choose K? | Elbow (SSE vs K) and silhouette; state it is a heuristic and often a business decision. |
| I5 | 5 | State the assumptions and two consequences. | Spherical, similar size, comparable density → fails on crescents/rings and unequal clusters. |
| I6 | 5 | Compare Euclidean, Manhattan and Minkowski for K-Means. | Euclidean → mean, spherical; Manhattan → median (K-Medians), robust; Minkowski generalises with h. |
| I7 | 5 | Why is normalisation essential? | The largest-range attribute dominates distance; scaling equalises contribution. |
| I8 **(N)** | 10 | 8 points, K=3, initial centroids (2,10),(5,8),(1,2). Run K-Means to convergence. | Iterations as in the note → {A1,A4,A8}, {A3,A5,A6}, {A2,A7}; centroids (3.667,9), (7,4.333), (1.5,3.5); **SSE 14.3333**. |
| I9 **(N)** | 5 | Compute the elbow values and choose K. | 100.75, 51.47, **14.33**, 8.67, 3.67 → elbow at **K = 3**. |
| I10 **(N)** | 5 | On convergence, verify no point is closer to another centroid. | Check each point against all three final centroids; assignments unchanged. |

---

## Part J — K-Medoid / PAM (Topic 7)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| J1 | 2 | Define medoid. | The actual data object with minimum average dissimilarity to its cluster. |
| J2 | 5 | Why is K-Medoid more robust than K-Means? | Representative must be a real point → bounded outlier influence; works for categorical/mixed data. |
| J3 | 5 | Write the PAM algorithm. | BUILD (initial medoids) → assign → evaluate all swaps → accept improving swap → repeat until none. |
| J4 | 5 | Why is PAM expensive, and what fixes it? | `O(k(n−k)²)` per iteration; CLARA (sampling), CLARANS (randomised search). |
| J5 | 5 | Compare K-Means and K-Medoid. | Mean vs real object; squared vs plain distance; fast vs slow; numeric vs any dissimilarity. |
| J6 **(N)** | 10 | 6 points, K=2, initial medoids {B,E}. Run PAM to convergence. | Cost 4.8284 → swap B→A → 4.4142 → swap E→D → **4.0000** → no improving swap; clusters {A,B,C} (A), {D,E,F} (D). |
| J7 **(N)** | 5 | Compute the total cost for medoids {A,D}. | 2.000 + 2.000 = **4.0000**. |

---

## Part K — Hierarchical Clustering (Topics 8, 14)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| K1 | 2 | Define hierarchical clustering and dendrogram. | Nested hierarchy of clusters; tree diagram whose merge heights are distances. |
| K2 | 5 | Agglomerative vs divisive. | Bottom-up merges vs top-down splits; agglomerative common, divisive expensive. |
| K3 | 5 | Define the four linkages. | Single (min), complete (max), average (mean of all pairs), centroid (distance between centroids). |
| K4 | 5 | What is the chaining effect? | Single linkage merges via a chain of close points, joining distinct clusters at a low height. |
| K5 | 5 | Compare single and complete linkage. | Min vs max; elongated vs compact; chaining vs over-segmentation; dendrogram heights. |
| K6 | 5 | Advantages and limitations of hierarchical clustering. | No K needed, deterministic, visual → O(n²) memory, irreversible merges, noise-sensitive. |
| K7 | 2 | How do you obtain K clusters from a dendrogram? | **Cut** it at a chosen height; choose the largest vertical gap. |
| K8 **(N)** | 10 | 5 points: P1(1,1) P2(1.5,1.5) P3(5,5) P4(3,4) P5(4,4). Run single linkage. | Merges: P1+P2 @0.7071, P4+P5 @1.0000, P3 @1.4142, final @**2.9155**. |
| K9 **(N)** | 10 | Same data, complete linkage. | Same first two merges, P3 @**2.2361**, final @**5.6569**. |
| K10 **(N)** | 5 | Points 0,1,2,3,4.5,6,7,8 — when does single linkage merge everything? | By height **1.5** (chaining through 4.5); complete holds until **8.0**; average 4.875. |
| K11 | 2 | In Lance–Williams, what single parameter distinguishes single from complete? | The **sign of γ**: −½ (min) vs +½ (max). |

---

## Part L — DBSCAN (Topic 9)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| L1 | 2 | Expand DBSCAN. | Density-Based Spatial Clustering of Applications with Noise. |
| L2 | 5 | Define core, border and noise points. | ≥MinPts in ε / within ε of a core but not core / neither. |
| L3 | 5 | Define density-reachability and density-connectivity. | Chain of core points / both reachable from a common point (symmetric → cluster definition). |
| L4 | 5 | What happens when ε is too small or too large? | Too small → many points labelled noise, fragmentation; too large → clusters merge. |
| L5 | 5 | Advantages and limitations of DBSCAN. | Arbitrary shapes, no K, explicit noise → sensitive to ε/MinPts, fails on varying density, degrades in high dimensions. |
| L6 | 5 | Compare DBSCAN with K-Means. | Shape, K requirement, noise handling, determinism, complexity, density variation. |
| L7 **(N)** | 10 | 10 points, ε=1.5, MinPts=4. Classify every point and give the clusters. | A,B,C,D core; E border; F,G,H,I core; J noise → clusters {A,B,C,D,E} and {F,G,H,I}, **J noise**. |
| L8 | 2 | Which parameters must be tuned, and how? | ε and MinPts together; **k-distance plot**, choose ε at the knee. |

---

## Part M — Case Studies (Topic 15)

| # | Marks | Question | Model answer outline |
|---|---|---|---|
| M1 | 10 | Describe a real-time classification case study end to end. | Spam / medical / credit / churn: data, algorithm choice, metric choice, deployment, failure mode. |
| M2 | 10 | Describe a real-time clustering case study end to end. | Segmentation / image / documents / anomaly: features, algorithm, K choice, validation, action. |
| M3 | 5 | Why is precision critical in spam and recall critical in diagnosis? | FP deletes a real email; FN misses a disease. |
| M4 | 5 | Compare classification and clustering deployment. | Real-time decision engine vs periodic analysis; latency, explainability, failure visibility. |
| M5 | 5 | Explain "cluster to discover, label, then classify". | Clustering finds segments → humans name them → classifier assigns new records in real time. |
| M6 | 5 | Give three benefits and two risks of real-time data mining. | Automation, consistency, scale / data-quality debt, drift, feedback loops, accountability. |

---

## Part N — Cross-topic / 10-mark integrative

| # | Question | Model answer outline |
|---|---|---|
| N1 | A bank wants to detect fraudulent transactions. Which technique, which metric, why? | **Classification** if labels exist (precision/recall by cost, high recall then review); **clustering/DBSCAN** if fraud is novel (noise label). Discuss drift and class imbalance. |
| N2 | Compare all four clustering algorithms studied, on six criteria. | Table from the cheat sheet: K requirement, shape, noise, complexity, determinism, representative. |
| N3 | Compare decision tree, Naïve Bayes and kNN for a text-classification task. | NB best (high dimension, sparse, fast); tree poor on wide sparse features; kNN needs cosine + reduction, slow at prediction. |
| N4 | A dataset has numerical, ordinal and nominal attributes. How do you cluster it? | Normalise numerics, rank-normalise ordinals, encode nominals; use heterogeneous similarity or Gower; then PAM (any dissimilarity) rather than K-Means. |
| N5 | Explain why pre-processing decides the outcome of every algorithm in this unit. | Scaling for distances (kNN, K-Means, DBSCAN); missing values for NB/trees; discretisation for trees; encoding for distance measures. |
| N6 | You have 10 million records and must find groups. What do you choose and why? | K-Means (linear, memory-light) or MiniBatch K-Means; PAM and hierarchical are infeasible (`O(n²)`); DBSCAN only with spatial indexing. |
| N7 | Model A: accuracy 0.95, recall 0.10. Model B: accuracy 0.80, recall 0.85, precision 0.60. Which do you deploy for fraud? | **B** — accuracy is dominated by the majority class; B actually detects fraud. Justify with the confusion matrix and cost. |
| N8 | Design an evaluation plan for a churn model. | Held-out/cross-validation, confusion matrix, precision/recall/F1, ROC/AUC, calibration, subgroup fairness, business metric (retained revenue). |

---

**Total: 108 questions** (A8 · B13 · C11 · D9 · E10 · F10 · G7 · H10 · I10 · J7 · K11 · L8 · M6 · N8).

**Numericals with verified answers: B10, B11, B12, C9, C10, C11, D7, D8, D9, E8, E9, F8, F9, H8, H9, H10, I8, I9, I10, J6, J7, K8, K9, K10, L7 — 25 in total.**

---
**Full explanations:** [notes/](../notes/) · **Definitions and formulas:** [cheat-sheet.md](cheat-sheet.md)
