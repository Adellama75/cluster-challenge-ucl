# Video script (5:00, about 700 words)

Draft narration, updated by `/script` after each work session. Budgets are at 140 words per minute.
Mark finished lines with `<!-- locked -->` so `/script` leaves them alone.

**Status 29 Oct (D):** timing pass done. The spoken total is about 662 words, about 4:43 at 140 words
per minute, after a plain-language pass on Q4, Q6 and Q7 and cutting the Q2 lscpu sentence. It was 840 words, about 6:00. Segments were cut down to their main points, and what was
cut is noted under each one. Intro, Q1, Q2, Q8 and the outro are final. Q3 to Q7 owners: check your
lines, time one read-through against `storyboard.md`, then lock them. One paragraph per line, so the
cut list in `storyboard.md` can be found by searching.

| Segment | Time | Words |
|---|---|---|
| Intro | 0:15 | ~35 |
| Q1 Cloud compute | 0:25 | ~60 |
| Q2 Data security | 0:35 | ~80 |
| Q3 File permissions | 0:30 | ~70 |
| Q4 Representative data | 0:30 | ~70 |
| Q5 Synthetic data | 0:25 | ~60 |
| Q6 Final model | 0:45 | ~105 |
| Q7 Other techniques | 0:25 | ~60 |
| Q8 Teamwork | 1:00 | ~140 |
| Outro | 0:10 | ~25 |

## Intro (0:15, ~35 words)

We're UCLuster Too: Ada, Bobby, Eric and James. We used tree models to predict which patients' E. coli infections resist the antibiotic co-amoxiclav, and ran them on UCL's Condenser cloud. <!-- locked -->
[screen: title card: "UCLuster Too", CIUK 2026 UCL challenge, Ada Ge, Bobby Ta, Eric Huang, James Loke]

## Q1: What is cloud compute? (0:25, ~60 words)

Cloud computing means renting computers over the internet, on demand, instead of owning them. Condenser is UCL's private cloud. It gave us a virtual machine: a computer made in software, running on hardware shared with other users. That's infrastructure as a service: UCL runs the hardware, we run our code. <!-- locked -->
[screen: lscpu on the VM, highlighting the "Hypervisor vendor" line — TODO(A): capture before recording]
<!-- src: condenser.arc.ucl.ac.uk/about ("a private cloud platform for research computing at UCL", shared between tenancies), checked 29 Oct; README.md section 1 -->
<!-- drafted by A (25 Oct) and James (29 Oct); final by D, 29 Oct -->

## Q2: What are key data security considerations for cloud computing? (0:35, ~80 words)

Cloud security is shared. UCL keeps the hardware in its own facilities and walls each team's machines off from other teams'. Access goes only through UCL's JupyterHub with an SSH key, our connections are encrypted, and no passwords or keys go in our public repository. And Condenser isn't certified for sensitive data, so real patient records would need extra safeguards first. <!-- locked -->
[screen: condenser.arc.ucl.ac.uk/about with "not certified for the secure storage and processing of sensitive data" highlighted]
<!-- src: condenser.arc.ucl.ac.uk/about, checked 29 Oct: "All hardware resides in UCL facilities"; "Condenser is not certified for the secure storage and processing of sensitive data" (it adds that a secure platform can be built on it after consulting UCL's Information Governance Advisory Service). Each tenancy gets its own namespace and network (same page). README.md section 1 (JupyterHub over https, then ssh) -->
<!-- cut by D, 29 Oct, after an outside review: lscpu shows the patches in our VM's own kernel, which says little about how UCL secures the shared hardware. It was also on the cut list and saves about 6 s -->
<!-- left out for time: encryption at rest (Condenser doesn't say); Condenser's terms say it "should not be treated as the sole repository for your data" (condenser.arc.ucl.ac.uk/terms_and_conditions) -->
<!-- drafted by A (25 Oct) and James (29 Oct); final by D, 29 Oct, after review: "our connections" instead of "everything", "extra safeguards" instead of "shouldn't go there" -->

## Q3: The data file was world-readable. Why is this not desirable? Did we change it, how and why? (0:30, ~70 words)

When the data file landed on our machine, any user could read it. On a shared machine, that exposes patient-style records to anyone with an account. Ours is synthetic, but we treated it as real: we moved it into a folder only we can open and ran chmod 600, so only our account can read it. Our script's outputs are closed to other users too.
[screen: ls -l before (`-rw-r--r--`) and after (`-rw-------`): `cat notes/permissions-before.txt notes/permissions-after.txt` in a large-font terminal, or Bobby's screenshots if he took them, IP cropped out]
[TODO(A): optional, after getfacl on the VM: add "We also checked no extra access rules were set." On 27 Oct both mode strings in notes/permissions-after.txt end in "." (SELinux label only), not "+" (an ACL), so it is likely true]
<!-- src: notes/permissions-before.txt, notes/permissions-after.txt (VM, 27 Oct); src/amr_trees.py and src/risk_factors.py set umask 027 -->
<!-- shortened by D for time, 29 Oct: permission strings moved to the screen line -->

## Q4: Why would you want a representative data set for machine learning? (0:30, ~70 words)

A model only learns the patients it's shown, so training data should match the people it will be used on. Ours covers only ages 20 to 79. Each ethnic group is about a fifth of it, yet about 82% of people in England and Wales are White, so most real people belong to our data's smallest group. A model can score well in testing and still do badly for them, and that's algorithmic bias.
[screen: video/q4_our_data_vs_england_wales.png]
<!-- src: notes/2026-10-25-data-first-look.md and notes/2026-10-29-model-checks.md (ages 20-79; each ethnic group 17.6-21.1%, White the smallest at 17.6%); ONS Census 2021, England and Wales: White 81.7% (ethnicity-facts-figures.service.gov.uk) -->
<!-- chart made by D, 29 Oct, from the same numbers; C: replace it if you have your own -->
<!-- reworded by D, 29 Oct, after review: names White as the under-represented group, and "algorithmic bias" because the marking criteria use the term -->
<!-- plainer last sentence by D, 29 Oct, after an outside review flagged "that's how algorithmic bias arises" -->

## Q5: Why would we want to use synthetic data instead of actual patient data? (0:25, ~60 words)

Real patient records are sensitive health data, tightly protected by UK GDPR, and patients may not have agreed to this use. Synthetic data is designed to mimic real data without containing any real people, so we can build and test models, even on a shared cloud machine, with far less privacy risk.
[screen: text slide: "Synthetic data is made to mimic real data, with no real people in it"]
<!-- shortened by D, 29 Oct; UK GDPR and "far less privacy risk" as guide C puts it -->

## Q6: What is our final tree model, and why is it the most optimal? (0:45, ~105 words)

Only about a quarter of patients are resistant, so plain accuracy is misleading: calling everyone safe scores 76% but misses every resistant patient. So we weighted resistant cases more heavily and ranked models on balanced accuracy, which gives both groups equal weight.
[screen: video/q6_model_comparison.png, or the deck slide with it and the score table]

Random forests scored higher, but that's two hundred trees voting, which you can't read like a single tree. Our depth-3 tree scored best of the single trees in cross-validation, a doctor can read it, and deeper trees overfit.
[screen: video/q6_final_tree_readable.png]

Older patients are most at risk: resistance is 8% at ages 20 to 40, but 41% over 70. No other factor beat random noise in both tests.
[screen: deck slide with resistance by age group and video/q6_risk_factors_vs_noise.png]
<!-- src: outputs/run_summary_age_imd.txt, model_comparison.csv, tree_balanced_depth3_age_imd.txt (laptop run; the VM run on 27 Oct gave the same numbers) -->
<!-- 76%: test accuracy of the trees that flag nobody (model_comparison.csv, decision_tree depth 1-3: 0.76); 24.1% resistant -->
<!-- two hundred trees: RandomForestClassifier(n_estimators=200) in src/amr_trees.py -->
<!-- best single tree: balanced, depth 3, CV balanced accuracy 0.659 (depth 1: 0.655, depth 8: 0.584); with other seeds the best depth moves between 1 and 3 (notes/2026-10-29-model-checks.md) -->
<!-- test: tree balanced acc 0.622, recall 0.650, AUC 0.685; forest balanced acc 0.675, recall 0.733, AUC 0.718 -->
<!-- 8% and 41%: resistance at ages 20-40 (8.4%) and 71-79 (40.7%), notes/2026-10-29-model-checks.md -->
<!-- "no other factor beat random noise": outputs/risk_factors_summary.txt. Sex, surgery in the past year, deprivation, ethnicity, NHS trust and ICD chapter each fail at least one of the two tests; age scores 0.71, where 95% of its shuffled copies stay below 0.54. Reasoning: notes/2026-10-29-risk-factors.md -->
<!-- note: the depth-3 tree's 61.5-64.5 branch predicts susceptible, so "above 48 resistant" is a simplification; the tree screen now spells out the rule at the bottom -->
<!-- note: feature_importance_age_imd.png gives imd 0.09 (impurity importance), and that measure favours many-valued columns: in the noise-check forest a continuous column of random numbers gets 0.16 against imd's 0.07, while permutation importance puts imd (0.004) level with the noise columns (outputs/risk_factors_forest_importance.csv), so it isn't evidence that deprivation matters -->
<!-- shortened by D, 29 Oct, after review: depth-3 reason is its score; who-is-at-risk figures and the noise check added -->
<!-- plainer wording by D, 29 Oct, after an outside review flagged "misleads" and "which no one can follow"; first cut-list line ("We compared tree types and depths.") applied to stay under 5:00 -->
<!-- "in cross-validation" added (D, 29 Oct, after review): on the test set the depth-3 tree (0.622) scores below depths 1, 2 and 5 (0.651, 0.651, 0.653) -->
<!-- "in both tests" added (D, 29 Oct, after review): the slide's chart shows the diagnosis tree dot just past its band, so "no other factor beat noise" needed the both-models rule said out loud -->
<!-- "higher", not "slightly higher" (D, 29 Oct, after an outside review): 0.670 vs 0.659 in cross-validation, but 0.675 vs 0.622 on the 250 held-back test patients. The slide shows both -->
<!-- note: "beat random noise" means beating its shuffled copies in both the regression and the tree; the diagnosis (ICD chapter) tree alone scores 0.524 against 0.519, but its regression doesn't (outputs/risk_factors_summary.txt) -->

## Q7: What other modelling techniques could we use, and why? (0:25, ~60 words)

Logistic regression suits this data. It fits risk rising smoothly with age, where a tree can only make steps, and it gives odds ratios, which clinicians already use. We tried it and it matched our tree, with the odds of resistance rising by more than half per decade of age. We didn't need a neural network for a thousand patients and one clear risk factor.
[screen: video/q7_odds_ratios.png, or the deck slide with it and the two scores]
<!-- src: "matched our tree": class-weighted logistic regression on age and imd, same split and folds, CV balanced accuracy 0.660 vs the tree's 0.659 (notes/2026-10-29-model-checks.md). "More than half per decade": odds ratio per 10 years of age 1.54 in that fit, and 1.59 (1.44 to 1.76) adjusted for sex, surgery, deprivation and ethnicity (outputs/risk_factors_adjusted_odds_ratios.csv) -->
<!-- updated by D with C's checks, 29 Oct; C: check before recording -->
<!-- plainer wording by D, 29 Oct, after an outside review flagged "not sharp cut-offs" and "overkill" -->
<!-- "clear" instead of "real" (D, 29 Oct, after review): in the odds-ratio plot deprivation quintile 3 (0.60, 0.36 to 0.97) clears 1, with no trend across quintiles (notes/2026-10-29-risk-factors.md); the slide says so -->

## Q8: How did we work as a team? (1:00, ~140 words)

We split the work into four roles. Bobby ran the cloud machine, the environment and the ReadMe; James wrote the model script; Ada explored the data and chose how to evaluate the models; and Eric led the video. We paired up to cover each other and checked in for fifteen minutes each evening. A shared GitHub repository held our plan, role guides and a log of our work sessions. <!-- locked -->
[screen: PLAN.md roles table on GitHub, then video/teamwork-log.md, then the repo's commit history]

We hit a few problems. Login details reached only one of us, with no username, so we shared that login as instructed and found the username in the organisers' access guide. The machine has no git, so we edited on laptops, pushed to GitHub and fetched files with curl. And our first model flagged nobody as resistant, which is why we switched to balanced accuracy. <!-- locked -->
<!-- src: PLAN.md sections 2-3; video/teamwork-log.md (25 and 27 Oct) -->
<!-- roles: A Bobby, B James, C Ada, D Eric; role sentence kept as James wrote it (Eric, 29 Oct) -->
<!-- evening check-ins confirmed by Eric, 29 Oct -->

## Outro (0:10, ~25 words)

In short: our final model is a depth-3 class-balanced tree, and age is the only clear risk factor. Thanks for watching, from UCLuster Too. <!-- locked -->
[screen: closing card: UCLuster Too, the four names, and github.com/adellama75/cluster-challenge-ucl]
<!-- D, 29 Oct; "only clear risk factor": outputs/risk_factors_summary.txt -->
