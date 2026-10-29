# Video script (5:00, about 700 words)

Draft narration, updated by `/script` after each work session. Budgets are at 140 words per minute.
Mark finished lines with `<!-- locked -->` so `/script` leaves them alone.

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

We're UCLuster Too: Ada, Bobby, Eric and James. Our task was to predict which patients' E. coli
infections resist the antibiotic co-amoxiclav, using tree models, and to run it all on UCL's Condenser
cloud platform.
[screen: title card with team name and members]

## Q1: What is cloud compute? (0:25, ~60 words)

Cloud computing means renting computers over the internet instead of owning them. 

Condenser is UCL cloud computing service and provides a way for us to rent a virtual machine (which is a software based computer that runs on shared physical hardware) to run our code. We can access it from anywhere and we don't have to worry about maintaining the hardware. 
[screen: lscpu on the VM, highlighting the "Hypervisor vendor" line — TODO(A): capture Monday]
<!-- src: README.md section 1; lscpu output -->
<!-- draft by A from the 25 Oct session; D owns this segment -->

## Q2: What are key data security considerations for cloud computing? (0:35, ~80 words)

In the cloud, our data sits on someone else's hardware, so security is shared between UCL and us.

**Isolation.** The hypervisor (the software that splits one physical server into many virtual
machines) walls our virtual machine off from other teams' machines, but they all
share the same physical processor. lscpu lists the patches for Spectre-style bugs that could otherwise
let one machine spy on another.

**Access.** Our server is only reachable through UCL's JupyterHub, with an SSH key, and no passwords
or keys ever go into our public repository.

**Data.** SSH encrypts everything in transit, and inside the machine only our account can read the
data file.
[screen: lscpu "Vulnerabilities" section]
[TODO(D): optional, if time: data at rest (is the disk encrypted?) and where it physically lives (UK, UCL)]
<!-- src: README.md section 1; lscpu "Vulnerabilities" section; ARC Slack 26 Oct ("you need the terminal in the interface") -->
<!-- draft by A from the 25 Oct session; D owns this segment -->

## Q3: The data file was world-readable. Why is this not desirable? Did we change it, how and why? (0:30, ~70 words)

When the data landed on our machine, it was readable by every user: `-rw-r--r--`.
On a shared cloud machine that means anyone with an account could read patient-style records. Patient
data is confidential: only people with the right authorisation should be able to read it, and even
though ours is synthetic, we treated it as real. So we moved it into a data folder only we can open and restricted the file to our own account with
`chmod 600`, giving `-rw-------`. Our script creates its outputs without access for other users.
[screen: ls -l before and after (ucl-evidence/q3-perms-*.png; crop out the IP)]
[TODO(A): after checking on the VM, add one clause if true: no extra access via ACLs (`getfacl`, a `+` after the mode bits)]
<!-- src: notes/2026-10-25-data-first-look.md; VM session 27 Oct (ls -l before/after) -->

## Q4: Why would you want a representative data set for machine learning? (0:30, ~70 words)

A model is only useful if it generalises: if what it learned from its training data still holds for
the real patients it will be used on. That only works if the training data looks like those patients.
Ours doesn't quite: it covers ages 20 to 79, so it says nothing about children or anyone over 80, and
its ethnic groups are about a fifth each, while about 82% of people in England and Wales are White.
A model trained on it could perform well in testing and still be wrong in the real world, especially
for the groups it rarely saw.
[screen: bar chart of age range and ethnicity mix — TODO(C): make it]
<!-- src: notes/2026-10-25-data-first-look.md (data), 2021 Census for the 82% -->

## Q5: Why would we want to use synthetic data instead of actual patient data? (0:25, ~60 words)

Real patient data is confidential and sensitive. Patients may not have agreed to its use, and data
protection law limits who can see and share it. Synthetic data is generated to copy the statistical
patterns of real data, but contains no real people. So we can build and test models that reflect real
patients, even on a shared cloud machine, without risking anyone's privacy.

## Q6: What is our final tree model, and why is it the most optimal? (0:45, ~105 words)

Most patients in our data are not resistant, so plain accuracy is misleading: a model that calls
everyone safe looks accurate while missing every patient we actually care about. So we weighted the
resistant cases more heavily and compared models on balanced accuracy, which scores both groups fairly.

We compared single decision trees with ensembles of trees, including a random forest, at different
depths. The random forest predicted slightly better, but it's hundreds of trees voting, so no one can
follow its reasoning. Our final model is a single class-balanced decision tree of depth 3: it can be
drawn and checked by a doctor, and deeper trees started to overfit.
[screen: outputs/balanced_accuracy_vs_depth_age_imd.png]

The tree splits on age first, and age drives almost every decision: older patients are the ones most
at risk. Deprivation barely matters, and the random forest agrees.
[screen: outputs/best_tree_age_imd.png]
<!-- src: VM run 29 Oct (outputs/run_summary_age_imd.txt, tree_balanced_depth3_age_imd.txt, model_comparison.csv) -->
<!-- CV balanced accuracy, balanced tree: 0.659 at depth 3, falling to 0.584 at depth 8 -->
<!-- test: tree balanced acc 0.622, recall 0.650, AUC 0.685; forest balanced acc 0.675, recall 0.733, AUC 0.718 -->
<!-- resistance-by-age figures (8% at 20-40, 41% over 70) moved out for time; source notes/2026-10-25-data-first-look.md -->
<!-- note: the depth-3 tree's 61.5-64.5 branch predicts susceptible, so "above 48 resistant" is a simplification -->
<!-- note: a depth-1 tree has the same CV score (0.655 vs 0.659) and higher test recall (0.733) -->
<!-- feature importance (random forest): age 0.91, imd 0.09; first split at age 48 -->

## Q7: What other modelling techniques could we use, and why? (0:25, ~60 words)

We could use logistic regression: it fits a smooth rise in risk with age instead of sharp cut-offs,
and gives odds ratios that clinicians already understand. A neural network such as an MLP is a bad fit
here: a thousand patients and two fields is far too little data for it, and it would be even harder
to explain than a random forest. It would only be worth trying with much more data and many more fields.

## Q8: How did we work as a team? (1:00, ~140 words)

How we worked together and the challenges we overcame. Evidence: `teamwork-log.md`.

We split the work into four roles, each with one owner. Bobby ran the cloud machine, the environment
and the ReadMe; James wrote the model script; Ada explored the data and chose how to evaluate the
models; and Eric led the video. We paired up to cover each other, machine with script and data with
video, and checked in for fifteen minutes each evening. Everything lived in one shared GitHub
repository: a plan, a guide for each role, and a log of every work session.
[screen: PLAN.md roles table, then video/teamwork-log.md]

We hit a few problems along the way. Login details arrived for only one of us, without the username,
so we shared that login as instructed and found the username in the organisers' access guide. The
machine has no git, so we edited on our laptops, pushed to GitHub and downloaded files with curl. And
our first model flagged nobody as resistant, which is why we switched to balanced accuracy.
<!-- src: PLAN.md sections 2-3; video/teamwork-log.md (25 and 27 Oct) -->
<!-- roles: A Bobby, B James, C Ada, D Eric -->
<!-- TODO: confirm the evening check-ins actually happened before recording -->
<!-- TODO: about 150 words, 65 s; trim the pairs sentence if over time -->


## Outro (0:10, ~25 words)
