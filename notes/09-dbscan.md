# Topic 9 — Density-Based Clustering: DBSCAN

> **LMS page:** *Density-Based – DBSCAN* · **CO5**.
> The neighbourhood counts and point types below are **computed and verified**.

---

## 1. What it is

**DBSCAN stands for Density-Based Spatial Clustering of Applications with Noise.**

It is a **density-based** clustering algorithm that groups objects **based on the density of data points in a region**. Unlike partition-based and hierarchical methods:

- it **discovers clusters of arbitrary shapes**,
- it **explicitly identifies noise and outliers**.

**DBSCAN does not require the number of clusters to be specified in advance**, making it **highly suitable for exploratory data analysis**.

**This is the algorithm that fixes K-Means' two deepest assumptions** — spherical clusters and no concept of noise.

---

## 2. The basic idea

**Clusters are regions of high point density separated by regions of low density.** A cluster forms when **a sufficient number of points exist within a specified neighbourhood**.

**Points that lie in low-density regions and do not belong to any cluster are treated as noise.**

```text
high density  →  cluster
low density   →  boundary between clusters, or noise
```

**The definition of "dense" is entirely parameter-driven** — two numbers decide everything:

| Parameter | Meaning |
|---|---|
| **ε (epsilon)** | the **neighbourhood radius** around a point |
| **MinPts** | the **minimum number of points** required inside that radius for the region to count as dense |

---

## 3. Core concepts (all five from your page)

### 3.1 Epsilon neighbourhood

**ε is the radius of the neighbourhood around a data point.** It defines **how close points must be to count as neighbours**:

```text
N_ε(p) = { q ∈ D : d(p, q) ≤ ε }
```

**The choice of ε directly influences the result:**
- **too small** → most points have fewer than MinPts neighbours → **many points labelled noise**, clusters fragment;
- **too large** → neighbourhoods merge → **distinct clusters fuse into one**.

### 3.2 Minimum points

**MinPts specifies the minimum number of points required within an ε-neighbourhood for a region to be considered dense.** It **distinguishes dense regions that form clusters from sparse regions that represent noise.**

**Rule of thumb:** `MinPts ≥ d + 1` for d dimensions (often `2·d`), because at least d+1 points are needed to define a d-dimensional neighbourhood. Common default: `MinPts = 4` or `2·dim`.

### 3.3 Core point

**A point with at least MinPts points within its ε-neighbourhood.** **Core points form the interior of clusters**; clusters grow by connecting core points.

```text
p is a CORE point  ⇔  |N_ε(p)| ≥ MinPts
```

### 3.4 Border point

**A point that lies within the ε-neighbourhood of a core point but does not itself satisfy the MinPts condition.**

**Border points belong to a cluster but do not contribute to its expansion** — they are the edge, not the interior.

### 3.5 Noise point

**A point that is neither a core point nor a border point.** **Noise points do not belong to any cluster and are considered outliers.**

**Identifying noise is one of the key strengths of DBSCAN** — K-Means has no such category; it forces every point into a cluster, distorting the centroids.

**The three types in one line:** a **core** point has many neighbours, a **border** point has few neighbours but sits next to a core point, a **noise** point has few neighbours and no core point nearby.

---

## 4. Density reachability and density connectivity

These two definitions are what let a cluster grow.

**Density-reachable.** A point `q` is **directly density-reachable** from `p` if `q ∈ N_ε(p)` and `p` is a core point. It is **density-reachable** from `p` if there is a **chain of core points** `p = p₁, p₂, …, pₙ = q` where each `pᵢ₊₁` is directly density-reachable from `pᵢ`.

```text
p → q  directly reachable   :  q ∈ N_ε(p) and p is core
p → q  reachable             :  a chain of core points connects them
```

**Note the asymmetry:** reachability is **not symmetric**. A border point is reachable from its core point, but not vice versa — which is exactly why border points belong to a cluster without extending it.

**Density-connected.** Two points `p` and `q` are **density-connected** if **there exists a third point `o` from which both are density-reachable**.

**Density connectivity ensures that all points within a cluster are connected through dense regions** — it is the relation that is symmetric, and therefore the one a cluster is defined with:

```text
Cluster C = a maximal set of density-connected points
```

**This definition is what allows arbitrary shapes:** nothing in it refers to a centre, a radius from a centroid, or convexity — only to chains of dense neighbourhoods. A crescent, a ring, a spiral all qualify.

---

## 5. Working principle (the algorithm)

```text
DBSCAN(D, ε, MinPts):
1. Label every point as UNVISITED.
2. FOR each point p in D:
     IF p is already assigned to a cluster or labelled noise: skip
     compute N_ε(p)
     IF |N_ε(p)| < MinPts:
         label p as NOISE (tentatively — it may later become a border point)
     ELSE:
         create a new cluster C
         expand: for every point q in N_ε(p):
             IF q is NOISE: re-label q as BORDER of C
             IF q is UNVISITED:
                 mark visited
                 IF q is core: add N_ε(q) to the expansion queue
                 add q to C
3. Points still labelled NOISE after the scan are noise.
```

**In words (your page's version):** *DBSCAN begins by selecting an unvisited point and checking whether it is a core point. If it is, a new cluster is created and expanded by recursively including all density-reachable points. If not, the point is temporarily labelled noise. The process continues until all points are visited.*

**Why "temporarily":** a point that looks like noise on its own may turn out to be a **border point** of a cluster discovered later. Only at the end is the label final.

**Order dependence:** the *labels* can depend on scan order in edge cases (a border point equidistant between two clusters), but the **set of clusters is essentially determined by (ε, MinPts)** — unlike K-Means, where random initialisation changes the answer.

---

## 6. Full worked example

**Dataset (10 points in 2D — two dense blocks, one border point, one outlier):**

| Point | Coordinates |
|---|---|
| A | (1, 1) |
| B | (1, 2) |
| C | (2, 1) |
| D | (2, 2) |
| E | (3, 1.5) |
| F | (8, 8) |
| G | (8, 9) |
| H | (9, 8) |
| I | (9, 9) |
| J | (20, 20) |

**Parameters: ε = 1.5, MinPts = 4.** *(Convention: the neighbourhood of a point **includes the point itself** — state this in an exam, because some texts exclude it and the counts shift by one.)*

### Step 1 — Neighbourhood of every point

| Point | Neighbours within ε = 1.5 | Count | Type |
|---|---|---|---|
| **A (1,1)** | A, B (1.0), C (1.0), D (1.414) | **4** | **CORE** |
| **B (1,2)** | A (1.0), B, C (1.414), D (1.0) | **4** | **CORE** |
| **C (2,1)** | A (1.0), B (1.414), C, D (1.0), E (1.118) | **5** | **CORE** |
| **D (2,2)** | A (1.414), B (1.0), C (1.0), D, E (1.118) | **5** | **CORE** |
| **E (3,1.5)** | C (1.118), D (1.118), E | **3** | **BORDER** |
| **F (8,8)** | F, G (1.0), H (1.0), I (1.414) | **4** | **CORE** |
| **G (8,9)** | F (1.0), G, H (1.414), I (1.0) | **4** | **CORE** |
| **H (9,8)** | F (1.0), G (1.414), H, I (1.0) | **4** | **CORE** |
| **I (9,9)** | F (1.414), G (1.0), H (1.0), I | **4** | **CORE** |
| **J (20,20)** | J only (nearest neighbour F is 16.97 away) | **1** | **NOISE** |

**Sample calculations:**
```text
d(A,B) = √((1−1)² + (1−2)²) = 1.000      ≤ 1.5  ✔ neighbour
d(A,D) = √((1−2)² + (1−2)²) = 1.414      ≤ 1.5  ✔ neighbour
d(E,C) = √((3−2)² + (1.5−1)²) = √1.25 = 1.118  ≤ 1.5  ✔
d(E,B) = √((3−1)² + (1.5−2)²) = √4.25 = 2.062  > 1.5  ✘ not a neighbour
d(J,F) = √((20−8)² + (20−8)²) = 16.971   ≫ 1.5  ✘
```

### Step 2 — Grow the clusters

**Cluster 1 starts at A (core).** Its neighbours A, B, C, D are core, so their neighbours are added: C and D reach **E**, which is not core but is within ε of the core points C and D → **E becomes a border point of cluster 1**.

```text
Cluster 1 = {A, B, C, D, E}      (4 core + 1 border)
```

**Cluster 2 starts at F (core).** G, H, I are all core and mutually within ε → the whole block.

```text
Cluster 2 = {F, G, H, I}         (4 core)
```

**J** has no neighbour within ε and is not within ε of any core point → **noise**.

```text
Clusters: 2     Noise: 1 (J)
```

**The output in words:** DBSCAN found two clusters **without being told K = 2**, correctly attached the edge point E to the cluster it touches, and flagged the distant point J as an outlier instead of forcing it into a cluster.

### Step 3 — How the parameters would change the answer

| Change | Effect |
|---|---|
| **ε = 1.0** | A now reaches only B and C (2 neighbours + itself = 3 < 4) → A becomes **border/noise**; the block fragments; many points drop out. **Too small.** |
| **ε = 3.0** | The two blocks are still 7+ apart, so they stay separate — but E's neighbourhood grows and low-density gaps start filling in. |
| **ε = 4.0** | Still not enough to join the blocks (they are ~9.9 apart), but J remains noise. |
| **MinPts = 3** | E's 3 neighbours now qualify → **E becomes core**, and the cluster still grows; fewer border points. |
| **MinPts = 6** | A, B, F, G, H, I (all count 4) drop below the threshold → most of the block becomes border or noise. **Too large.** |

**The lesson:** ε and MinPts are **not independent** — raising MinPts is roughly equivalent to lowering ε. Tune them together (the standard method is the **k-distance plot**: sort each point's distance to its k-th nearest neighbour, and choose ε at the "knee").

---

## 7. Distance measures used in DBSCAN

**DBSCAN commonly uses Euclidean distance for numeric data**, but **can also work with other measures** — Manhattan distance or cosine similarity, depending on the dataset:

| Measure | Use |
|---|---|
| **Euclidean** | spatial/geographic data (the default) |
| **Manhattan** | grid movement, robust to single large coordinate differences |
| **Cosine** | high-dimensional sparse vectors (text) — but requires care, since cosine is not a metric in the same sense |
| **Haversine** | latitude/longitude on the globe |
| **Custom** | any metric satisfying the triangle inequality works best |

**The distance measure should align with the meaning of similarity in the application domain** — a point is in a "dense region" only relative to the metric you chose.

---

## 8. Advantages (your page)

- **Discovers clusters of arbitrary shapes and sizes** — rings, crescents, chains, anything defined by density.
- **Does not require the number of clusters to be predefined** — K comes out of the data.
- **Effectively identifies noise and outliers** — they are a first-class output, not a distortion.
- **Performs well even when clusters vary in size** — no equal-size assumption.
- **Deterministic** given (ε, MinPts) and a fixed scan order — no random initialisation.
- Needs only **one pass** over the data once neighbourhoods are indexed (`O(n log n)` with a spatial index such as a k-d tree).

## 9. Limitations (your page)

- **Sensitive to the choice of ε and MinPts** — the single biggest practical difficulty; wrong values give either one giant cluster or all-noise.
- **Struggles with datasets of varying density** — a single ε cannot be both small enough for the dense region and large enough for the sparse one (this is what **OPTICS** and **HDBSCAN** solve).
- **Performance degrades in high-dimensional spaces** due to the **curse of dimensionality** — distance concentration destroys the notion of "dense neighbourhood".
- Results depend on the **distance metric** chosen.
- Border points lying between two clusters are assigned to whichever cluster reaches them first (minor order dependence).
- **Not suitable when clusters overlap heavily** in dense regions — they merge.

---

## 10. DBSCAN vs K-Means (your page's comparison, extended)

| Aspect | **K-Means** | **DBSCAN** |
|---|---|---|
| Cluster shape | **spherical** (Voronoi cells) | **arbitrary** |
| K needed | **yes, in advance** | **no** |
| Noise/outliers | forced into a cluster, distort centroids | **detected and excluded** |
| Parameters | K | **ε and MinPts** |
| Determinism | random init → varies | deterministic given parameters |
| Varying density | handled (each cluster independent) | **fails** (one global ε) |
| High dimensions | works (with care) | **degrades** |
| Complexity | `O(n·K·d·i)` | `O(n log n)` with index, `O(n²)` without |
| Output | partition only | partition **+ noise label** |

*The exam one-liner: K-Means forms spherical clusters and is sensitive to outliers, whereas DBSCAN can form arbitrary-shaped clusters and explicitly detects noise; K-Means requires the number of clusters in advance, while DBSCAN does not.*

---

## 11. Applications

**Spatial data analysis, geographic information systems, image processing, anomaly detection, fraud detection, scientific data analysis** — *especially useful when data contains noise or clusters of irregular shapes*: identifying crime hotspots, grouping GPS traces, finding connected components in images, detecting network intrusions.

---

## 12. Summary

DBSCAN defines clusters as **regions of high density** separated by low density, using two parameters — **ε**, the neighbourhood radius, and **MinPts**, the minimum number of points inside it. Points are classified as **core** (≥ MinPts neighbours), **border** (fewer, but within ε of a core point) or **noise** (neither); clusters grow by **density reachability** through chains of core points and are defined as maximal sets of **density-connected** points, which is what allows **arbitrary shapes**. On the ten-point example with ε = 1.5 and MinPts = 4, four core points plus border point E form **{A, B, C, D, E}**, the block **{F, G, H, I}** forms a second cluster, and **J (20,20) is correctly labelled noise** — with **no K supplied**. Its power is shape-independence and explicit noise handling; its price is sensitivity to ε and MinPts and failure on data whose density varies across the dataset.

---

**Want more from this unit?** The [revision cheat sheet](../exam/cheat-sheet.md), [question bank](../exam/question-bank.md) and code toolkit are being built once the remaining LMS pages arrive.
