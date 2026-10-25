# Video script (5:00, about 700 words)

Draft narration, updated by `/script` after each work session. Budgets are at 140 words per minute.
Mark finished lines with `<!-- locked -->` so `/script` leaves them alone.

## Intro (0:15, ~35 words)

We're UCLuster Too: Ada, Bobby, Eric and James. Our task was to predict which patients' E. coli
infections resist the antibiotic co-amoxiclav, using tree models, and to run it all on UCL's Condenser
cloud platform.
[screen: title card with team name and members]

## Q1, Q2: cloud compute and data security (0:55, ~130 words)

What is cloud compute? What are the key data security considerations for cloud computing?

Cloud computing means renting computers over the internet instead of owning them. Our "machine" on
Condenser is a virtual machine: a slice of a bigger physical server that UCL runs, which we got in
minutes and never had to touch.
[screen: lscpu on the VM, highlighting the "Hypervisor vendor" line — TODO(A): capture Monday]
Sharing a server is also the security problem. Other people's machines run on the same hardware, so
access has to be locked down: our own login, no passwords or keys in our public code repository, and
data files only we can read. Even the processor needs protecting: lscpu lists the patches for
Spectre-style bugs, which could let one virtual machine spy on another through the shared CPU.
[TODO(D): data in transit and at rest (SSH, encryption), and where the data physically lives]
<!-- src: README.md section 2; lscpu "Vulnerabilities" section -->
<!-- draft by A from the 25 Oct session; D owns this segment -->

## Q3: file permissions (0:30, ~70 words)

The data file was world-readable. Why is this not desirable? Did we change it, how and why?

When we downloaded the data, it came out readable by every user on the machine.
[TODO(A): the VM's actual `ls -l` before, from notes/permissions-before.txt]
On a shared cloud machine that means anyone with an account could read patient-style records, so we
restricted it to our own account with `chmod 600`, and our script creates its outputs without access
for other users.
[screen: ls -l before and after]
[TODO(A): after checking on the VM, add one clause if true: no extra access via ACLs (`getfacl`, a `+` after the mode bits)]
<!-- src: notes/2026-10-25-ada-setup.md -->

## Q4, Q5: data (0:55, ~130 words)

Why a representative data set for machine learning? Why synthetic data instead of real patient data?

A model only learns the people it's shown. Our data covers ages 20 to 79, so it can't tell us anything
about children or anyone over 80. And the ethnic groups are split almost evenly, about a fifth each,
while in England and Wales about 82% of people are White. A model trained on unrepresentative data
can be confidently wrong for the groups it rarely saw.
[screen: bar chart of age range and ethnicity mix — TODO(C): make it]
<!-- src: notes/2026-10-25-ada-setup.md (data), 2021 Census for the 82% -->

[TODO(C): Q5, synthetic data]

## Q6, Q7: model and alternatives (1:10, ~165 words)

Our final tree model and why it's the best. Who is more at risk from AMR? What other modelling
techniques could we use, and why?

Age is by far the biggest risk factor. Resistance rises from about 8% in people aged 20 to 40 to about
41% in people over 70, and every tree we built splits on age first, at about 48. Deprivation adds very
little.
[screen: outputs/best_tree_age_imd.png]
Our first attempt taught us something: the tree with the best ranking score flagged nobody as resistant,
because only a quarter of patients are. So we chose models on balanced accuracy and weighted the classes.
[TODO(B): final model and numbers once frozen on Wednesday; draft: depth-3 random forest catches 73% of
resistant patients in the test set]
<!-- src: outputs/run_summary_age_imd.txt, notes/2026-10-25-ada-setup.md -->

[TODO(C): Q7, other techniques]

## Q8: how we worked as a team (1:00, ~140 words)

How we worked together and the challenges we overcame. Evidence: `teamwork-log.md`.

We kept the same four roles that worked in the Durham challenge: one person on the cloud machine and
environment, one on the script, one on data and evaluation, and one on the video. A shared repository
held a plan, a step-by-step guide for each role, and this script, which we updated after every work
session.
[TODO(D): two or three concrete problems from teamwork-log.md]

## Outro (0:15, ~35 words)
