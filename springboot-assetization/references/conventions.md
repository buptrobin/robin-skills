# 通用约定(贴进 agent 项目规则)

每个任务都默认遵守以下约定。建议把本文件内容直接放进 Claude Code 的项目规则(`CLAUDE.md` 或 `.claude/` 规则),让每个任务自动继承。

## 产物目录结构

```
/docs/ai/
  00-project-overview.md
  01-module-map.md
  02-domain-model.md
  03-api-map.md
  api-openapi-draft.yaml
  04-database-raw-observations.md   ← T3 只记录,不下结论
  04-database-schema.md             ← T5 带证据的推断
  05-config-and-env.md
  06-external-dependencies.md
  07-startup-and-auth-flow.md
  08-risk-and-tech-debt.md
  08b-suspected-unused-apis.md
  09-agent-working-rules.md         ← 由你口述、agent 整理,不能 agent 独立生成
  12-adversarial-review.md          ← T12B 对抗式回查结果
  test-candidates.md
  upgrade-assessment.md
  REVIEW-QUEUE.md                   ← 所有"需人工确认"项的汇总队列(核心交付)
  diagrams/                         ← Mermaid 图
  .assetize/state.json              ← 流水线状态(续跑用,勿手改)
/docs/ai/cross-project/             ← 跨项目分析(多个项目都跑完后)
```

## 可信度标签(每条结论必须带其一)

```
[代码已证实]   有明确代码直接证明
[多处代码支持] 多处代码间接支持,但无单点铁证
[推测]         合理推断,无直接证据
[与代码冲突]   不同代码处出现矛盾
[需人工确认]   只有你/线上数据/外部系统能确认
[可能过期]     代码痕迹显示这块可能已废弃
```

## 证据块格式(涉及业务语义/数据的结论一律用这个)

```
结论:<一句话结论>
可信度:高 / 中 / 低 + 标签
证据:
  - 文件路径:它说明了什么
  - 文件路径:它说明了什么
限制:
  - 未检查的东西(如:未检查线上数据 / 未确认外部系统是否依赖)
需人工确认:
  - <具体到能回答的问题>
```

## 三条铁律

1. **推断 ≠ 事实。** 任何从代码推出来的结论都要带可信度和证据。自信的错误文档比没有文档更危险。
2. **最值钱的结论往往是 token 关不掉的。** 金额单位、软删除语义、状态枚举这类高危项,最终交付是一份排好序、尽量短的人工复核队列,不是"更多分析"。
3. **候选 ≠ 结论。** "没找到内部调用方"不等于"没人用","看着像死代码"不等于能删。只进候选清单,绝不让 agent 直接动手。

## 通用 guardrails

- 不要把推断写成业务事实,统一用证据块。
- 输出 Mermaid 图时,节点必须能在代码里找到对应物,找不到的不画。
- 凡是"建议删除/合并/重构"的,只输出候选 + 理由 + 证据,**不直接改代码**。
- 所有"需人工确认"的条目,同时追加一行到 `docs/ai/REVIEW-QUEUE.md`。
