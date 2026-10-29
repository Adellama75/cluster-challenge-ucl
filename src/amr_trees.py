#!/usr/bin/env python3
"""Tree models for co-amoxiclav resistance in E. coli (CIUK 2026 UCL challenge, team UCLuster Too).

Fits decision trees and tree ensembles (bagging, random forest, gradient boosting) at several depths,
compares them on held-out data, and writes tree diagrams, plots and a comparison table to the output
folder. Runs headless (no display, no graphviz), so it works on the Condenser VM.

Usage:
    python src/amr_trees.py --data data/dig_health_hub_amr.csv --out outputs
"""

import argparse
import os
import platform
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display on the VM: render straight to files
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

TARGET = "coamox"  # 1 = resistant to co-amoxiclav
DEFAULT_FEATURES = ["age", "imd"]  # the columns the brief asks about
OPTIONAL_FEATURES = ["sex_male", "had_surgery_past_yr"]  # extra numeric columns in the data set


def parse_args():
    """Command-line options: input file, output folder, features, deepest tree, test size and seed."""
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--data", default="data/dig_health_hub_amr.csv", help="input CSV")
    p.add_argument("--out", default="outputs", help="folder for figures and tables")
    p.add_argument("--features", nargs="+", default=DEFAULT_FEATURES,
                   help=f"predictor columns (default: {' '.join(DEFAULT_FEATURES)}; "
                        f"also available: {' '.join(OPTIONAL_FEATURES)})")
    p.add_argument("--max-depth", type=int, default=8, help="deepest tree to try")
    p.add_argument("--test-size", type=float, default=0.25, help="fraction held out for testing")
    p.add_argument("--seed", type=int, default=42, help="random seed, for reproducible results")
    return p.parse_args()


def load_data(path, features):
    """Read the CSV and check it has the columns we need, with a binary target."""
    df = pd.read_csv(path, index_col=0)
    missing = [c for c in features + [TARGET] if c not in df.columns]
    if missing:
        sys.exit(f"error: {path} has no column(s) {', '.join(missing)}")
    df = df[features + [TARGET]].dropna()
    if set(df[TARGET].unique()) - {0, 1}:
        sys.exit(f"error: {TARGET} must be 0/1")
    return df


def candidate_models(max_depth, seed):
    """(model type, depth, estimator) for every model we compare.

    Single trees are tried with and without class weighting, because resistant cases are the
    minority and an unweighted tree can score well on accuracy while missing most of them.
    """
    models = []
    for depth in range(1, max_depth + 1):
        models.append(("decision_tree", depth,
                       DecisionTreeClassifier(max_depth=depth, random_state=seed)))
        models.append(("decision_tree_balanced", depth,
                       DecisionTreeClassifier(max_depth=depth, class_weight="balanced",
                                              random_state=seed)))
        models.append(("bagging", depth,
                       BaggingClassifier(DecisionTreeClassifier(max_depth=depth), n_estimators=100,
                                         random_state=seed)))
        models.append(("random_forest", depth,
                       RandomForestClassifier(max_depth=depth, n_estimators=200,
                                              class_weight="balanced", random_state=seed)))
        models.append(("gradient_boosting", depth,
                       GradientBoostingClassifier(max_depth=depth, n_estimators=100,
                                                  learning_rate=0.05, random_state=seed)))
    return models


def evaluate(models, X_train, X_test, y_train, y_test, seed):
    """Fit every model; score it by 5-fold cross-validation on the training set and on the test set.

    Models are ranked on cross-validated balanced accuracy (training data only), so the test set stays
    an honest check rather than something we tuned against. Balanced accuracy averages the hit rate on
    resistant and susceptible patients: a model that calls everyone susceptible scores only 0.5 on it,
    even though its plain accuracy would be 76%. ROC AUC is reported too, as a threshold-free measure
    of how well a model ranks patients by risk.
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    rows, fitted = [], {}
    for kind, depth, model in models:
        cv_scores = cross_validate(model, X_train, y_train, cv=cv,
                                   scoring=["balanced_accuracy", "roc_auc"])
        model.fit(X_train, y_train)
        prob = model.predict_proba(X_test)[:, 1]
        pred = (prob >= 0.5).astype(int)
        rows.append({
            "model": kind, "max_depth": depth,
            "cv_balanced_accuracy_mean": cv_scores["test_balanced_accuracy"].mean(),
            "cv_balanced_accuracy_std": cv_scores["test_balanced_accuracy"].std(),
            "cv_roc_auc_mean": cv_scores["test_roc_auc"].mean(),
            "cv_roc_auc_std": cv_scores["test_roc_auc"].std(),
            "test_roc_auc": roc_auc_score(y_test, prob),
            "test_accuracy": accuracy_score(y_test, pred),
            "test_balanced_accuracy": balanced_accuracy_score(y_test, pred),
            "test_recall_resistant": recall_score(y_test, pred, zero_division=0),
            "test_precision_resistant": precision_score(y_test, pred, zero_division=0),
        })
        fitted[(kind, depth)] = model
    table = pd.DataFrame(rows).sort_values(["cv_balanced_accuracy_mean", "max_depth"],
                                           ascending=[False, True]).reset_index(drop=True)
    return table, fitted


def best_of(table, kinds):
    """Best row among the given model types: highest CV balanced accuracy, ties go to the shallower model."""
    return table[table["model"].isin(kinds)].iloc[0]


def save_tree_diagram(model, features, path, title):
    """Draw a fitted tree with sklearn's plot_tree, since the VM has no graphviz.

    Each box shows its split (leaves have none), the share of patients reaching it and the class
    proportions. For class-balanced trees the proportions are after weighting, so the root reads
    0.5/0.5. The figure gets wider and taller with depth so the boxes stay readable.
    """
    depth = model.get_depth()
    fig, ax = plt.subplots(figsize=(min(4 + 3 * 2 ** min(depth, 4), 40), 2.5 + 2 * depth))
    plot_tree(model, feature_names=features, class_names=["susceptible", "resistant"],
              filled=True, rounded=True, impurity=False, proportion=True, fontsize=8, ax=ax)
    ax.set_title(title)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_decision_surface(model, X, y, features, path, title):
    """Decision surface over the two features (only drawn when the model uses exactly two)."""
    fig, ax = plt.subplots(figsize=(7, 5))
    DecisionBoundaryDisplay.from_estimator(model, X, response_method="predict_proba",
                                           cmap="RdBu_r", alpha=0.6, ax=ax,
                                           xlabel=features[0], ylabel=features[1])
    jitter = np.random.default_rng(0).uniform(-0.15, 0.15, size=len(X))  # imd is 1-5: spread points out
    ax.scatter(X[features[0]], X[features[1]] + jitter, c=y, cmap="RdBu_r", edgecolor="k",
               linewidth=0.3, s=12)
    ax.set_title(title)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_balanced_accuracy_vs_depth(table, path):
    """Cross-validated balanced accuracy against depth, one line per model type.

    Error bars are the spread across the 5 folds. A line that falls as depth grows shows overfitting.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for kind, group in table.sort_values("max_depth").groupby("model"):
        ax.errorbar(group["max_depth"], group["cv_balanced_accuracy_mean"],
                    yerr=group["cv_balanced_accuracy_std"],
                    marker="o", capsize=3, label=kind)
    ax.set_xlabel("max depth")
    ax.set_ylabel("balanced accuracy (5-fold CV, training set)")
    ax.set_title("Model comparison by depth")
    ax.legend(fontsize=8)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_feature_importance(model, features, path, title):
    """Bar chart of the model's feature importances: which risk factors its predictions rely on most."""
    fig, ax = plt.subplots(figsize=(6, 1 + 0.5 * len(features)))
    order = np.argsort(model.feature_importances_)
    ax.barh(np.array(features)[order], model.feature_importances_[order])
    ax.set_xlabel("importance (mean decrease in impurity)")
    ax.set_title(title)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    """Load the data, fit and compare every model, then write the table, figures and summary."""
    args = parse_args()
    os.umask(0o027)  # files we create are not readable by other users on the VM
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = load_data(args.data, args.features)
    X, y = df[args.features], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, stratify=y, random_state=args.seed)
    print(f"{len(df)} patients, {y.mean():.1%} resistant; features: {', '.join(args.features)}")

    table, fitted = evaluate(candidate_models(args.max_depth, args.seed),
                             X_train, X_test, y_train, y_test, args.seed)
    table.round(4).to_csv(out / "model_comparison.csv", index=False)

    # Tree diagrams for every single-tree depth up to 4 (deeper trees aren't readable as pictures),
    # plus text versions for all depths.
    tag = "_".join(args.features)
    for depth in range(1, args.max_depth + 1):
        tree = fitted[("decision_tree_balanced", depth)]
        if depth <= 4:
            save_tree_diagram(tree, args.features, out / f"tree_balanced_depth{depth}_{tag}.png",
                              f"Decision tree (balanced), max depth {depth}")
        (out / f"tree_balanced_depth{depth}_{tag}.txt").write_text(
            export_text(tree, feature_names=args.features))

    best_tree = best_of(table, ["decision_tree", "decision_tree_balanced"])
    best_any = best_of(table, table["model"].unique())
    tree_model = fitted[(best_tree["model"], best_tree["max_depth"])]
    any_model = fitted[(best_any["model"], best_any["max_depth"])]

    save_tree_diagram(tree_model, args.features, out / f"best_tree_{tag}.png",
                      f"Best single tree: {best_tree['model']}, depth {best_tree['max_depth']}")
    save_balanced_accuracy_vs_depth(table, out / f"balanced_accuracy_vs_depth_{tag}.png")
    save_feature_importance(any_model, args.features, out / f"feature_importance_{tag}.png",
                            f"Risk factors: {best_any['model']}, depth {best_any['max_depth']}")
    if len(args.features) == 2:
        for name, row, model in [("best_tree", best_tree, tree_model),
                                 ("best_model", best_any, any_model)]:
            save_decision_surface(model, X, y, args.features,
                                  out / f"decision_surface_{name}_{tag}.png",
                                  f"P(resistant): {row['model']}, depth {row['max_depth']}")

    summary = [
        f"data: {args.data} ({len(df)} rows, {y.mean():.1%} resistant)",
        f"features: {', '.join(args.features)}; test size {args.test_size}; seed {args.seed}",
        f"best single tree: {best_tree['model']} depth {best_tree['max_depth']} "
        f"(CV balanced accuracy {best_tree['cv_balanced_accuracy_mean']:.3f}; test: balanced accuracy "
        f"{best_tree['test_balanced_accuracy']:.3f}, recall on resistant "
        f"{best_tree['test_recall_resistant']:.3f}, ROC AUC {best_tree['test_roc_auc']:.3f})",
        f"best model overall: {best_any['model']} depth {best_any['max_depth']} "
        f"(CV balanced accuracy {best_any['cv_balanced_accuracy_mean']:.3f}; test: balanced accuracy "
        f"{best_any['test_balanced_accuracy']:.3f}, recall on resistant "
        f"{best_any['test_recall_resistant']:.3f}, ROC AUC {best_any['test_roc_auc']:.3f})",
        "feature importance (best model): " + ", ".join(
            f"{f} {v:.2f}" for f, v in zip(args.features, any_model.feature_importances_)),
        f"python {platform.python_version()}, scikit-learn {sklearn.__version__}, "
        f"pandas {pd.__version__}, matplotlib {matplotlib.__version__}",
    ]
    (out / f"run_summary_{tag}.txt").write_text("\n".join(summary) + "\n")
    # umask only covers new files: outputs/ comes with the repo, and overwriting keeps old modes
    out.chmod(0o750)
    for f in out.iterdir():
        if f.is_file():
            f.chmod(0o640)
    print("\n".join(summary))
    print(f"wrote {len(list(out.iterdir()))} files to {out}/")


if __name__ == "__main__":
    main()
