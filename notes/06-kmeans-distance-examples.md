# Topic 6 — K-Means: Distance Measures & Examples

> **LMS pages:** *K-Means – Distance Measures & Examples* · **CO5**.
> The iteration below is fully computed and **verified by running the algorithm**; the LMS illustration is an image, so the numeric example is supplied here.

---

## 1. Why distance decides everything

**In K-Means, distance measures determine how points are assigned to clusters.** The algorithm groups objects by computing the distance between each point and each centroid, and assigns the point to the **cluster whose centroid is closest according to the chosen measure**.

**The effectiveness of K-Means depends heavily on the choice of distance measure**, especially in multidimensional data.

**Distance defines similarity** — and in K-Means, **similarity is inversely related to distance**: smaller distance = higher similarity, larger distance = lower similarity.

**Since K-Means relies on numerical calculations, distance measures are primarily applicable to numeric and continuous data.**

---

## 2. Euclidean distance

**The most commonly used measure**: the straight-line distance between two points in multidimensional space.

```text
d(p, q) = √( Σᵢ (pᵢ − qᵢ)² )
```

**Properties:**
- sensitive to **scale**, so attributes should be normalised;
- squaring **magnifies large differences**, so a single big deviation dominates;
- its level sets are **circles/spheres**, which is exactly why K-Means produces spherical clusters;
- minimising squared Euclidean distance is what makes the **mean** the correct centroid.

**Worked:** `p = (2, 10)`, `q = (5, 8)`
```text
d = √((2−5)² + (10−8)²) = √(9 + 4) = √13 = 3.6056
```

---

## 3. Manhattan distance

Also called **city-block distance**: the sum of the **absolute differences** of the coordinates.

```text
d(p, q) = Σᵢ |pᵢ − qᵢ|
```

**Unlike Euclidean, it does not square the differences**, making it **less sensitive to large deviations in individual attributes** — an outlier contributes linearly, not quadratically.

**Useful when data dimensions are independent and when movement is restricted to grid-like paths** (hence "city-block": you cannot walk diagonally through buildings).

**Worked:** `p = (2, 10)`, `q = (5, 8)`
```text
d = |2−5| + |10−8| = 3 + 2 = 5
```

**Important consequence for K-Means:** if you use Manhattan distance, the **mean is no longer the optimal centroid** — the **median** is (it minimises the sum of absolute deviations). This is **K-Medians**, a variant worth naming.

---

## 4. Minkowski distance

A **generalised measure that includes Euclidean and Manhattan as special cases**:

```text
d(p, q) = ( Σᵢ |pᵢ − qᵢ|^h )^(1/h)
```

| `h` | Measure |
|---|---|
| 1 | **Manhattan** |
| 2 | **Euclidean** |
| 3, 4, … | intermediate (increasingly favours the largest coordinate difference) |
| ∞ | **Chebyshev**: `maxᵢ |pᵢ − qᵢ|` |

**Worked:** `p = (2, 10)`, `q = (5, 8)`, `h = 3`
```text
d = (|−3|³ + |2|³)^(1/3) = (27 + 8)^(1/3) = 35^(1/3) = 3.2711
```

**Although flexible, Minkowski distance is less commonly used directly in K-Means due to increased computational complexity** — the fractional power costs more than a square root, and the benefit over h = 1 or 2 is rarely worth it.

---

## 5. Squared Euclidean distance

**Squared Euclidean distance is often used internally by K-Means**, because the algorithm minimises the **sum of squared distances** between points and centroids:

```text
d²(p, q) = Σᵢ (pᵢ − qᵢ)²
```

**Two reasons it is used:**
1. **It avoids the computational cost of calculating square roots** — and comparison of distances is unaffected, since √ is monotonic.
2. **It emphasises larger deviations more strongly** than Euclidean distance, which is exactly the behaviour the SSE objective encodes.

**Worked:** `p = (2,10)`, `q = (5,8)` → `d² = 9 + 4 = 13` (compare `d = 3.6056`).

*Note the equivalence:* minimising `d²` and minimising `d` give the **same assignments**; they differ only as an **objective**, where the square changes how much a distant point matters.

---

## 6. The need for data normalisation

**Distance-based clustering methods are sensitive to the scale of attributes.** If attributes are measured in different units — age in years, income in rupees — **the attribute with the larger numeric range dominates the distance calculation**.

**Example of the failure:** two customers differing by **5 years** of age and **10,000** in income:
```text
d² = 5² + 10,000² = 25 + 100,000,000
```
**Age contributes 0.000025 % of the distance** — the clustering is effectively performed on income alone, and the age structure is invisible.

**Normalisation or standardisation ensures all attributes contribute equally, improving clustering quality.** Apply the Unit 2 transforms first:

| Method | Formula | Effect |
|---|---|---|
| **Min–max normalisation** | `(v − min)/(max − min)` | all values into [0, 1] |
| **Z-score standardisation** | `(v − μ)/σ` | mean 0, sd 1 — preferred when outliers exist |

**Fit the scaler on the training data only**; normalising with statistics from the whole dataset leaks information.

---

## 7. The full worked example — K-Means by hand

**Dataset** (8 points in two dimensions — the classic textbook set):

| Point | x | y |
|---|---|---|
| A1 | 2 | 10 |
| A2 | 2 | 5 |
| A3 | 8 | 4 |
| A4 | 5 | 8 |
| A5 | 7 | 5 |
| A6 | 6 | 4 |
| A7 | 1 | 2 |
| A8 | 4 | 9 |

**K = 3**, initial centroids chosen from the data: **C1 = (2, 10)**, **C2 = (5, 8)**, **C3 = (1, 2)**.

### Iteration 1 — assign, then update

Distances from each point to the three centroids:

| Point | to C1 (2,10) | to C2 (5,8) | to C3 (1,2) | Assigned |
|---|---|---|---|---|
| A1 (2,10) | **0.000** | 3.606 | 8.062 | **C1** |
| A2 (2,5) | 5.000 | 4.243 | **3.162** | **C3** |
| A3 (8,4) | 8.485 | **5.000** | 7.280 | **C2** |
| A4 (5,8) | 3.606 | **0.000** | 7.211 | **C2** |
| A5 (7,5) | 7.071 | **3.606** | 6.708 | **C2** |
| A6 (6,4) | 7.211 | **4.123** | 5.385 | **C2** |
| A7 (1,2) | 8.062 | 7.211 | **0.000** | **C3** |
| A8 (4,9) | 2.236 | **1.414** | 7.616 | **C2** |

**Clusters after iteration 1:** `C1 = {A1}`, `C2 = {A3, A4, A5, A6, A8}`, `C3 = {A2, A7}`

**Update the centroids (component-wise means):**
```text
C1 = (2, 10)                                            ← single point
C2 = ((8+5+7+6+4)/5 , (4+8+5+4+9)/5) = (30/5, 30/5) = (6.0, 6.0)
C3 = ((2+1)/2 , (5+2)/2) = (1.5, 3.5)
```

### Iteration 2 — with centroids (2,10), (6,6), (1.5,3.5)

| Point | to C1 | to C2 | to C3 | Assigned |
|---|---|---|---|---|
| A1 (2,10) | **0.000** | 5.657 | 6.519 | C1 |
| A2 (2,5) | 5.000 | 4.123 | **1.581** | C3 |
| A3 (8,4) | 8.485 | **2.828** | 6.519 | C2 |
| A4 (5,8) | 3.606 | **2.236** | 5.701 | C2 |
| A5 (7,5) | 7.071 | **1.414** | 5.701 | C2 |
| A6 (6,4) | 7.211 | **2.000** | 4.528 | C2 |
| A7 (1,2) | 8.062 | 6.403 | **1.581** | C3 |
| A8 (4,9) | **2.236** | 3.606 | 6.042 | **C1** ← moved |

**Clusters:** `C1 = {A1, A8}`, `C2 = {A3, A4, A5, A6}`, `C3 = {A2, A7}`

**Update:**
```text
C1 = ((2+4)/2 , (10+9)/2) = (3.0, 9.5)
C2 = ((8+5+7+6)/4 , (4+8+5+4)/4) = (26/4, 21/4) = (6.5, 5.25)
C3 = (1.5, 3.5)                                   ← unchanged
```

### Iteration 3 — with centroids (3, 9.5), (6.5, 5.25), (1.5, 3.5)

| Point | to C1 | to C2 | to C3 | Assigned |
|---|---|---|---|---|
| A1 (2,10) | **1.118** | 6.543 | 6.519 | C1 |
| A2 (2,5) | 4.610 | 4.507 | **1.581** | C3 |
| A3 (8,4) | 7.433 | **1.953** | 6.519 | C2 |
| A4 (5,8) | **2.500** | 3.132 | 5.701 | **C1** ← moved |
| A5 (7,5) | 6.021 | **0.559** | 5.701 | C2 |
| A6 (6,4) | 6.265 | **1.346** | 4.528 | C2 |
| A7 (1,2) | 7.762 | 6.388 | **1.581** | C3 |
| A8 (4,9) | **1.118** | 4.507 | 6.042 | C1 |

**Clusters:** `C1 = {A1, A4, A8}`, `C2 = {A3, A5, A6}`, `C3 = {A2, A7}`

**Update:**
```text
C1 = ((2+5+4)/3 , (10+8+9)/3) = (11/3, 27/3) = (3.667, 9.000)
C2 = ((8+7+6)/3 , (4+5+4)/3) = (21/3, 13/3) = (7.000, 4.333)
C3 = (1.5, 3.5)
```

### Iteration 4 — check for stability

| Point | to C1 (3.667,9) | to C2 (7,4.333) | to C3 (1.5,3.5) | Assigned |
|---|---|---|---|---|
| A1 (2,10) | **1.944** | 7.557 | 6.519 | C1 |
| A2 (2,5) | 4.333 | 5.044 | **1.581** | C3 |
| A3 (8,4) | 6.616 | **1.054** | 6.519 | C2 |
| A4 (5,8) | **1.667** | 4.177 | 5.701 | C1 |
| A5 (7,5) | 5.207 | **0.667** | 5.701 | C2 |
| A6 (6,4) | 5.518 | **1.054** | 4.528 | C2 |
| A7 (1,2) | 7.491 | 6.438 | **1.581** | C3 |
| A8 (4,9) | **0.333** | 5.548 | 6.042 | C1 |

**The assignment is identical to iteration 3 → the algorithm has converged.** (Note it converged even though the centroids moved slightly in iteration 3 — the *assignments* are what must stabilise.)

### Final result

| Cluster | Members | Centroid | SSE contribution |
|---|---|---|---|
| **C1** | A1, A4, A8 | (3.667, 9.000) | 6.6667 |
| **C2** | A3, A5, A6 | (7.000, 4.333) | 2.6667 |
| **C3** | A2, A7 | (1.500, 3.500) | 5.0000 |
| | | **Total SSE** | **14.3333** |

*Reading the clusters:* C1 is the "high" group (top of the plane), C2 the "right/low" group, C3 the "small values" pair — which matches what the eye sees. **That agreement is the point of the example.**

---

## 8. The example "concept" walkthrough (your page's sequence)

Your page describes the customer-segmentation framing — *annual income* and *spending score*, `K = 2`. The stages it lists, with what actually happens at each:

| Stage | What happens | In the worked example above |
|---|---|---|
| **Initial centroid selection** | two (or K) centroids selected randomly from the data | C1, C2, C3 chosen as A1, A4, A7 |
| **Distance calculation and assignment** | each point goes to the nearest centroid | iteration 1 table |
| **Centroid update** | new centroids = mean of assigned points | (6,6) and (1.5,3.5) |
| **Iteration and convergence** | repeat until assignments stop changing | stopped at iteration 4 |

**The choice of initial centroids can influence the final result** — which is why the *same* data can give different clusters on different runs (Topic 5, §8).

---

## 9. Effect of the distance measure on the result

**Different distance measures can produce different clustering results.**

| Measure | Cluster shape it favours | Centroid that is correct |
|---|---|---|
| **Euclidean / squared Euclidean** | **spherical**, isotropic | **mean** |
| **Manhattan** | elongated / grid-aligned | **median** (K-Medians) |
| **Cosine** | direction-based (text, high-dim sparse) | normalised mean |
| **Mahalanobis** | correlated attributes, elliptical | generalised mean |

**Euclidean distance favours spherical clusters, while Manhattan distance can handle elongated cluster shapes better.** **Choosing an inappropriate distance measure may lead to poor cluster formation even if the algorithm is correctly implemented** — the algorithm will still converge, just to the wrong partition, which is the harder failure to notice.

**Concrete demonstration from the kNN data set (Topic 4):** for `q = (3,4)`, Manhattan gives a **tie** between P2 and P7 (both 2.00) where Euclidean ranks P2 strictly closer (1.41 vs 2.00). A distance measure that produces ties produces ties in cluster assignment too.

---

## 10. Checking your answer (do this in an exam)

1. **Every point is assigned** — count the members, `Σ|C_k| = n`.
2. **Centroids are the arithmetic means of their members** — recompute one by hand.
3. **No point is closer to another centroid** — re-check with the final centroids (this is exactly iteration 4 above).
4. **SSE matches the sum of per-cluster SSEs.**
5. **K is stated, initialisation is stated, and the stopping criterion is stated.**

A hand-worked K-Means answer without step 3 is only half-checked — a point that should have moved is the most common mistake in student solutions.

---

## 11. Summary

Distance is the decision rule in K-Means: **Euclidean** is the default (spherical clusters, mean as centroid, squared form used internally because it avoids square roots and matches the SSE objective), **Manhattan** handles grid-like and outlier-heavy data (and implies the **median**, i.e. K-Medians), and **Minkowski** generalises both with a parameter `h`. **Normalisation is mandatory**, because otherwise the attribute with the largest numeric range supplies almost the whole distance. The worked example — 8 points, K = 3, starting centroids (2,10), (5,8), (1,2) — converges in **four iterations** to clusters **{A1,A4,A8}**, **{A3,A5,A6}**, **{A2,A7}** with centroids **(3.667, 9.0)**, **(7.0, 4.333)**, **(1.5, 3.5)** and **SSE 14.3333**, and the assignment is stable against every centroid at the end. On the same data the elbow curve falls **100.75 → 51.47 → 14.33 → 8.67 → 3.67** for K = 1…5, bending exactly at K = 3.

---

**Next:** [Topic 7 — K-Medoid Clustering: The PAM Algorithm](07-kmedoid-pam.md)
