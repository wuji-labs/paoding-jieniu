# 例 01 · 拆解 40k 行遗留模块(Legacy Refactor)

锁定本 skill 在「重构一个庞大遗留模块」场景下的标准产出与细节级别。

---

## INPUT(用户请求)

> 这个 `src/billing/` 是个 40k 行的祖传计费模块,没人敢动。现在要把发票生成逻辑抽出来独立。帮我重构。

## 没有本 skill 的产出(反模式)

```
好的,我打开 src/billing/invoice.ts 开始抽取……
（直接编辑最中心的 BillingService,牵动 12 处,无法回退,
 对加密/对账路径与对样式同样的轻率速度）
"要不我把整个模块重写一遍?"  ← 新刀又卷
```

## 有本 skill 的产出(循四步法)

```
[庖丁 | 目标:src/billing 抽出发票生成 | 第一刀:invoice 纯渲染函数(窾)| 硬骨头:对账/退款双写、金额定点数(軱)| 余地:每步独立 commit + 快照测试]
```

### 1 观(依乎天理)
先读结构,不下结论。映射出这头牛:

| 模块 | 角色 | 依赖方向 |
|------|------|---------|
| `BillingService` | 核心编排 | 被所有人依赖(軱) |
| `invoice/render.ts` | 纯渲染:数据→PDF/HTML | 无副作用(窾)|
| `invoice/calc.ts` | 金额/税额计算 | 依赖 Money 定点数(肯綮)|
| `reconcile.ts` | 对账双写 | 触账本 + 退款(軱/族)|

天理:**渲染是纯的、计算半纯、对账是硬骨头**。抽发票应顺这条纹理。

### 2 寻(批大郤·导大窾)
第一刀落在 `invoice/render.ts`——它是窾(纯函数、无副作用、可单测)。
先把渲染层连同其输入类型抽成独立包 `@billing/invoice-render`,**不碰 BillingService**。

### 3 慎(怵然为戒)
`calc.ts` 涉及 Money 定点数与税率——肯綮。抽它之前:
- 先对现有 calc 补黄金测试(真实历史发票样本快照)。
- `reconcile.ts` 是軱:本次**不动**,只在边界留接口。降速,不蛮干。

### 4 养(刀刃若新)
提交序列(每步测试常绿、可独立回退):
1. `test: 为 invoice render/calc 补快照黄金测试`
2. `refactor: 抽 invoice/render 为纯函数包(不改行为)`
3. `refactor: invoice/calc 依赖注入 Money,抽包`
4. `feat: BillingService 改调新 invoice 包(保留旧路径 feature-flag)`

对账双写(軱)留待独立 PR,绝不与本次混在一刀。

---

**要点**:不是「更快地砍」,而是先看清哪里是窾(先下)、哪里是軱(绕行/降速)。
