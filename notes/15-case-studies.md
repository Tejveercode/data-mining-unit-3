# Topic 15 — Real-Time Case Studies for Classification & Clustering

> **LMS page:** *Real-Time Case Studies for Classification & Clustering* · **CO5**.
> This note closes the unit by showing where everything in notes 01–14 is actually used — and what each technique costs in production.

---

## 1. The frame

**Classification and clustering are widely used data mining techniques, applied across industries to solve real-world problems.**

- **Classification focuses on assigning predefined labels** to data objects.
- **Clustering groups similar data objects without predefined labels.**

**Real-time case studies help understand how these techniques are used practically to support decision-making and automation.**

**The unit's two halves map to two business postures:**

| | **Classification** | **Clustering** |
|---|---|---|
| Business question | *"Is this one of X?"* | *"What kinds of things are these?"* |
| Data needed | historic labelled outcomes | current unlabelled data |
| Deployment | **inside the transaction path** (real time) | **in analysis cycles** (batch/periodic) |
| Cost of being wrong | a wrong decision on one record | a wrong segment strategy, discovered late |
| Typical refresh | continuous or daily | weekly/monthly |

**That asymmetry is the practical difference:** classifiers gate decisions, so they must be fast and auditable; clusterings inform strategy, so they must be interpretable and stable.

---

## 2. Classification case studies

### 2.1 Email spam detection

**Emails are classified into spam and non-spam based on features such as keywords, sender information and message structure.** A model is trained on **labelled email data**; when a new email arrives it predicts spam or legitimate, **filtering unwanted messages automatically**.

**Under the hood:** text → token counts → **Naïve Bayes** (Topic 3) is the classic choice because it is fast, handles high dimensionality and updates incrementally. The independence assumption is nearly harmless here — a word's presence is roughly independent of another's given the topic.

**Which metric matters:** **precision** (Topic 10). A false positive deletes a real email — catastrophic and invisible to the sender. Spam that slips through is annoying; a lost invoice is not. Hence the industry convention of blocking only at high confidence and quarantining the rest.

**Worked operating point** (the confusion matrix from Topic 10, `TP=8, FN=2, FP=4, TN=6`): **precision 0.6667**, **recall 0.8000**, **F1 0.7273**. For a spam filter that precision would be unacceptable — 4 false positives per 20 emails — so the threshold would be raised, trading recall for precision until FP ≈ 0.

### 2.2 Medical diagnosis system

**Patient data such as symptoms, test results and medical history are input attributes; the model predicts whether a patient belongs to a disease class or a healthy class.** This **assists doctors in early diagnosis and decision support**.

**Algorithms:** decision trees (Topic 2) where **the rule must be explainable to a clinician and auditable by a regulator**, Naïve Bayes where probabilistic reasoning and priors matter, kNN where similar past patients are the best evidence.

**Which metric matters:** **recall** — a missed disease is dangerous, while a false alarm leads to a follow-up test. This is why screening models are tuned to high sensitivity and the *specificity* is reported alongside.

**The governance point worth writing:** the model **assists**, it does not diagnose. A prediction without the rule that produced it (decision tree) or the evidence behind it (the k nearest similar cases) will not be trusted by a clinician — interpretability is a functional requirement, not a nicety.

### 2.3 Credit approval and risk assessment

**Banks decide whether a loan application should be approved or rejected.** Attributes include **income, credit history, employment status and existing debts**; the model classifies applicants into **low-risk or high-risk**, **reducing financial losses and improving decision consistency**.

**Why consistency is the real benefit:** a human loan officer's decisions drift with mood, workload and bias. A model applies the same policy to every application — which is also a legal requirement in many jurisdictions (adverse action must be explainable).

**Which metric matters:** both, weighted by the **expected monetary loss** of each error type. A false "approve" costs the defaulted amount; a false "reject" costs the margin plus a customer. This is the textbook case for a **cost-sensitive** threshold rather than 0.5.

**Fairness caveat:** if `postcode` or `gender` correlates with repayment, the model will use it — high accuracy, illegal outcome. Excluding protected attributes is not enough; their proxies must be handled.

### 2.4 Customer churn prediction

**Telecom companies predict churn** from **usage patterns, service complaints and payment behaviour**, enabling **preventive actions such as discounts or improved services**.

**This is the highest-ROI classification in most service businesses**, because retention is cheaper than acquisition.

**Worked shape of the problem:**
- Target: churn in next 90 days (binary → **classification**, per Topic 1).
- Typical imbalance: 5–10 % churners, so **accuracy is useless** (predicting "nobody churns" scores 92 %). Report **recall, precision and AUC**; the AUC computation in Topic 10 (worked value **0.7778**) is exactly this evaluation.
- The decision is not the label but the **action**: a `P(churn) = 0.55` customer gets an offer, `0.15` gets nothing. **The probability, not the label, drives the business** — the point made in Topic 1 §6.

### 2.5 Face recognition systems

**Systems classify images into known identities.** Features extracted from facial images are compared against trained models to assign a person's identity, used in **security, surveillance and authentication**.

**The distinguishing feature of this case:** the dimensionality is enormous (an image is `10⁵`–`10⁶` numbers) and the classes are many, with **very few examples per class**. That is why the pipeline leans on **feature extraction** (Unit 2 dimensional reduction — PCA, embeddings) far more than on the classifier: **kNN in a reduced feature space** is the canonical structure.

**Which metric matters:** the false-positive rate at a fixed false-negative rate (the ROC operating point), plus **per-demographic error analysis** — the widely documented failure mode of these systems is that average accuracy is fine and subgroup accuracy is not.

---

## 3. Clustering case studies

### 3.1 Customer segmentation in retail

**Customers are grouped by purchasing behaviour, spending habits and demographics**; members of a cluster share similar buying patterns, enabling **targeted marketing and personalised offers**.

**Method:** **K-Means** (Topic 5–6) on **normalised** spend/frequency/recency features. **Why K-Means:** the features are numeric and ratio-scale (Topic 13), segments are expected to be roughly spherical and comparable in size, and *bright-line centroids are what a marketing team can actually action* ("the high-spend low-frequency group").

**Two caveats that decide whether the project succeeds:**
1. **K is a business decision, not a mathematical one.** The elbow on a synthetic dataset fell `100.75 → 51.47 → 14.33 → 8.67 → 3.67`, bending at **K = 3** — but a retailer who can run three campaigns should choose K = 3 even if the SSE says 5.
2. **Segments must be stable.** If re-running with a different random seed moves 30 % of customers between segments, no campaign can be evaluated. Use **k-means++ and many restarts** (Topic 5 §8), and compare assignments across runs.

### 3.2 Market basket analysis

**Clustering groups transactions or customers by item-purchase similarity**, helping retailers **understand shopping patterns, improve store layouts and recommend related products**.

**Two legitimate framings:**
- **as clustering** — Jaccard distance between baskets (Topic 13 §4: `a/(a+b+c)`), then hierarchical clustering, because the number of "shopping missions" is unknown;
- **as association rules** — Unit 2's Apriori/FP-Growth, which answers the sharper question *"given milk, what else?"*

**The distinction worth stating in an exam:** clustering says **"these baskets resemble each other"**; association rules say **"this item implies that one, with support and confidence"**. The rules are actionable at the shelf; the clusters are actionable at the store-format level.

### 3.3 Image segmentation

**Clustering segments an image into regions with similar pixel characteristics** such as colour or intensity, used in **medical imaging, satellite analysis and object detection**.

**Method:** K-Means on pixel colour values — literally the vector-quantisation reading of K-Means (Topic 5), where each pixel is replaced by its centroid colour. **Compression is a by-product:** 16 clusters = 4 bits per pixel.

**Which algorithm instead, when?** **DBSCAN** (Topic 9) when regions are irregular and the background should be **noise** rather than a cluster; **hierarchical** when you want segmentations at several granularities from one run.

### 3.4 Document and news article clustering

**News portals and search engines group articles or documents by topic**, improving **content organisation, recommendation and retrieval efficiency**.

**Method:** TF-IDF vectors → **cosine similarity** (Topic 13 §11: the worked pair scored **0.9245**) → spherical k-means or hierarchical clustering. **Cosine is mandatory here** — Euclidean distance would make a long article dissimilar to a short one on the same topic.

**The evaluation catch:** there is no "correct" topic set, so quality is judged by **cohesion/separation** and by whether a human can name each cluster (Topic 12 §7).

### 3.5 Social network community detection

**Clustering identifies communities of users with similar interests or interaction patterns**, helping platforms **recommend friends, groups and targeted content**.

**Method:** the object is a **graph**, not a point — so the "distance" is connectivity or modularity, and the natural algorithms are graph-specific (Louvain, spectral). **Single linkage** (Topic 14) is the closest classical analogue: it merges whatever is connected, which is precisely the community intuition **and** precisely its weakness (one cross-community edge chains two communities together).

### 3.6 Anomaly detection in network security

**Normal traffic forms dense clusters; unusual activity appears as outliers** — useful for **detecting cyber-attacks, fraud and intrusions**.

**Method:** **DBSCAN** (Topic 9), because it labels noise explicitly. In the worked example, points formed two dense clusters and `(20,20)` came out as **noise** with `ε = 1.5, MinPts = 4` — that label *is* the alert.

**Why clustering rather than classification here:** attacks are **novel**; there are no labels for next year's attack. **Unsupervised detection generalises to unseen behaviour** — the one advantage that no classifier has.

**Operational reality:** the output is ranked anomaly scores, not verdicts. Alert volume is the binding constraint, so the threshold is set by how many investigations the security team can absorb per day.

---

## 4. Classification vs clustering in real-time systems (your page's comparison)

**Classification requires labelled data and is used for prediction and decision-making. Clustering does not require labelled data and is used for exploration and pattern discovery.**

**Classification systems are often deployed in real-time decision engines, while clustering systems are commonly used in analysis and strategy planning.**

| | **Classification** | **Clustering** |
|---|---|---|
| Data requirement | labelled history | current data, no labels |
| Latency | must answer per request (ms) | can run overnight |
| Failure visible? | **immediately** (wrong decision) | **slowly** (bad strategy) |
| Update cadence | retrain on drift | re-cluster periodically |
| Explainability demand | **high** (regulatory, user-facing) | moderate (must be nameable) |
| Typical owner | operations / product | analytics / strategy |

**The lifecycle pairing that actually happens in industry:** cluster first to **discover** the segments, then **label** them by inspection, then train a classifier to **assign new customers to those segments in real time**. Clustering finds the structure; classification operationalises it. **That two-step is the single most useful sentence in this note**, and it is why both halves of this unit exist in one course.

---

## 5. Benefits of data mining in real-time applications (your page)

**Data mining techniques automate decision-making, improve accuracy, reduce human effort and handle large volumes of data efficiently. They enable organisations to gain insights, improve customer experience and optimise operations.**

In production terms, that means four concrete gains:

| Gain | Mechanism |
|---|---|
| **Automation** | the decision no longer waits for a human — milliseconds instead of hours |
| **Consistency** | the same policy applies to every record, removing drift and bias |
| **Scale** | millions of records processed per hour, impossible manually |
| **Learning** | the model improves as labelled outcomes accumulate |

**And four costs that any honest answer should include:**

| Cost | What it looks like |
|---|---|
| **Data quality debt** | garbage in, confidently wrong out — the whole of Unit 2 exists because of this |
| **Drift** | customer behaviour shifts; a model trained on last year silently decays |
| **Feedback loops** | acting on predictions changes the data the next model learns from (offering a discount to likely churners makes them look retained) |
| **Accountability** | someone must own a wrong automated decision |

---

## 6. A single worked case, end to end (exam-ready sketch)

**Problem:** a telecom wants to reduce churn. **Deliverable:** decide *who* to call.

```text
1. FRAME        target = churn in 90 days → binary → CLASSIFICATION (Topic 1)
2. PREPARE      clean missing usage records, normalise minutes/spend (Unit 2, Topic 13)
3. EXPLORE      K-Means on usage features, K = 3, elbow at 14.33 SSE (Topics 5-6)
                → discover "low-usage", "heavy-usage", "contract-expiring" groups
4. MODEL        Naïve Bayes or decision tree per group (note 3 / note 2)
5. EVALUATE     confusion matrix TP=8, FN=2, FP=4, TN=6
                precision 0.6667, recall 0.8000, F1 0.7273, AUC ~0.78 (Topic 10)
6. OPERATE      score nightly, act on P(churn) not on the label
                call list = top N by probability, N set by call-centre capacity
7. MONITOR      track drift, re-fit quarterly, audit subgroup error rates
```

**Why this answer scores well:** it uses the correct technique for the target type (step 1), does not skip pre-processing (2), uses clustering for discovery and classification for decision (3–4), reports metrics appropriate to imbalance (5), and converts the model into an operation with a capacity constraint (6).

---

## 7. Summary

Classification is deployed where **labelled history exists and a decision must be made per record now** — spam filtering (precision-critical), medical diagnosis (recall-critical, explainability mandatory), credit scoring (cost-weighted, legally auditable), churn prediction (probability drives the action) and face recognition (feature extraction dominates). Clustering is deployed where **structure must be discovered** — retail segmentation with K-Means on normalised ratio data, basket similarity with Jaccard, pixel segmentation by vector quantisation, document grouping by cosine, community detection on graphs and anomaly detection with DBSCAN's noise label. The practical difference is posture: **classifiers gate transactions and must be fast, stable and explainable; clusterings inform strategy and must be interpretable and reproducible.** The industrial pattern that ties the unit together is **cluster to discover, label by inspection, then classify to assign** — exploration followed by automation, with pre-processing, evaluation and monitoring as the non-negotiable steps around both.

---

**End of notes.** Continue to the [revision cheat sheet](../exam/cheat-sheet.md) and the [question bank](../exam/question-bank.md).
