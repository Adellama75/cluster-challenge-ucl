# Storyboard and recording plan

Target length 4:45 to 4:55, hard limit 5:00, saved as MP4. Narration is in `script.md`: about 662
spoken words, about 4:43 at 140 words per minute. Each segment is recorded as its own clip by its owner,
and Eric (D) edits.

## Storyboard

Times are from the word counts at 140 words per minute.

| # | Segment | Speaker | On screen | Starts | Length |
|---|---|---|---|---|---|
| 1 | Intro | Eric | Title card: "UCLuster Too", CIUK 2026 UCL challenge, Ada Ge, Bobby Ta, Eric Huang, James Loke | 0:00 | 0:13 |
| 2 | Q1 Cloud compute | Eric | VM terminal: `lscpu` with the "Hypervisor vendor" line highlighted | 0:13 | 0:21 |
| 3 | Q2 Data security | Eric | condenser.arc.ucl.ac.uk/about with "not certified for the secure storage and processing of sensitive data" highlighted | 0:34 | 0:26 |
| 4 | Q3 File permissions | Bobby | `ls -l` of the data file before (`-rw-r--r--`) and after (`-rw-------`) | 1:00 | 0:28 |
| 5 | Q4 Representative data | Ada | `video/q4_our_data_vs_england_wales.png` | 1:28 | 0:32 |
| 6 | Q5 Synthetic data | Ada | Text slide: "Synthetic data is made to mimic real data, with no real people in it" | 2:00 | 0:22 |
| 7 | Q6 Final model | James | `video/q6_model_comparison.png` with the score table, then `video/q6_final_tree_readable.png` from "Random forests", then resistance by age and `video/q6_risk_factors_vs_noise.png` from "Older patients" (one deck slide each) | 2:22 | 0:46 |
| 8 | Q7 Other techniques | Ada | `video/q7_odds_ratios.png` with the two scores | 3:08 | 0:28 |
| 9 | Q8 Teamwork | Eric | `PLAN.md` roles table on GitHub, `video/teamwork-log.md`, then the repo's commit history | 3:36 | 0:57 |
| 10 | Outro | Eric | Closing card: team name, the four names, github.com/adellama75/cluster-challenge-ucl | 4:33 | 0:10 |
| | **Total** | | | | **4:43** |

Every segment also has a slide in the team deck: 13 slides in storyboard order, with each segment's
narration in its speaker notes. Record over the slide, or over the screens above where you have
them. Q4 and the Q6 tree are full-frame figures.

Numbers and words such as "76%" or "chmod 600" take longer to say than to count, and each cut
between clips adds a moment, so expect the edit to come out nearer 4:52. If Bobby can't record Q3,
Eric reads it over Bobby's screen recording (guide A allows this).

## Screens to prepare before recording

- [ ] Q1: `lscpu` on the VM, "Hypervisor vendor" line (Bobby). Terminal font at 20 pt or more. Crop
      out the prompt if it shows the host name or IP.
- [ ] Q2: screenshot of https://condenser.arc.ucl.ac.uk/about at 150% zoom with the sentence above
      highlighted (Eric).
- [ ] Q3: `cat notes/permissions-before.txt notes/permissions-after.txt` in a large-font terminal, or
      Bobby's screenshots from 27 Oct if he took them (IP cropped out).
- [x] Q4: `video/q4_our_data_vs_england_wales.png`, 1920 × 1080, ready.
- [x] Title card, Q5 slide and closing card: in the team slide deck (Eric shares the link, or exports
      it as PDF or PowerPoint).
- [x] Q6 and Q7: `video/q6_model_comparison.png`, `video/q6_final_tree_readable.png` (the final tree
      with plain questions, 1920 × 1080), `video/q6_risk_factors_vs_noise.png` and
      `video/q7_odds_ratios.png`, each with the result the narration names in colour. The deck slides
      pair them with the scores. The tree in `outputs/` is 3285 px wide, too small to read in a video.
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
- No background music under the narration.

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
| Q3 | "Our script's outputs are closed to other users too." | 4 s |
| Q7 | ", and it gives odds ratios, which clinicians already use" | 4 s |

Two earlier cuts are already applied in `script.md`: Q6 "We compared tree types and depths." and the
Q2 lscpu sentence.

Don't cut Q8. Teamwork carries 15 marks.
