# Data Mining (24CAT-307) — Unit 3

Study pack for **Unit 3** (classification and clustering), built the same way as [data-mining-unit-2](https://github.com/Tejveercode/data-mining-unit-2): every note follows its CU-LMS page in the same order, with the same examples, worked out in full and **verified by running the algorithm**.

**Status: 9 of the unit's LMS pages received** — notes 01–09 are complete. The exam pack, code toolkit and PDFs follow once the remaining pages arrive.

---

## Notes

| # | File | Contents |
|---|---|---|
| 01 | [notes/01-classification-vs-prediction.md](notes/01-classification-vs-prediction.md) | Supervised context, categorical vs numeric targets, confusion matrix vs MAE/RMSE, why "predict churn" is classification |
| 02 | [notes/02-decision-tree-induction.md](notes/02-decision-tree-induction.md) | Entropy, information gain, gain ratio, Gini — the full 14-record computation, `age` as root, level-2 splits, continuous thresholds, pruning |
| 03 | [notes/03-naive-bayes.md](notes/03-naive-bayes.md) | Bayes' theorem, priors and posteriors, the 14-record worked example, zero-probability problem + Laplace smoothing, Gaussian NB with numbers |
| 04 | [notes/04-knn.md](notes/04-knn.md) | Lazy learning, K selection, all three distance measures computed, distance-weighted voting that flips the K = 7 answer, scaling |
| 05 | [notes/05-kmeans-concept.md](notes/05-kmeans-concept.md) | Partitioning, centroid, SSE objective, why it converges, local optima, k-means++, elbow verified (100.75 → 14.33 → 3.67) |
| 06 | [notes/06-kmeans-distance-examples.md](notes/06-kmeans-distance-examples.md) | Euclidean/Manhattan/Minkowski/squared, normalisation, four full iterations to convergence, SSE 14.3333 |
| 07 | [notes/07-kmedoid-pam.md](notes/07-kmedoid-pam.md) | Medoids vs centroids, cost function, every swap of the 6-point example: 4.8284 → 4.4142 → 4.0000 → stop |
| 08 | [notes/08-hierarchical-clustering.md](notes/08-hierarchical-clustering.md) | Agglomerative vs divisive, four linkages, dendrograms, the same data under single (2.9155), complete (5.6569) and average (4.1510) |
| 09 | [notes/09-dbscan.md](notes/09-dbscan.md) | ε and MinPts, core/border/noise, density reachability and connectivity, all 10 points classified, parameter sensitivity |

---

## The unit in one paragraph

Unit 3 splits into two halves. **Classification and prediction** (notes 01–04) are supervised: decision trees split data on the attribute with the highest information gain, Naïve Bayes multiplies conditional probabilities under an independence assumption, and kNN defers everything to prediction time and takes a vote among the nearest examples. **Clustering** (notes 05–09) is unsupervised: K-Means alternates assignment and centroid updates to minimise within-cluster variance but needs K in advance, PAM swaps medoids to keep representatives real and robust, hierarchical clustering builds a dendrogram you can cut at any level, and DBSCAN grows clusters through dense regions so that shape is free and noise is an output rather than a distortion.

---

## Method used (identical to Unit 2)

1. **Extract** each LMS page to plain text, keeping its own headings, definitions and examples.
2. **Write one note per LMS topic**, in LMS order.
3. **Verify every number** by actually running the algorithm.
4. **Flag any error or omission** in the source page and show the correct working.
5. **Build the exam pack**: revision cheat sheet + question bank with model answers.
6. **Implement it in code**, so each algorithm can be run and inspected.
7. **Generate PDFs** for printing.

**Note on the source pages:** all nine are prose — the worked illustrations on the LMS pages are images that do not carry numbers. Every numeric example in these notes was therefore built to standard textbook datasets (the 14-record *buys_computer* table for the classifiers, the 8-point set for K-Means) and **computed by code, not sketched**.

---

## Coverage map

| Topic | LMS page | Note |
|---|---|---|
| Classification vs prediction | yes | 01 |
| Decision tree induction | yes | 02 |
| Bayesian classification — Naïve Bayes | yes | 03 |
| K-nearest neighbour classification | yes | 04 |
| K-Means clustering — concept | yes | 05 |
| K-Means — distance measures & examples | yes | 06 |
| K-Medoid clustering — PAM | yes | 07 |
| Hierarchical clustering — concepts | yes | 08 |
| Density-based — DBSCAN | yes | 09 |
| *remaining pages* | awaiting | — |

**On the course-outcome tags:** the LMS tags *Classification vs Prediction* and *Decision Tree Induction* as **CO5**, while their content is plainly **CO4** (apply prediction and classification algorithms). Treat the classification notes as CO4 and the clustering notes as CO5.

---

## References

1. Han, Pei & Tong — *Data Mining: Concepts and Techniques*, 4th ed., Morgan Kaufmann, 2022 (LMS cites the 3rd ed., 2011).
2. Tan, Steinbach, Karpatne & Kumar — *Introduction to Data Mining*, 2nd ed., Pearson, 2018.
3. Witten, Frank, Hall, Pal & Foulds — *Data Mining: Practical ML Tools and Techniques*, 5th ed., 2025.
4. Aggarwal — *Data Mining: The Textbook*, Springer, 2015.
5. Leskovec, Rajaraman & Ullman — *Mining of Massive Datasets*, 3rd ed., free at mmds.org.

---

## Companion

Unit 2 (pre-processing, association rules) is complete: [data-mining-unit-2](https://github.com/Tejveercode/data-mining-unit-2).
