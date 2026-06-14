---
name: springboot-assetization
description: 把历史/老旧 Spring Boot 项目"AI 资产化"——自动生成可理解、可审查、可验证的交接文档资产(模块图、API 清单、数据库语义、调用链、风险扫描、升级体检、对抗式验证、人工复核队列)。当用户提到"老项目交接""项目资产化""历史代码梳理""祖传代码/遗留系统文档化""给老 Spring Boot 项目生成文档/上下文""把项目交给 AI 之前先梳理""一键跑完资产化流水线""legacy 项目分析"等,或希望对老 Java/Spring Boot 仓库做系统性、流水线式的理解与归档时,务必使用本 skill。本 skill 内置状态机,可在单个项目上自动连跑十余个任务、中途不需用户反复催促"继续",只在两个真正需要人工的检查点停下。
---

# 老 SpringBoot 项目 AI 资产化

把一个(或多个)老 Spring Boot 仓库,变成结构化、带可信度标注、可继续交给 AI 的文档资产。核心价值在 epistemics:**推断必带证据和可信度,高危项进人工复核队列,候选绝不直接改代码。**

## 这个 skill 怎么让流水线"自动跑完"

关键机制是一个状态机脚本 `scripts/assetize.py`,它知道 14 个任务的依赖顺序,每次只吐给你"依赖已满足、现在该做"的那一个任务的完整提示词。你的工作就是一个循环:**取任务 → 执行 → 标完成 → 立刻再取**,直到脚本返回 `HUMAN_GATE` 或 `ALL_DONE`。

> ⚠️ 自动连跑的纪律(最重要):做完一个任务后,**立刻**运行 `next` 取下一个并继续执行。**不要**在任务之间停下来总结、不要问用户"要继续吗"、不要等用户回话。把整条流水线当成一个连续的工作来做。只有脚本明确返回 `HUMAN_GATE` 时才停。

## 启动流程

### 第 0 步:读约定

先读 `references/conventions.md`(可信度标签、证据块格式、guardrails、产物目录),并把其中"通用 guardrails + 可信度标签 + 证据块格式"作为贯穿所有任务的硬约束。建议同时把它写进项目的 `CLAUDE.md`,让每个任务自动继承。

如需了解整体策略和分层逻辑,读 `references/playbook.md`。

### 第 1 步:初始化(向用户确认三个参数)

需要:项目名、仓库根路径、技术栈。若用户没给全,**一次性问清**(用 ask 工具或直接问),不要逐个挤牙膏。

```bash
python <skill>/scripts/assetize.py init \
  --project "订单中心" \
  --repo "/abs/path/to/repo" \
  --stack "Spring Boot 2.7 / Java 8 / MyBatis"
```

这会在 `<repo>/docs/ai/` 下建好目录、`REVIEW-QUEUE.md` 骨架和状态文件。

### 第 2 步:进入自动连跑循环

用 `run` 一个命令驱动整条流水线:它会(可选地)标记上一个任务完成,然后吐出下一个该做的任务。循环到 `HUMAN_GATE` 或 `ALL_DONE`:

```bash
# 第一次(取第一个任务):
python <skill>/scripts/assetize.py run --repo "<repo>"
```

- 输出 `TASK <id> ...` + 提示词 → **严格按提示词执行**(扫代码、写 `docs/ai/` 对应文件)。涉及业务语义的结论用证据块格式;"需人工确认"项追加到 `REVIEW-QUEUE.md`。做完后用**同一个命令**标记完成并取下一个,一步到位:
  ```bash
  python <skill>/scripts/assetize.py run --completed <id> --repo "<repo>"
  ```
  拿到下一个任务后**立刻**执行,再 `run --completed`,如此循环。**中途不要停、不要问。**
- 输出 `HUMAN_GATE` → 停下,把脚本给的说明转达用户,按下文处理。
- 输出 `ALL_DONE` → 对照 `playbook.md` 收尾清单逐项核对,向用户汇报产物位置。

> 即每个任务只需一条命令(`run --completed`),取代了过去 `done` + `next` 两条。`next` / `done` 子命令仍保留,可单独使用。
>
> 续跑保障:`run` 只读 `state.json`。会话被压缩/中断/重开后,跑一次 `run --repo "<repo>"`(不带 `--completed`)即可从断点无缝继续,不会重做已完成任务。

## 两个 HUMAN GATE(唯一会停的地方)

1. **校准 gate(`after_T12C`)**:首个项目跑完 Layer 1→5 后触发。请用户本人(真懂这份代码的人)抽查:标 `[代码已证实]` 的结论是否真可信、可信度标签是否校准。
   - 用户确认通过 → 运行 `python <skill>/scripts/assetize.py gate-clear after_T12C --repo "<repo>"`,然后继续循环。
   - 若用户发现 `[代码已证实]` 贴错了 → 说明提示词在量产"自信的垃圾"。先和用户一起改提示词(`scripts/tasks.json`),再重跑相关任务,**不要**急着铺开。
2. **working-rules 访谈(T14)**:这一步 agent 不能自己编。按提示词先向用户提一份结构化访谈清单 → 等用户逐条回答 → 再整理成 `09-agent-working-rules.md`,每条标来源 `[用户口述]/[代码佐证]/[需进一步确认]`。

## 多项目 / 跨项目分析(T11)

状态机按**单项目**组织,每个仓库各跑一遍。所有项目都跑完 Layer 1-2 后,再单独发起跨项目分析(重复工具类、错误码/鉴权不一致、可抽 starter 的候选等):把各项目的 `docs/ai/` 一起作为上下文,产物写到 `docs/ai/cross-project/`,只给建议不改代码。

## 协作:springboot-dependency-analyzer

若环境里有 `springboot-dependency-analyzer` skill,在 T4(调用链)和 T9(未使用接口)优先调用它——基于注入链/知识图谱比纯 grep 更准更省 token。

## 红线(任何任务都不得突破)

- 推断不写成业务事实;一律证据块 + 可信度标签。
- "建议删除/合并/重构""疑似未被调用"全部只进候选清单,**绝不直接改代码**。
- 金额单位、软删除语义、状态枚举、时区、是否幂等——不能用一条 grep 或一个测试证明的,标 `[需人工确认]`,不许标 `[代码已证实]`,并进 `REVIEW-QUEUE.md`。
- 脚手架(T13)一律标"未在真实环境验证";说不清能不能跑就老实列"为什么可能跑不起来"。
