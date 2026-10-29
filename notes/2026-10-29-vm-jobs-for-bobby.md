# VM jobs left for A (Bobby), 29 to 30 Oct

Everything here needs the Condenser VM (JupyterHub terminal, then `ssh cc@<server IP>`). Do 1 to 4
before Q1 to Q3 are recorded, and 7 by Friday 18:00. Never paste the IP, the key or login details
into the repo or the group chat.

## 1 Update the VM copy

What changed on 29 Oct:

- `src/amr_trees.py` gained docstrings. Nothing else changed: a rerun gives byte-identical results.
- `src/risk_factors.py` is new (the risk-factor screen).
- `README.md` documents the new script.
- The comment line in `requirements.txt` changed. The pinned versions didn't, so the venv stays as it is.
- `video/` and `notes/` changed.

The "Everything again" block in `guides/A-vm-environment.md` updates all of it and leaves `outputs/`,
`data/` and `.venv/` alone. Or fetch just the files the markers look at:

```bash
cd ~/cluster-challenge-ucl
R=https://raw.githubusercontent.com/adellama75/cluster-challenge-ucl/main
for f in README.md requirements.txt src/amr_trees.py src/risk_factors.py; do
  curl -fsSL -o $f.new $R/$f && mv $f.new $f && head -1 $f   # a failed download leaves the old file
done
```

## 2 Run the risk-factor screen

It takes about 2 minutes on a laptop and adds 6 files to `outputs/` (25 in all), all named
`risk_factors_*`.

```bash
cd ~/cluster-challenge-ucl && source .venv/bin/activate
python src/risk_factors.py --data data/dig_health_hub_amr.csv --out outputs
chmod 750 outputs && chmod 640 outputs/* outputs/.gitkeep   # outputs/* skips the hidden .gitkeep
```

The last lines should read "beats noise on its own: Age", with the same numbers as
`outputs/risk_factors_summary.txt` on GitHub (age 0.708 and 0.685; odds ratio 1.59 per 10 years).
Only the version line should differ.

## 3 Screens for Q1 and Q2

Terminal font 20 pt or more. Crop the prompt out if it shows the host name or IP. Send both to Eric.

```bash
lscpu | grep -i hypervisor        # Q1: "Hypervisor vendor" line
lscpu | grep -i -A20 vulnerab | cut -c1-90   # Q2: the Spectre-style fixes
```

Check the Vulnerabilities lines say "Mitigation" or "Not affected". If any say "Vulnerable", tell
Eric: Q2 then drops its lscpu sentence.

## 4 ACL check for Q3

Q3 has one optional line waiting on this: "We also checked no extra access rules were set." On 27 Oct
both lines of `notes/permissions-after.txt` ended in `.` (an SELinux label only); `ls -l` shows `+`
there when an ACL is set. Confirm it:

```bash
cd ~/cluster-challenge-ucl
getfacl data data/dig_health_hub_amr.csv
ls -ld data; ls -l data          # "." after the mode bits is fine; "+" means an ACL exists
```

If `getfacl` lists only the `user::`, `group::` and `other::` lines and `ls` shows no `+`, tell Eric
and he can add that line to Q3. Also record Q3 yourself (about 30 s, script in
`video/script.md`), or send a screen recording of the before and after `ls -l` and Eric will read
the lines over it.

## 5 Optional: make GitHub's outputs/ match the VM

GitHub's `outputs/` come from laptop runs. The `amr_trees.py` summary says python 3.14.4 and the
`risk_factors.py` one says 3.12.10. The numbers should match the VM's: the 27 Oct VM run did for
`amr_trees.py`, and step 2 shows it for `risk_factors.py`. To make the copies match, download
the VM's `outputs/` (README section 5), unpack it into the repo on a laptop, check that only the
version lines changed, and push.

## 6 Fresh-download test (guide A, step 12)

Do this in its own folder. Run from `~`, the README's `mv cluster-challenge-ucl-main
cluster-challenge-ucl` would put the copy inside the real project, and the data and run steps would
overwrite the real data and outputs.

```bash
mkdir -p ~/readme-test && cd ~/readme-test
# the README word for word: "From scratch", section 3 (data), section 4 (both scripts)
cd ~ && rm -r ~/readme-test
```

Anything you had to do that isn't written down goes into the README.

## 7 Final check, Friday by 18:00

```bash
cd ~/cluster-challenge-ucl
ls README.md src/amr_trees.py src/risk_factors.py requirements.txt data/dig_health_hub_amr.csv
ls outputs | wc -l                                             # 25
find data outputs -perm -o=r                                   # prints nothing if nothing is world-readable
R=https://raw.githubusercontent.com/adellama75/cluster-challenge-ucl/main
for f in README.md requirements.txt src/amr_trees.py src/risk_factors.py; do
  [ "$(curl -sL $R/$f | md5sum)" = "$(md5sum < $f)" ] && echo "same as GitHub: $f" || echo "DIFFERENT: $f"
done
```

This compares against GitHub directly. A laptop on Windows can check files out with CRLF line
endings, so its `md5sum` would differ even when the files are the same. GitHub can serve the old
copy for a few minutes after a push, so rerun the loop before trusting a DIFFERENT.
