# Topic 3 — Bayesian Classification: Naïve Bayes

> **LMS page:** *Bayesian Classification – Naïve Bayes* · **CO4**.
> The page's illustration is an image; the worked computations below are the standard ones and **every figure has been verified by running the classifier**.

---

## 1. What it is

**Bayesian classification is a supervised learning approach based on probability theory.** It uses **Bayes' theorem** to predict the class of a data object by calculating the probability that the object belongs to a particular class **given its attribute values**.

Among Bayesian classifiers, **Naïve Bayes** is one of the simplest and most widely used techniques in data mining and machine learning — popular because of its **simplicity, efficiency and good performance on large datasets**.

---

## 2. The basic idea

**Compute the probability of each possible class for a given data object, then assign the class with the highest probability.**

That probability is the **posterior probability**, obtained by combining **prior knowledge** with **observed data**. Formally, for attributes `X = (x₁, x₂, …, xₙ)` and classes `C₁ … Cₘ`:

```text
predict class Cᵢ that maximises  P(Cᵢ | X)
```

This decision rule is called **maximum a posteriori (MAP) estimation**.

---

## 3. Bayes' theorem — the engine

```text
P(C | X) = P(X | C) · P(C) / P(X)
```

| Term | Name | Meaning |
|---|---|---|
| `P(C)` | **prior** | probability of the class **before** seeing any attributes |
| `P(X \| C)` | **likelihood** | probability of observing these attribute values **if** the class is C |
| `P(X)` | **evidence** | probability of observing these attribute values at all |
| `P(C \| X)` | **posterior** | probability of the class **after** seeing the attributes |

**The evidence `P(X)` is the same for every class** and plays no part in the comparison — so in practice we compute only `P(X | C) · P(C)` for each class and compare. That simplification is worth stating explicitly; it is where most marks are lost.

### Prior probability

The probability of a class **before observing any attribute values**, estimated from the training data as the **proportion of objects belonging to that class**:

```text
P(Cᵢ) = |records of class Cᵢ| / |total records|
```

Priors capture the **general distribution of classes** in the dataset — and they matter: a rare class needs much stronger evidence to win.

### Posterior probability

The probability that an object belongs to a class **after considering its attribute values**. **The class with the highest posterior is the predicted class.**

---

## 4. The Naïve Bayes classifier and its "naïve" assumption

Naïve Bayes is a probabilistic classifier based on Bayes' theorem **with a strong assumption of conditional independence among attributes**: the value of one attribute is **independent of the values of the other attributes, given the class label**.

```text
P(X | C) = P(x₁ | C) · P(x₂ | C) · … · P(xₙ | C) = Π P(xᵢ | C)
```

**Why the assumption is needed:** without it, estimating `P(x₁,…,xₙ | C)` requires a probability for **every combination** of attribute values — with 10 binary attributes that is 1,024 combinations per class, and with 30 attributes it is a billion. Independence reduces the estimate to **n one-dimensional counts**, so the model is **scalable to large, high-dimensional datasets**.

**Why it still works even when the assumption is false:** classification only needs the **ranking** of the classes to be right, not the probabilities themselves. Correlated attributes double-count evidence, which distorts the magnitudes but often leaves the argmax intact. *This is the standard answer to "why does Naïve Bayes perform surprisingly well despite an unrealistic assumption?"*

---

## 5. Working principle

**Training phase:**
1. Compute the **prior** `P(Cᵢ)` for each class.
2. Compute the **conditional probability** `P(xⱼ | Cᵢ)` for every attribute value and class.

**Classification phase:**
3. For the new object, compute `P(X | Cᵢ) · P(Cᵢ)` for each class.
4. **Assign the class with the maximum value.**

No iterative optimisation, no gradient descent — one pass over the data. That is the source of its speed.

---

## 6. Worked example — the 14-record dataset

Using the same `buys_computer` table as Topic 2 (9 yes, 5 no). **Classify the new object:**

```text
X = (age = youth, income = medium, student = yes, credit_rating = fair)
```

### Step 1 — Priors

```text
P(buys = yes) = 9/14 = 0.6429
P(buys = no)  = 5/14 = 0.3571
```

### Step 2 — Conditional probabilities

**For class `yes`** (9 records: #3,4,5,7,9,10,11,12,13):

| Attribute value | Count in yes | Probability |
|---|---|---|
| age = youth | 2 | 2/9 = 0.2222 |
| income = medium | 4 | 4/9 = 0.4444 |
| student = yes | 6 | 6/9 = 0.6667 |
| credit = fair | 6 | 6/9 = 0.6667 |

**For class `no`** (5 records: #1,2,6,8,14):

| Attribute value | Count in no | Probability |
|---|---|---|
| age = youth | 3 | 3/5 = 0.6000 |
| income = medium | 2 | 2/5 = 0.4000 |
| student = yes | 1 | 1/5 = 0.2000 |
| credit = fair | 2 | 2/5 = 0.4000 |

### Step 3 — Multiply

```text
P(X|yes)·P(yes) = 0.6429 × 0.2222 × 0.4444 × 0.6667 × 0.6667 = 0.028219
P(X|no) ·P(no)  = 0.3571 × 0.6000 × 0.4000 × 0.2000 × 0.4000 = 0.006857
```

### Step 4 — Compare and decide

`0.028219 > 0.006857` → **predict `buys_computer = yes`**.

*For completeness the true posteriors (dividing by the evidence) are 0.804 and 0.196 — but the comparison alone is enough, and stating that saves time and shows understanding.*

**Reading the result like an analyst:** the decisive factor is `student = yes` (6/9 among buyers vs 1/5 among non-buyers), which outweighs the fact that `age = youth` slightly favours *no*.

---

## 7. The zero-probability problem, and Laplace smoothing

**If an attribute value never appears with a class in the training data, its conditional probability is zero — and because the terms are multiplied, the whole product becomes zero.** One unseen combination can therefore veto a class entirely, no matter how strong the other evidence.

**Worked demonstration.** Classify `X = (age = middle, income = medium, student = no, credit = fair)`:

```text
yes: 9/14 × (4/9) × (4/9) × (3/9) × (6/9) = 0.028219
no : 5/14 × (0/5) × (2/5) × (4/5) × (2/5) = 0.000000     ← age = middle never occurs among "no"
```

Without smoothing, `no` is eliminated by a single unseen value and the answer is **yes**.

**Laplace (add-one) smoothing** adds a small count to every attribute-value cell:

```text
P(xᵢ | C) = (count(xᵢ, C) + 1) / (count(C) + |values of attribute i|)
P(C)      = (count(C) + 1) / (|total| + |classes|)
```

**Same object, smoothed:**

| Term | yes | no |
|---|---|---|
| prior | (9+1)/(14+2) = 10/16 = 0.6250 | (5+1)/(14+2) = 6/16 = 0.3750 |
| age = middle | (4+1)/(9+3) = 0.4167 | **(0+1)/(5+3) = 0.1250** |
| income = medium | (4+1)/(9+3) = 0.4167 | (2+1)/(5+3) = 0.3750 |
| student = no | (3+1)/(9+2) = 0.3636 | (4+1)/(5+2) = 0.7143 |
| credit = fair | (6+1)/(9+2) = 0.6364 | (2+1)/(5+2) = 0.4286 |
| **product** | **0.025109** | **0.005381** |

**The prediction does not change here** (yes still wins, now 0.0251 vs 0.0054), but note *how much closer* the two got: smoothing turned a hard zero into a small probability, which is exactly its purpose — **it prevents one missing observation from dominating the model**.

**Generalised (Lidstone / m-estimate):**

```text
P(xᵢ | C) = (count(xᵢ, C) + m·p) / (count(C) + m)
```

with `p` a prior probability for the value and `m` a tunable strength. `m = |values|` and `p = 1/|values|` recovers Laplace.

---

## 8. Handling continuous attributes — Gaussian Naïve Bayes

Continuous attributes are handled by **assuming a normal distribution for the attribute within each class**, then computing the probability density from that class's **mean and standard deviation**:

```text
P(xᵢ | C) = 1/(σ√(2π)) · exp( −(xᵢ − μ)² / (2σ²) )
```

where `μ` and `σ` are estimated **from the training records of class C only**.

**Worked example.** Predict the class of a person **174 cm tall**, with training heights:

- class **yes** (5 records): 168, 170, 172, 174, 176 → `μ = 172.00`, `σ = 2.8284`
- class **no** (3 records): 160, 164, 166 → `μ = 163.33`, `σ = 2.4944`
- priors: `P(yes) = 5/8 = 0.625`, `P(no) = 3/8 = 0.375`

```text
P(174|yes) = 1/(2.8284·√2π) · exp(−(174−172)²/(2·8))     = 0.1410 × 0.7788 = 0.109848
P(174|no)  = 1/(2.4944·√2π) · exp(−(174−163.33)²/(2·6.222)) = 0.1600 × 0.00011 ≈ 0.000017

P(174|yes)·P(yes) = 0.625 × 0.109848 = 0.068655
P(174|no) ·P(no)  = 0.375 × 0.000017 = 0.0000064
```

→ **class = yes**, with overwhelming confidence: 174 is close to the yes-class mean and more than four standard deviations from the no-class mean.

*Note the units:* this is a **density**, not a probability — it can exceed 1 for a very small σ. That is harmless, because only the comparison between classes matters.

---

## 9. Types of Naïve Bayes classifiers (your page's point)

| Variant | Data type | Likelihood model |
|---|---|---|
| **Gaussian** | continuous | normal distribution per class |
| **Multinomial** | counts (word frequencies) | multinomial distribution |
| **Bernoulli** | binary presence/absence | Bernoulli distribution |
| **Categorical** | nominal categories | frequency counts |

These variations **allow Naïve Bayes to handle different kinds of datasets** — the choice follows the data, not the algorithm's preference.

---

## 10. Practical implementation notes (worth marks)

- **Work in log space.** Multiplying many small probabilities underflows to zero in floating point; sum the logs instead — the argmax is unchanged.
  ```text
  log P(C|X) ∝ log P(C) + Σ log P(xᵢ|C)
  ```
- **Ignore the evidence term** `P(X)` — identical across classes.
- **Attribute independence is per class**, so a correlated pair (e.g. `income` and `occupation`) effectively counts twice; feature selection helps.
- **Class imbalance** flows straight into the prior; a 99:1 split makes the majority class hard to beat — use class priors or resampling.

---

## 11. Advantages (your page)

- **Simple to implement and computationally efficient** — one pass to train.
- **Works well with high-dimensional data** (text with 10,000 terms is routine).
- **Effective even with a small amount of training data.**
- **Robust to irrelevant features** (they contribute nearly equal factors to all classes).
- **Scales well to large datasets**; supports incremental/online updates.
- Handles **missing values naturally** (skip the term, or use the marginal).

## 12. Limitations (your page)

- The **strong independence assumption may not hold** in real data.
- **May perform poorly when attributes are highly correlated.**
- **Probability estimates may be inaccurate** if training data is insufficient or biased — the ranking is usually better than the calibration.
- Cannot learn **interactions** between attributes (unless you engineer them).
- **Zero-frequency problem** without smoothing.

---

## 13. Naïve Bayes vs decision trees (your page's comparison, extended)

| Aspect | **Naïve Bayes** | **Decision tree** |
|---|---|---|
| Model type | **probabilistic** | **rule-based / tree** |
| Interpretability | moderate (probabilities, per-attribute contributions) | **high** (rules, visual) |
| Training speed | **very fast** | fast, but split search costs more |
| Attribute interactions | **cannot capture** | **captures naturally** |
| Correlated attributes | **harmful** (double counting) | tolerated (splits choose among them) |
| Small data | **works** | can overfit |
| Missing values | handled natively | needs a strategy |
| Continuous attributes | Gaussian assumption | threshold search |

*The exam one-liner: Naïve Bayes is faster and simpler and builds a probabilistic model; decision trees build rule-based models that can capture complex attribute interactions but overfit more easily.*

---

## 14. Applications

**Text classification, spam detection, sentiment analysis, document categorisation, medical diagnosis, recommendation systems** — *particularly effective in applications involving large volumes of textual data*, where the independence assumption is least harmful (a word's presence is roughly independent of another's, conditional on topic) and dimensionality is highest.

---

## 15. Summary

Bayesian classification applies **Bayes' theorem** to compute the **posterior** `P(C|X) ∝ P(X|C)·P(C)` for each class and predicts the class with the **highest posterior**. The **prior** comes from class frequencies; the likelihood is simplified by the **conditional independence assumption** into a product of per-attribute probabilities, which is what makes the method fast and scalable. On the 14-record dataset, `X = (youth, medium, yes, fair)` gives **0.0282 for yes vs 0.0069 for no** → yes. Unseen attribute values cause the **zero-probability problem**, fixed by **Laplace smoothing**; continuous attributes use **Gaussian** likelihoods from each class's mean and standard deviation. Its weaknesses — the independence assumption and poor probability calibration — are exactly why it is used for high-dimensional text and why decision trees remain the choice when attributes interact.

---

**Next:** [Topic 4 — K-Nearest Neighbor Classification (kNN)](04-knn.md)
