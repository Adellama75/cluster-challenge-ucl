# Storyboard and recording plan

Target length 4:45 to 4:55, hard limit 5:00, saved as MP4. Narration is in `script.md`: about 660
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
| 5 | Q4 Representative data | Ada | Deck slide with `video/q4_our_data_vs_england_wales.png` | 1:28 | 0:32 |
| 6 | Q5 Synthetic data | Ada | Deck slide: "Synthetic data lets us test our models without using anyone's real medical records", a real patient's record next to a synthetic one | 2:00 | 0:22 |
| 7 | Q6 Final model | James | `video/q6_model_comparison.png` with the score table, then `video/q6_final_tree_readable.png` from "Random forests", then resistance by age and `video/q6_risk_factors_vs_noise.png` from "Older patients" (one deck slide each) | 2:22 | 0:45 |
| 8 | Q7 Other techniques | Ada | Deck slide: 1.5 times the odds per 10 years of age, and every model we tried ranked by balanced accuracy | 3:07 | 0:28 |
| 9 | Q8 Teamwork | Eric | `PLAN.md` roles table on GitHub, `video/teamwork-log.md`, then the repo's commit history | 3:35 | 0:58 |
| 10 | Outro | Eric | Closing card: team name, the four names, github.com/adellama75/cluster-challenge-ucl | 4:33 | 0:10 |
| | **Total** | | | | **4:43** |

Every segment also has a slide in the team deck: 13 slides in storyboard order, with each segment's
narration in its speaker notes. The deck is in this folder as `UCLuster-Too-video-slides.pptx`
(notes in Presenter View; slides are images, so edit the deck, not the file) and
`UCLuster-Too-video-slides.pdf`. Record over the slide, or over the screens above where you have
them.

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
- [x] Q4: the deck slide, with the chart in `video/q4_our_data_vs_england_wales.png`.
- [x] Title card, closing card, and slides for every question: in `video/UCLuster-Too-video-slides.pptx`
      and `.pdf`. Q1 and Q2 draw the cloud and our login route, Q3 shows the permissions before and
      after above the real `ls -l` lines, Q5 compares a real record with a synthetic one, and Q8 shows
      the two pairs and the three problems.
- [x] Q6: `video/q6_model_comparison.png`, `video/q6_final_tree_readable.png` (the final tree with
      plain questions and a 55-year-old's path) and `video/q6_risk_factors_vs_noise.png`,
      each with the result the narration names in colour. The tree in `outputs/` is 3285 px wide, too
      small to read in a video.
- [x] Q7: the deck slide shows 1.5 times the odds per 10 years of age and every model we tried, ranked.
      `video/q7_odds_ratios.png` is a spare with the full odds-ratio table.
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
