# 在 Claude Code 加载 / 调用 庖丁解牛

## 安装

把本 skill 目录放进 Claude Code 的 skills 目录:

```bash
# 全局(对所有项目可用)
cp -r paoding-jieniu ~/.claude/skills/

# 或项目级(随仓库走)
cp -r paoding-jieniu .claude/skills/
```

`SKILL.md` 的 YAML frontmatter(`name` / `description`)即 Claude Code 识别 skill 的入口。

## 调用方式

### 自动触发
Claude Code 会读取 `description`。当你的请求命中拆解 / 重构 / 大型代码库 / 架构划分 / 深层调试等场景时,会自动加载本 skill 的四底层原则。

典型触发语:
- "这个遗留模块太大了,帮我拆 / 重构"
- "我不知道从哪读起这个代码库"
- "帮我把这个大任务拆成可执行的小步"
- "设计这个系统的模块边界"

### 显式调用
直接点名:

```
用庖丁解牛的方法拆解 src/legacy/ 这个目录
```

```
按 paoding-jieniu 的四步法(观/寻/慎/养)做这次重构
```

## 与 Claude Code 工作流的结合

| Claude Code 习惯动作 | 庖丁解牛对应原则 |
|---------------------|-----------------|
| 先读文件 / 建心智模型再动手 | 原则 1 依乎天理(观) |
| 从纯函数 / 接口边界切入 | 原则 2 批大郤·导大窾(寻) |
| 核心 / 并发 / 安全路径加测试再改 | 原则 3 怵然为戒(慎) |
| 小步提交、保持测试常绿 | 原则 4 刀刃若新(养) |

## 推荐配套
- 配合 `TaskCreate` / `TaskUpdate` 把「拆解四步法」落成可追踪的任务清单。
- 弹药库 `reference/zhuangzi.md` 提供完整概念体系(天理/郤/窾/軱/族/游刃),可在拆解时引用。
