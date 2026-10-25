# Sun 25 Oct, Ada (A): repo setup, draft script, first look at the data

Numbers below are from `data/dig_health_hub_amr.csv` (local copy) and `outputs/run_summary_age_imd.txt`.

## Data
- 1000 patients, no missing values, all E. coli. 24.1% resistant to co-amoxiclav.
- Age 20 to 79 only (no children, nobody 80+). Sex 50.1% male.
- Ethnicity split almost evenly: Black 21.1%, Other 20.9%, Asian 20.7%, Mixed 19.7%, White 17.6%.
  Far from the real population (England and Wales 2021 Census: about 82% White), so the synthetic
  data is not representative by ethnicity.
- Resistance by age: 8.4% (20–40), 25.9% (41–60), 37.5% (61–70), 40.7% (71–79).
- Resistance by imd quintile 1–5: 26.4%, 20.7%, 20.0%, 28.9%, 24.6%. No clear trend.
- curl saved the data file as `-rw-rw-r--` (world-readable) because the laptop's umask is 002.
  Changed to `chmod 600`.

## Draft model results (seed 42)
- First version picked the best tree by ROC AUC and chose a tree that flagged **no** resistant patients
  (recall 0.000): with 24% resistant, an unweighted tree's predicted risk never reaches 50%.
  Switched model selection to cross-validated balanced accuracy and added class-balanced trees.
- Best single tree: class-balanced decision tree, depth 3. First split at age 48.5. Test recall on
  resistant 0.650, ROC AUC 0.685.
- Best overall: random forest, depth 3. Test recall 0.733, ROC AUC 0.718. Importance: age 0.91, imd 0.09.

## Team
- Made the public repo, invited Bobby, Eric and James; wrote the A–D plan and per-role guides.
- Roles so far: A Ada, B Bobby. C and D between Eric and James.
