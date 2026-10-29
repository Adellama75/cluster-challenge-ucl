#!/usr/bin/env python3
"""Which patient factors predict co-amoxiclav resistance, and which are just noise (CIUK 2026 UCL challenge).

Tests each patient factor in the data on its own, with a simple logistic regression and a small decision
tree, and compares its score with what shuffled copies of the same factor reach by luck. Then looks at all
factors together: adjusted odds ratios from one logistic regression, and permutation importance in a
random forest that is also given two columns of random numbers. Writes tables, figures and a summary to
the output folder. Runs headless (no display), so it works on the Condenser VM.

Usage:
    python src/risk_factors.py --data data/dig_health_hub_amr.csv --out outputs
"""

import argparse
import math
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
from matplotlib.lines import Line2D
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

TARGET = "coamox"  # 1 = resistant to co-amoxiclav
# Patient factors known before the lab result, with readable names. Left out: id and dob (identifiers;
# age is worked out from dob), organism (always E. coli), spec_date (all within five weeks of 2014, so
# there is no trend to find), and cipro and gentam (results from the same sample, not known beforehand).
FACTORS = {
    "age": "Age",
    "sex_male": "Sex (male)",
    "had_surgery_past_yr": "Surgery in past year",
    "imd": "Deprivation (IMD quintile)",
    "ethnicity": "Ethnicity",
    "trust": "NHS trust (238)",
    "icd_chapter": "Diagnosis (ICD chapter)",
    "random_noise": "Random numbers (control)",
}
CATEGORICAL = ["imd", "ethnicity", "trust", "icd_chapter"]  # one 0/1 column per level in a regression
# Factors fitted together. Trust and ICD chapter are left out: with about 4 patients per trust and
# 40 per chapter there is too little data to estimate their effects next to the others.
ADJUSTED = ["age", "sex_male", "had_surgery_past_yr", "imd", "ethnicity"]
NOISE_COLUMNS = {"noise_continuous": "Random numbers (continuous)",
                 "noise_five_levels": "Random numbers (5 levels)"}

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#c3c2b7"
plt.rcParams.update({"font.size": 11, "text.color": INK, "axes.edgecolor": GREY,
                     "xtick.color": INK2, "ytick.color": INK})


def parse_args():
    """Command-line options: input file, output folder, number of shuffled copies and seed."""
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--data", default="data/dig_health_hub_amr.csv", help="input CSV")
    p.add_argument("--out", default="outputs", help="folder for figures and tables")
    p.add_argument("--permutations", type=int, default=100,
                   help="shuffled copies per factor, which set the noise level")
    p.add_argument("--seed", type=int, default=42, help="random seed, for reproducible results")
    return p.parse_args()


def load_data(path, seed):
    """Read the CSV and add the derived factors: NHS trust, ICD chapter and a column of random numbers."""
    df = pd.read_csv(path, index_col=0)
    needed = ["age", "sex_male", "had_surgery_past_yr", "imd", "ethnicity", "trst_cd", "icd_cd", TARGET]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        sys.exit(f"error: {path} has no column(s) {', '.join(missing)}")
    df = df[needed].dropna()
    ethnicity = df["ethnicity"].str.split(r"[ ,]").str[0]  # "Black, Black British, ..." -> "Black"
    return df.assign(
        ethnicity=pd.Categorical(ethnicity, categories=["White"] + sorted(set(ethnicity) - {"White"})),
        trust=df["trst_cd"],
        icd_chapter=df["icd_cd"].str[0],  # 964 different codes for 1000 patients; the letter groups them
        random_noise=np.random.default_rng(seed).normal(size=len(df)),
    )


def design(df, factors):
    """Columns a regression can use: numbers as they are, categories as one 0/1 column per level.

    The first level of each category is left out as the reference (imd quintile 1, White).
    """
    cats = [f for f in factors if f in CATEGORICAL]
    return pd.get_dummies(df[factors], columns=cats, drop_first=True, dtype=float)


def screen(df, y, n_perm, seed):
    """Score each factor on its own with two simple models, and compare with shuffled copies of it.

    The score is the 5-fold cross-validated ROC AUC: 0.5 means the factor ranks resistant patients no
    better than chance. Shuffling a factor across patients breaks any link with resistance but keeps its
    levels and how common each one is, so the shuffled scores show how high this factor can score by luck.
    That matters most for factors with many levels, like 238 NHS trusts. A factor beats noise only if
    both models score above 95% of their shuffled copies.
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    models = {"regression": LogisticRegression(max_iter=1000),
              "tree": DecisionTreeClassifier(max_depth=2, class_weight="balanced", random_state=seed)}
    rng = np.random.default_rng(seed)
    rows = []
    for factor, label in FACTORS.items():
        X = design(df, [factor])
        row = {"factor": factor, "label": label, "columns": X.shape[1]}
        for name, model in models.items():
            score = cross_val_score(model, X, y, cv=cv, scoring="roc_auc").mean()
            null = np.array([cross_val_score(model, X.iloc[rng.permutation(len(X))], y, cv=cv,
                                             scoring="roc_auc").mean() for _ in range(n_perm)])
            row |= {f"{name}_cv_roc_auc": score,
                    f"{name}_noise_p05": np.percentile(null, 5),
                    f"{name}_noise_p95": np.percentile(null, 95),
                    f"{name}_p_value": (1 + (null >= score).sum()) / (1 + n_perm)}
        row["verdict"] = "beats noise" if all(row[f"{m}_p_value"] <= 0.05 for m in models) else "noise"
        rows.append(row)
    return pd.DataFrame(rows)


def adjusted_odds_ratios(df, y):
    """Odds ratios for the patient factors fitted together in one logistic regression, with 95% intervals.

    Age is per 10 years, and each category is compared with its reference (female, no surgery, imd
    quintile 1, White). The intervals are Wald intervals from the standard errors of the coefficients.
    An interval that includes 1 means the data can't tell that factor's effect apart from no effect.
    """
    X = design(df.assign(age=df["age"] / 10), ADJUSTED)
    model = LogisticRegression(C=np.inf, tol=1e-10, max_iter=5000).fit(X, y)  # tight tol: exact MLE
    beta = np.r_[model.intercept_, model.coef_[0]]
    Xc = np.c_[np.ones(len(X)), X.to_numpy()]
    p = 1 / (1 + np.exp(-Xc @ beta))
    se = np.sqrt(np.diag(np.linalg.inv(Xc.T @ (Xc * (p * (1 - p))[:, None]))))[1:]
    return pd.DataFrame({
        "term": X.columns,
        "odds_ratio": np.exp(model.coef_[0]),
        "ci_low": np.exp(model.coef_[0] - 1.96 * se),
        "ci_high": np.exp(model.coef_[0] + 1.96 * se),
        "p_value": [math.erfc(abs(b / s) / math.sqrt(2)) for b, s in zip(model.coef_[0], se)],
    })


def forest_importance(df, y, seed):
    """Permutation importance in a random forest given the patient factors plus two columns of noise.

    Importance is how much the test-set ROC AUC drops when one column is shuffled. The noise columns, one
    continuous like age and one with five levels like imd, show what a column earns by chance, so a real
    risk factor has to clear them. Same split and forest settings as the best model in amr_trees.py.
    """
    rng = np.random.default_rng(seed + 1)
    X = df[ADJUSTED].assign(ethnicity=df["ethnicity"].cat.codes,
                            noise_continuous=rng.normal(size=len(df)),
                            noise_five_levels=rng.integers(1, 6, size=len(df)))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y,
                                                        random_state=seed)
    forest = RandomForestClassifier(max_depth=3, n_estimators=200, class_weight="balanced",
                                    random_state=seed).fit(X_train, y_train)
    imp = permutation_importance(forest, X_test, y_test, scoring="roc_auc", n_repeats=50,
                                 random_state=seed)
    return pd.DataFrame({"column": X.columns, "auc_drop_mean": imp.importances_mean,
                         "auc_drop_std": imp.importances_std,
                         "impurity_importance": forest.feature_importances_}
                        ).sort_values("auc_drop_mean", ascending=False).reset_index(drop=True)


def term_label(term):
    """Readable name for a regression term such as imd_4 or ethnicity_Black."""
    if term.startswith("imd_"):
        return f"IMD quintile {term[4:]} (vs 1, most deprived)"
    if term.startswith("ethnicity_"):
        return f"{term[len('ethnicity_'):]} (vs White)"
    return {"age": "Age (per 10 years)", "sex_male": "Male (vs female)",
            "had_surgery_past_yr": "Surgery in past year (vs none)"}[term]


def save_noise_figure(table, forest, path):
    """Left: each factor alone against its band of shuffled scores. Right: forest importance vs noise."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"width_ratios": [3, 2]})
    ys = np.arange(len(table))[::-1]
    for offset, model, colour, name in [(0.16, "regression", BLUE, "simple regression"),
                                        (-0.16, "tree", ORANGE, "small tree (depth 2)")]:
        ax1.hlines(ys + offset, table[f"{model}_noise_p05"], table[f"{model}_noise_p95"],
                   color=GREY, linewidth=7)
        ax1.plot(table[f"{model}_cv_roc_auc"], ys + offset, "o", color=colour, markersize=8, label=name)
    ax1.axvline(0.5, color=MUTED, linewidth=1)
    ax1.set_yticks(ys, table["label"])
    ax1.set_xlabel("cross-validated ROC AUC (0.5 = chance)")
    ax1.set_title("Each factor on its own (beats noise only if both dots clear their grey bands)",
                  loc="left", fontsize=13)
    handles = ax1.get_legend_handles_labels()[0] + [Line2D([], [], color=GREY, linewidth=7)]
    ax1.legend(handles, ["simple regression", "small tree (depth 2)", "90% of shuffled copies"],
               fontsize=10, loc="lower right", frameon=False)

    labels = {**FACTORS, **NOISE_COLUMNS}
    yf = np.arange(len(forest))[::-1]
    colours = [GREY if c in NOISE_COLUMNS else BLUE for c in forest["column"]]
    ax2.barh(yf, forest["auc_drop_mean"], xerr=forest["auc_drop_std"], color=colours, height=0.5,
             error_kw={"ecolor": MUTED, "elinewidth": 1})
    ax2.axvline(0, color=MUTED, linewidth=1)
    ax2.set_yticks(yf, [labels[c] for c in forest["column"]])
    ax2.set_xlabel("drop in test ROC AUC when the column is shuffled")
    ax2.set_title("All together in a random forest (grey: noise)", loc="left", fontsize=13)
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(length=0)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_odds_ratio_figure(ors, path):
    """Adjusted odds ratios on a log scale. An interval crossing 1 means no detectable effect."""
    fig, ax = plt.subplots(figsize=(9, 0.45 * len(ors) + 1.6))
    ys = np.arange(len(ors))[::-1]
    ax.hlines(ys, ors["ci_low"], ors["ci_high"], color=BLUE, linewidth=2)
    ax.plot(ors["odds_ratio"], ys, "o", color=BLUE, markersize=8)
    ax.axvline(1, color=MUTED, linewidth=1)
    ax.set_xscale("log")
    ax.set_xlim(0.25, 4)
    ax.set_xticks([0.25, 0.5, 1, 2, 4], ["0.25", "0.5", "1", "2", "4"])
    ax.minorticks_off()
    ax.set_yticks(ys, [term_label(t) for t in ors["term"]])
    for yi, (o, lo, hi) in zip(ys, ors[["odds_ratio", "ci_low", "ci_high"]].to_numpy()):
        ax.text(1.02, yi, f"{o:.2f} ({lo:.2f} to {hi:.2f})", transform=ax.get_yaxis_transform(),
                va="center", fontsize=10, color=INK2)
    ax.set_xlabel("odds ratio for resistance, with 95% interval (log scale)")
    ax.set_title("Age, sex, surgery, deprivation and ethnicity fitted together", loc="left", fontsize=13)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=0)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def summary_lines(args, df, table, ors, forest):
    """The plain-language results, for the summary file and the terminal."""
    lines = [f"data: {args.data} ({len(df)} rows, {df[TARGET].mean():.1%} resistant); seed {args.seed}; "
             f"{args.permutations} shuffled copies per factor",
             "each factor on its own (5-fold cross-validated ROC AUC, 0.5 = chance; in brackets the score "
             "95% of shuffled copies stay below):"]
    lines += [f"  {r.label}: regression {r.regression_cv_roc_auc:.3f} ({r.regression_noise_p95:.3f}), "
              f"tree {r.tree_cv_roc_auc:.3f} ({r.tree_noise_p95:.3f}) -> {r.verdict}"
              for r in table.itertuples()]
    lines.append("age, sex, surgery, deprivation and ethnicity together (trust and diagnosis left out), "
                 "adjusted odds ratio (95% interval):")
    lines += [f"  {term_label(r.term)}: {r.odds_ratio:.2f} ({r.ci_low:.2f} to {r.ci_high:.2f})"
              for r in ors.itertuples()]
    labels = {**FACTORS, **NOISE_COLUMNS}
    lines.append("random forest, drop in test ROC AUC when a column is shuffled (mean +/- sd):")
    lines += [f"  {labels[r.column]}: {r.auc_drop_mean:.3f} +/- {r.auc_drop_std:.3f}"
              for r in forest.itertuples()]
    real = table.loc[table["verdict"] == "beats noise", "label"].tolist()
    lines.append(f"beats noise on its own: {', '.join(real) or 'nothing'}; every other factor fails at "
                 "least one of the two tests")
    lines.append(f"python {platform.python_version()}, scikit-learn {sklearn.__version__}, "
                 f"pandas {pd.__version__}, matplotlib {matplotlib.__version__}")
    return lines


def main():
    """Load the data, run the three analyses, then write the tables, figures and summary."""
    args = parse_args()
    os.umask(0o027)  # files we create are not readable by other users on the VM
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = load_data(args.data, args.seed)
    y = df[TARGET].to_numpy()
    table = screen(df, y, args.permutations, args.seed)
    ors = adjusted_odds_ratios(df, y)
    forest = forest_importance(df, y, args.seed)

    table.round(4).to_csv(out / "risk_factors_one_at_a_time.csv", index=False)
    ors.round(4).to_csv(out / "risk_factors_adjusted_odds_ratios.csv", index=False)
    forest.round(4).to_csv(out / "risk_factors_forest_importance.csv", index=False)
    save_noise_figure(table, forest, out / "risk_factors_vs_noise.png")
    save_odds_ratio_figure(ors, out / "risk_factors_adjusted_odds_ratios.png")
    lines = summary_lines(args, df, table, ors, forest)
    (out / "risk_factors_summary.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
