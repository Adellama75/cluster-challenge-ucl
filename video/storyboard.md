# Storyboard and recording plan

Target length 4:45 to 4:55, hard limit 5:00, saved as MP4. Narration is in `script.md`: about 670
spoken words, about 4:47 at 140 words per minute. Each segment is recorded as its own clip by its owner,
and Eric (D) edits.

## Storyboard

Times are from the word counts at 140 words per minute.

| # | Segment | Speaker | On screen | Starts | Length |
|---|---|---|---|---|---|
| 1 | Intro | Eric | Title card: "UCLuster Too", CIUK 2026 UCL challenge, Ada Ge, Bobby Ta, Eric Huang, James Loke | 0:00 | 0:13 |
| 2 | Q1 Cloud compute | Eric | VM terminal: `lscpu` with the "Hypervisor vendor" line highlighted | 0:13 | 0:21 |
| 3 | Q2 Data security | Eric | `lscpu` "Vulnerabilities" lines, then condenser.arc.ucl.ac.uk/about with "not certified for the secure storage and processing of sensitive data" highlighted | 0:34 | 0:33 |
| 4 | Q3 File permissions | Bobby | `ls -l` of the data file before (`-rw-r--r--`) and after (`-rw-------`) | 1:07 | 0:28 |
| 5 | Q4 Representative data | Ada | `video/q4_our_data_vs_england_wales.png` | 1:35 | 0:30 |
| 6 | Q5 Synthetic data | Ada | Text slide: "Synthetic data: real patterns, no real patients" | 2:05 | 0:22 |
| 7 | Q6 Final model | James | `outputs/balanced_accuracy_vs_depth_age_imd.png`, then `video/q6_final_tree_readable.png` from "Random forests", then the left panel of `outputs/risk_factors_vs_noise.png` from "Older patients" | 2:27 | 0:46 |
| 8 | Q7 Other techniques | Ada | `outputs/risk_factors_adjusted_odds_ratios.png` | 3:13 | 0:26 |
| 9 | Q8 Teamwork | Eric | `PLAN.md` roles table on GitHub, `video/teamwork-log.md`, then the repo's commit history | 3:39 | 0:57 |
| 10 | Outro | Eric | Closing card: team name, the four names, github.com/adellama75/cluster-challenge-ucl | 4:36 | 0:10 |
| | **Total** | | | | **4:46** |

Numbers and words such as "76%" or "chmod 600" take longer to say than to count, and each cut
between clips adds a moment, so expect the edit to come out nearer 4:55. If Bobby can't record Q3,
Eric reads it over Bobby's screen recording (guide A allows this).

## Screens to prepare before recording

- [ ] Q1, Q2: `lscpu` on the VM, "Hypervisor vendor" and the "Vulnerabilities" lines (Bobby). Terminal
      font at 20 pt or more. Crop out the prompt if it shows the host name or IP. If any
      Vulnerabilities line says "Vulnerable" rather than "Mitigation" or "Not affected", tell Eric:
      the lscpu sentence in Q2 is then cut.
- [ ] Q2: screenshot of https://condenser.arc.ucl.ac.uk/about at 150% zoom with the sentence above
      highlighted (Eric).
- [ ] Q3: `cat notes/permissions-before.txt notes/permissions-after.txt` in a large-font terminal, or
      Bobby's screenshots from 27 Oct if he took them (IP cropped out).
- [x] Q4: `video/q4_our_data_vs_england_wales.png`, 1920 × 1080, ready.
- [ ] Q5 text slide, title card and closing card: made in the editor (Eric).
- [x] Q6: `video/q6_final_tree_readable.png` is the final tree at 1920 × 1080 with large text. The
      tree in `outputs/` is 3285 px wide, too small to read in a video. The other Q6 and Q7 figures are
      in `outputs/`. Open each one full screen and crop to the plot.
- [ ] Q8: GitHub pages for `PLAN.md`, the teamwork log and the commit list, at 150% zoom (Eric).

Never on screen: IP addresses, the SSH key or anything in `~/.ssh`, the welcome emails, a JupyterHub
URL that contains a token, passwords.

## Recording

- One clip per segment, named by number, segment and speaker (`04_q3_bobby.mp4`). Send clips to Eric
  by Friday 12:00 so the edit is done by 18:00.
- Before recording, time one read-through of your segment. If it runs more than 3 seconds over its
  length above, take your segment's line from the cut list before you record, not in the edit.
- Tool: Panopto, Teams or Clipchamp. Clipchamp comes with Windows 11 and records screen and
  microphone. Export a 10-second test first and check that it comes out at 1080p and as MP4.
- Before the first real take, record 20 seconds of screen and voice and listen back on headphones.
- Settings: 1920 × 1080, notifications off, terminal font 20 pt or more, browser zoom 150%. Use a
  headset or a phone microphone close to your mouth, in a quiet room.
- Read from `script.md`, and retake a clip rather than editing around a stumble.

## Edit and submit (Friday, by 18:00)

1. Clips in storyboard order, title card at the start, closing card at the end, plain cuts.
2. Check the total: 4:45 to 4:55, never over 5:00. If it runs over, use the cut list.
3. Export MP4 at 1080p.
4. Watch the whole file once: audio level even across speakers, every screen readable, nothing private
   visible.
5. Upload to the team's CIUK Challenge folder and post the link in the group chat.

## Cut list, in order, if a segment or the edit runs long

Each cut is a whole sentence or clause, so what's left still reads correctly.

| Segment | Cut | Saves |
|---|---|---|
| Q6 | "We compared tree types and depths." (the depth plot shows it) | 3 s |
| Q3 | "Our script's outputs are closed to other users too." | 4 s |
| Q7 | ", and gives odds ratios clinicians already use" | 3 s |
| Q2 | "lscpu lists the fixes for Spectre-style bugs that could let one machine spy on another." Drop the `lscpu` Vulnerabilities screen with it | 6 s |

Don't cut Q8. Teamwork carries 15 marks.
