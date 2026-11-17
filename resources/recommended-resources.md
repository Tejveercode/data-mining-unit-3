# Recommended resources — Unit 3

A short, opinionated list. Everything here is either free or in the library, and each item is tied to the note it helps with.

## Books (the three that matter)

| Book | Chapters | Use it for |
|---|---|---|
| Han, Kamber & Pei — *Data Mining: Concepts and Techniques*, 3rd ed. | 8 (classification), 10 (cluster analysis), 3.5 (evaluation) | The course's obvious reference. Section 10.2 on partitioning methods is the closest match to notes 05–07. |
| Tan, Steinbach & Kumar — *Introduction to Data Mining*, 2nd ed. | 4 (classification), 5 (cluster analysis), 7 (association) | The clearest explanations of entropy/gain ratio and of single vs complete linkage; also the best treatment of proximity measures for note 13. |
| Witten, Frank & Hall — *Data Mining: Practical Machine Learning Tools and Techniques*, 4th ed. | 4, 6 | Practical advice: pruning, missing values, evaluating with cross-validation. |

Two others worth knowing about: *Pattern Recognition and Machine Learning* (Bishop) ch. 9 for the EM/Gaussian-mixture view of clustering, and *The Elements of Statistical Learning* (Hastie et al.) ch. 3 for regression done properly.

## Video

- **StatQuest (Josh Starmer)** — short, visual, and accurate: "Decision Trees", "Naive Bayes", "K-nearest neighbors", "K-means clustering", "Hierarchical clustering", "ROC and AUC". Best for a first pass before reading a note.
- **Andrew Ng, Machine Learning (Coursera)** — the K-Means and anomaly-detection lectures are the classic treatment.
- **MIT 6.036 / Caltech CS156** — free full courses if you want a semester-level view.

## Reading algorithms interactively

- **`scikit-learn` user guide**, sections *Supervised learning* and *Clustering*. The text is good; the parameter tables are the part to read — `min_samples`, `eps`, `linkage`, `metric`.
- **`scipy.cluster.hierarchy`** documentation for dendrogram plotting, and **`yellowbrick`** for elbow and silhouette plots in one line.
- **`playground.tensorflow.org`** — good intuition for why some data shapes defeat linear boundaries.
- **`mlu-explain.github.io`** — visual explanations of ROC/AUC, precision/recall and the confusion matrix; ideal alongside note 10.
- **`distill.pub/2016/misread-tsne`** — read before you trust any 2-D cluster picture.

## Datasets to practise on

| Dataset | Where | Try |
|---|---|---|
| Iris | `sklearn.datasets.load_iris` | K-Means with K = 2, 3, 4; see why K = 3 is not automatic |
| Wine, Breast Cancer | same module | Classification + confusion matrix; compare tree vs NB vs kNN |
| Wholesale customers | UCI | Segmentation with K-Means and PAM; compare the cluster profiles |
| Mall customers | Kaggle | The canonical elbow-method example |
| Old Faithful geyser | `sklearn` / R | The 2-D case where DBSCAN and K-Means disagree |
| Credit card fraud | Kaggle | Imbalanced data — accuracy lies, precision/recall tell the truth |
| Twenty Newsgroups | `sklearn.datasets` | Text clustering; cosine similarity and high dimensions |
| MNIST | `sklearn` / `keras` | kNN's slow prediction in the flesh |

## Papers worth a look (short and readable)

- Ester, Kriegel, Sander & Xu (1996), *A Density-Based Algorithm for Discovering Clusters* — the original DBSCAN paper; the definitions in note 09 come straight from it.
- Kaufman & Rousseeuw (1990), *Finding Groups in Data* — the source of PAM and of the silhouette coefficient.
- Quinlan (1986), *Induction of Decision Trees* — ID3, in the author's own words.
- Sneath & Sokal (1973) — where single/complete linkage and the Lance–Williams formula come from.
- Fawcett (2006), *An Introduction to ROC Analysis* — the clearest 12 pages ever written on note 10.

## Exam technique for this unit

- Numericals are worth the most marks and are the most predictable: entropy/gain, a Naïve Bayes classification, a K-Means iteration table, a PAM cost table, a linkage merge sequence, a confusion matrix, and a regression line. Practise each **by hand, on paper, with a calculator that has log₂** — the exam will not give you clean numbers.
- Always show the intermediate table. Marks are given for the iteration rows, not just the final answer.
- For theory questions, name the algorithm, state the assumption, give one example, and name the limitation. Three sentences gets a 5-mark answer most of the way.
- When asked to "compare", draw the table — even a rough one — before writing prose.
