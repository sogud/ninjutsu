---
name: happy-feat
description: Delight mode. Skip the usual ticket/spec process — scan the target codebase, pick the one thing that would make it more fun or delightful to use, and ship it complete on a happy-feat/<short-name> branch with a single commit and a one-paragraph "what & why cool" note. The user reviews in the morning and either merges or chucks it. Use when the user says "happy feat", "happy hour", "make it delightful", "build something fun", "end-of-day surprise", or pastes the happy-hour prompt.
---

# Happy Feat

After-hours mode: build one small delight, ship it complete, let the user
decide in the morning — merge or chuck. Optimize for "worth merging",
not for "safe".

Invoking this skill is the user's standing authorization for exactly what
this skill describes (branch + commit on the target repo). It authorizes
nothing else: no pushes, no merges, no PRs unless asked, no changes outside
the branch.

## Constraints (hard)

- New branch: `happy-feat/<short-name>`.
- Ship complete and working, not a sketch. Tests if they're cheap.
- Nothing the user would have to un-touch: no dependency bumps, no refactors
  of shared code, no config/infra changes.
- One commit. One-paragraph note at the top of the PR body: what you built
  and why you thought it'd be cool.
- If nothing delightful fits the constraints, say so and stop.
  A forced delight is worse than none.

## Pick the delight

Scan for small joys with a small blast radius:

- a fun CLI subcommand or easter egg that fits the project's voice
- a better default that removes a papercut the user hits often
- a tiny UX joy: status line, theme, sound, animation, confetti on success
- a delightful test or dev-tool that makes the loop more fun

Tests for the pick: Would the user smile? Is it complete within one branch?
Does it avoid everything in Constraints?

## Build & ship

1. Branch `happy-feat/<short-name>` from the default branch.
2. Build it complete; run the project's verify; add cheap tests if any.
3. Single commit, clear message.
4. Write the one-paragraph note (what + why cool); hand it to the user as
   PR-body top. Do not open the PR unless asked.
5. Report: branch name, what was built, the note, how to try it,
   how to discard (`git branch -D happy-feat/<short-name>`).
