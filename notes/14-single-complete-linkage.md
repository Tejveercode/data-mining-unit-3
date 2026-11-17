# Topic 14 — Single & Complete Linkage

> **LMS page:** *Single & Complete Linkage* · **CO5**.
> This note zooms in on the two linkages that define the extremes; Topic 8 covered the family and the dendrogram view. The 1-D chaining example below is **computed and verified**.

---

## 1. What linkage means

**Linkage is the rule used to measure the distance between two clusters based on the distances between their data points.**

At each step of **agglomerative** hierarchical clustering, the linkage method **determines which clusters should be merged**:

```text
repeat:
    for every pair of clusters (A, B):
        compute cluster distance  d(A, B)   ← this is the linkage rule
    merge the pair with the smallest d(A, B)
until one cluster remains
```

**Different linkage methods can produce significantly different dendrogram structures even on the same dataset** — the data does not change, only the definition of "close", and the hierarchy follows.

**Why this is the crux of hierarchical clustering:** every other design choice (the distance metric, the merge rule) is fixed by textbook convention. **The linkage is the one place where the analyst genuinely chooses**, and it decides whether the result is compact and separated or long and chained.

---

## 2. Single linkage (nearest neighbour / MIN)

**The distance between two clusters is the minimum distance between any pair of data points, one from each cluster.**

```text
d_single(A, B) = min { d(a, b) : a ∈ A, b ∈ B }
```

**This method focuses on the closest pair of points between clusters, and merges clusters that have at least one pair of very similar data points.**

### Working principle

1. **Initially each data object is a separate cluster.**
2. **Compute the distance between all pairs of clusters** and identify the pair with the **smallest minimum distance**.
3. **Merge those two clusters.**
4. **Repeat** until all objects form one cluster or the desired structure is obtained.

**Computationally this is the cheapest linkage:** the merge distance is read straight off the sorted list of pairwise point distances, and after a merge the new cluster's distance to any other is `min(d(A,C), d(B,C))` — two numbers compared, nothing recomputed across `|A|·|B|` pairs.

### Characteristics

**Single linkage is capable of detecting clusters of arbitrary shapes, especially elongated or irregular clusters** — two crescents that touch at one tip are joined at that tip, which is exactly right.

**However, it is highly sensitive to noise and outliers.** **A major drawback is the chaining effect, where clusters are formed by a sequence of close points, even if the overall cluster structure is weak.** A single intermediate point can weld two well-separated groups into one long chain — and *the height at which that merge happens is low*, so the dendrogram looks confident about a merger that is an artefact.

**Why the chaining happens, mechanically:** single linkage only ever asks "is there *one* close pair?" It never checks the rest of the cluster. So a chain of points each 1 unit apart, spanning 20 units, is "one cluster at height 1" — even though its diameter is 20.

---

## 3. Complete linkage (farthest neighbour / MAX)

**The distance between two clusters is the maximum distance between any pair of points, one from each cluster.**

```text
d_complete(A, B) = max { d(a, b) : a ∈ A, b ∈ B }
```

**This method considers the farthest pair of points between clusters and merges clusters only when all points in the clusters are relatively close to each other.**

### Working principle

1. **Each data object starts as an individual cluster.**
2. **At each step, the distance between all cluster pairs is calculated using the maximum distance criterion.**
3. **The pair of clusters with the smallest maximum distance is merged.**
4. Repeat iteratively.

**After a merge the update is `max(d(A,C), d(B,C))`** — again two numbers, so it is also cheap to maintain.

### Characteristics

**Complete linkage tends to create compact clusters with small diameters.** **It reduces the chaining effect seen in single linkage and is less sensitive to noise.**

**However, complete linkage may break large natural clusters into smaller clusters** — because the merge is vetoed by the single farthest member, a natural group with one outlying member gets split. **It is sensitive to extreme values within clusters** for exactly that reason.

**The mechanism is the mirror image of single linkage:** complete linkage only asks "is *every* pair close?" A genuine cluster whose corner is slightly far gets rejected; the same single far point that causes chaining to run wild cannot cause complete linkage to merge at all.

---

## 4. The definitive worked example — chaining, demonstrated

**Dataset (1-D, two obvious groups plus one bridge point):**

```text
A = 0    B = 1    C = 2    D = 3      M = 4.5      E = 6    F = 7    G = 8
├────┼────┼────┼──────────┤────────────────────────┼────┼────┼
 left group (0–3)          bridge              right group (6–8)
```

**Truth:** two clusters, `{A,B,C,D}` and `{E,F,G}`. **M is a bridge point** — exactly equidistant from D (1.5) and E (1.5), which is the worst case and therefore the clearest demonstration.

### Single linkage

| Step | Merge | Height |
|---|---|---|
| 1 | A + B | **1.0000** |
| 2 | {A,B} + C | **1.0000** |
| 3 | {A,B,C} + D | **1.0000** |
| 4 | E + F | **1.0000** |
| 5 | {E,F} + G | **1.0000** |
| 6 | {A,B,C,D} + **M** | **1.5000** |
| 7 | {A,B,C,D,M} + {E,F,G} | **1.5000** |

**At height 1.5 the whole dataset is one cluster.** Single linkage saw a continuous chain `0 → 1 → 2 → 3 → 4.5 → 6 → 7 → 8` with no gap larger than 1.5, and concluded there is no separation at all. **This is the chaining effect, in numbers: two obviously distinct groups are merged at a height barely above the internal spacing.**

### Complete linkage

| Step | Merge | Height |
|---|---|---|
| 1 | A + B | **1.0000** |
| 2 | C + D | **1.0000** |
| 3 | E + F | **1.0000** |
| 4 | {E,F} + G | **2.0000** |
| 5 | {C,D} + M | **2.5000** |
| 6 | {A,B} + {C,D,M} | **4.5000** |
| 7 | {A,B,C,D,M} + {E,F,G} | **8.0000** |

**Now the last merge is at height 8.0, more than three times the largest internal merge height.** The dendrogram shows two clusters with a huge gap — which matches the truth. **Same data, same distance metric, opposite conclusion**, purely because complete linkage asked "are *all* the points close?" and the bridge point did not satisfy that for both sides.

### Average linkage (the middle ground, for contrast)

| Step | Merge | Height |
|---|---|---|
| 1 | A + B | 1.0000 |
| 2 | C + D | 1.0000 |
| 3 | E + F | 1.0000 |
| 4 | {E,F} + G | 1.5000 |
| 5 | {A,B} + {C,D} | 2.0000 |
| 6 | M + {E,F,G} | 2.5000 |
| 7 | {A,B,C,D} + {E,F,G,M} | **4.8750** |

**Final heights: single 1.5 → complete 8.0 → average 4.875.** *The three numbers are the same data's answer to "how far apart are these two groups?" — and they differ by a factor of more than five.*

**Which is correct?** For this data, **complete or average**. But single linkage is not wrong in general — if the two groups had been crescents interlocking at one point, single would have been the only one to find them. **The linkage encodes an assumption about cluster shape; the data decides which assumption is true, and you often cannot know in advance** — which is a legitimate exam answer, and the reason practitioners run all three and compare.

---

## 5. The Lance–Williams view (why the two are one formula)

Both linkages are special cases of a single update rule for the distance from a merged cluster `A∪B` to any other cluster `C`:

```text
d(A∪B, C) = α_A·d(A,C) + α_B·d(B,C) + β·d(A,B) + γ·|d(A,C) − d(B,C)|

Single:    α_A = α_B = ½    β = 0    γ = −½      →  min(d(A,C), d(B,C))
Complete:  α_A = α_B = ½    β = 0    γ = +½      →  max(d(A,C), d(B,C))
Average:   α_A = |A|/(|A|+|B|), α_B = |B|/(|A|+|B|), β = 0, γ = 0
Ward:      β ≠ 0 (variance-based)
```

**The whole difference between single and complete linkage is the sign of γ.** Negative γ takes the minimum, positive γ takes the maximum — one sign, and the entire shape of the dendrogram changes. *That is a strong sentence for a 10-mark answer on linkage.*

---

## 6. Distance measures used

**Both single and complete linkage rely on an underlying distance measure** such as **Euclidean distance, Manhattan distance or cosine similarity**.

**The linkage method determines how these point-to-point distances are aggregated to measure cluster-to-cluster distance** — the metric supplies the numbers, the linkage supplies the aggregation.

**A subtle but examinable point:** single linkage is invariant to **monotone transformations** of the metric (only the ordering matters), which is why it pairs well with rank-based or correlation distances. Complete linkage uses the maximum, which is **not** order-invariant in the same way — a compact cluster's diameter is sensitive to which value is largest.

---

## 7. Comparison (your page's contrast, completed)

| Aspect | **Single linkage** | **Complete linkage** |
|---|---|---|
| Cluster distance | **minimum** pair distance | **maximum** pair distance |
| Emphasis | **local proximity** | **global compactness and separation** |
| Cluster shape found | **elongated, chain-like, irregular** | **compact, spherical, similar diameter** |
| Chaining effect | **severe** | **reduced** |
| Noise / outlier sensitivity | **high** | **sensitive to extreme values within clusters** |
| Risk | merges distinct clusters via one bridge | **splits natural clusters** (over-segmentation) |
| Complexity | cheaper update (min of two) | cheaper update (max of two) |
| Dendrogram look | merges happen early and low | merges happen late and high |
| Best when | connectivity matters, shapes are irregular | clearly separated, compact groups are expected |

**Single linkage emphasises local proximity and can connect clusters through nearest neighbours, while complete linkage emphasises global compactness and separation.**

**Single linkage is suitable when clusters are expected to have irregular shapes, whereas complete linkage is preferred when compact and clearly separated clusters are desired.**

---

## 8. Advantages and limitations

### Single linkage

**Advantages**
- **Simple to compute** and the cheapest linkage to maintain.
- **Effective in identifying non-spherical and chain-like cluster structures.**
- **Can capture natural connections between data points** — the right model for networks, trajectories and filamentary data.
- Invariant to monotone transformations of the distance.
- Can be implemented with a minimum spanning tree — `O(n²)` and elegant.

**Limitations**
- **Highly sensitive to noise and outliers.**
- **The chaining effect can lead to poor cluster quality and difficulty in interpreting results** (as demonstrated above: one bridge point collapsed two clusters into one).
- No notion of cluster diameter, so "cluster" can mean a very long snake.

### Complete linkage

**Advantages**
- **Produces compact and well-separated clusters** with small diameters.
- **Less affected by noise and chaining compared to single linkage.**
- Every member is guaranteed to be within a bounded distance of every other — a strong, checkable guarantee.

**Limitations**
- **May over-segment data** and split large natural clusters.
- **Sensitive to outliers within clusters** — one far member blocks a sound merge.
- **Can be computationally expensive for large datasets** when implemented naively.

---

## 9. Applications (your page)

**Single linkage** — *applications where connectivity is important*: **network analysis** (community connectivity, connected components), **image segmentation** (contiguous regions), trajectory and filament detection, clustering of connected geographical features.

**Complete linkage** — *biological classification, document clustering and market segmentation where compact clusters are required*: taxonomy building, grouping similar documents by topic, customer segments that must be tight enough to target.

---

## 10. Practical guidance

1. **Plot all three dendrograms** (single, complete, average) and compare the merge heights — if they agree, you have structure; if they disagree, look at *why* (a bridge point? an outlier?).
2. **Look for the largest gap** in merge heights and cut there; the chaining example's gap is 2.5 → 8.0 for complete (cut in between) but there is no gap at all for single.
3. **Check the diameter of every cluster you accept.** A "cluster" of points 8 units apart reported at height 1.5 is an artefact.
4. **Scale the attributes first** — linkage inherits every scaling problem of the metric (Unit 2).
5. **For large n**, neither is practical: use `O(n²)` memory only up to tens of thousands of points, otherwise K-Means or DBSCAN.

---

## 11. Summary

Linkage is the rule that turns point-to-point distances into cluster-to-cluster distances, and it is the one genuine choice in agglomerative clustering. **Single linkage** takes the **minimum** distance between any pair — cheap, able to find **elongated and chain-like clusters**, but **highly sensitive to noise**, with the **chaining effect** as its signature failure. **Complete linkage** takes the **maximum** — producing **compact, well-separated clusters** and resisting chaining, at the cost of **over-segmenting** natural clusters when one member is far away. The 1-D bridge example makes the difference concrete: on points `0,1,2,3,4.5,6,7,8`, **single linkage merges everything by height 1.5**, while **complete linkage holds the two groups apart until height 8.0**, with **average at 4.875** between them — the same data, the same metric, and answers that differ by a factor of more than five. In the Lance–Williams formulation the only difference is **the sign of γ**: negative takes the minimum, positive takes the maximum.

---

**Next:** [Topic 15 — Real-Time Case Studies for Classification & Clustering](15-case-studies.md)
