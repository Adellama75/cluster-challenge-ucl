# Role A: VM and environment lead, editor

You own the marks that are easiest to lose by accident: accessing Condenser (5, and it weights the whole
technical score), the Python environment (5), the ReadMe (10) and file permissions and storage (10).
Video: Q3, about 30 seconds on file permissions.

Run `/script` after each session, with a line of notes.

## Monday: get in and set up

1. **Watch for two emails** (to the captain): an automated one with the login for the main interface,
   then one from **ARC Education** with your server details. Never paste these details into the repo or
   the group chat.
2. **Log in** as the emails describe. Note the exact steps for the README (section 2), without
   passwords or IPs.
3. **Check what's there:**
   ```bash
   python3 --version; which git curl vim; df -h ~; echo $SHELL
   ```
   *Interpret:* the Python version decides which package versions install. Below 3.11, pandas 3 won't
   install, but older pandas works fine with our script.
4. **Install micro** (no root needed; it lands in the current folder):
   ```bash
   mkdir -p ~/bin && cd ~/bin && curl https://getmic.ro | bash && cd ~
   export PATH="$HOME/bin:$PATH"   # also add this line to ~/.bashrc
   ```
5. **Get the code.** Condenser has **no git** (and we can't install it), so download the repo as a
   tarball with curl:
   ```bash
   cd ~ && curl -L -o repo.tar.gz https://github.com/adellama75/cluster-challenge-ucl/archive/refs/heads/main.tar.gz
   tar xzf repo.tar.gz && mv cluster-challenge-ucl-main cluster-challenge-ucl && rm repo.tar.gz
   cd cluster-challenge-ucl
   ```
   To refresh single files later, see "Updating the VM without git" below.
6. **Create the environment:**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install --upgrade pip && pip install -r requirements.txt
   pip freeze | grep -iE '^(pandas|scikit-learn|matplotlib|numpy)=='
   ```
   Put the exact versions from the last command into `requirements.txt` (replacing the TODO line). That
   pins the environment to what the VM really has, and keeps it to only what we import.
7. **Get the data and record the permissions *before* changing them** (this is the Q3 evidence):
   ```bash
   mkdir -p data && cd data
   curl -L -o dig_health_hub_amr.csv "https://drive.google.com/uc?export=download&id=1KeMv2GaR824SNW2_KDDfCrcSpIObjui0"
   ls -l dig_health_hub_amr.csv | tee ../notes/permissions-before.txt
   ```
   *Interpret:* something like `-rw-r--r--` means **everyone** on the machine can read it (the last `r`).
   On a shared cloud VM that includes other users and any compromised account.
   Also check if the brief's copy on the VM (if one was pre-placed) is world-readable: `ls -l` wherever it is.
8. **Fix the permissions and record the result:**
   ```bash
   chmod 600 dig_health_hub_amr.csv     # owner read/write only
   chmod 700 ..                          # or 750 if teammates share the account's group
   ls -l dig_health_hub_amr.csv | tee ../notes/permissions-after.txt && cd ..
   ```
   Take a screenshot of before and after for the video.
9. **Run the script once** (A↔B pair on this):
   ```bash
   python src/amr_trees.py --data data/dig_health_hub_amr.csv --out outputs
   ls -l outputs
   ```
   *Interpret:* about 20 files; the last lines printed are the best tree, the best model and the risk
   factors. Files should show `-rw-r-----` (not readable by others): the script sets that itself.

## Updating the VM without git

The VM has no git, so the repo on GitHub and the copy on the VM are two separate things. The rule:
**edit on the laptop, push to GitHub, then curl the changed file onto the VM.** Never edit the VM copy
directly, or the two drift apart and the README test will fail.

Pull one file (GitHub raw URL; the path after `main/` is the path in the repo):
```bash
cd ~/cluster-challenge-ucl
R=https://raw.githubusercontent.com/adellama75/cluster-challenge-ucl/main
curl -sL -o src/amr_trees.py   $R/src/amr_trees.py
curl -sL -o README.md          $R/README.md
curl -sL -o requirements.txt   $R/requirements.txt
```
Then check it really arrived (a wrong URL silently saves a "404: Not Found" text file):
```bash
head -3 src/amr_trees.py        # should be Python, not "404"
```

Pull everything again (safe: `data/`, `.venv/` and `outputs/` are not in the tarball):
```bash
cd ~ && curl -L -o repo.tar.gz https://github.com/adellama75/cluster-challenge-ucl/archive/refs/heads/main.tar.gz
tar xzf repo.tar.gz && cp -r cluster-challenge-ucl-main/. cluster-challenge-ucl/ && rm -r cluster-challenge-ucl-main repo.tar.gz
```

Getting results **off** the VM (there's no push): pack `outputs/` and download it through the
JupyterLab file browser (right-click the file, Download). If the file browser can't see your home
folder, copy the archive into the folder it does show first.
```bash
cd ~/cluster-challenge-ucl && tar czf outputs-$(date +%F).tar.gz outputs notes
```
Then on the laptop, unpack into the repo and commit, so the final `outputs/` on GitHub matches the VM.

## Tuesday to Thursday: README and checks

10. **Fill in the `[Mon: …]` gaps in `README.md`** (login steps, Python version, project path) and
    check every command matches what you actually ran. Every command must be copy-pasteable.
11. **After B's final script (Wednesday 18:00), rerun on the VM** so `outputs/` matches the final code.
12. **Thursday, fresh-download test:** in a new folder on the VM, follow the README word for word
    (tarball, venv, data, run). If you have to do anything not written down, add it to the README.
    ```bash
    mkdir -p ~/readme-test && cd ~/readme-test
    # now the README's "From scratch" block, exactly as written
    ```
    Delete `~/readme-test` afterwards so the home folder stays tidy.
13. **File-name and storage check:** everything the script makes is in `outputs/` with names that say
    what they are; no stray files in the home folder; `ls -l` on data and outputs shows nothing
    world-readable.

## Friday by 18:00: final VM check

- [ ] README, `src/amr_trees.py`, `data/dig_health_hub_amr.csv`, `outputs/` with the final run all on the VM
- [ ] VM copy of `src/amr_trees.py` and `README.md` is identical to GitHub `main` (`md5sum` both sides)
- [ ] `requirements.txt` pinned to the VM's versions
- [ ] `ls -l` shows no world-readable data or outputs
- [ ] Team name in the README

## Video: Q3 (about 70 words)

What to cover: the file was world-readable (show `permissions-before.txt`); why that's bad (patient-like
data, shared machine, least privilege); what we changed (`chmod 600`, show the after); that the script
also writes outputs as not world-readable. If you'd rather not be on camera, D can voice this over your
screen recording.
