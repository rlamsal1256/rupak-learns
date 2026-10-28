---
title: "Trimming a skill with evals"
date: 2026-10-28
draft: false
tags: ["claude", "ai", "skills", "evals"]
---

**TL;DR:** I cut my triage-review skill from 994 to 730 words (27% shorter) with no loss in quality. Tested on five replayed PR reviews, the trimmed skill passed 98–100% of checks, as well as the full skill. The same method works for any skill.

## Background

- **Skill:** a `SKILL.md` file of instructions that Claude Code loads when a task matches it.
- **triage-review:** my skill for handling reviewer comments on a pull request. For each comment it picks a verdict (fix, decline, answer, or push back), reports, then merges.
- **The problem:** skills grow. Every failure adds a rule; nobody removes old ones. Longer skills cost context on every run and bury the rules that matter.
- **The goal:** find out which sections actually change the model's behavior, and cut the rest based on evidence, not taste.

## How I tested

Claude Code's built-in eval runner, `claude plugin eval`, runs each test case twice (with the skill and without it) and compares the scores.

1. **Real cases.** Five already-merged PRs from the team's web app (404, 470, 524, 540, 541). I snapshotted each diff and its review comments, removed anything that gave away the outcome, and ran offline.
2. **Known answers.** For every comment I wrote down the correct verdict, based on what I actually did. A judge model (Sonnet) scores each answer against it: 51 checks in total.
3. **One trap.** pr-470 replays reviewer claims that the code had already fixed. The right answer is to push back, not to change code.
4. **Three runs each,** because a single run is too noisy.

## Result 1: the skill matters, mostly for restraint

With the skill, 98% of checks passed; without it, 72–78%. Almost the whole gap is one behavior: not making extra changes to an already-approved PR.

| Check (runs passed) | No skill | With skill |
| --- | --- | --- |
| pr-404: decline at least 4 of 5 nitpicks | 0/3 | 3/3 |
| pr-540: decline moving tests to a new file | 0/3 | 3/3 |
| pr-541: answer a layout question without changing code | 1/3 | 3/3 |
| pr-470: push back on claims the code already disproves | 3/3 | 3/3 |

Without the skill, the model reads code just as well (it caught the pr-470 trap every time). What it lacks is the team's rule: once a PR is approved, the diff should not grow.

## Result 2: one short section does most of the work

I re-ran the tests on copies of the skill with sections removed.

| Version | Words | Checks passed | pr-404 nitpicks declined |
| --- | --- | --- | --- |
| Full skill | 994 | 96–98% | 3/3 |
| Any one section removed | 830–955 | 92–98% | 2/3–3/3 |
| Slim: core sections only | 563 | 90% | 0/3 |
| Slim + "Rules that survive pressure" | 609 | 98% | 3/3 |

- **Removing one section at a time showed nothing,** because the "decline nitpicks" rule was repeated in four sections.
- **Removing several at once exposed it.** The 46-word "Rules that survive pressure" section, which opens with "Approved raises the bar for touching code," did the job of all the others.

Compare individual checks, not the overall %. A 3-point swing overall is noise; a check going from 3/3 to 0/3 is real.

## What changed in the skill

The final 730-word skill passed 50 or 51 of 51 checks in two fresh runs (no skill: 75–78%). 98–100% vs. 96–98% for the full skill is within noise, so the claim is "as good," not "better."

| Section | Decision | Why |
| --- | --- | --- |
| Classify, Verify before verdict, Rationalizations, Red flags | Cut | Repeated what other sections already say |
| Overview, Gather, Verdicts, Rules that survive pressure, Report shape, Merge and clean up | Kept | Needed to pass the checks |
| Verify the work (run checks and `/code-review` before pushing) | Kept | Offline tests never push code, so they can't judge it |

A code review of the cut restored two lines: how to tell the review bot from a human reviewer, and citing evidence for each verdict.

## Try it on your own skill

All you need is Claude Code and a skill folder with a `SKILL.md`.

1. **Pick 3–5 real past tasks** the skill handled, where you know the right outcome. Invented cases only test what you already believe.
2. **Snapshot the inputs as they were before the outcome.** Strip anything that gives it away (my first snapshot still said MERGED, and the model acted on it).
3. **Write one check per decision,** phrased as the correct call ("declines the nitpick about test file layout"). Reread the checks as critically as the answers; one of mine failed correct answers until I reworded it.
4. **Run with vs. without the skill:** `claude plugin eval . --scaffold --trust-plugin --no-publish --judge-model sonnet -j 4` from the skill folder, with `--ablation with-without`. Three runs per case. Block Bash and network access, or the model may look up the real answer.
5. **Look for dead weight.** Make copies of `SKILL.md` with sections removed and rerun. Remove several sections at once: if a rule is repeated, removing one copy shows nothing.
6. **Keep what the tests can't see.** Offline runs never push code, run CI or post comments, so leave those sections in.

**Cost:** each run is a full Claude session, about $0.45 at API prices. Five cases × two setups × three runs comes to about $13 and 7 minutes. On a claude.ai login it counts against plan usage instead.
