---
name: springboot-test-generator
description: >
  为 Spring Boot 项目生成完整的测试套件，包含中间件 Mock 基础设施、Service 行为分析与确认、以及基于 Behavior List 的测试用例生成。
  当用户提到"生成测试"、"写测试用例"、"测试基础设施"、"Service 测试"、"Controller 测试"、"行为清单"、"Behavior List"、"Mock 中间件"，
  或者用户提供了一个 Spring Boot 项目并想为某个 Service/Controller 写测试时，必须使用此 Skill。
  即使用户只说"帮我给 XxxService 写测试"也应触发此 Skill。
---

# Spring Boot 测试生成器

此 Skill 分为三个独立阶段，**按顺序执行**。每个阶段都有明确的输入和产出。

---

## 使用哪个阶段？

| 用户需求 | 使用阶段 |
|---------|---------|
| "搭测试基础设施" / "配置 Mock" / "初始化测试环境" | → **Prompt 0** |
| "分析 XxxService" / "生成行为清单" / "Service 画像" | → **Prompt 1** |
| "根据行为清单生成测试" / "写测试用例" | → **Prompt 2** |
| 用户直接说"帮我给 XxxService 写测试"（无其他上下文） | → 先问清楚，通常是 Prompt 1 → 2 |

**完整流程**（第一次接触新项目）：Prompt 0 → Prompt 1 → Prompt 2

---

## Prompt 0：搭测试公共基础设施

> **触发条件**：项目首次建测试体系，或用户明确要求配置测试基础设施
> **产出**：application-test.yml、BaseServiceTest、BaseControllerTest、RedisMockHelper 等

详细指令见：`references/prompt-0-infrastructure.md`

**关键约束速查**：
- 先扫描项目（技术栈、中间件、已有测试），再生成
- 本阶段**不写任何具体测试用例**
- 只禁用项目实际引入的中间件自动配置
- 必须通过冒烟测试验证基础设施可用
- `@Mock` / `@MockBean` 不放入基类，由各测试类自己声明

---

## Prompt 1：Service 画像与行为清单

> **触发条件**：用户提供 Service 类名，需要分析其行为
> **输入**：Service 类名（如 `OrderService`）+ 可选业务背景
> **产出**：`{ServiceName}-画像.md` + `{ServiceName}-behavior-list.md`

详细指令见：`references/prompt-1-behavior-list.md`

**关键约束速查**：
- Step 1（画像）完成后**必须停下来等人工确认**
- Step 2（行为清单）完成后**再次停下来等人工确认**
- 每条行为必须标注来源：✅（文档/确认）/ ⚠️（代码推断）/ ❓（可能有问题）
- 本阶段**不写任何测试代码**
- 行为清单中所有条目经人工确认后才能进入 Prompt 2

**两次停顿点**：
```
Step 1 画像产出 → 【停止，等待人工确认】
     ↓ 人工回复后
Step 2 行为清单产出 → 【停止，等待人工确认】
     ↓ 人工确认后（所有条目变为 ✅ 或 🐛）
进入 Prompt 2
```

---

## Prompt 2：基于 Behavior List 生成测试

> **触发条件**：已有经人工确认的 Behavior List
> **输入**：ServiceName + behavior-list.md + 画像.md + 基础设施清单（Prompt 0 产出）
> **产出**：`{ServiceName}Test.java` + 测试运行报告

详细指令见：`references/prompt-2-test-generation.md`

**关键约束速查**：
- Behavior List 中仍有 ⚠️ / ❓ 条目时，**停止并提醒人先完成确认**
- 每个测试方法对应一条 Behavior，注释引用编号（如 `// B-001`）
- 测试失败时**不修改断言**，分类报告给人判断
- 🐛 标记的行为也要生成测试，按修复后的预期写断言
- 继承 BaseServiceTest，复用基类工具方法

---

## 各阶段产出文件汇总

```
项目目录/
├── src/
│   └── test/
│       ├── java/
│       │   └── {package}/
│       │       ├── common/
│       │       │   ├── BaseServiceTest.java          ← Prompt 0
│       │       │   ├── BaseControllerTest.java       ← Prompt 0
│       │       │   ├── BaseSecurityTest.java         ← Prompt 0（可选）
│       │       │   └── RedisMockHelper.java          ← Prompt 0（如有 Redis）
│       │       ├── config/
│       │       │   └── TestHBaseConfig.java          ← Prompt 0（如有 HBase）
│       │       ├── SmokeTest.java                    ← Prompt 0
│       │       └── service/
│       │           └── {ServiceName}Test.java        ← Prompt 2
│       └── resources/
│           ├── application-test.yml                  ← Prompt 0
│           └── schema.sql                            ← Prompt 0（MyBatis 项目）
└── docs/
    └── test/
        ├── {ServiceName}-画像.md                    ← Prompt 1
        └── {ServiceName}-behavior-list.md           ← Prompt 1
```
