# 庖丁解牛 PaoDing JieNiu — The Ox-Carving Way

<p align="center">
  <a href="https://www.skills.sh/wuji-labs/paoding-jieniu"><img src="https://www.skills.sh/b/wuji-labs/paoding-jieniu" alt="skills.sh"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/wuji-labs/huaxia-skills"><img src="https://img.shields.io/badge/%E5%8D%8E%E5%A4%8F%E5%8D%81%E5%A4%A7-HuaXia%20Skills-c1272d" alt="HuaXia Skills"></a>
</p>

**[🇨🇳 简体中文](README.zh-CN.md)** · **[🇺🇸 English](README.md)** · **[🇯🇵 日本語](README.ja.md)** · **[🇰🇷 한국어](README.ko.md)** · **[🇪🇸 Español](README.es.md)** · **[🇧🇷 Português](README.pt.md)** · **[🇫🇷 Français](README.fr.md)**

这是华夏道脉献给世界开源社区的十件礼物之一(叩兩端·无极樞纽)。
我们不立华夏本位,不主张华夏文明优于任何文明;我们只是先从自己最熟悉的道脉开始,
把它打磨成一件可用的工具,放到人类共同的开源工具架上。未来还会有希腊、那烂陀、
犹太、波斯诸文明的礼物依次到来,共同构成十二文明对标的开源能力矩阵。

EN: This is one of ten gifts the Chinese stream of wisdom offers to the world's
open-source community. We make no claim that any civilization is superior; we
simply begin with the lineage we know best, and place it on humanity's shared
toolshelf. Gifts from the Greek, Nalanda, Hebrew, and Persian streams will follow.

---

> **依乎天理，批大郤，导大窾** — Follow the natural grain; cleave the great seams, guide the blade through the hollows.
> — Zhuangzi, *The Secret of Caring for Life* (《庄子·养生主》)

**Your AI carves complex systems with a butcher's cleaver. Teach it the cook's blade.**

When faced with a tangled codebase or an ambiguous "build me X" task, most AI charges in and starts hacking — editing files before it understands the structure, attacking the most coupled core first, swinging at the same speed everywhere. It chops through bone. The blade dulls. Things break.

**PaoDing JieNiu** (庖丁解牛) encodes a 2300-year-old answer from Zhuangzi's legendary cook, whose blade stayed razor-sharp for nineteen years because he never cut against the grain — he found the seams that were already there and let the knife glide through.

## The Problem

```
You: "Refactor this 40k-line legacy module."

AI without PaoDing:
  - Opens 3 files, starts editing the most central class immediately
  - Touches global state, breaks 12 things, can't roll back
  - Same reckless speed on the crypto path as on a CSS file
  - "Let me just rewrite the whole thing" (新刀又卷 — fresh blade, dulled again)

AI with PaoDing:
  - First READS the structure: dep graph, data flow, domain boundaries (依乎天理)
  - Finds the seams: pure modules, clean interfaces, low-coupling layers (批大郤·导大窾)
  - Slows DOWN at the hard knots — adds tests, small experiments (怵然为戒)
  - Small reversible commits; the toolchain and trust stay sharp (刀刃若新)
```

## What It Teaches AI

### 🔪 The Four Foundations (四底层原则)

| Principle | Chinese | What AI Does |
|-----------|---------|--------------|
| Follow the grain | 依乎天理 | Read the structure before touching anything |
| Enter the seams | 批大郤·导大窾 | Start from interfaces, pure modules, low-coupling layers |
| Slow at the knots | 怵然为戒·动刀甚微 | Decelerate on core / concurrency / security paths |
| Keep the blade sharp | 刀刃若新发于硎 | Small, reversible, test-backed steps — no accumulating debt |

### 🐂 The Anatomy of the Ox (拆解概念体系)

The skill gives AI a vocabulary for **where to cut**:

| Term | Chinese | Engineering Meaning |
|------|---------|---------------------|
| Natural grain | 天理 | The system's inherent structure lines |
| Great seam | 大郤 (xì) | A wide, obvious boundary — easy first cut |
| Hollow | 大窾 (kuǎn) | The gap between joints — where the blade flows free |
| Hard bone | 大軱 (gū) | Core abstraction / global state — do not hack through |
| Tangled knot | 族 (zú) | A dense cluster of coupling — slow down here |
| Room to roam | 游刃有余 | Reversibility and slack the blade always preserves |
| Meeting by spirit | 以神遇 | When structure is truly understood, carving becomes effortless |

### 📏 The Four-Stroke Method (拆解四步法)

```
1. 观 OBSERVE  — map the ox: dir tree, dep graph, data flow, domains
2. 寻 SEEK     — find the seam: the first reversible, testable cut
3. 慎 CARE     — at the knot, slow down: tests, small experiments, escape hatch
4. 养 SUSTAIN  — small commits, always-green, no debt: keep the blade new
```

### 以道驭术 — Mastery, Not Force

> 「良庖岁更刀，割也；族庖月更刀，折也。」
> A good cook changes his knife once a year — he *cuts*.
> An ordinary cook changes it monthly — he *hacks*.
> — Zhuangzi, *The Secret of Caring for Life*

The difference is never the knife. It is the **way** of using it. PaoDing JieNiu shares the same root as **NoPUA**: *drive the work with the Way, not with fear; replace panic-hacking with structural understanding.* Cutting along the grain is what keeps the blade — your tools, attention, context budget, and trust — forever new.

## East Meets West

PaoDing JieNiu does not replace your engineering training. It **sharpens** it.

| Western practice | + 庖丁解牛 | = Complete |
|------------------|-----------|------------|
| "Make it work, then refactor" | 依乎天理 first | Understand before cutting — fewer rewrites |
| Find the seams (Michael Feathers) | 批大郤·导大窾 | A philosophy of *where* the seams live |
| "Move fast and break things" | 怵然为戒 at the knots | Fast in the hollows, slow at the bone |
| Boy-scout rule | 刀刃若新发于硎 | Keep the whole toolchain & trust sharp, not just the file |

> **以无厚入有间，恢恢乎其于游刃必有余地矣。**
> Drive what-has-no-thickness into what-has-space, and the blade roams with room to spare.
> — Zhuangzi, *The Secret of Caring for Life*

## From the Same Lineage

- [**NoPUA**](https://github.com/wuji-labs/nopua) — drives AI with wisdom instead of fear.
- [**TianGong** 天工](https://github.com/wuji-labs) — 5000 years of Chinese aesthetics for AI design.

## Install

```bash
# As a Claude Code plugin (one-click)
/plugin marketplace add wuji-labs/paoding-jieniu
/plugin install paoding-jieniu

# Or bare clone into your skills dir
git clone https://github.com/wuji-labs/paoding-jieniu
cp -r paoding-jieniu ~/.claude/skills/        # global
# or:  cp -r paoding-jieniu .claude/skills/    # project-scoped
```

## Invoke

| Mode | How |
|------|-----|
| **Automatic** | Just describe the work — "refactor this legacy module", "I don't know where to start in this codebase", "split these boundaries". The `description` triggers auto-load. |
| **Manual** | `/paoding-jieniu <target>` — explicit entry with a fixed output format. |
| **Examples** | See `examples/` for input→output on legacy refactor, deep debug, and boundary design. |
| **Benchmark** | `benchmark/` ships a 6-scenario suite + a real test subject. Results are NOT pre-filled — run it yourself. |

## 基本信息

| 项 | 值 |
|----|-----|
| 归属 | WUJI Labs |
| 目录 | `labs/skills/paoding-jieniu/` |
| 许可证 | MIT |
| 上游 | github.com/wuji-labs/paoding-jieniu |
| 典源 | 《庄子·养生主》庖丁解牛 |
| 版本 | v1.1.0 · 2026-06-02 |

## License

MIT — Use freely. Carve along the grain.

---

*庖丁解牛 PaoDing JieNiu — by [WUJI](https://github.com/wuji-labs)*
*依乎天理，游刃有余。Follow the grain; the blade roams free.*
