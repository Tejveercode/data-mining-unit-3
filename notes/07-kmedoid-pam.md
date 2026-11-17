# Topic 7 — K-Medoid Clustering: The PAM Algorithm

> **LMS page:** *K-Medoid Clustering – PAM Algorithm* · **CO5**.
> The cost table and every swap below are **computed and verified**.

---

## 1. What it is

**K-Medoid clustering is a partition-based clustering technique closely related to K-Means.** Instead of using the **mean** of the points to represent a cluster, it uses an **actual data object** as the representative — called a **medoid**.

**The use of medoids makes this approach more robust to noise and outliers compared to K-Means.**

**The most well-known algorithm for K-Medoid clustering is PAM — Partitioning Around Medoids.**

---

## 2. The concept of a medoid

**A medoid is a data point from the dataset that best represents a cluster.** Specifically, it is the object whose **average dissimilarity to all other objects in the same cluster is minimal**:

```text
medoid of cluster C = argmin over m ∈ C of  Σ(x ∈ C) d(x, m)
```

**Two decisive differences from a centroid:**

| | **Centroid (K-Means)** | **Medoid (K-Medoid)** |
|---|---|---|
| Is it a real data point? | **no** — a computed average | **yes** — an actual object |
| Meaning in the domain | "an average customer" (who may not exist) | "the most typical customer" (who definitely does) |
| Works with arbitrary distance? | no — needs a mean, so Euclidean-like | **yes** — any dissimilarity matrix |
| Outlier effect | dragged strongly | bounded — an extreme point is simply a bad medoid |

**Because medoids are always actual data objects, K-Medoid works effectively with various distance measures and is less sensitive to extreme values.** This is why it is preferred for **categorical and mixed-type data** (where a "mean" has no meaning) and for **interpretability** ("cluster represented by this particular patient").

---

## 3. The basic idea

**Partition the dataset into K clusters by selecting K representative objects as medoids.** Each remaining object is assigned to **the cluster whose medoid is closest** to it, by the chosen distance/dissimilarity measure.

**The quality of a clustering is measured by the total cost** — the **sum of distances between each data point and its corresponding medoid**:

```text
Cost = Σ(k=1..K) Σ(x ∈ C_k) d(x, medoid_k)
```

**Lower cost = more compact, better-formed clusters.** This is the exact analogue of K-Means' SSE, but with **distances instead of squared distances**, and with **a real point instead of a mean**.

---

## 4. What PAM is

**PAM is the classical algorithm for K-Medoid clustering.** It follows an **iterative refinement** approach similar to K-Means, but **replaces centroid updates with medoid swapping**.

**The algorithm aims to minimise the overall dissimilarity between data points and their assigned medoids.**

```text
PAM:
1. BUILD:   select K data objects as initial medoids (randomly, or greedily)
2. ASSIGN:  assign every object to the nearest medoid
3. SWAP:    for every (medoid, non-medoid) pair, compute the cost of the swap
            if the best swap reduces total cost → perform it, go to 2
4. STOP:    when no swap improves the cost → converged
```

---

## 5. Initialisation

**PAM begins by selecting K data objects randomly from the dataset as initial medoids.** These serve as temporary cluster representatives.

**The selection influences the final result, although PAM is generally more stable than K-Means**, because a medoid is constrained to be a real point — a random object is rarely as pathological as a random point in empty space.

**BUILD (the better initialisation):** pick the first medoid as the point minimising total distance to all others; then repeatedly add the point that most reduces the cost. Slower, but far less dependent on luck.

---

## 6. Assignment of data points

**Each data object is assigned to the cluster represented by the nearest medoid.** Distance/dissimilarity is computed between the object and **each** medoid, and the object joins the cluster whose medoid has the **minimum distance**.

*This step is identical in spirit to K-Means — the difference is what the cluster is represented by.*

---

## 7. The cost function

```text
Cost = Σ(x) d(x, medoid(x))          medoid(x) = nearest medoid to x
```

**The objective is to minimise this total cost.** Lower cost indicates more compact, better-formed clusters.

**Note the contrast with K-Means:** K-Means minimises **squared** Euclidean distance (which makes the mean optimal); PAM minimises **plain** distance (which makes an actual point optimal). Squaring is what makes an artificial mean the best representative — remove it, and the best representative becomes a real object.

---

## 8. The medoid swapping process (the heart of PAM)

After the initial assignment, **PAM tries to improve the clustering by swapping medoids with non-medoid objects**:

1. For each current medoid `m` and each non-medoid object `o`, consider the swap `m → o`.
2. **Recompute the total cost** after the swap.
3. **If the swap lowers the cost, accept it**; otherwise reject it.
4. **Repeat until no swap improves the cost.**

Swapping is what replaces the "recompute the mean" step: K-Means moves the representative to the average, PAM **searches for a better representative among the data**.

**Cost of the search:** with `n` objects and `k` medoids there are `k(n − k)` candidate swaps per iteration, and each evaluation touches all `n` objects → **`O(k(n − k)²)` per iteration**. That is why PAM does not scale to millions of points, and why **CLARA** (sampling) and **CLARANS** (randomised search) exist.

---

## 9. Full worked example — BUILD, assign, swap, converge

**Dataset (6 points in 2D):**

| Object | Coordinates |
|---|---|
| A | (1, 1) |
| B | (2, 1) |
| C | (1, 2) |
| D | (7, 7) |
| E | (8, 7) |
| F | (7, 8) |

**K = 2.** Distance: Euclidean.

**All-pairs distance matrix** (everything below is read from this):

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **A** | 0.000 | 1.000 | 1.000 | 8.485 | 9.220 | 9.220 |
| **B** | 1.000 | 0.000 | 1.414 | 7.810 | 8.485 | 8.602 |
| **C** | 1.000 | 1.414 | 0.000 | 7.810 | 8.602 | 8.485 |
| **D** | 8.485 | 7.810 | 7.810 | 0.000 | 1.000 | 1.000 |
| **E** | 9.220 | 8.485 | 8.602 | 1.000 | 0.000 | 1.414 |
| **F** | 9.220 | 8.602 | 8.485 | 1.000 | 1.414 | 0.000 |

### Step 1 — Initial medoids: {B, E}

Assignment: `A → B` (1.000), `B → B` (0), `C → B` (1.414), `D → E` (1.000), `E → E` (0), `F → E` (1.414).

```text
Cost({B,E}) = 1.000 + 0 + 1.414 + 1.000 + 0 + 1.414 = 4.8284
```

### Step 2 — Evaluate every swap

| Swap | New medoids | New cost | Verdict |
|---|---|---|---|
| **B → A** | {A, E} | **4.4142** | **improves** ✔ |
| B → C | {C, E} | 4.8284 | same |
| B → D | {D, E} | 25.1058 | worse |
| B → F | {F, E} | 27.1901 | worse |
| **E → D** | {B, D} | **4.4142** | **improves** ✔ |
| E → C | {B, C} | 25.7808 | worse |
| E → A | {B, A} | 25.8979 | worse |
| E → F | {B, F} | 4.8284 | same |

**Two swaps tie for best, both reaching 4.4142. Choose `B → A`.**

*Check the winning swap by hand:* medoids {A, E} → `A→A` 0, `B→A` 1.000, `C→A` 1.000 (sum **2.000**); `D→E` 1.000, `E→E` 0, `F→E` 1.414 (sum **2.4142**) → total **4.4142** ✔

### Step 3 — Next iteration: medoids {A, E}, cost 4.4142

Now test swaps again. The improving candidate is **E → D**:

```text
{A, D}:  A→A 0, B→A 1.000, C→A 1.000            = 2.000
         D→D 0, E→D 1.000, F→D 1.000            = 2.000
                                    total cost  = 4.0000   ← improves
```

**Accept: medoids {A, D}, cost 4.0000.**

### Step 4 — Iteration from {A, D}, cost 4.0000

Every possible swap was evaluated:

| Swap | New cost | Verdict |
|---|---|---|
| A → B | 4.4142 | worse |
| A → C | 4.4142 | worse |
| A → E | 25.1058 | worse |
| A → F | 25.1058 | worse |
| D → B | 25.8979 | worse |
| D → C | 25.8979 | worse |
| D → E | 4.4142 | worse |
| D → F | 4.4142 | worse |

**No swap improves the cost → PAM terminates.**

### Final clustering

| Cluster | Members | Medoid |
|---|---|---|
| **1** | A, B, C | **A (1, 1)** |
| **2** | D, E, F | **D (7, 7)** |

**Total cost = 4.0000** (2.000 per cluster).

*Compare with K-Means on the same data:* the centroids would be `(1.333, 1.333)` and `(7.333, 7.333)` — points that **do not exist in the dataset**. The medoids A and D are real, and the cost is measured in the same units as the distances (mean distance 4/6 = 0.667 per object).

**The trajectory, which is exactly what an exam wants:** `4.8284 → 4.4142 → 4.0000 → stop`.

---

## 10. Convergence

**PAM converges when no medoid swap can further reduce the total cost.** At that point the medoid set is considered **locally optimal** and assignments become stable.

**PAM is guaranteed to converge** — the cost strictly decreases at each accepted swap and there are finitely many medoid sets — **but it may require significant computation for large datasets**, and it finds a **local**, not global, optimum (hence BUILD and multiple restarts).

---

## 11. Distance measures used in K-Medoid

**K-Medoid can use various distance or dissimilarity measures** — Euclidean, Manhattan, or **any domain-specific dissimilarity**, including precomputed matrices:

```text
Euclidean    d = √Σ(pᵢ − qᵢ)²
Manhattan    d = Σ|pᵢ − qᵢ|
Hamming      d = number of differing attributes
Jaccard      d = 1 − |A∩B|/|A∪B|          (sets, market baskets)
Edit / DTW   d = sequence dissimilarity    (strings, time series)
```

**This flexibility allows K-Medoid to handle numeric, categorical and mixed-type data more effectively than K-Means.** Note the deeper point: PAM never computes a mean, so it only ever needs **pairwise dissimilarities** — which means it works on data where a mean is undefined.

---

## 12. Advantages (your page)

- **Robust to noise and outliers**, because medoids are actual data points — an outlier cannot become a medoid without increasing the cost, and it cannot drag the representative.
- **Supports a wide range of distance measures** and can be applied to **different data types** (numeric, categorical, mixed, precomputed).
- **Clusters are often more interpretable** — each is represented by a real, exemplary object.
- No assumption that clusters are spherical in the metric sense — shape follows the distance function.
- Works with **any dissimilarity matrix**, including those derived from domain knowledge.

## 13. Limitations (your page)

- **Computationally expensive**, especially for large datasets, because it evaluates **all possible medoid swaps** — `O(k(n−k)²)` per iteration.
- **Does not scale well to very large data volumes** compared to K-Means; needs CLARA/CLARANS sampling variants.
- **Requires K to be specified in advance.**
- Converges to a **local optimum**, sensitive to the initial medoids.
- Fewer off-the-shelf implementations than K-Means.

---

## 14. K-Medoid vs K-Means (your page's comparison, extended)

| Aspect | **K-Means** | **K-Medoid / PAM** |
|---|---|---|
| Representative | **centroid** (mean, may be artificial) | **medoid** (a real object) |
| Objective | sum of **squared** distances | sum of **plain** distances |
| Outliers | **sensitive** — the mean is dragged | **robust** — bounded influence |
| Distance measures | essentially Euclidean (needs a mean) | **any dissimilarity** |
| Data types | numeric | **numeric, categorical, mixed** |
| Speed | **fast**, `O(n·K·d·i)` | **slow**, `O(k(n−k)²)` per iteration |
| Interpretability | "average customer" | "this customer represents the group" |
| Local optima | yes | yes (but more stable) |
| Typical use | large numeric data, image compression | noisy data, categorical/mixed data, small n |

*The exam one-liner: K-Means uses centroids that may not correspond to actual data points, while K-Medoid uses real objects; K-Medoid is more robust but slower, whereas K-Means is faster but sensitive to outliers.*

---

## 15. Applications

**Market segmentation, bioinformatics, document clustering, anomaly detection, and any scenario where robustness to noise is critical** — *particularly useful when datasets contain outliers or when non-Euclidean distance measures are required* (e.g. clustering gene-expression profiles by correlation distance, or customers by a mix of numeric and categorical attributes).

---

## 16. Summary

K-Medoid clustering represents each cluster by a **medoid** — the actual data object with the **minimum average dissimilarity** to its cluster — and PAM finds the K medoids by **iterative refinement with swaps**: initialise K medoids (BUILD), assign every object to the nearest medoid, then evaluate every medoid↔non-medoid swap and accept one that lowers the **total cost** `Σ d(x, medoid(x))`, repeating until no swap helps. The worked example starts at medoids {B, E} with cost **4.8284**, swaps B→A to reach **4.4142**, then E→D to reach **4.0000**, at which point all eight further swaps are worse and the algorithm stops with clusters **{A, B, C}** (medoid A) and **{D, E, F}** (medoid D). The trade-off is explicit: **robustness and flexibility of distance in exchange for `O(k(n−k)²)` cost**, which is why PAM suits noisy, categorical or small datasets and K-Means suits large numeric ones.

---

**Next:** [Topic 8 — Hierarchical Clustering: Concepts](08-hierarchical-clustering.md)
