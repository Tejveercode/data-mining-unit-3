# Data Mining (24CAT-307) — Unit 3: Classification & Clustering

A complete, self-contained study pack for **Unit 3** of the Data Mining course, built directly from the fifteen CU-LMS pages of the unit plus standard textbook worked examples.

Everything here is *worked out*, not asserted: every number in the notes was computed by script (`code/unit3_toolkit.py`) before it was written down.

---

## What's inside

| Folder | Contents |
|---|---|
| [`notes/`](notes/) | 15 chapter-style notes with full explanations, solved numericals and comparison tables |
| [`exam/`](exam/) | [`cheat-sheet.md`](exam/cheat-sheet.md) — one-sheet revision · [`question-bank.md`](exam/question-bank.md) — 108 questions with model answers |
| [`code/`](code/unit3_toolkit.py) | `unit3_toolkit.py` — dependency-free implementations of every algorithm in the unit, reproducing the notes' numbers |
| [`resources/`](resources/recommended-resources.md) | Books, videos and practice datasets worth your time |

---

## The 15 notes

| # | Note | CO | LMS page it covers |
|---|---|---|---|
| 01 | [Classification vs Prediction](notes/01-classification-vs-prediction.md) | CO4 | Classification vs Prediction |
| 02 | [Decision Tree Induction](notes/02-decision-tree-induction.md) | CO4 | Decision Tree Induction |
| 03 | [Bayesian Classification — Naïve Bayes](notes/03-naive-bayes.md) | CO4 | Bayesian Classification – Naïve Bayes |
| 04 | [K-Nearest Neighbour (kNN)](notes/04-knn.md) | CO4 | K-Nearest Neighbor Classification (kNN) |
| 05 | [K-Means Clustering — Concept](notes/05-kmeans-concept.md) | CO5 | K-Means Clustering – Concept |
| 06 | [K-Means — Distance Measures & Examples](notes/06-kmeans-distance-examples.md) | CO5 | K-Means – Distance Measures & Examples |
| 07 | [K-Medoid Clustering — PAM](notes/07-kmedoid-pam.md) | CO5 | K-Medoid Clustering – PAM Algorithm |
| 08 | [Hierarchical Clustering — Concepts](notes/08-hierarchical-clustering.md) | CO5 | Hierarchical Clustering – Concepts |
| 09 | [Density-Based — DBSCAN](notes/09-dbscan.md) | CO5 | Density-Based – DBSCAN |
| 10 | [Model Evaluation](notes/10-model-evaluation.md) | CO4 | Model Evaluation – Confusion Matrix, Accuracy, Precision, Recall, F1, ROC |
| 11 | [Prediction — Linear Regression](notes/11-linear-regression.md) | CO4 | Prediction: Linear Regression |
| 12 | [Overview of Clustering](notes/12-clustering-overview.md) | CO5 | Overview of Clustering & Need for Clustering |
| 13 | [Types of Data in Cluster Analysis](notes/13-types-of-data.md) | CO5 | Types of Data in Cluster Analysis |
| 14 | [Single & Complete Linkage](notes/14-single-complete-linkage.md) | CO5 | Single & Complete Linkage |
| 15 | [Real-Time Case Studies](notes/15-case-studies.md) | CO4/CO5 | Real-Time Case Studies for Classification & Clustering |

**Note numbering** follows the order in which the pages were supplied, not the LMS list order, so that existing cross-links between notes keep working. The table above is the coverage map: all 15 LMS pages of the unit are covered, nothing is missing.

**A note on CO mapping.** The LMS tags *Classification vs Prediction* and *Decision Tree Induction* as CO5, while the rest of the classification material is CO4. That looks like a tagging slip in the source system; the notes follow the standard grouping (classification → CO4, clustering → CO5) and say so where it matters.

---

## How the pack was built

1. Each LMS page was extracted to plain text and stripped of the portal's navigation, so the notes reflect the actual lecture scope.
2. **All 15 Unit 3 pages are prose only** — every worked illustration on them is an image with no readable numbers. So each algorithm in the notes is illustrated with a standard textbook dataset (the 14-record `buys_computer` set, the 8-point K-Means set, the 6-point PAM set, and so on), chosen so the arithmetic stays checkable by hand.
3. Every number was then recomputed in Python before being written down, and the implementations live in `code/unit3_toolkit.py`. If you edit a note, run the toolkit first — it is the source of truth for the figures.

Verified figures include: tree entropy 0.9403 with gains 0.2467 / 0.1518 / 0.0481 / 0.0292; gain ratio 0.1564; Gini 0.3429; the continuous threshold 26.0 (gain 0.4464); Naïve Bayes 0.028219 vs 0.006857 and Laplace 0.025109 vs 0.005381; K-Means converging in 4 iterations with SSE 14.3333 and an elbow at K = 3; PAM 4.8284 → 4.4142 → 4.0000; linkage finals 2.9155 / 5.6569 / 4.1510; DBSCAN with one border point and one noise point; accuracy 0.7000, precision 0.6667, recall 0.8000, F1 0.7273 and AUC 0.7778; regression ŷ = 2.2 + 0.6x with R² = 0.60 and multiple regression R² = 0.9799.

---

## Running the code

```bash
python3 code/unit3_toolkit.py            # every demo
python3 code/unit3_toolkit.py tree       # one topic
python3 code/unit3_toolkit.py bayes knn  # several
```

Available demos: `tree`, `bayes`, `knn`, `kmeans`, `pam`, `linkage`, `dbscan`, `metrics`, `regress`, `sims`. No dependencies beyond the standard library.

## Building the PDFs

```bash
python3 -m venv .venv && ./.venv/bin/pip install reportlab markdown pypdf
./.venv/bin/python build_pdf.py          # writes into pdf/
```

`build_pdf.py` renders the three PDFs — the 81-page notes, the revision sheet and the question bank — with a consistent A4 layout.

---

## Suggested study order

1. **Read 01 and 12 first.** They frame the whole unit: supervised vs unsupervised, and why anyone clusters.
2. **Classification block:** 02 → 03 → 04, then 10 (evaluation) and 11 (regression) — evaluation applies to everything, so read it once and reuse it.
3. **Clustering block:** 13 (data types) → 05 → 06 → 07 (partitional), 08 → 14 (hierarchical), 09 (density).
4. **Finish with 15** — the case studies are what exam questions dress the algorithms up as.
5. **Then the question bank**, one part per sitting, and the cheat sheet the night before.

---

## Reference texts

Han, Kamber & Pei, *Data Mining: Concepts and Techniques* (3rd ed.) — chapters 3, 8 and 10. Tan, Steinbach & Kumar, *Introduction to Data Mining* — chapters 4, 5 and 7. Witten, Frank & Hall, *Data Mining: Practical Machine Learning Tools and Techniques* — chapters 4 and 6. Free video walkthroughs and practice datasets are listed in [`resources/recommended-resources.md`](resources/recommended-resources.md).
