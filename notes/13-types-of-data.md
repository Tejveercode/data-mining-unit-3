# Topic 13 — Types of Data in Cluster Analysis

> **LMS page:** *Types of Data in Cluster Analysis* · **CO5**.
> Every similarity measure below is computed on a small example, so the formulas are checkable.

---

## 1. Why data types come first

**Cluster analysis can be applied to different kinds of data. The type of data determines the choice of similarity or distance measure and the clustering algorithm.**

**Understanding data types is essential because clustering results are highly dependent on how data objects and attributes are represented.**

**Data is described from two perspectives: data objects and attribute types.** **Attributes define how similarity between objects is measured** — so the attribute type *is* the distance formula.

| Attribute type | Correct measure | Wrong measure and why |
|---|---|---|
| Nominal | simple matching, Jaccard | Euclidean — treating "red = 3" as a number invents order |
| Ordinal | rank-normalised distance | raw Euclidean — assumes equal spacing between ranks |
| Interval | Euclidean on differences | ratios — 40 °C is not twice 20 °C |
| Ratio | Euclidean, Manhattan, Minkowski | — (all valid) |
| Text | cosine, Jaccard | Euclidean — length dominates |

---

## 2. Data objects

**A data object is an entity represented by a collection of attributes** — **each row in a dataset is one data object**.

**Examples:** customers in a database, documents in a text corpus, images in an image dataset, transactions in a retail system.

**Depending on the application, data objects can be points in multidimensional space, sequences, graphs or spatial entities.** This matters: a customer is a point, a DNA strand is a sequence, a social network is a graph — and each representation implies a different notion of distance.

**Notation:** an object `i` is a vector `x_i = (x_i1, x_i2, …, x_ip)` over p attributes; the collection is a matrix `n × p`.

---

## 3. Nominal (categorical) data

**Names, labels or categories with no inherent order.** The values **cannot be meaningfully compared using greater-than or less-than**.

**Examples:** gender (male, female), blood group (A, B, AB, O), colour (red, blue, green), product category.

**Similarity is measured by simple matching** — count agreements, divide by the number of attributes:

```text
d(i, j) = (p − m) / p          m = number of attributes where i and j agree
                              p = total number of nominal attributes
```

**Worked:** `o₁ = (red, medium, yes, high)`, `o₂ = (blue, medium, no, high)`

| Attribute | o₁ | o₂ | Match? |
|---|---|---|---|
| colour | red | blue | ✘ |
| size | medium | medium | ✔ |
| response | yes | no | ✘ |
| rating | high | high | ✔ |

```text
m = 2, p = 4 →  similarity = 2/4 = 0.5000      distance = 1 − 0.5 = 0.5000
```

**Distance-based measures like Euclidean are not suitable** — encoding colours as 1, 2, 3 would make "blue" halfway between "red" and "green", which is meaningless. **Clustering algorithms for nominal data often use matching coefficients or probabilistic models** (k-modes, latent class models).

---

## 4. Binary data

**A special type of nominal data with only two values, usually 0 and 1.**

**Examples:** yes/no responses, true/false, presence or absence of an attribute.

### Symmetric vs asymmetric

| | **Symmetric binary** | **Asymmetric binary** |
|---|---|---|
| Both values equally important? | **yes** | **no** — presence matters more |
| Example | gender (male=1, female=0) | **medical symptoms**, **transaction items** |
| Measure | simple matching coefficient | **Jaccard coefficient** |

**The 2×2 contingency table:**

|  | j = 1 | j = 0 |
|---|---|---|
| **i = 1** | **a** | **b** |
| **i = 0** | **c** | **d** |

```text
Simple matching coefficient (symmetric)  d = (b + c) / (a + b + c + d)
Jaccard coefficient (asymmetric)         d = (b + c) / (a + b + c)        [d ignored]
```

**Worked.** Seven binary attributes:

```text
x = (1, 1, 0, 1, 0, 0, 0)
y = (1, 1, 1, 0, 0, 0, 1)
```

Counting: **a = 2** (both 1), **b = 1** (x=1, y=0), **c = 2** (x=0, y=1), **d = 2** (both 0).

```text
Simple matching (symmetric):  (b + c)/(a+b+c+d) = 3/7 = 0.4286   → similarity 0.5714
Jaccard (asymmetric):          (b + c)/(a+b+c)   = 3/5 = 0.6000   → similarity a/(a+b+c) = 2/5 = 0.4000
```

**Why the two disagree is the whole point:** the two shared absences (d = 2) count as agreement under simple matching, but **"neither patient has a fever" is not evidence of similarity** in a medical context. **Jaccard ignores d**, so it measures agreement on *what is present* — which is why it is the standard for market baskets (two customers who both bought nothing have nothing in common).

---

## 5. Ordinal data

**Categories with a meaningful order but no fixed numerical differences between values.**

**Examples:** rankings such as low/medium/high, grades poor/average/good/excellent.

**Although ordinal data shows relative order, arithmetic operations are not meaningful** — the gap between "poor" and "average" need not equal the gap between "good" and "excellent". **Ordinal values are often converted into ranks or normalised scores before clustering.**

**The standard treatment** (rank `rᵢ` from 1…M, then map to [0,1]):

```text
z = (r − 1) / (M − 1)
```

then use any numeric distance on the normalised values.

**Worked.** Three attributes with values {fair, good, excellent}, so `M = 3` and the mapping is fair → 0, good → 0.5, excellent → 1.

| Object | Raw values | Ranks | Normalised |
|---|---|---|---|
| o₁ | excellent, fair, good | 3, 1, 2 | **1.0, 0.0, 0.5** |
| o₂ | fair, good, excellent | 1, 2, 3 | **0.0, 0.5, 1.0** |

```text
Euclidean  = √(1² + 0.5² + 0.5²) = √1.5 = 1.2247
Manhattan  = 1 + 0.5 + 0.5        = 2.0000
```

**The normalisation is doing real work:** on raw ranks the same comparison gives `√(4 + 1 + 1) = 2.449`, a different number — and if you skip this step, an attribute with 10 levels silently outweighs one with 3.

---

## 6. Interval data

**Numeric data where the difference between values is meaningful, but there is no true zero point.**

**Examples:** temperature in Celsius or Fahrenheit, calendar dates, time values.

**Distance-based clustering algorithms can be applied to interval data, but ratios are not meaningful** — **40 °C is not twice as hot as 20 °C**, because the zero is arbitrary.

**The standard measure after scaling** (mean-absolute-deviation or z-score normalisation is preferred, because it reduces outlier influence):

```text
d(i, j) = √( Σ (x_if − x_jf)² )          after normalising each attribute
```

**Worked:** `A = (40, 10, 6)`, `B = (42, 12, 8)` → raw Euclidean `√(4 + 4 + 4) = 3.4641`.

**But note the trap:** if the attributes are temperature in °C, height in cm and count, those raw distances are mixing units, and the third attribute contributes almost nothing. **Normalise each attribute first** (min–max or z-score, from Unit 2), then compute — that is the step that makes interval data usable.

---

## 7. Ratio data

**Numeric data with a meaningful zero point, so both differences and ratios are interpretable.**

**Examples:** height, weight, age, income, distance, number of purchases.

**Ratio data is the most suitable type for clustering using Euclidean, Manhattan or Minkowski distance.** **Most popular clustering algorithms such as K-means work best with ratio-scale data** — because a centroid is a mean, and a mean is only meaningful when ratios are.

**Worked:** `(170 cm, 60 kg)` vs `(180 cm, 80 kg)` → `√(100 + 400) = 22.3607` — *and again, meaningless until both columns are normalised, because 10 cm and 20 kg are not comparable units.*

---

## 8. Discrete and continuous data

**Discrete data** — **countable values, usually integers**: number of customers, number of visits, number of items purchased.
**Often treated as numeric, but care must be taken when choosing distance measures** — a Poisson-like distribution makes Euclidean distance misleading, and count data with huge ranges needs log transforms.

**Continuous data** — **any value within a range**: temperature, time, speed, salary.
**Ideal for clustering algorithms that rely on geometric distance calculations.**

---

## 9. Spatial data

**Objects with a location in space** — geographic coordinates, satellite images, map data.

**In spatial clustering, both location and attribute values are important.** **Specialised distance measures and algorithms are used, especially in geographic information systems** — Haversine distance for latitude/longitude, and DBSCAN (Topic 9) was designed for exactly this case.

---

## 10. Time-series data

**Observations collected over time** — stock prices, sensor readings, weather data.

**Clustering time-series requires similarity measures that consider temporal behaviour rather than just point-wise distance.** Two series may have identical values shifted by one day; Euclidean distance calls them far apart, **dynamic time warping (DTW)** calls them a match. Other options: correlation distance (shape), spectral features, or piecewise aggregate approximation to reduce dimension.

---

## 11. Text and document data

**Unstructured or semi-structured information** — emails, articles, social-media posts, reviews.

**Text is typically transformed into numerical representations such as term-frequency vectors before clustering** (TF or TF-IDF, from Unit 2). **Clustering then groups documents by topic or content similarity.**

**Worked (cosine similarity).** Term vectors over {data, mining, rules}:

| Document | data | mining | rules |
|---|---|---|---|
| d₁ | 3 | 2 | 0 |
| d₂ | 2 | 2 | 1 |

```text
cos(d₁, d₂) = (3×2 + 2×2 + 0×1) / (√13 · √9)
            = 10 / (3.6056 × 3.0000) = 10/10.8167 = 0.9245
cosine distance = 1 − 0.9245 = 0.0755   → the two documents are very similar
```

**Why cosine and not Euclidean:** d₂ is essentially d₁ with one extra "rules" mention. Euclidean distance would also **punish a long document** merely for being long; cosine compares **direction** (topic mix), which is the property you actually want.

---

## 12. Mixed-type data — the general formula

Real datasets mix nominal, ordinal and numeric attributes. **Han's heterogeneous similarity** handles them in one expression:

```text
d(i, j) = Σ(f=1..p) δ_ij^(f) · d_ij^(f)  /  Σ(f=1..p) δ_ij^(f)

δ_ij^(f) = 0  if x_if or x_jf is missing
         = 0  if attribute f is asymmetric binary and both values are 0
         = 1  otherwise

d_ij^(f) = 0 if x_if = x_jf  (nominal)
         = 1 if x_if ≠ x_jf
         = |x_if − x_jf| / (max_f − min_f)              (numeric)
         = |r_if − r_jf| / (M_f − 1)                    (ordinal)
```

**Worked.** Three objects, three attributes (nominal gender, ordinal grade, ratio age):

| Object | gender | grade (fair < good < excellent) | age |
|---|---|---|---|
| o₁ | male | excellent → 1.0 | 45 → 0.5 |
| o₂ | female | fair → 0.0 | 40 → 0.0 |
| o₃ | male | good → 0.5 | 50 → 1.0 |

*(ordinal normalised by `(r−1)/(M−1)` with M = 3; age min–max normalised over 40–50)*

```text
d(o₁,o₂) = (1 [gender] + 1.0 [grade] + 0.5 [age]) / 3 = 2.5/3 = 0.8333
d(o₁,o₃) = (0 [gender] + 0.5 [grade] + 0.5 [age]) / 3 = 1.0/3 = 0.3333
d(o₂,o₃) = (1 [gender] + 0.5 [grade] + 1.0 [age]) / 3 = 2.5/3 = 0.8333
```

**Reading the result:** o₁ and o₃ are the similar pair (same gender, adjacent grades, modest age gap); o₂ is equally distant from both. **Without per-attribute normalisation the age column — spanning 10 units — would have swamped the 0/1 gender flag entirely.**

---

## 13. The proximity matrix

Whatever the measure, the output is the same object: an `n × n` **proximity (distance) matrix**, symmetric with zeros on the diagonal.

```text
        o₁      o₂      o₃
o₁    0.0000  0.8333  0.3333
o₂    0.8333  0.0000  0.8333
o₃    0.3333  0.8333  0.0000
```

**Every algorithm in this unit consumes exactly this matrix.** That is the practical payoff of the topic: **PAM needs only dissimilarities** (so it works with any of these measures), **hierarchical clustering is built from the matrix alone**, **DBSCAN needs a metric** satisfying the triangle inequality, and **K-Means needs a mean** — which quietly restricts it to numeric, ratio-scale data.

---

## 14. Choosing the right measure (decision table)

| Data | Measure | Avoid |
|---|---|---|
| Nominal | simple matching, k-modes | Euclidean on arbitrary codes |
| Binary, symmetric | simple matching coefficient | Jaccard (over-penalises) |
| Binary, asymmetric | **Jaccard** | simple matching (shared absences inflate similarity) |
| Ordinal | rank-normalise to [0,1], then distance | raw differences of codes |
| Interval | normalise, then Euclidean | ratios |
| Ratio | normalise, then Euclidean/Manhattan/Minkowski | nothing, but scaling is mandatory |
| Spatial | Haversine, DBSCAN | Euclidean on lat/long near poles |
| Time series | DTW, correlation, spectral | point-wise Euclidean under shifts |
| Text | **cosine**, Jaccard on shingles | Euclidean on raw counts |
| Mixed | weighted heterogeneous similarity | forcing everything numeric |

---

## 15. Summary

The attribute type determines the similarity measure, and the measure determines the clustering. **Nominal** attributes use **simple matching** (2/4 = 0.5 on the colour/size/response/rating example); **binary** attributes split into **symmetric** (simple matching, 0.5714 here) and **asymmetric** (**Jaccard**, 0.4000 here, because shared absences are not evidence); **ordinal** attributes are **rank-normalised** `(r−1)/(M−1)` before any distance (giving 1.0/0.0/0.5 for excellent/fair/good); **interval** data allows differences but not ratios (40 °C ≠ 2 × 20 °C) and needs normalisation; **ratio** data is the natural home of K-Means and Euclidean distance; and **spatial, time-series, text and mixed** data each demand their own measure — Haversine, DTW, **cosine (0.9245 for the worked pair)** and the **weighted heterogeneous formula** (0.8333 / 0.3333 / 0.8333 for the three-object example). Everything collapses to one artefact — the **n × n proximity matrix** — which is what the algorithms in Topics 5–9 actually consume.

---

**Next:** [Topic 14 — Single & Complete Linkage](14-single-complete-linkage.md)
