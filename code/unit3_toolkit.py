#!/usr/bin/env python3
"""
Unit 3 toolkit — classification, clustering, evaluation and regression.
No dependencies. Every function reproduces a worked example from the notes.

Usage:
    python unit3_toolkit.py              # all demos
    python unit3_toolkit.py tree         # decision tree only
    python unit3_toolkit.py bayes knn    # several at once

Demos: tree, bayes, knn, kmeans, pam, linkage, dbscan, metrics, regress, sims
"""

import math
import sys
from collections import Counter

# ---------------------------------------------------------------- utilities

def entropy(labels):
    """Shannon entropy in bits. 0 = pure."""
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def gini(labels):
    """Gini impurity 1 - sum p^2."""
    n = len(labels)
    if n == 0:
        return 0.0
    return 1 - sum((c / n) ** 2 for c in Counter(labels).values())


def euclid(a, b):
    return math.dist(a, b)


def manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def minkowski(a, b, h):
    return sum(abs(x - y) ** h for x, y in zip(a, b)) ** (1 / h)


def standardise(rows):
    """Z-score each column of a list of tuples."""
    if not rows:
        return []
    p = len(rows[0])
    means = [sum(r[j] for r in rows) / len(rows) for j in range(p)]
    sds = []
    for j in range(p):
        var = sum((r[j] - means[j]) ** 2 for r in rows) / len(rows)
        sds.append(math.sqrt(var) or 1.0)
    return [tuple((r[j] - means[j]) / sds[j] for j in range(p)) for r in rows]


# ---------------------------------------------------------------- decision tree

BUYS = [
    ("youth", "high", "no", "fair", "no"),
    ("youth", "high", "no", "excellent", "no"),
    ("middle", "high", "no", "fair", "yes"),
    ("senior", "medium", "no", "fair", "yes"),
    ("senior", "low", "yes", "fair", "yes"),
    ("senior", "low", "yes", "excellent", "no"),
    ("middle", "low", "yes", "excellent", "yes"),
    ("youth", "medium", "no", "fair", "no"),
    ("youth", "low", "yes", "fair", "yes"),
    ("senior", "medium", "yes", "fair", "yes"),
    ("youth", "medium", "yes", "excellent", "yes"),
    ("middle", "medium", "no", "excellent", "yes"),
    ("middle", "high", "yes", "fair", "yes"),
    ("senior", "medium", "no", "excellent", "no"),
]
BUYS_ATTRS = ["age", "income", "student", "credit"]


def gain(rows, idx, target=-1):
    """Information gain of attribute idx."""
    parent = entropy([r[target] for r in rows])
    total = 0.0
    for value in {r[idx] for r in rows}:
        subset = [r[target] for r in rows if r[idx] == value]
        total += len(subset) / len(rows) * entropy(subset)
    return parent - total


def split_info(rows, idx):
    n = len(rows)
    return -sum((len(s) / n) * math.log2(len(s) / n)
                for s in ([r for r in rows if r[idx] == v]
                          for v in {r[idx] for r in rows}))


def gain_ratio(rows, idx):
    return gain(rows, idx) / split_info(rows, idx)


def gini_split(rows, idx):
    n = len(rows)
    return sum(len(s) / n * gini([r[-1] for r in s])
               for s in ([r for r in rows if r[idx] == v]
                         for v in {r[idx] for r in rows}))


def best_attribute(rows, pairs, target=-1, measure="gain"):
    """pairs: list of (attribute_name, column_index) — the index is global and
    fixed, so choosing a subset of attributes never shifts the columns."""
    scores = {}
    for name, i in pairs:
        if measure == "gain":
            scores[name] = gain(rows, i, target)
        elif measure == "gainratio":
            scores[name] = gain_ratio(rows, i)
        else:
            scores[name] = -gini_split(rows, i)   # higher is better
    return max(scores, key=scores.get), scores


def build_tree(rows, pairs, target=-1, depth=0, max_depth=6):
    """ID3-style tree. Returns nested dict; leaves are class labels."""
    labels = [r[target] for r in rows]
    if len(set(labels)) == 1:
        return labels[0]
    if not pairs or depth >= max_depth:
        return Counter(labels).most_common(1)[0][0]
    name, _ = best_attribute(rows, pairs, target)
    idx = dict(pairs)[name]
    tree = {name: {}}
    for value in sorted({r[idx] for r in rows}):
        subset = [r for r in rows if r[idx] == value]
        if not subset:
            tree[name][value] = Counter(labels).most_common(1)[0][0]
        else:
            tree[name][value] = build_tree(subset, [(n, i) for n, i in pairs if n != name],
                                           target, depth + 1, max_depth)
    return tree


def predict_tree(tree, row, index):
    """index: dict name -> column position (fixed for the whole table)."""
    while isinstance(tree, dict):
        name = next(iter(tree))
        value = row[index[name]]
        tree = tree[name].get(value)
        if tree is None:
            return None
    return tree


def demo_tree():
    print("=== DECISION TREE (14 records, buys_computer) ===")
    labels = [r[4] for r in BUYS]
    print(f" root entropy          = {entropy(labels):.4f}")
    print(f" root gini             = {gini(labels):.4f}")
    for i, name in enumerate(BUYS_ATTRS):
        print(f" Gain({name:7s})        = {gain(BUYS, i):.4f}"
              f"   gainratio = {gain_ratio(BUYS, i):.4f}"
              f"   gini_split = {gini_split(BUYS, i):.4f}")
    pairs = list(enumerate(BUYS_ATTRS))
    pairs = [(name, i) for i, name in pairs]
    root, scores = best_attribute(BUYS, pairs)
    print(f" chosen root           = {root}  (gain {scores[root]:.4f})")
    for value in ("youth", "middle", "senior"):
        sub = [r for r in BUYS if r[0] == value]
        remaining = [(n, i) for n, i in pairs if n != "age"]
        att, sc = best_attribute(sub, remaining)
        print(f"   age={value:6s} n={len(sub)} H={entropy([r[4] for r in sub]):.4f}"
              f"  best next = {att:12s} gain={sc[att]:.4f}")
    tree = build_tree(BUYS, pairs)
    index = {name: i for i, name in enumerate(BUYS_ATTRS)}
    hits = sum(1 for r in BUYS if predict_tree(tree, r, index) == r[4])
    print(f" tree                 = {tree}")
    print(f" training accuracy    = {hits}/{len(BUYS)}")
    # continuous threshold search
    cont = [(23, "N"), (25, "N"), (27, "Y"), (29, "Y"), (31, "Y"),
            (35, "N"), (38, "Y"), (42, "Y"), (45, "Y"), (50, "Y")]
    parent = entropy([c for _, c in cont])
    best = None
    values = sorted({v for v, _ in cont})
    for i in range(len(values) - 1):
        t = (values[i] + values[i + 1]) / 2
        left = [c for v, c in cont if v <= t]
        right = [c for v, c in cont if v > t]
        g = parent - (len(left) / 10 * entropy(left) + len(right) / 10 * entropy(right))
        if best is None or g > best[1]:
            best = (t, g)
    print(f" best continuous threshold: age <= {best[0]}  gain {best[1]:.4f}\n")


# ---------------------------------------------------------------- naive bayes

def nb_train(rows, attrs, target=-1):
    classes = sorted({r[target] for r in rows})
    model = {"prior": {}, "counts": {}, "n": len(rows), "classes": classes}
    for c in classes:
        subset = [r for r in rows if r[target] == c]
        model["prior"][c] = len(subset) / len(rows)
        model["counts"][c] = {i: Counter(r[i] for r in subset) for i in range(len(attrs))}
    return model


def nb_predict(model, x, laplace=False, nvalues=None):
    scores = {}
    for c in model["classes"]:
        total = sum(model["counts"][c][0].values())
        p = model["prior"][c]
        if laplace:
            p = (total + 1) / (model["n"] + len(model["classes"]))
        for i, value in enumerate(x):
            count = model["counts"][c][i].get(value, 0)
            if laplace:
                k = nvalues[i] if nvalues else 2
                prob = (count + 1) / (total + k)
            else:
                prob = count / total
            p *= prob
        scores[c] = p
    return max(scores, key=scores.get), scores


def demo_bayes():
    print("=== NAIVE BAYES (14 records) ===")
    model = nb_train(BUYS, BUYS_ATTRS)
    for x in [("youth", "medium", "yes", "fair"), ("middle", "medium", "no", "fair")]:
        pred, sc = nb_predict(model, x)
        print(f" {x} -> {pred}   scores " +
              "  ".join(f"{k}={v:.6f}" for k, v in sc.items()))
    nvalues = [len({r[i] for r in BUYS}) for i in range(len(BUYS_ATTRS))]
    x = ("middle", "medium", "no", "fair")
    pred, sc = nb_predict(model, x, laplace=True, nvalues=nvalues)
    print(f" {x} with Laplace -> {pred}   scores " +
          "  ".join(f"{k}={v:.6f}" for k, v in sc.items()))
    # Gaussian
    yes = [168, 170, 172, 174, 176]
    no = [160, 164, 166]

    def gauss(x, vals):
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / len(vals)
        sd = math.sqrt(var)
        return mu, sd, 1 / (sd * math.sqrt(2 * math.pi)) * math.exp(-((x - mu) ** 2) / (2 * var))

    for name, vals, prior in (("yes", yes, 5 / 8), ("no", no, 3 / 8)):
        mu, sd, p = gauss(174, vals)
        print(f" Gaussian class {name}: mu={mu:.2f} sd={sd:.4f} P(174)={p:.6f} "
              f"x prior = {prior * p:.8f}")
    print()


# ---------------------------------------------------------------- kNN

KNN_POINTS = [
    ("P1", (1, 2), "+"), ("P2", (2, 3), "+"), ("P3", (3, 3), "+"),
    ("P4", (6, 5), "-"), ("P5", (7, 7), "-"), ("P6", (8, 6), "-"),
    ("P7", (5, 4), "-"),
]


def knn(query, data, k, weighted=False, metric="euclid"):
    if metric == "euclid":
        dist = lambda a, b: euclid(a, b)
    elif metric == "manhattan":
        dist = manhattan
    else:
        dist = lambda a, b: minkowski(a, b, 3)
    ranked = sorted(((dist(query, p), name, label) for name, p, label in data))
    near = ranked[:k]
    if not weighted:
        votes = Counter(label for _, _, label in near)
        return votes.most_common(1)[0][0], votes, near
    weights = {}
    for d, _, label in near:
        weights[label] = weights.get(label, 0.0) + 1 / (d if d else 1e-9)
    return max(weights, key=weights.get), weights, near


def demo_knn():
    print("=== kNN (7 points, query (3,4)) ===")
    query = (3, 4)
    for name, p, label in sorted(KNN_POINTS, key=lambda d: euclid(d[1], query)):
        print(f" {name} {p} {label}  euclid={euclid(p, query):.4f}"
              f"  manhattan={manhattan(p, query):.2f}"
              f"  minkowski3={minkowski(p, query, 3):.4f}")
    for k in (3, 5, 7):
        pred, votes, near = knn(query, KNN_POINTS, k)
        wpred, w, _ = knn(query, KNN_POINTS, k, weighted=True)
        print(f" K={k}: plain {dict(votes)} -> {pred}   weighted "
              + " ".join(f"{c}={v:.4f}" for c, v in w.items()) + f" -> {wpred}")
    print()


# ---------------------------------------------------------------- k-means

KM_POINTS = {"A1": (2, 10), "A2": (2, 5), "A3": (8, 4), "A4": (5, 8),
             "A5": (7, 5), "A6": (6, 4), "A7": (1, 2), "A8": (4, 9)}


def kmeans(points, k, init=None, max_iter=100, seed=0):
    """points: dict name -> tuple. Returns labels, centroids, sse, history."""
    import random
    names = list(points)
    if init is None:
        rnd = random.Random(seed)
        centroids = [points[rnd.choice(names)] for _ in range(k)]
    else:
        centroids = list(init)
    history = []
    for _ in range(max_iter):
        groups = {i: [] for i in range(k)}
        for name in names:
            idx = min(range(k), key=lambda i: euclid(points[name], centroids[i]))
            groups[idx].append(name)
        if any(not g for g in groups.values()):
            break
        new = [tuple(sum(points[n][j] for n in groups[i]) / len(groups[i])
                     for j in range(len(centroids[0]))) for i in range(k)]
        history.append(({i: sorted(v) for i, v in groups.items()},
                        [tuple(round(c, 4) for c in cc) for cc in new]))
        if all(euclid(a, b) < 1e-12 for a, b in zip(new, centroids)):
            centroids = new
            break
        centroids = new
    sse = sum(euclid(points[n], centroids[i]) ** 2
              for i in range(k) for n in groups[i])
    return {n: next(i for i in range(k) if n in groups[i]) for n in names}, centroids, sse, history


def demo_kmeans():
    print("=== K-MEANS (8 points, K=3) ===")
    labels, cent, sse, hist = kmeans(KM_POINTS, 3, init=[(2, 10), (5, 8), (1, 2)])
    for it, (groups, cents) in enumerate(hist, 1):
        print(f" iteration {it}: groups {groups}  -> centroids {cents}")
    print(f" final centroids: {[tuple(round(c, 4) for c in cc) for cc in cent]}")
    print(f" final SSE      : {sse:.4f}")
    print(" elbow sweep (best of 30 random starts):")
    for k in range(1, 6):
        best = min(kmeans(KM_POINTS, k, seed=s)[2] for s in range(30))
        print(f"   K={k}: SSE={best:.4f}")
    print()


# ---------------------------------------------------------------- PAM

PAM_POINTS = {"A": (1, 1), "B": (2, 1), "C": (1, 2), "D": (7, 7), "E": (8, 7), "F": (7, 8)}


def pam_cost(points, medoids):
    total, assign = 0.0, {}
    for name, p in points.items():
        best = min(medoids, key=lambda m: euclid(p, points[m]))
        assign[name] = best
        total += euclid(p, points[best])
    return total, assign


def pam(points, k, init, max_iter=50):
    medoids = list(init)
    history = [("init", tuple(medoids), pam_cost(points, medoids)[0])]
    for _ in range(max_iter):
        cost, _assign = pam_cost(points, medoids)
        best_swap, best_cost = None, cost
        for out in medoids:
            for cand in points:
                if cand in medoids:
                    continue
                trial = [cand if m == out else m for m in medoids]
                c, _ = pam_cost(points, trial)
                if c < best_cost - 1e-12:
                    best_swap, best_cost = (out, cand), c
        if best_swap is None:
            break
        out, cand = best_swap
        medoids = [cand if m == out else m for m in medoids]
        history.append((f"{out}->{cand}", tuple(medoids), best_cost))
    return medoids, pam_cost(points, medoids), history


def demo_pam():
    print("=== PAM (6 points, K=2, start {B,E}) ===")
    medoids, (cost, assign), history = pam(PAM_POINTS, 2, ["B", "E"])
    for step, meds, c in history:
        print(f" {step:8s} medoids={meds} cost={c:.4f}")
    print(f" assignments: {assign}")
    print(f" final medoids {medoids} cost {cost:.4f}\n")


# ---------------------------------------------------------------- linkage

LINK_POINTS = {"P1": (1, 1), "P2": (1.5, 1.5), "P3": (5, 5), "P4": (3, 4), "P5": (4, 4)}
CHAIN_POINTS = {"A": (0, 0), "B": (1, 0), "C": (2, 0), "D": (3, 0),
                "M": (4.5, 0), "E": (6, 0), "F": (7, 0), "G": (8, 0)}


def agglomerative(points, link="single"):
    """Returns list of (height, merged groups) steps."""
    clusters = {k: [k] for k in points}
    steps = []
    while len(clusters) > 1:
        keys = list(clusters)
        best = None
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                ds = [euclid(points[x], points[y]) for x in clusters[a] for y in clusters[b]]
                if link == "single":
                    d = min(ds)
                elif link == "complete":
                    d = max(ds)
                else:
                    d = sum(ds) / len(ds)
                if best is None or d < best[0] - 1e-12:
                    best = (d, a, b)
        d, a, b = best
        steps.append((d, sorted(clusters[a]), sorted(clusters[b])))
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
    return steps


def demo_linkage():
    print("=== HIERARCHICAL LINKAGE (5 points) ===")
    for link in ("single", "complete", "average"):
        print(f" {link}:")
        for h, a, b in agglomerative(LINK_POINTS, link):
            print(f"   {h:7.4f}  {a} + {b}")
    print("=== CHAINING DEMO (1-D, bridge point M) ===")
    for link in ("single", "complete", "average"):
        steps = agglomerative(CHAIN_POINTS, link)
        print(f" {link:9s} final merge at {steps[-1][0]:.4f}")
    print()


# ---------------------------------------------------------------- DBSCAN

DB_POINTS = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1.5),
             (8, 8), (8, 9), (9, 8), (9, 9), (20, 20)]


def dbscan(points, eps, min_pts, include_self=True):
    def neighbours(p):
        found = [q for q in points if euclid(p, q) <= eps]
        return found if include_self else [q for q in found if q != p]

    nbrs = {p: neighbours(p) for p in points}
    label = {p: "unvisited" for p in points}
    cluster = 0
    for p in points:
        if label[p] != "unvisited":
            continue
        if len(nbrs[p]) < min_pts:
            label[p] = "noise"
            continue
        cluster += 1
        label[p] = cluster
        queue = list(nbrs[p])
        while queue:
            q = queue.pop()
            if label[q] == "noise":
                label[q] = cluster
            if label[q] != "unvisited":
                continue
            label[q] = cluster
            if len(nbrs[q]) >= min_pts:
                queue.extend(nbrs[q])
    types = {}
    for p in points:
        if label[p] == "noise":
            types[p] = "noise"
        elif len(nbrs[p]) >= min_pts:
            types[p] = "core"
        else:
            types[p] = "border"
    return label, types, {p: len(nbrs[p]) for p in points}


def demo_dbscan():
    print("=== DBSCAN (10 points, eps=1.5, MinPts=4) ===")
    labels, types, counts = dbscan(DB_POINTS, 1.5, 4)
    for p in DB_POINTS:
        print(f" {str(p):10s} neighbours={counts[p]}  {types[p]:6s}  cluster={labels[p]}")
    clusters = sorted({v for v in labels.values() if isinstance(v, int)})
    print(f" clusters found: {len(clusters)}   noise points: "
          f"{[p for p, v in labels.items() if v == 'noise']}\n")


# ---------------------------------------------------------------- metrics

def confusion_metrics(tp, fn, fp, tn):
    n = tp + tn + fp + fn
    acc = (tp + tn) / n
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    spec = tn / (tn + fp) if (tn + fp) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {"accuracy": acc, "precision": prec, "recall": rec,
            "specificity": spec, "fpr": 1 - spec, "f1": f1,
            "balanced_accuracy": (rec + spec) / 2}


def roc_auc(scores_labels):
    """scores_labels: list of (score, 1/0). Returns points and AUC (trapezoid)."""
    data = sorted(scores_labels, reverse=True)
    pos = sum(l for _, l in data)
    neg = len(data) - pos
    points = [(0.0, 0.0)]
    tp = fp = 0
    for _, l in data:
        if l:
            tp += 1
        else:
            fp += 1
        points.append((fp / neg, tp / pos))
    auc = sum((x2 - x1) * (y1 + y2) / 2
              for (x1, y1), (x2, y2) in zip(points, points[1:]))
    return points, auc


def demo_metrics():
    print("=== EVALUATION (TP=8 FN=2 FP=4 TN=6) ===")
    for k, v in confusion_metrics(8, 2, 4, 6).items():
        print(f" {k:18s} = {v:.4f}")
    data = [(0.95, 1), (0.90, 1), (0.85, 0), (0.80, 1), (0.75, 1), (0.70, 0),
            (0.65, 1), (0.60, 0), (0.55, 0), (0.50, 1), (0.45, 0), (0.40, 0)]
    pts, auc = roc_auc(data)
    print(f" ROC points: {[(round(a,4), round(b,4)) for a, b in pts]}")
    print(f" AUC = {auc:.4f}\n")


# ---------------------------------------------------------------- regression

def simple_linear(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b1 = sxy / sxx
    b0 = my - b1 * mx
    pred = [b0 + b1 * x for x in xs]
    resid = [y - p for y, p in zip(ys, pred)]
    sse = sum(r * r for r in resid)
    sst = sum((y - my) ** 2 for y in ys)
    return {"b0": b0, "b1": b1, "pred": pred, "resid": resid,
            "sse": sse, "r2": 1 - sse / sst,
            "mae": sum(abs(r) for r in resid) / n,
            "mse": sse / n, "rmse": math.sqrt(sse / n)}


def solve_linear(A, b):
    """Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[c][c]:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def multiple_linear(rows):
    """rows: list of (x1, ..., xp, y). Returns coefficients [b0, b1, ...]."""
    X = [[1.0] + list(r[:-1]) for r in rows]
    y = [r[-1] for r in rows]
    p = len(X[0])
    XtX = [[sum(X[k][i] * X[k][j] for k in range(len(X))) for j in range(p)] for i in range(p)]
    Xty = [sum(X[k][i] * y[k] for k in range(len(X))) for i in range(p)]
    return solve_linear(XtX, Xty)


def demo_regress():
    print("=== SIMPLE LINEAR REGRESSION ===")
    res = simple_linear([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
    print(f" b1={res['b1']:.4f}  b0={res['b0']:.4f}  line: y = {res['b0']:.1f} + {res['b1']:.1f}x")
    print(f" predictions {[round(p,4) for p in res['pred']]}")
    print(f" residuals   {[round(r,4) for r in res['resid']]}")
    print(f" SSE={res['sse']:.4f}  R2={res['r2']:.4f}  MAE={res['mae']:.4f}"
          f"  MSE={res['mse']:.4f}  RMSE={res['rmse']:.4f}")
    print(f" predict x=6 -> {res['b0'] + res['b1']*6:.4f}")
    print("=== MULTIPLE LINEAR REGRESSION ===")
    rows = [(1, 2, 5), (2, 1, 6), (3, 3, 10), (4, 2, 11), (5, 4, 15), (6, 3, 14)]
    coef = multiple_linear(rows)
    print(f" coefficients (b0,b1,b2) = {[round(c,4) for c in coef]}")
    pred = [coef[0] + coef[1] * r[0] + coef[2] * r[1] for r in rows]
    ys = [r[2] for r in rows]
    my = sum(ys) / len(ys)
    sse = sum((y - p) ** 2 for y, p in zip(ys, pred))
    sst = sum((y - my) ** 2 for y in ys)
    print(f" predictions {[round(p,4) for p in pred]}")
    print(f" SSE={sse:.4f}  R2={1-sse/sst:.4f}  RMSE={math.sqrt(sse/len(rows)):.4f}")
    print(f" predict (7,3) -> {coef[0] + coef[1]*7 + coef[2]*3:.4f}\n")


# ---------------------------------------------------------------- similarity

def simple_matching(x, y):
    return sum(1 for a, b in zip(x, y) if a == b) / len(x)


def jaccard(x, y):
    a = sum(1 for i in range(len(x)) if x[i] == 1 and y[i] == 1)
    b = sum(1 for i in range(len(x)) if x[i] == 1 and y[i] == 0)
    c = sum(1 for i in range(len(x)) if x[i] == 0 and y[i] == 1)
    return a / (a + b + c) if (a + b + c) else 0.0


def cosine(x, y):
    dot = sum(a * b for a, b in zip(x, y))
    nx = math.sqrt(sum(a * a for a in x))
    ny = math.sqrt(sum(b * b for b in y))
    return dot / (nx * ny)


def ordinal_normalise(ranks, m):
    return [(r - 1) / (m - 1) for r in ranks]


def heterogeneous(o1, o2, kinds):
    """kinds: 'nom', 'ord' (already normalised), 'num' with range."""
    total, count = 0.0, 0
    for v1, v2, kind in zip(o1, o2, kinds):
        if kind == "nom":
            d = 0.0 if v1 == v2 else 1.0
        else:
            d = abs(v1 - v2)
        total += d
        count += 1
    return total / count


def demo_sims():
    print("=== SIMILARITY MEASURES ===")
    o1, o2 = ["red", "medium", "yes", "high"], ["blue", "medium", "no", "high"]
    print(f" nominal simple matching = {simple_matching(o1, o2):.4f}")
    x, y = [1, 1, 0, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0, 1]
    print(f" Jaccard (asymmetric)    = {jaccard(x, y):.4f}")
    print(f" simple matching (bin)   = {simple_matching(x, y):.4f}")
    r1 = ordinal_normalise([3, 1, 2], 3)
    r2 = ordinal_normalise([1, 2, 3], 3)
    print(f" ordinal normalised      = {r1} vs {r2}  euclid={euclid(r1, r2):.4f}")
    print(f" cosine (3,2,0)/(2,2,1)  = {cosine([3,2,0], [2,2,1]):.4f}")
    a = ["male", 1.0, 0.5]
    b = ["female", 0.0, 0.0]
    c = ["male", 0.5, 1.0]
    kinds = ["nom", "num", "num"]
    print(f" mixed d(o1,o2) = {heterogeneous(a, b, kinds):.4f}"
          f"   d(o1,o3) = {heterogeneous(a, c, kinds):.4f}"
          f"   d(o2,o3) = {heterogeneous(b, c, kinds):.4f}\n")


# ---------------------------------------------------------------- main

DEMOS = {
    "tree": demo_tree,
    "bayes": demo_bayes,
    "knn": demo_knn,
    "kmeans": demo_kmeans,
    "pam": demo_pam,
    "linkage": demo_linkage,
    "dbscan": demo_dbscan,
    "metrics": demo_metrics,
    "regress": demo_regress,
    "sims": demo_sims,
}


def main(argv):
    wanted = argv[1:] or list(DEMOS)
    unknown = [w for w in wanted if w not in DEMOS]
    if unknown:
        print(f"unknown demo(s): {unknown}\navailable: {list(DEMOS)}")
        return 1
    for name in wanted:
        DEMOS[name]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
