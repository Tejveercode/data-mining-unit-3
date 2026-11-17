# Topic 2 — Decision Tree Induction

> **LMS page:** *Decision Tree Induction* · **CO5** tag on the page, content belongs to **CO4**.
> The page's worked illustration is an image; the full computation below is supplied from the standard 14-record *buys_computer* dataset and **every figure has been verified by running the algorithm**.

---

## 1. What it is

**Decision Tree Induction is a supervised learning technique used for classification and prediction.** It constructs a **tree-structured model** that represents decisions and their possible consequences, learned from a training dataset of **input attributes** and a **target attribute**.

Decision trees are popular because they are **easy to understand, interpret and visualise** — suitable for both technical and non-technical users. A tree can be read aloud as a set of **if–then rules**, which is why banks and hospitals still prefer them to black-box models.

---

## 2. The basic idea

**Recursively partition the dataset into smaller subsets based on attribute tests.** At each step the algorithm **selects the best attribute** — the one that separates the data into the **most homogeneous subsets** with respect to the target class. The process continues until the data is **sufficiently pure** or no meaningful split remains.

This is a **greedy, top-down, divide-and-conquer** strategy: greedy because each split is chosen to be best *right now*, without lookahead; recursive because each subset is then handled by the same procedure.

---

## 3. Structure of a decision tree

| Part | Meaning |
|---|---|
| **Root node** | the topmost node — the first decision, on the most important attribute |
| **Internal node** | a **test on an attribute** (e.g. `age = ?`) |
| **Branch** | an **outcome** of that test (e.g. `youth`, `middle`, `senior`) |
| **Leaf node** | a **class label** (classification) or a **predicted value** (regression tree) |

A path from root to leaf is one **if–then rule**: `IF age = youth AND student = yes THEN buys_computer = yes`.

---

## 4. Attribute selection — the heart of the algorithm

The goal is to choose the attribute that best splits the data into **subsets that are as pure as possible**. Four measures are used; your page lists all four.

### 4.1 Entropy

Entropy measures **impurity or uncertainty**. A dataset with objects from **only one class has zero entropy**; an **evenly distributed** dataset has **high entropy** (maximum = log₂ of the number of classes).

```text
Entropy(S) = − Σ pᵢ log₂ pᵢ          pᵢ = proportion of class i in S
```

For two classes this is:
```text
Entropy(S) = − p⊕ log₂ p⊕ − p⊖ log₂ p⊖
```

*Lower entropy = higher purity.* Worked values you should recognise instantly:

| Class split | Entropy |
|---|---|
| 4 yes, 0 no | **0** (pure) |
| 3 yes, 1 no | 0.8113 |
| 2 yes, 2 no | **1** (maximum for two classes) |
| 3 yes, 2 no | 0.9710 |

### 4.2 Information gain

Information gain measures the **reduction in entropy** achieved by splitting on an attribute. **The attribute with the highest information gain is chosen.**

```text
Gain(S, A) = Entropy(S) − Σ (|Sᵥ|/|S|) · Entropy(Sᵥ)
                          v ∈ values(A)
```

Information gain **favours attributes that provide the most information about the class label** — but it is **biased toward attributes with many distinct values** (an ID-like attribute has a different value in every row, so it splits perfectly and appears to have maximum gain). That bias is exactly what gain ratio fixes.

### 4.3 Gain ratio

An **extension of information gain that reduces the bias toward attributes with many distinct values**. It **normalises information gain by the intrinsic information of the split**:

```text
SplitInfo(S, A) = − Σ (|Sᵥ|/|S|) · log₂(|Sᵥ|/|S|)
GainRatio(S, A) = Gain(S, A) / SplitInfo(S, A)
```

*SplitInfo is simply the entropy of the attribute's own value distribution — it grows as the attribute has more, more-evenly-used values, so dividing by it penalises the bias.*

Gain ratio is **commonly used in C4.5**. (Practical detail worth a mark: C4.5 first filters out attributes whose gain is below average, then applies gain ratio — otherwise it can over-penalise a genuinely good binary split.)

### 4.4 Gini index

The Gini index measures the **probability of incorrectly classifying a randomly chosen data object** if it were labelled by the class distribution of the node:

```text
Gini(S) = 1 − Σ pᵢ²
Gini_split(S, A) = Σ (|Sᵥ|/|S|) · Gini(Sᵥ)
```

**Lower Gini = purer subsets**, so the attribute with the **lowest weighted Gini** is chosen. It is **widely used in CART** (Classification and Regression Trees) — and because CART handles numeric targets too, the same measure serves **prediction** as regression trees (variance reduction).

---

## 5. Full worked example — the 14-record dataset

**Training data.** Attribute `age` ∈ {youth, middle, senior}, `income` ∈ {high, medium, low}, `student` ∈ {yes, no}, `credit_rating` ∈ {fair, excellent}; class `buys_computer` ∈ {yes, no}.

| # | age | income | student | credit_rating | buys_computer |
|---|---|---|---|---|---|
| 1 | youth | high | no | fair | **no** |
| 2 | youth | high | no | excellent | **no** |
| 3 | middle | high | no | fair | **yes** |
| 4 | senior | medium | no | fair | **yes** |
| 5 | senior | low | yes | fair | **yes** |
| 6 | senior | low | yes | excellent | **no** |
| 7 | middle | low | yes | excellent | **yes** |
| 8 | youth | medium | no | fair | **no** |
| 9 | youth | low | yes | fair | **yes** |
| 10 | senior | medium | yes | fair | **yes** |
| 11 | youth | medium | yes | excellent | **yes** |
| 12 | middle | medium | no | excellent | **yes** |
| 13 | middle | high | yes | fair | **yes** |
| 14 | senior | medium | no | excellent | **no** |

### Step 1 — Entropy of the whole set

`S` has **9 yes, 5 no**:

```text
Entropy(S) = −(9/14)log₂(9/14) − (5/14)log₂(5/14)
           = −(0.6429)(−0.6374) − (0.3571)(−1.4855)
           = 0.4098 + 0.5305 = 0.9403
```

### Step 2 — Information gain for each attribute

**`age`** — three subsets:

| age | records | yes | no | Entropy |
|---|---|---|---|---|
| youth | 5 | 2 | 3 | **0.9710** |
| middle | 4 | 4 | 0 | **0.0000** |
| senior | 5 | 3 | 2 | **0.9710** |

```text
E(age) = (5/14)(0.9710) + (4/14)(0) + (5/14)(0.9710) = 0.3468 + 0 + 0.3468 = 0.6936
Gain(age) = 0.9403 − 0.6936 = 0.2467
```

**`income`**:

| income | records | yes | no | Entropy |
|---|---|---|---|---|
| high | 4 | 2 | 2 | 1.0000 |
| medium | 6 | 4 | 2 | 0.9183 |
| low | 4 | 3 | 1 | 0.8113 |

```text
E(income) = (4/14)(1.0000) + (6/14)(0.9183) + (4/14)(0.8113) = 0.2857 + 0.3936 + 0.2318 = 0.9111
Gain(income) = 0.9403 − 0.9111 = 0.0292
```

**`student`**:

| student | records | yes | no | Entropy |
|---|---|---|---|---|
| yes | 7 | 6 | 1 | 0.5917 |
| no | 7 | 3 | 4 | 0.9852 |

```text
E(student) = (7/14)(0.5917) + (7/14)(0.9852) = 0.2959 + 0.4926 = 0.7885
Gain(student) = 0.9403 − 0.7885 = 0.1518
```

**`credit_rating`**:

| credit_rating | records | yes | no | Entropy |
|---|---|---|---|---|
| fair | 8 | 6 | 2 | 0.8113 |
| excellent | 6 | 3 | 3 | 1.0000 |

```text
E(credit) = (8/14)(0.8113) + (6/14)(1.0000) = 0.4636 + 0.4286 = 0.8922
Gain(credit) = 0.9403 − 0.8922 = 0.0481
```

### Step 3 — Compare

| Attribute | Gain | Rank |
|---|---|---|
| **age** | **0.2467** | **1 ← chosen as root** |
| student | 0.1518 | 2 |
| credit_rating | 0.0481 | 3 |
| income | 0.0292 | 4 |

**`age` gives the highest information gain, so it becomes the root node.**

### Step 4 — Gain ratio for the same split (the C4.5 check)

```text
SplitInfo(age) = −(5/14)log₂(5/14) − (4/14)log₂(4/14) − (5/14)log₂(5/14)
               = 0.5305 + 0.5164 + 0.5305 = 1.5774
GainRatio(age) = 0.2467 / 1.5774 = 0.1564
```

### Step 5 — The same split under Gini (the CART check)

```text
Gini(S) = 1 − (9/14)² − (5/14)² = 1 − 0.4133 − 0.1276 = 0.4592     (root impurity)

Gini_split(age)     = (4/14)(0)      + (5/14)(0.4800) + (5/14)(0.4800) = 0.3429   ← lowest, so still the root
Gini_split(student) = (7/14)(0.4898) + (7/14)(0.2449)               = 0.3673
Gini_split(credit)  = (8/14)(0.3750) + (6/14)(0.5000)               = 0.4286
Gini_split(income)  = (4/14)(0.5000) + (6/14)(0.4444) + (4/14)(0.3750) = 0.4405
```

**Note the disagreement worth mentioning in an exam:** entropy and Gini **agree on the root (`age`)** but **rank the middle attributes differently**. Different measures can build different trees from the same data — that is a legitimate, examinable observation.

### Step 6 — Grow each branch recursively

**Branch `age = middle`** — 4 records (3, 7, 12, 13), **all yes** → entropy 0 → **pure leaf: yes**. No further split is possible or needed.

**Branch `age = youth`** — 5 records (1, 2, 8, 9, 11): labels `no, no, no, yes, yes`, entropy **0.9710**. Recompute gains **within this subset only**:

| Attribute | Gain within youth |
|---|---|
| **student** | **0.9710** (student=yes → 2 yes, 0 no; student=no → 0 yes, 3 no — both pure) |
| income | 0.5710 |
| credit_rating | 0.0200 |

**`student` splits it perfectly** → youth + student=yes → **yes**; youth + student=no → **no**. Two leaves.

**Branch `age = senior`** — 5 records (4, 5, 6, 10, 14): labels `yes, yes, no, yes, no`, entropy **0.9710**. Within it:

| Attribute | Gain within senior |
|---|---|
| **credit_rating** | **0.9710** (fair → 3 yes; excellent → 2 no) |
| income | 0.0200 |
| student | 0.0200 |

**`credit_rating` splits it perfectly** → senior + fair → **yes**; senior + excellent → **no**.

### The final tree

```text
                        age?
             ┌───────────┼────────────┐
          youth        middle        senior
             │            │              │
        student?        yes        credit_rating?
        ┌───┴───┐                 ┌──────┴───────┐
      yes      no              fair         excellent
       │        │                │              │
      yes      no               yes             no
```

**Training accuracy: 14/14 = 100 %** — every record is correctly classified. (Verify it yourself against the table: this is the check that proves your tree is right.)

**As rules:**

```text
IF age = middle                                  THEN yes
IF age = youth  AND student = yes                THEN yes
IF age = youth  AND student = no                 THEN no
IF age = senior AND credit_rating = fair         THEN yes
IF age = senior AND credit_rating = excellent    THEN no
```

---

## 6. The tree growing process (general algorithm)

```text
TreeGrowth(D, attribute_list):
  1. create node N
  2. IF all tuples in D are of the same class C:  return N as leaf labelled C
  3. IF attribute_list is empty:  return N as leaf labelled with the majority class
  4. select the attribute A with the best measure (gain / gain ratio / Gini)
  5. label N with A;  remove A from attribute_list
  6. FOR each value v of A:
        grow a branch;  Dᵥ = tuples in D with A = v
        IF Dᵥ is empty:  attach a leaf labelled with the majority class of D
        ELSE:            attach TreeGrowth(Dᵥ, attribute_list)
  7. return N
```

The algorithm starts with the **full training dataset at the root**, splits on the best attribute, and **repeats recursively for each subset**.

---

## 7. Stopping conditions

Growth stops when:

1. **All records in a node belong to the same class** (pure — a definitive leaf), or
2. **No attributes remain** for further splitting (leaf labelled with the **majority class**), or
3. **No records remain** in the subset (empty branch — labelled with the parent's majority class), or
4. A **predefined stopping criterion** is reached — minimum node size, maximum depth, or a minimum gain threshold.

**Stopping conditions prevent overfitting and excessive tree growth.** A tree that is allowed to grow until every leaf is pure will memorise noise.

---

## 8. Overfitting and pruning

**Overfitting** occurs when a tree becomes **too complex and models noise instead of the underlying pattern**. It performs **well on training data but poorly on unseen data**, reducing **generalisation**.

*The tell-tale sign:* training accuracy 100 %, test accuracy much lower — and the tree has long, thin branches built from one or two records.

**Tree pruning** removes branches that **do not contribute significantly to predictive accuracy**, producing a **simpler, more generalisable** tree.

| | **Pre-pruning** (early stopping) | **Post-pruning** |
|---|---|---|
| When | during construction | after the full tree is built |
| How | stop splitting when a criterion fails (min gain, min records, max depth, statistical test) | remove or collapse subtrees, then compare error |
| Risk | **horizon effect** — a weak split may enable a strong one below it | more computation, but sees the whole tree |
| Typical | ID3 with thresholds, C4.5's early criteria | **C4.5 reduced-error pruning, CART cost-complexity pruning** |

**Cost-complexity pruning (CART):** minimise `Error(T) + α·|leaves(T)|`; α controls how strongly a large tree is penalised.
**Reduced-error pruning (C4.5):** test each subtree on a pruning set; if replacing it with a leaf does not increase error, prune it.

---

## 9. Handling continuous attributes (worked)

Continuous attributes are handled by **choosing threshold values that split the data into intervals**; the best threshold is the one with the **greatest impurity reduction**.

**Method:** sort the distinct values, take the **midpoint between every adjacent pair** as a candidate threshold, compute the gain of the binary split for each candidate, and keep the best. (`n` distinct values give `n − 1` candidates.)

**Worked example.** Attribute `age` (numeric) with 10 records:

| age | 23 | 25 | 27 | 29 | 31 | 35 | 38 | 42 | 45 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| class | N | N | Y | Y | Y | N | Y | Y | Y | Y |

`Entropy(root) = 0.8813` (6 Y, 4 N). Candidate thresholds and gains:

| Threshold | Left (≤ t) | Right (> t) | Gain |
|---|---|---|---|
| 24.0 | 1 record, H=0 | 9 records, H=0.7642 | 0.1935 |
| **26.0** | **2 records, H=0** | **8 records, H=0.5436** | **0.4464 ← best** |
| 28.0 | 3 records, H=0.9183 | 7 records, H=0.5917 | 0.1916 |
| 30.0 | 4, H=1.0000 | 6, H=0.6500 | 0.0913 |
| 33.0 | 5, H=0.9710 | 5, H=0.7219 | 0.0349 |
| 36.5 | 6, H=1.0000 | 4, H=0 | 0.2813 |
| 40.0 | 7, H=0.9852 | 3, H=0 | 0.1916 |
| 43.5 | 8, H=0.9544 | 2, H=0 | 0.1177 |
| 47.5 | 9, H=0.9183 | 1, H=0 | 0.0548 |

**Best split: `age ≤ 26` vs `age > 26`, gain 0.4464.** The node then becomes a binary test, and the same procedure recurses.

*Practical note:* a continuous attribute can be reused further down the tree with a **different threshold** — unlike a categorical attribute, which is consumed once.

---

## 10. Handling missing values

Your page's three strategies:

1. **Ignore the record** — simplest, but throws away information (and can bias the model if missingness is not random).
2. **Replace with the most frequent value** (mode) — keeps all records, no information added.
3. **Distribute the record probabilistically among branches** — assign weights in proportion to the branch populations (C4.5). Most principled; keeps all records and preserves the attribute's information, at the cost of weighted training.

---

## 11. Advantages (your page)

- **Simple to understand and interpret** — white-box, unlike a neural network.
- **Minimal data preparation** — no normalisation needed (splits are order-based).
- **Handles both categorical and numeric data**.
- **Efficient** and widely used in practice.
- Handles **non-linear relationships** and **interactions** naturally.
- Can be **converted to rules** for domain review.

## 12. Limitations (your page)

- **Sensitive to noisy data and small changes** — a single flipped record can change the root.
- **Overfits easily** if not properly pruned.
- **Trees may become unstable** — this instability is exactly what ensemble methods (bagging, random forests, boosting) fix.
- **Biased toward attributes with many values** — hence gain ratio and pruning.
- Splits are **greedy/local**: a good split may be missed because of an earlier choice.
- **Axis-parallel only** — cannot split diagonally; needs deep trees for diagonal boundaries.

---

## 13. Applications

**Medical diagnosis** (symptom → disease), **credit risk assessment** (applicant → default/no default), **customer churn prediction**, **fraud detection**, **decision support systems** — *especially applications requiring transparent decision-making*, because every prediction comes with the rule that produced it (a regulatory requirement in lending and insurance).

---

## 14. Which algorithm is which (a table that earns marks)

| Algorithm | Split measure | Handles continuous? | Missing values | Pruning |
|---|---|---|---|---|
| **ID3** | Information gain | no (discretise first) | no | none |
| **C4.5** | **Gain ratio** | **yes** | **yes** (fractional) | **reduced-error** |
| **CART** | **Gini index** | **yes** | surrogate splits | **cost-complexity** |

---

## 15. Summary

Decision tree induction recursively partitions data into purer-and-purer subsets, choosing at each node the attribute that maximises a purity measure — **entropy reduction (information gain)**, its normalised form **gain ratio**, or **Gini index** — until a node is pure, no attributes remain, or a stopping criterion fires. On the standard 14-record dataset the root set has entropy **0.9403**, gains are **age 0.2467 > student 0.1518 > credit 0.0481 > income 0.0292**, so `age` becomes the root; `age = middle` is immediately pure, `youth` splits perfectly on `student`, and `senior` splits perfectly on `credit_rating`, giving a tree that reproduces all 14 records. Continuous attributes are handled by mid-point threshold search (here `age ≤ 26` with gain 0.4464), missing values by ignoring, imputing or fractional distribution, and the overfitting that greedy growth causes is controlled by **pre- or post-pruning** — the difference between a model that memorises and one that generalises.

---

**Next:** [Topic 3 — Bayesian Classification: Naïve Bayes](03-naive-bayes.md)
