# Topic 12 — Overview of Clustering & Need for Clustering

> **LMS page:** *Overview of Clustering & Need for Clustering* · **CO5**.
> This is the conceptual entry point to the clustering half of the unit (notes 12–15).

---

## 1. Introduction to clustering

**Clustering is one of the most important tasks in data mining and machine learning, especially under unsupervised learning.** It refers to the process of **grouping a set of data objects into meaningful subsets called clusters**, such that:

- objects **within the same cluster are highly similar**,
- objects **belonging to different clusters are dissimilar**.

**Unlike classification, clustering does not require predefined class labels.** Instead, **the structure of the data itself is analysed to discover natural groupings**.

**Clustering helps in understanding the hidden structure of data and plays a crucial role in exploratory data analysis.** *That is the honest framing: clustering does not tell you what a group means — it tells you where the structure is, and a domain expert names it.*

---

## 2. Definition

**Clustering is the process of partitioning a dataset into groups (clusters) so that:**

1. objects in the **same** cluster are **more similar** to each other, and
2. objects in **different** clusters are **less similar**.

**Similarity or dissimilarity is usually measured using:**

| Family | Examples |
|---|---|
| **Distance measures** | Euclidean, Manhattan, Minkowski, cosine |
| **Density- or connectivity-based measures** | ε-neighbourhoods (DBSCAN), graph connectivity |

**The measure is a modelling choice, and it decides the answer.** Two clustering runs on identical data with different distance measures are answering different questions — which is why "the clustering" is never unique.

---

## 3. Characteristics of clustering (your page's five)

| Characteristic | Meaning |
|---|---|
| **Unsupervised learning** | **no class labels** are provided |
| **Data-driven** | clusters are formed from **inherent patterns**, not from a target |
| **Exploratory** | used to **discover unknown structures** |
| **Flexible** | applies to **numeric, categorical, spatial and text** data |
| **Application-dependent** | **no single clustering method works best for all datasets** |

**That last point is a theorem in practice, not a preference.** K-Means assumes convex, similar-sized clusters; DBSCAN assumes density-separated clusters; single linkage assumes chain-like connectedness. Each is optimal for its own assumption and wrong for the others. **Any exam question of the form "which clustering algorithm is best?" is answered "it depends on the cluster shape, noise level and whether K is known" — with the comparison table from the cheat sheet as the evidence.**

---

## 4. Clustering vs classification (your page's table, completed)

| Aspect | **Clustering** | **Classification** |
|---|---|---|
| **Learning type** | **Unsupervised** | **Supervised** |
| **Labels** | **not required** | **required** |
| **Goal** | **discover groups** | **predict class** |
| **Output** | **clusters** (with no names) | **class labels** (predefined) |
| **Evaluation** | internal (cohesion/separation) or external (if labels exist) | accuracy, precision, recall, F1, AUC |
| **Number of groups** | often **discovered** (hierarchical, DBSCAN) or supplied (K-Means) | fixed by the label set |
| **Example** | customer segmentation | email spam detection |
| **When it fails** | clusters have no business meaning | a class is missing from the training data |

**The practical consequence:** a classifier can be **scored** (we know the right answer); a clustering can only be **judged** (we do not). That asymmetry explains the whole evaluation sub-topic in §7.

---

## 5. The clustering process (your page's seven steps)

```text
1. Data collection        gather raw data from various sources
2. Data pre-processing    missing values, noise, normalisation, scaling
3. Feature selection      keep the attributes that matter for similarity
4. Similarity measurement choose the distance/similarity measure
5. Algorithm application  K-Means, Hierarchical, DBSCAN, …
6. Cluster evaluation     cohesion, separation, silhouette, domain review
7. Interpretation         name the clusters, act on them
```

**Note steps 2 and 3 are Unit 2.** This is not decoration: **clustering is the algorithm most damaged by poor pre-processing**, because every distance is computed on whatever scale you left the data in. A salary column in lakhs and an age column in years means you clustered on salary.

**Step 7 is where most projects actually fail** — a technically valid clustering whose groups nobody can name is an answer without a question.

---

## 6. The need for clustering (your page's eight reasons)

**Clustering is required due to the increasing volume, complexity and variety of data.**

### 6.1 Data understanding and exploration
Large datasets are difficult to analyse manually. Clustering helps in **discovering natural groupings, understanding data distribution and identifying hidden patterns**.
*Example: grouping students by performance level.*

### 6.2 Data summarisation
Clustering reduces complexity by **representing large datasets with clusters** and providing a **high-level summary**. Decision-makers focus on **groups instead of individual records**.
*Mechanically this is compression: 1,000,000 customers become 6 segments with centroids.*

### 6.3 Pattern discovery
Identifies **customer behaviour patterns, purchase trends and usage habits**.
*Example: grouping customers with similar buying behaviour.*

### 6.4 Customer segmentation
The most common application: grouping customers by **age, income and purchasing history** for **targeted marketing and personalised services**.

### 6.5 Anomaly and outlier detection
Objects that **do not belong to any cluster or lie far from cluster centres** may indicate **fraud, errors or rare events**.
*Example: detecting fraudulent credit-card transactions.*
**Note the inversion:** here the clusters are the background and the **noise is the finding** — which is exactly why DBSCAN's explicit noise label matters more than its clusters in this use case.

### 6.6 Information retrieval and text mining
Grouping similar documents, organising search results, improving recommendations.
*Example: news articles grouped by topic.*

### 6.7 Image and pattern recognition
Image segmentation, object recognition, medical image analysis.
*Example: grouping pixels with similar colour intensity.*

### 6.8 Bioinformatics and healthcare
Gene-expression analysis, disease classification, patient grouping.
*Example: identifying patients with similar symptoms.*

---

## 7. How clusters are judged (cohesion and separation)

Since there are no labels, quality is measured from the geometry itself.

**Cohesion** — how tightly a cluster is packed (lower = better):
```text
within-cluster SSE  =  Σ(k) Σ(x ∈ C_k) ‖x − c_k‖²
```

**Separation** — how far clusters are from each other (higher = better):
```text
between-cluster SS  =  Σ(k) |C_k| · ‖c_k − c‖²
```

**The silhouette coefficient combines both**, per point:
```text
a = mean distance to points in its own cluster
b = mean distance to points in the nearest other cluster
s = (b − a)/max(a,b)          range −1 … +1
```
Average `s` over all points: **above 0.5 is a reasonable structure, near 0 is overlapping, negative means the point is in the wrong cluster.**

**The identity that ties cohesion to K:** `Total SS = within-cluster SS + between-cluster SS`. Minimising within-cluster SSE is the same as maximising between-cluster separation — **this is precisely what K-Means does** (Topic 5).

**External evaluation** (when labels happen to exist): purity, Rand index, adjusted Rand index, NMI — used to *validate* a clustering against a known partition, never to produce one.

---

## 8. Advantages of clustering (your page)

- **No need for labelled data** — the expensive part of supervised learning disappears.
- **Helps discover unknown patterns** that no one thought to label.
- **Useful for large datasets** (K-Means is linear in n).
- **Supports decision-making** through segmentation and summarisation.
- **Widely applicable across domains** — retail, biology, security, text, images.

## 9. Limitations of clustering (your page)

| Limitation | Why it matters |
|---|---|
| **Choice of algorithm affects results** | K-Means, DBSCAN and hierarchical can give three different answers on one dataset |
| **Sensitive to noise and outliers** | centroids are dragged, distances distorted (K-Medoids and DBSCAN mitigate) |
| **Difficult to determine the optimal number of clusters** | the elbow and silhouette are heuristics, not proofs |
| **Interpretation may be subjective** | a cluster is only useful if a human can name and act on it |
| **Results depend on scaling and distance measure** | pre-processing decisions become clustering decisions |

---

## 10. The five clustering paradigms (the map for the rest of the unit)

| Paradigm | Idea | Algorithms | Strength | Weakness |
|---|---|---|---|---|
| **Partitional** | split into K groups, optimise a criterion | **K-Means**, **K-Medoids/PAM**, CLARA | fast, simple | needs K, spherical clusters |
| **Hierarchical** | build a nested tree | **agglomerative (single/complete/average)**, divisive | no K needed, dendrogram | O(n²) memory, irreversible |
| **Density-based** | grow regions of high density | **DBSCAN**, OPTICS, HDBSCAN | arbitrary shapes, finds noise | ε and MinPts sensitive |
| **Grid-based** | quantise space into cells | STING, CLIQUE | fast on large/spatial data | loses fine detail |
| **Model-based** | fit a statistical model | Gaussian mixture (EM), SOM | soft assignments, principled | assumptions, local optima |

**This table is the answer to "categorize the different clustering approaches" — the CO5 verb itself.** The four algorithms this unit examines sit in the first three rows.

---

## 11. Real-world applications (your page)

**Market basket analysis, social-network analysis, recommendation systems, web-usage mining, fraud detection, healthcare diagnostics** — plus image segmentation, document organisation and gene-expression analysis from §6.

---

## 12. Summary

Clustering is **unsupervised** grouping of data objects so that **within-cluster similarity is high and between-cluster similarity is low**, measured by distance, density or connectivity, and requiring **no predefined labels** — the essential difference from classification, which is supervised and label-driven. Its characteristics are being **unsupervised, data-driven, exploratory, flexible and application-dependent**, and its process runs **collection → pre-processing → feature selection → similarity → algorithm → evaluation → interpretation**, where steps 2–3 are exactly the Unit 2 pre-processing that scaling-sensitive methods demand. It is needed for **exploration, summarisation, pattern discovery, customer segmentation, anomaly detection, text mining, image analysis and bioinformatics**, and its quality is judged by **cohesion and separation** — with `Total SS = within + between`, so minimising within-cluster SSE (what K-Means does) is the same as maximising separation. Its limitations — **algorithm dependence, noise sensitivity, uncertain K, subjective interpretation** — are why the unit then examines five paradigms: **partitional, hierarchical, density-based, grid-based and model-based**.

---

**Next:** [Topic 13 — Types of Data in Cluster Analysis](13-types-of-data.md)
