# Spring Boot 测试生成器 Skill

一个基于 Agent Skills 开放标准 的 Skill，帮助你为 Spring Boot 项目**系统性地生成测试套件**。

兼容 **Claude Code** 和 **OpenAI Codex CLI**，同一份文件无需任何修改即可在两个工具中使用。

覆盖从测试基础设施搭建、Service 行为分析与人工确认，到最终测试用例生成的完整流程。

---

## 这是什么

很多团队写测试时面临的问题：

- 测试环境配置繁琐——Redis、Kafka、HBase 各有不同的 Mock 策略，每次新项目都要重来

- 测试断言缺乏依据——expected 值是"跑一下看看是什么就写什么"，不是真正的业务规约

- 测试覆盖不系统——只测了 happy path，边界条件和副作用验证缺失

这个 Skill 把测试工作拆成三个阶段，每个阶段职责单一：

| 阶段           | 做什么                           | 产出                                                     |
| ------------ | ----------------------------- | ------------------------------------------------------ |
| **Prompt 0** | 扫描项目，搭测试公共基础设施                | application-test.yml、测试基类、中间件 Mock 辅助类                 |
| **Prompt 1** | 分析 Service，生成画像和行为清单，**人工确认** | `{ServiceName}-画像.md`、`{ServiceName}-behavior-list.md` |
| **Prompt 2** | 基于确认好的行为清单，生成测试代码             | `{ServiceName}Test.java`、测试运行报告                        |

**核心设计原则**：测试的 expected 值来自人工确认的行为清单，而不是运行代码反推。发现了 Bug 也照样生成测试——按修复后的预期写断言，标记为 🐛，等代码改好后测试自然通过。

---

## 项目结构

```
springboot-test-generator/
├── README.md                               # 本文件
├── SKILL.md                                # Skill 主入口（导航 + 各阶段约束速查）
├── references/
│   ├── prompt-0-infrastructure.md         # 测试基础设施搭建的完整指令
│   ├── prompt-1-behavior-list.md          # Service 画像与行为清单的完整指令
│   └── prompt-2-test-generation.md        # 测试用例生成的完整指令
└── springboot-test-generator.skill        # 打包后的安装文件
```

`SKILL.md` 是轻量的导航层，Claude 优先读它；执行具体阶段时才按需读取 `references/` 下对应的详细指令，保持上下文精简。

---

## 安装

### Claude Code

**全局安装（推荐，所有项目可用）**

```bash
mkdir -p ~/.claude/skills

git clone https://github.com/your-org/springboot-test-generator.git
cp -r springboot-test-generator/springboot-test-generator ~/.claude/skills/
```

Claude Code 会自动检测 `~/.claude/skills/` 下的变化，**无需重启**即可生效。

**项目级安装（随代码库共享给团队）**

```bash
# 在项目根目录执行
mkdir -p .claude/skills
cp -r path/to/springboot-test-generator .claude/skills/
```

提交到 Git 后，团队成员克隆项目即可直接使用，无需单独安装。

**验证**：在 Claude Code 中输入 `/`，应能看到 `springboot-test-generator` 出现在命令列表中。

---

### OpenAI Codex CLI

SKILL.md 是跨 agent 的开放标准，同一份文件在 Codex CLI 中**无需任何修改**即可使用。

**全局安装（所有项目可用）**

```bash
mkdir -p ~/.codex/skills

git clone https://github.com/your-org/springboot-test-generator.git
cp -r springboot-test-generator/springboot-test-generator ~/.codex/skills/
```

**项目级安装（仅当前项目）**

Codex 会从当前目录向上扫描，在每一级目录的 `.agents/skills/` 下查找 skill：

```bash
# 在项目根目录执行
mkdir -p .agents/skills
cp -r path/to/springboot-test-generator .agents/skills/
```

**启动时启用 Skills**

```bash
codex --enable skills
```

> **注意**：Codex 在启动时加载 skills，安装新 skill 后需要**重启 Codex** 才能生效（与 Claude Code 的热加载不同）。

**验证**：启动后 Codex 会在上下文中列出已发现的 skills，应能看到 `springboot-test-generator`。

---

## 使用方式

安装后，在 Claude Code 或 Codex CLI 的对话中直接说：

```
帮我给 OrderService 写测试
```

Claude 会自动识别并调用此 Skill。你也可以明确指定阶段：

### 第一次接触新项目（完整流程）

**Step 1：搭基础设施（只做一次）**

```
请先扫描项目，搭建测试公共基础设施
```

Claude 会扫描 pom.xml 和源码，识别技术栈和中间件，生成：

- `src/test/resources/application-test.yml`

- `BaseServiceTest.java` / `BaseControllerTest.java`

- `RedisMockHelper.java`（如果项目用了 Redis）

- `SmokeTest.java`（验证基础设施可用）

**Step 2：分析 Service（每个 Service 做一次）**

```
分析 OrderService，生成行为清单
```

Claude 会读源码，然后**停下来两次等你确认**：

1. 第一次：确认 Service 画像（职责、依赖、你不确定的地方）

2. 第二次：确认行为清单（每个方法的每个场景的预期行为）

**Step 3：生成测试**

```
根据已确认的行为清单，生成 OrderService 的测试用例
```

Claude 会把每条确认好的行为翻译为测试方法，并输出运行报告。

---

### 已有基础设施时（日常使用）

```
分析 UserService，生成行为清单
```

或者，如果你已经有行为清单：

```
根据 UserService-behavior-list.md 生成测试代码
```

---

## 生成的文件示例

### 行为清单片段（Prompt 1 产出）

```markdown
## createOrder(CreateOrderRequest) → OrderVO

| 编号 | 场景 | 预期 | 状态 |
|------|------|------|------|
| B-001 | 正常创建订单 | 返回 OrderVO, status=PENDING, amount=price×qty | ✅ |
| B-002 | 用户不存在 | 抛出 BusinessException(404, "用户不存在") | ✅ |
| B-003 | 库存不足 | 抛出 BusinessException(400, "库存不足") | ✅ |
| B-004 | 重复提交（Redis 锁） | 抛出 BusinessException(400, "重复提交") | ✅ |
| B-005 | 库存服务不可用 | 当前直接抛 FeignException | 🐛 需补充错误包装 |
```

### 测试代码片段（Prompt 2 产出）

```java
/**
 * B-001: 正常创建订单
 * 预期: 返回 OrderVO, status=PENDING, totalAmount=unitPrice×quantity
 */
@Test
@DisplayName("createOrder - B-001 正常创建订单")
void createOrder_B001_success() {
    // Arrange
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));
    when(inventoryFeignClient.checkStock(100L, 2)).thenReturn(new InventoryResponse(true, 100));
    when(valueOperations.setIfAbsent(eq("order:lock:1"), anyString(), any())).thenReturn(true);
    when(orderRepository.save(any())).thenAnswer(inv -> { ... });

    // Act
    OrderVO result = orderService.createOrder(request);

    // Assert — 断言来自 Behavior List B-001
    assertThat(result.getStatus()).isEqualTo("PENDING");
    assertThat(result.getTotalAmount()).isEqualByComparingTo(new BigDecimal("100.00"));

    // Verify 副作用
    verify(orderRepository).save(any());          // B-001: 应写入数据库
    verify(kafkaTemplate).send(eq("order-topic"), anyString()); // B-001: 应发送消息
}
```

---

## 适用范围

**支持的技术栈**

- Spring Boot 2.x / 3.x

- ORM：JPA / MyBatis / MyBatis-Plus

- 安全：Spring Security

- 服务发现：Nacos / Eureka

- 消息队列：Kafka / RabbitMQ / RocketMQ

- 缓存：Redis（RedisTemplate / StringRedisTemplate / Redisson）

- 其他：HBase、Elasticsearch、MongoDB、RestTemplate、第三方 SDK

**不适用**

- 非 Spring Boot 项目

- 需要 Testcontainers 的集成测试（本 Skill 使用 H2 + Mockito 策略）

- 前端/UI 测试

---

## 注意事项

1. **人工确认不可跳过**：Prompt 1 有两次停顿点。行为清单没有经过确认就直接生成测试，相当于在错误的规约上建测试，没有意义。

2. **基础设施只搭一次**：Prompt 0 针对整个项目，不需要为每个 Service 重复执行。

3. **H2 兼容性**：MySQL 的 JSON 函数、`ON DUPLICATE KEY UPDATE`、全文索引等在 H2 中不支持，Claude 会在 schema.sql 中标注 TODO，这部分需要人工处理。

4. **Bug 测试**：行为清单中标记为 🐛 的条目，生成的测试**当前会失败**。这是预期的——它们是等代码修复后自动变绿的回归测试，不要删除。