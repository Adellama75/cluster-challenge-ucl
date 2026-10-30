# Video script (5:00, about 700 words)

Draft narration, updated by `/script` after each work session. Budgets are at 140 words per minute.
Mark finished lines with `<!-- locked -->` so `/script` leaves them alone.

**Status 30 Oct (D):** speakers changed: Ada Q1 and Q2, Bobby Q3 and Q4, James Q5 and Q6, Eric the intro, Q7, Q8
and the outro. New Q7, Q8 and outro lines from Eric. The spoken total is now about 747 words, about 5:20 at 140 words
per minute, so it is over the 5:00 limit until the cut list in `storyboard.md` is applied. One paragraph per line, so
the cut list can be found by searching.

| Segment | Speaker | Time | Words |
|---|---|---|---|
| Intro | Eric | 0:13 | 30 |
| Q1 Cloud compute | Ada | 0:23 | 53 |
| Q2 Data security | Ada | 0:28 | 65 |
| Q3 File permissions | Bobby | 0:28 | 65 |
| Q4 Representative data | Bobby | 0:32 | 74 |
| Q5 Synthetic data | James | 0:22 | 52 |
| Q6 Final model | James | 0:45 | 105 |
| Q7 Other techniques | Eric | 0:36 | 83 |
| Q8 Teamwork | Eric | 1:25 | 198 |
| Outro | Eric | 0:12 | 29 |

## Intro (0:15, ~35 words)

We're UCLuster Too: Ada, Bobby, Eric and James. We used tree models to predict which patients' E. coli infections resist the antibiotic co-amoxiclav, and ran them on UCL's Condenser cloud. <!-- locked -->
[screen: title card: "UCLuster Too", CIUK 2026 UCL challenge, Ada Ge, Bobby Ta, Eric Huang, James Loke]

## Q1: What is cloud compute? (0:25, ~60 words)

Cloud computing means renting computers over the internet, on demand, like AWS or Azure, instead of owning them. Condenser is UCL's private cloud. It gave us a virtual machine: a computer made in software, on hardware shared with other users. That's infrastructure as a service: UCL runs the hardware, we run our code. <!-- locked -->
[screen: lscpu on the VM, highlighting the "Hypervisor vendor" line (Ada has the screenshot, IP not shown)]
<!-- src: condenser.arc.ucl.ac.uk/about ("a private cloud platform for research computing at UCL", shared between tenancies), checked 29 Oct; README.md section 1 -->
<!-- drafted by A (25 Oct) and James (29 Oct); final by D, 29 Oct; AWS/Azure examples merged in from Ada's draft, 30 Oct -->

## Q2: What are key data security considerations for cloud computing? (0:35, ~80 words)

Cloud security is shared: we can't see the physical machine, so we rely on the provider. UCL walls each team's machines off from the others. We only get in through UCL's JupyterHub with an SSH key, connections are encrypted, and no keys or passwords go in our public repository. And Condenser isn't certified for sensitive data, so real patient records would need extra safeguards first. <!-- locked -->
[screen: condenser.arc.ucl.ac.uk/about with "not certified for the secure storage and processing of sensitive data" highlighted]
<!-- src: condenser.arc.ucl.ac.uk/about, checked 29 Oct: "All hardware resides in UCL facilities"; "Condenser is not certified for the secure storage and processing of sensitive data" (it adds that a secure platform can be built on it after consulting UCL's Information Governance Advisory Service). Each tenancy gets its own namespace and network (same page). README.md section 1 (JupyterHub over https, then ssh) -->
<!-- 30 Oct: opening line merged in from Ada's draft (we can't see the machine, so we rely on the provider) -->
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
[screen: the Q4 deck slide, with the chart in video/q4_our_data_vs_england_wales.png]
<!-- src: notes/2026-10-25-data-first-look.md and notes/2026-10-29-model-checks.md (ages 20-79; each ethnic group 17.6-21.1%, White the smallest at 17.6%); ONS Census 2021, England and Wales: White 81.7% (ethnicity-facts-figures.service.gov.uk) -->
<!-- chart made by D, 29 Oct, from the same numbers; C: replace it if you have your own -->
<!-- reworded by D, 29 Oct, after review: names White as the under-represented group, and "algorithmic bias" because the marking criteria use the term -->
<!-- plainer last sentence by D, 29 Oct, after an outside review flagged "that's how algorithmic bias arises" -->

## Q5: Why would we want to use synthetic data instead of actual patient data? (0:25, ~60 words)

Real patient records are sensitive health data, tightly protected by UK GDPR, and patients may not have agreed to this use. Synthetic data is designed to mimic real data without containing any real people, so we can build and test models, even on a shared cloud machine, with far less privacy risk.
[screen: the Q5 deck slide: "Synthetic data lets us test our models without using anyone's real medical records", with a real patient's record next to a synthetic one]
<!-- shortened by D, 29 Oct; UK GDPR and "far less privacy risk" as guide C puts it -->

## Q6: What is our final tree model, and why is it the most optimal? (0:45, ~105 words)

Only about a quarter of patients are resistant, so plain accuracy is misleading: calling everyone safe scores 76% but misses every resistant patient. So we weighted resistant cases more heavily and ranked models on balanced accuracy, which gives both groups equal weight.
[screen: video/q6_model_comparison.png, or the deck slide with it and the score table]

Random forests scored slightly higher, but that's two hundred trees voting, which you can't read like a single tree. Our depth-3 tree scored best of the single trees, a doctor can read it, and deeper trees overfit.
[screen: the Q6 tree deck slide, with the tree in video/q6_final_tree_readable.png]

Older patients are most at risk: resistance is 8% at ages 20 to 40, but 41% over 70. No other factor we tested beat random noise.
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
<!-- note: "beat random noise" means beating its shuffled copies in both the regression and the tree; the diagnosis (ICD chapter) tree alone scores 0.524 against 0.519, but its regression doesn't (outputs/risk_factors_summary.txt) -->

## Q7: What other modelling techniques could we use, and why? (0:36, 83 words)

Our decision tree performs well, but it divides age into stepped thresholds. Logistic regression is a strong alternative because it models risk rising continuously with age. It also produces odds ratios, which clinicians already use when evaluating patient risk. When we tested logistic regression, its output agreed with our tree. Each decade of age increased the odds of resistance by over 50 percent. Given a sample of one thousand patients and a single clear risk factor, a neural network would add unnecessary complexity. <!-- locked -->
[screen: the Q7 deck slide with 1.5 times the odds per 10 years of age and every model ranked by balanced accuracy]
<!-- src: "agreed with our tree": class-weighted logistic regression on age and imd, same split and folds, CV balanced accuracy 0.660 vs the tree's 0.659 (notes/2026-10-29-model-checks.md); the two give the same prediction for 86.8% of test patients (checked 30 Oct). "Over 50 percent": odds ratio per 10 years of age 1.54 in that fit, and 1.59 (1.44 to 1.76) adjusted for sex, surgery, deprivation and ethnicity (outputs/risk_factors_adjusted_odds_ratios.csv) -->
<!-- new wording by Eric, 30 Oct -->

## Q8: How did we work as a team? (1:25, 198 words)

To manage the project effectively, we paired up across two main tracks. For cloud setup and modelling, James developed the modelling script while Bobby kept the cloud machine updated. Bobby also tested a fresh install from our README and ran the final submission checks. For analysis and presentation, Ada set up the initial VM environment and README, before exploring the data to choose our evaluation metric. Alongside her, Eric tested each risk factor against random noise, ran the logistic regression, and led the slides and video. Every evening, we held a fifteen-minute catch-up to review our progress. We also stored our project plan, role guides, and work-session notes in a single GitHub repository. <!-- locked -->
[screen: the roles deck slide, then PLAN.md on GitHub, video/teamwork-log.md, and the commit history]

This structure helped us resolve several early technical issues. Initially, the server login details reached only one team member and omitted the username. We found the username in the organisers' access guide and shared the login details as instructed. Because the cloud machine did not have Git installed, we archived our scripts on GitHub for our records and fetched the files onto the machine using curl. Finally, our baseline model flagged no patients as resistant, which led us to evaluate our models using balanced accuracy. <!-- locked -->
<!-- src: PLAN.md sections 2-3; video/teamwork-log.md (25, 27 and 29 Oct). Ada's setup: teamwork log, 27 Oct. Eric's checks: teamwork log, 29 Oct -->
<!-- Bobby's sentence comes from notes/2026-10-29-vm-jobs-for-bobby.md, the work assigned to him for 29 to 30 Oct: confirm with him before recording -->
<!-- evening check-ins confirmed by Eric, 29 Oct; new wording by Eric, 30 Oct -->

## Outro (0:12, 29 words)

Our final model is a depth-3 class-balanced decision tree, and in our data, older age is the single clear predictor of resistance. Thank you for watching, from UCLuster Too. <!-- locked -->
[screen: closing card: UCLuster Too, the four names, and github.com/adellama75/cluster-challenge-ucl]
<!-- Eric, 30 Oct; "single clear predictor": outputs/risk_factors_summary.txt -->
