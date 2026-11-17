# Topic 5 — K-Means Clustering: Concept

> **LMS page:** *K-Means Clustering – Concept* · **CO5 (categorize the different clustering approaches)**.

---

## 1. What it is

**K-Means is one of the most widely used partition-based clustering techniques** in data mining and machine learning. It is an **unsupervised** learning algorithm that groups data objects into a **predefined number of clusters** based on similarity.

**Objective:** partition the dataset into K clusters such that objects **within a cluster are highly similar** to each other and **dissimilar to objects in other clusters**.

**Mechanically:** the algorithm works by **minimising the intra-cluster variance** and **maximising inter-cluster separation**.

*Unsupervised is the key word:* there is no target attribute, no labels, no ground truth. K-Means finds structure, and a human decides whether the structure means anything.

---

## 2. The basic idea

**Each cluster is represented by the mean value of its data points, called the centroid.** Each object is assigned to the cluster **whose centroid is closest** to it, usually by **Euclidean distance**.

The two steps — **assign points, update centroids** — repeat **iteratively until the assignments become stable**.

```text
      ┌──────────────────────────────────────┐
      │  1. assign each point to nearest     │
      │     centroid                          │
      │  2. recompute each centroid as the    │──── repeat until stable
      │     mean of its assigned points       │
      └──────────────────────────────────────┘
```

This is **Lloyd's algorithm**, and the two-step loop is the whole method.

---

## 3. The meaning of K

**K is the number of clusters to be formed, and it must be specified by the user before running the algorithm.**

**Choosing an appropriate K is very important because it directly affects the quality of clustering:**

| K | Consequence |
|---|---|
| **too small** | different groups are **merged together** — real structure is hidden |
| **too large** | clusters become **fragmented** — one natural group split into pieces |
| **right** | clusters match the structure the data actually has |

**Note the asymmetry with the rest of Unit 3:** decision trees, Naïve Bayes and kNN are told the answer set (the classes) by the labels; DBSCAN and hierarchical clustering discover the number of clusters themselves. **K-Means is the one that demands the answer in advance** — its single biggest practical weakness.

---

## 4. Working principle (the full algorithm)

```text
1. Choose K (the number of clusters).
2. Initialise K centroids — usually at random points (or random data objects).
3. REPEAT
     a. Assignment step:
          for each data point x:
              assign x to the cluster whose centroid is nearest to x
     b. Update step:
          for each cluster k:
              new centroid = mean of all points currently assigned to k
   UNTIL no point changes cluster (or centroids stop moving)
4. Output the clusters and their centroids.
```

**Steps 3a and 3b are exactly "assign then recompute".** Each pass is cheap: computing distances is `O(n·K·d)` for n points, K clusters and d dimensions, and the mean is `O(n)`.

---

## 5. The centroid

**A centroid is the arithmetic mean of all data points in a cluster**, representing the cluster's **central location in feature space**:

```text
centroid_k = (1/|C_k|) · Σ x        (component-wise mean of the points in cluster k)
```

**Centroids are updated after every iteration** to better represent the current cluster composition. The accuracy of the clustering depends heavily on **how well the centroids capture the structure of the data**.

**Two properties worth stating:**
1. A centroid is **not necessarily a data point** — it can sit in empty space between points (this is precisely what K-Medoids fixes, Topic 7).
2. With Euclidean distance, the mean is the point that **minimises the sum of squared distances** to the cluster members — which is why K-Means uses squared Euclidean error and why it is sensitive to outliers (a mean is dragged by extremes).

---

## 6. Distance measure

**K-Means primarily uses Euclidean distance** to measure similarity between points and centroids — the **straight-line distance in multidimensional space**:

```text
d(x, c) = √( Σ (xᵢ − cᵢ)² )
```

**Because of its reliance on distance, K-Means works best with numeric and continuous data**, and performs poorly with categorical data **unless it is properly transformed** (one-hot encoding, or a distance designed for categories).

Topic 6 covers the distance measures in full, with a complete worked iteration.

---

## 7. The objective function

The goal is to **minimise the sum of squared distances between data points and their assigned centroids**:

```text
SSE = J = Σ(k=1..K) Σ(x ∈ C_k) ‖x − centroid_k‖²
```

This is the **within-cluster sum of squares (WCSS)** — also called **inertia**. **Lower values indicate compact, well-formed clusters.**

`SSE` is the quantity the algorithm provably decreases at every step:

- the **assignment step** cannot increase SSE (each point moves to its nearest centroid, so its own contribution falls),
- the **update step** cannot increase SSE (the mean is the minimiser of squared distance for a fixed assignment).

**Consequence:** SSE decreases monotonically, and because there are finitely many partitions, **the algorithm must terminate**.

---

## 8. Convergence

**K-Means converges when cluster assignments no longer change, or when centroid positions stabilise.**

**The algorithm is guaranteed to converge — but it may converge to a local optimum rather than the global optimum.** Different initial centroid selections can lead to **different clustering results**.

**This is the most examinable weakness of K-Means.** Two fixes:

| Fix | How it works |
|---|---|
| **Multiple restarts** | run K-Means many times with different random initialisations, keep the solution with the lowest SSE |
| **k-means++ initialisation** | choose the first centroid at random, then each next centroid with probability proportional to `D(x)²` (squared distance to the nearest chosen centroid) — spreads the seeds out, and is provably close to optimal in expectation |

---

## 9. Choosing K in practice

**The elbow method:** plot SSE against K; SSE always falls as K rises (at K = n it is exactly 0), but the **rate of improvement** collapses at the true number of clusters — the plot bends like an elbow.

*Verified on the 8 two-dimensional points used in Topic 6 (best of 60 random starts each):*

| K | SSE | Drop from previous |
|---|---|---|
| 1 | 100.7500 | — |
| 2 | 51.4667 | −49.28 |
| **3** | **14.3333** | **−37.13 ← elbow** |
| 4 | 8.6667 | −5.67 |
| 5 | 3.6667 | −5.00 |

**The bend is between K = 2 and K = 3, and after K = 3 the gains collapse — so K = 3 is the elbow.** That is exactly how the method is used: not a proof, a signal.

**Silhouette analysis** is the stronger alternative: for each point compare its mean distance to its own cluster (`a`) with its mean distance to the nearest other cluster (`b`):
```text
s = (b − a) / max(a, b)        range −1 … +1
```
Average `s` over all points for each K, and pick the K with the highest average silhouette.

---

## 10. Assumptions made by K-Means

**K-Means assumes:**

1. **Clusters are spherical** (isotropic) in shape — because it assigns by distance to a centre, it can only carve convex, roundish regions.
2. **Clusters are roughly equal in size** — a small cluster next to a large one tends to be absorbed.
3. **Points closer to each other are more similar** than points farther apart.
4. **The number of clusters K is known.**
5. Clusters have **comparable density** and are separable by straight boundaries (Voronoi cells).

**These assumptions make K-Means unsuitable for datasets with irregularly shaped clusters or varying cluster densities** — a crescent-shaped cluster will be cut in half, and a ring-shaped one cannot be found at all. **DBSCAN (Topic 9) exists precisely for those cases.**

---

## 11. Advantages (your page)

- **Simple to understand and easy to implement** — two steps, no probability, no tree.
- **Computationally efficient** — `O(n·K·d·i)` for i iterations; linear in n.
- **Works well for large datasets.**
- **Converges quickly** — typically in a handful of iterations.
- **Widely supported** by tools such as WEKA, scikit-learn, R.
- Every cluster is **summarised by one centroid**, which is easy to report and to act on.
- Naturally extends to **vector quantisation / compression** (each point replaced by its centroid).

## 12. Limitations (your page)

- **Requires K to be specified in advance.**
- **Sensitive to initial centroid selection** — different runs, different answers.
- **Sensitive to outliers**, which significantly affect centroid positions.
- **Does not perform well with non-numeric data** or **clusters of arbitrary shapes**.
- Assumes **spherical, similar-sized** clusters.
- **Scale-sensitive** — attributes must be normalised first (Topic 6).
- Hard assignment only — no notion of "this point belongs 60 % here".
- **Empty clusters** can occur when a centroid loses all its points; standard fixes are to re-seed it to the farthest point, or drop K.

---

## 13. Applications

**Customer segmentation, image compression (colour quantisation), document clustering, market analysis, pattern recognition, recommendation systems, bioinformatics** (grouping similar samples or gene-expression profiles).

---

## 14. The one-paragraph answer

K-Means is a **partition-based, unsupervised** algorithm that splits data into **K clusters** by alternating two steps — **assign each point to the nearest centroid** (Euclidean distance), then **recompute each centroid as the mean of its cluster** — until membership stops changing. It minimises the **within-cluster sum of squares**, which decreases monotonically at both steps and therefore guarantees convergence, though only to a **local optimum** that depends on initialisation (fixed in practice by restarts or k-means++). Its speed and simplicity make it the default clustering method for large numeric data, while its assumptions — **K known in advance, spherical clusters, similar sizes, sensitivity to outliers and scale** — define exactly when to reach for K-Medoids, hierarchical clustering or DBSCAN instead.

---

**Next:** [Topic 6 — K-Means: Distance Measures & Examples](06-kmeans-distance-examples.md)
