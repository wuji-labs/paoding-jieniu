---
name: paoding-lite
description: >-
  PaoDing Lite — the Ox-Carving decomposition method as pure action items, ~800
  tokens, no parable. For small/local models and tight context budgets where the
  full paoding-jieniu skill's length would crowd attention. Activates when:
  refactoring a legacy module, decomposing a large/unfamiliar codebase, splitting a
  vague task into safe steps, drawing module/system boundaries, or finding the root
  cause of a deep bug along a call chain. (庄子·养生主 庖丁解牛; action-items only.)
version: 1.0.0
license: MIT
author: WUJI (wuji-labs)
homepage: https://github.com/wuji-labs/paoding-jieniu
---

# PaoDing Lite — Decompose Along the Grain

A capable model already does this by default; this lean form exists for small models
and tight budgets, where the full skill's length distracts more than it helps
(measured — see `benchmark/results/weak-model/FINDINGS.md`). Four moves, in order:

## 1. Read structure before cutting (观)
Before editing anything, build a map: directory tree, dependency direction, call
chain, data model. Know what the system looks like before you touch it.
- **Don't**: start editing the first file you open; treat the system as uniform mush.

## 2. Enter at the seam, not the bone (寻)
Make the first cut at a pure, low-coupling, testable part — an interface boundary, a
pure function, a side-effect-free leaf. Leave room to reverse (small commits, tests).
- **Don't**: attack the most-coupled core first; make one change that moves half the system.

## 3. Slow down at the hard knot (慎)
At a god object, global state, concurrency, or a money/security/auth path: slow down.
Re-read, add tests, write a small experiment, ask. Be 10× slower here on purpose.
- **Don't**: keep top speed through the most dangerous code.

## 4. Keep the blade sharp (养)
Follow the grain so you don't dull the blade: small reversible commits, stay green,
no tech debt. Brute force + big rewrites + rollbacks is dulling the blade.
- **Don't**: treat "rewrite it all" as the normal mode.

## Four-step quick card
| Step | Action |
|---|---|
| 1 观 read | map structure (tree / deps / call chain / domain) |
| 2 寻 seam | first cut at a pure low-coupling boundary |
| 3 慎 slow | hard knot → tests + small experiment + reversible |
| 4 养 sharp | small commits, stay green, no debt |

For the full method, sources (《庄子·养生主》), examples, and benchmark, see the
parent **paoding-jieniu** skill.

*WUJI Labs · PaoDing Lite · v1.0.0*
