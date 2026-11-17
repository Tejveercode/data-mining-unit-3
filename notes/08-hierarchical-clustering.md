# Topic 8 — Hierarchical Clustering: Concepts

> **LMS page:** *Hierarchical Clustering – Concepts* · **CO5**.
> The merge tables for all three linkage methods below are **computed and verified**.

---

## 1. What it is

**Hierarchical clustering builds a hierarchy of clusters rather than forming a single flat partition.** It is an **unsupervised** method used to discover **nested groupings** of data objects based on similarity.

**The result is usually represented as a tree-like structure called a dendrogram.**

**Crucially: hierarchical clustering does not require the number of clusters to be specified in advance**, making it useful for **exploratory data analysis**. You build the whole hierarchy once, then **cut it** at whatever level answers your question — and cutting at a different level gives a different number of clusters **without re-running anything**.

---

## 2. The basic idea

**Create a sequence of cluster merges or splits that reflect the similarity relationships among data objects.**

- At the **lowest level**, each data object is treated as an **individual cluster**.
- At **higher levels**, clusters are **gradually merged (or divided)** based on similarity.
- The process continues until all objects form a **single cluster** (agglomerative) or the **hierarchy is fully resolved** (divisive).

**This hierarchical structure provides insights into data organisation at different levels of granularity** — a gene may belong to a sub-family, a family and a super-family, and the dendrogram shows all three at once.

---

## 3. The two types

| | **Agglomerative** | **Divisive** |
|---|---|---|
| Direction | **bottom-up** | **top-down** |
| Start | every object is its own cluster | **all** objects in one cluster |
| Each step | **merge** the two most similar clusters | **split** the most heterogeneous cluster |
| Ends | one cluster containing everything | singletons |
| Cost | `O(n³)` naive, `O(n²)` with a priority queue | `O(2ⁿ)` to search all splits — heuristics needed |
| Usage | **the common form** | less common (DIANA, bisecting k-means) |

### Agglomerative (bottom-up)

**Initially each data object is considered a separate cluster. At each step, the two most similar clusters are merged.** The merging continues until all objects are in a single cluster or a stopping condition is met.

**This is the most commonly used form of hierarchical clustering.** The reason is practical: the search space at each step is `O(n²)` pairs, and early merges are cheap because the clusters are small.

### Divisive (top-down)

**Initially all data objects are placed in one cluster, which is then repeatedly divided into smaller clusters based on dissimilarity.**

**Divisive clustering is computationally more complex and less commonly used** — deciding *which* cluster to split and *how* is a combinatorial problem, so practical implementations use a proxy method (e.g. run k-means with k = 2 inside the chosen cluster) rather than an exhaustive search.

**The advantage divisive keeps:** it looks at the **global** structure first. Agglomerative methods commit to local merges early and cannot undo them — divisive makes the big decisions first.

---

## 4. Cluster similarity — linkage methods

**Cluster similarity refers to how the distance between two clusters is measured; the method used is called a linkage method.**

**The choice of linkage significantly affects the shape and structure of the resulting clusters** — same data, same algorithm, different dendrogram.

Let `A` and `B` be two clusters, `d(a, b)` the distance between objects.

### 4.1 Single linkage (MIN)

**The minimum distance between any pair of data points, one from each cluster.**

```text
d(A, B) = min { d(a, b) : a ∈ A, b ∈ B }
```

- **Can identify elongated or chain-like clusters** — two long clusters that approach at one point are joined.
- **Sensitive to noise and may produce the chaining effect**: a bridge of intermediate points links two genuinely separate clusters into one long chain.

### 4.2 Complete linkage (MAX)

**The maximum distance between any pair of points from different clusters.**

```text
d(A, B) = max { d(a, b) : a ∈ A, b ∈ B }
```

- **Tends to produce compact and well-separated clusters** — two clusters only merge when *every* pair is close.
- **May break large clusters into smaller ones** — a single far-away member blocks a merge that the rest of the cluster "wants".
- **Sensitive to outliers** for the same reason.

### 4.3 Average linkage

**The average distance between all pairs of data points across the two clusters.**

```text
d(A, B) = (1/(|A|·|B|)) · Σ(a∈A) Σ(b∈B) d(a, b)
```

- **Provides a balance between single and complete linkage** and is **less sensitive to noise**.
- The usual default recommendation: a compromise between chaining (single) and fragmentation (complete).

### 4.4 Centroid linkage

**The distance between the centroids of the two clusters.**

```text
d(A, B) = d(centroid(A), centroid(B))
```

- **Efficient** — one distance per pair of clusters instead of `|A|·|B|`.
- **May lead to inversions in the dendrogram**: because centroids move when clusters merge, a later merge can occur at a *lower* height than an earlier one, which produces crossing lines and a dendrogram that is not monotonically increasing. **This is the standard criticism of centroid linkage and the reason Ward's method is usually preferred.**

### 4.5 Ward's method (worth naming)

Merge the pair that increases the **within-cluster variance** least:
```text
Δ = (|A||B| / (|A|+|B|)) · ‖centroid(A) − centroid(B)‖²
```
Produces compact, similarly-sized clusters and is the default in most statistical packages.

---

## 5. The dendrogram

**A dendrogram is a tree-like diagram that visually represents the hierarchical relationships among clusters.** The **height at which clusters merge indicates the distance or dissimilarity between them.**

**Reading it:**
- each **leaf** is one object;
- each **horizontal line (join)** is a merge, drawn at the height of the linkage distance;
- **vertical lines** connect an object/cluster to the merge it participates in;
- **cutting** the tree with a horizontal line at height `h` yields the clusters that exist at that dissimilarity level.

**By cutting the dendrogram at a specific height, different numbers of clusters can be obtained.** Cut low → many small clusters; cut high → few large ones. **This is the mechanism that replaces "choose K in advance."**

**Practical way to choose the cut:** look for the **largest vertical gap** between consecutive merge heights — cutting through that gap gives the most stable clustering.

---

## 6. Worked example — all three linkages on the same 5 points

**Points:**

| Point | Coordinates |
|---|---|
| P1 | (1, 1) |
| P2 | (1.5, 1.5) |
| P3 | (5, 5) |
| P4 | (3, 4) |
| P5 | (4, 4) |

**All-pairs Euclidean distances:**

| | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| **P1** | 0.0000 | **0.7071** | 5.6569 | 3.6056 | 4.2426 |
| **P2** | 0.7071 | 0.0000 | 4.9497 | 2.9155 | 3.5355 |
| **P3** | 5.6569 | 4.9497 | 0.0000 | 2.2361 | **1.4142** |
| **P4** | 3.6056 | 2.9155 | 2.2361 | 0.0000 | **1.0000** |
| **P5** | 4.2426 | 3.5355 | 1.4142 | 1.0000 | 0.0000 |

### Single linkage

| Step | Merge | Height | Why |
|---|---|---|---|
| 1 | **P1 + P2** | **0.7071** | smallest pair distance in the matrix |
| 2 | **P4 + P5** | **1.0000** | next smallest |
| 3 | **P3 + {P4,P5}** | **1.4142** | min(P3–P4 2.2361, P3–P5 **1.4142**) |
| 4 | **{P1,P2} + {P3,P4,P5}** | **2.9155** | min over all cross pairs = P2–P4 = 2.9155 |

### Complete linkage

| Step | Merge | Height | Why |
|---|---|---|---|
| 1 | **P1 + P2** | **0.7071** | same |
| 2 | **P4 + P5** | **1.0000** | same |
| 3 | **P3 + {P4,P5}** | **2.2361** | max(P3–P4 **2.2361**, P3–P5 1.4142) |
| 4 | **{P1,P2} + {P3,P4,P5}** | **5.6569** | max over cross pairs = P1–P3 = 5.6569 |

### Average linkage

| Step | Merge | Height | Why |
|---|---|---|---|
| 1 | **P1 + P2** | **0.7071** | same |
| 2 | **P4 + P5** | **1.0000** | same |
| 3 | **P3 + {P4,P5}** | **1.8251** | (2.2361 + 1.4142)/2 |
| 4 | **{P1,P2} + {P3,P4,P5}** | **4.1510** | mean of all 6 cross distances |

**The fourth merge, step by step (why average = 4.1510):**
```text
P1–P3 5.6569   P1–P4 3.6056   P1–P5 4.2426
P2–P3 4.9497   P2–P4 2.9155   P2–P5 3.5355
sum = 24.9058  / 6 pairs = 4.1510
```

### What the three dendrograms show

```text
single            complete           average
 h=5.66 |                              |
 h=4.15 |                     |        |
 h=2.92 |   ┌────┐            |        |
 h=2.24 |   |    |            |   ┌────┤
 h=1.83 |   |    |            |   |    |
 h=1.41 |   |    ├────┐       |   ├────┤
 h=1.00 |   |    |  ┌─┤       |   |  ┌─┤
 h=0.71 |  ┌┤    |  | |       ┌┤   |  | |
        └──┴┴────┴──┴─┴───────┴┴───┴──┴─┴──
           P1 P2  P4 P5 P3   (same leaves)
```

**All three agree on the first two merges** — `{P1,P2}` and `{P4,P5}` are unambiguous. **They differ only in the final heights**: single says the two groups are 2.92 apart, complete says 5.66, average 4.15. *The clusters are the same; the confidence about their separation is not.* That is exactly what linkage choice controls, and the sentence to write in an exam.

**Cutting these dendrograms at height 2.0** gives **three clusters** in every case: `{P1,P2}`, `{P4,P5}`, `{P3}` for single and average; `{P1,P2}`, `{P4,P5}`, `{P3}` for complete too (its step-3 merge is at 2.2361, above the cut). **Cutting at 4.5** gives **two**: `{P1,P2}` and `{P3,P4,P5}` in all three.

---

## 7. Distance measures used in hierarchical clustering

**Hierarchical clustering can use various distance measures** — **Euclidean**, **Manhattan**, or **cosine similarity**:

```text
Euclidean   d = √Σ(pᵢ − qᵢ)²          geometric closeness
Manhattan   d = Σ|pᵢ − qᵢ|            robust to single large deviations
Cosine      d = 1 − (p·q)/(‖p‖‖q‖)    direction/pattern, ignores magnitude
Correlation d = 1 − Pearson r         shape of profiles (gene expression)
```

**The choice depends on the type of data and the application domain.** For gene-expression data, **correlation distance** is standard because the *pattern* matters more than the absolute level; for documents, **cosine** ignores length.

---

## 8. The algorithm and its cost

```text
Agglomerative (naive):
1. Compute the n×n distance matrix.
2. Let each object be a cluster.
3. REPEAT
     a. find the closest pair of clusters (using the linkage rule)
     b. merge them, record the height
     c. update the distance matrix (Lance–Williams formula)
   UNTIL one cluster remains
4. Draw the dendrogram.
```

**Lance–Williams update** (the reason it is efficient): the distance from a new merged cluster `A∪B` to any other cluster `C` is a weighted combination of `d(A,C)` and `d(B,C)` — computable without touching the original data.

**Complexity:** `O(n²)` space (the matrix) and `O(n³)` time naively, `O(n² log n)` with a priority queue. **This is why it does not scale** beyond tens of thousands of points.

---

## 9. Advantages (your page)

- **Does not require prior knowledge of the number of clusters** — the dendrogram shows every K at once.
- **Provides a clear visual representation of data structure** through dendrograms — arguably the best exploratory tool in clustering.
- **Can be applied to different types of data and distance measures.**
- The hierarchy is **informative at multiple levels of granularity** (a taxonomy, not just a partition).
- **Deterministic** — no random initialisation, so no run-to-run variation (unlike K-Means).
- Cutting at different heights gives different clusterings **without re-running**.

## 10. Limitations (your page)

- **Computationally expensive and does not scale well for very large datasets** — `O(n²)` memory is the hard wall.
- **Once a merge or split is made, it cannot be undone** — greedy and irreversible, so an early mistake propagates.
- **Sensitive to noise and outliers** — especially single and complete linkage.
- Linkage choice **changes the result**, and there is no universally correct choice.
- **No objective function** being optimised, so "best clustering" is not well defined.
- Cutting the dendrogram is **subjective** unless a clear gap exists.

---

## 11. Hierarchical vs partitional (K-Means)

| Aspect | **Hierarchical** | **K-Means (partitional)** |
|---|---|---|
| Output | **dendrogram** (all levels) | single flat partition |
| K needed in advance | **no** | **yes** |
| Determinism | **deterministic** | random init → varies |
| Scalability | poor, `O(n²)` memory | **good, linear in n** |
| Reversibility | **merges are final** | assignments can change each iteration |
| Cluster shape | depends on linkage (single finds chains) | **spherical only** |
| Typical n | thousands | millions |

---

## 12. Applications

**Biological taxonomy, gene-expression analysis, document clustering, image analysis, social-network analysis** — *particularly useful in domains where understanding hierarchical relationships is important*, i.e. wherever the levels themselves carry meaning (species → genus → family; document → topic → subject).

---

## 13. Summary

Hierarchical clustering builds a **nested hierarchy** instead of a flat partition — **agglomeratively** (bottom-up, merging the two most similar clusters repeatedly, the common form) or **divisively** (top-down, splitting repeatedly) — and displays it as a **dendrogram** whose join heights are the inter-cluster distances, so that **cutting the tree at any height yields a different number of clusters without re-running the algorithm**. The distance between clusters is defined by the **linkage**: **single** (minimum — finds elongated clusters, suffers chaining), **complete** (maximum — compact clusters, can fragment), **average** (mean of all pairs — the usual compromise), **centroid** (efficient but can invert the dendrogram) or **Ward** (minimum variance increase). On the five-point example all three linkages agree on the first merges `{P1,P2}` at 0.7071 and `{P4,P5}` at 1.0000, then diverge: the final merge sits at **2.9155 (single)**, **5.6569 (complete)** or **4.1510 (average)** — the same clusters, with very different claims about how separate they are. Its strengths are needing no K and giving a readable structure; its costs are `O(n²)` memory, irreversible merges and sensitivity to noise.

---

**Next:** [Topic 9 — Density-Based Clustering: DBSCAN](09-dbscan.md)
