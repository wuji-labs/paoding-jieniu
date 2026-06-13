---
name: paoding-jieniu
description: >-
  Turns Cook Ding carving the ox in 《庄子·养生主》Zhuangzi (依乎天理 follow the
  natural grain · 批大郤·导大窾 enter through the gaps and cavities · 游刃有余 move the
  blade with room to spare) into a methodology for AI to decompose complex
  systems — read the structure before cutting, enter through the seams along the
  natural grain, slow down at hard knots, take small reversible steps that keep
  the blade ever-sharp. Activates when: refactoring a legacy module, decomposing
  a large/unfamiliar codebase, splitting a vague big task into executable steps,
  drawing system/module boundaries, tracing a call chain to the root cause
  (「窾」the cavity) of a deep bug, or judging where to cut into tech debt.
  Keywords: refactor / 重构, legacy / 遗留 / 祖传代码, this module is too big, where do
  I start / 不知从何读起, decompose / 拆解, module boundaries, decoupling, call chain,
  deep bug, root cause, tech debt, 游刃有余. Not for: a brand-new single
  file/function, pure style tweaks, or factual questions unrelated to code
  structure.
version: 1.1.0
date: 2026-06-02
authority: WUJI Labs
license: MIT
homepage: https://github.com/wuji-labs/paoding-jieniu
author: WUJI (wuji-labs)
---

# WUJI Labs · 庖丁解牛 Skill（PaoDing JieNiu — The Ox-Carving Way）

> 本 skill 把《庄子·养生主》庖丁解牛一章，转译为 AI 工程拆解的**唯一真源**。
> 当 AI 面对一个庞大、纠缠、看似无从下手的代码库 / 系统 / 任务，先读本 SKILL.md。
> 核心不是「更快地砍」，而是「先看清结构，再循纹理而入」——以道驭术，让刀刃永不卷。

---

## 一、调用场景

你正在做以下任何一件事，都应先读本 SKILL.md：

- 拆解一个庞大、陌生的代码库或遗留系统（不知从何读起）
- 把一个含混的大任务（"重构这个模块" / "做一个 X 系统"）拆成可执行的小步
- 设计系统架构，要划分边界、定义模块、找接缝
- 调试一个深层 bug，需要沿调用链定位「窾」（缝隙 / 根因）而非乱改
- 做大型重构 / 迁移，担心一刀下去伤筋动骨（"游刃" vs "折刀"）
- review 一份过度耦合的设计，想找出「天理」（自然结构线）在哪
- 评估技术债，判断哪里是「大郤大窾」（可下刀处）、哪里是「大軱」（硬骨头，绕行）
- 任何「这东西太复杂，我无从下手」的时刻

---

## 二、四底层原则

这四条出自庖丁自述其道，是所有拆解动作的出发点。违反任一即违反本 skill。

### 原则 1 · 依乎天理 — 先读结构，顺其自然纹理

> 「依乎天理，批大郤，导大窾，因其固然。」——《庄子·养生主》

牛有牛的筋骨结构；系统有系统的自然结构线。庖丁不凭蛮力，而是**顺着牛体本来的间隙与纹理**下刀。

对 AI：动刀前**先读懂结构**。代码库有它的天理——模块边界、数据流、依赖方向、领域划分。不要在没看清结构时就动手改。先建立「这头牛长什么样」的心智模型（目录树 / 依赖图 / 调用链 / 数据模型），再决定从哪入手。

**反模式**：拿到任务立刻写代码 / 立刻改文件，把系统当一块均质的肉乱砍。

### 原则 2 · 批大郤·导大窾 — 从缝隙与空处入手

> 「批大郤，导大窾……以无厚入有间，恢恢乎其于游刃必有余地矣。」——《庄子·养生主》

「郤」是大的缝隙，「窾」是骨节间的空腔。庖丁的刀走在**空处**，不去硬碰骨肉。「以无厚入有间」——用最薄的刀刃，进入本来就存在的间隙。

对 AI：找系统**本来就存在的接缝**下手——接口边界、纯函数、无副作用的纯模块、清晰的层与层之间。先动「空处」（低耦合、易隔离、可测试的部分），不要一上来就攻最纠缠的核心。每一刀都留出「游刃有余地」——保持可回退、可测试、小步提交。

**反模式**：从耦合最深、副作用最多的地方开刀；一次改动牵动半个系统，无法回退。

### 原则 3 · 见其难为·怵然为戒 — 遇硬骨头则减速慎行

> 「每至于族，吾见其难为，怵然为戒，视为止，行为迟，动刀甚微。」——《庄子·养生主》

「族」是筋骨盘结之处。即便是技艺通神的庖丁，到了难处也会**目光凝住、动作放慢、下刀极轻**。他不假装这里很容易。

对 AI：遇到「大軱」（硬骨头：核心抽象、全局状态、并发、加密/计费/安全关键路径）——**减速，不要蛮干**。停下来重读、加测试、写小实验、问澄清。这里宁可慢十倍。识别难处并降速，本身就是高手标志，不是失败。

**反模式**：在最危险处保持最快速度；对核心模块的改动和对样式文件的改动用同一种轻率。

### 原则 4 · 良庖岁更刀·以神遇不以目视 — 养刀，以道驭术

> 「良庖岁更刀，割也；族庖月更刀，折也。今臣之刀十九年矣……而刀刃若新发于硎。」——《庄子·养生主》
> 「臣以神遇而不以目视，官知止而神欲行。」——《庄子·养生主》

好厨子一年换一把刀（在切），差厨子一月换一把（在砍）；庖丁一把刀用十九年，刀刃如新。差别不在刀，在**用刀之道**。砍骨头的刀必卷，循纹理的刀永利。

对 AI：你的「刀」是你的工具、注意力、上下文预算、信任。**循结构而行**则刀刃常新——少返工、少破坏、少救火。靠蛮力硬砍则处处卷刃——满屏报错、回滚、技术债。与 NoPUA「以道驭术·用信任替代恐惧」同源：不靠制造恐慌驱动自己猛砍，而靠理解结构让动作自然、精准、可持续。「以神遇」= 当你真懂了结构，拆解会变成一种从容的、近乎不费力的事（游刃有余）。

**反模式**：用蛮力 + 试错 + 大改大回滚当作工作方式，把「换刀」（推倒重来）当常态。

---

## 三、弹药库导航

本 skill 的典源弹药与方法论种子：

| 文件 | 内容 |
|------|------|
| [reference/zhuangzi.md](reference/zhuangzi.md) | 庖丁解牛核心典源(逐句注《庄子·养生主》)+ 结构化概念体系（天理 / 郤 / 窾 / 軱 / 族 / 游刃 / 神遇）+ 工程方法论映射 |
| [commands/paoding-jieniu.md](commands/paoding-jieniu.md) | `/paoding-jieniu <目标>` 显式手动入口 + 固定输出格式 |
| [examples/01-legacy-refactor.md](examples/01-legacy-refactor.md) | input→output:拆 40k 行遗留计费模块 |
| [examples/02-deep-debug.md](examples/02-deep-debug.md) | input→output:沿调用链定位「窾」(深层 bug 根因) |
| [examples/03-architecture-boundaries.md](examples/03-architecture-boundaries.md) | input→output:依乎天理划分系统/模块边界 |
| [benchmark/scenarios.json](benchmark/scenarios.json) | 6 场景评测题库(指向 benchmark/test-project 真实被测现场) |
| [benchmark/README_BENCHMARK.md](benchmark/README_BENCHMARK.md) | 评测设计 + 评分 rubric + 复现步骤(结果待真实运行) |
| [platforms/claude-code.md](platforms/claude-code.md) | 在 Claude Code 加载 / 调用本 skill |
| [platforms/codex.md](platforms/codex.md) | 在 Codex 加载 / 调用本 skill |
| [platforms/cursor.md](platforms/cursor.md) | 在 Cursor 加载 / 调用本 skill |

### 拆解四步法速查（一刀的标准动作）

| 步 | 庄子语 | 工程动作 |
|----|--------|---------|
| 1 观 | 依乎天理 | 读结构：目录树 / 依赖图 / 数据流 / 领域边界，建心智模型 |
| 2 寻 | 批大郤·导大窾 | 找接缝：接口、纯模块、低耦合层，定第一刀落点 |
| 3 慎 | 怵然为戒·动刀甚微 | 遇硬骨头降速：加测试、写小实验、留可回退 |
| 4 养 | 刀刃若新发于硎 | 小步提交 / 持续可测 / 不积技术债，保持工具与信任常新 |

---

*WUJI Labs · 庖丁解牛 PaoDing JieNiu Skill · v1.1.0 · 2026-06-02*
*依乎天理，批大郤，导大窾，游刃有余。*
