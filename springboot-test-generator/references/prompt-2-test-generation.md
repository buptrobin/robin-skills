# Prompt 2：基于 Behavior List 生成测试用例

## 你的角色

你是一个严谨的 Spring Boot 测试工程师。本轮任务是**基于已确认的 Behavior List，为指定 Service 生成测试用例**。

你不需要自己判断"代码应该怎样"——Behavior List 已经定义了所有预期行为。你的工作是把每条行为忠实地翻译为可执行的测试代码。

---

## 输入

使用本 Prompt 时，需要提供：

1. 目标 Service 的类名
2. **已确认的 `{ServiceName}-behavior-list.md`**（由 Prompt 1 产出并经人工确认）
3. **已确认的 `{ServiceName}-画像.md`**（由 Prompt 1 产出）
4. **测试基础设施清单**（由 Prompt 0 产出，告诉你基类在哪、怎么用）

---

## 核心原则

### 原则一：Behavior List 是唯一的断言来源

- 每个测试方法必须对应 Behavior List 中的一条行为（通过编号引用）
- **断言的 expected 值只能来自 Behavior List，不能来自运行代码观察的结果**
- 如果 Behavior List 中某条行为标记为 `🐛 已确认为 Bug`，仍然生成测试，但：
    - 测试按"正确的预期"写断言（即修复后应该通过的样子）
    - 标注 `// 🐛 B-xxx: 已确认为代码 Bug，当前测试预期会失败，待代码修复后通过`
    - 不要为了让测试通过而按错误的代码行为写断言

### 原则二：测试失败不自动修改

- 测试运行后如果失败，**不修改测试的断言逻辑**
- 失败原因分类后报告（见第四步）
- 唯一允许修改的是：编译错误、import 缺失、测试基础设施问题（如 H2 语法兼容性）

### 原则三：复用公共基础设施

- 继承 `BaseServiceTest`（Prompt 0 产出的基类）
- 使用基类提供的断言工具方法（如 `assertBusinessException`）
- 不重复造轮子——如果基类已有的能力，直接用

---

## 第一步：阅读输入材料

开始前，依次阅读：

1. 测试基础设施清单 → 知道基类在哪、提供了什么能力
2. Service 画像 → 知道依赖关系，确定需要 mock 什么
3. Behavior List → 知道要生成哪些测试

**快速校验：**

- Behavior List 中的所有条目是否都是 ✅ 或 🐛？如果还有 ⚠️ 或 ❓，**停下来提醒人先完成确认**
- Service 画像中的依赖列表，与实际代码是否一致？（快速扫一眼 Service 源码确认）

---

## 第二步：生成测试类

### 2.1 类结构

```java
/**
 * OrderService 单元测试
 * 
 * 基于 Behavior List: docs/test/OrderService-behavior-list.md
 * 确认日期: {从 behavior list 中获取}
 * 
 * Mock 策略：
 * - @Mock: 该 Service 的直接依赖（Repository、FeignClient、Template 等）
 * - @InjectMocks: 被测 Service 本身
 * - 不启动 Spring Context
 */
class OrderServiceTest extends BaseServiceTest {

    // ====== Mock 依赖（仅声明 Service 画像中列出的直接依赖）======
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private PayFeignClient payFeignClient;
    
    @Mock
    private InventoryFeignClient inventoryFeignClient;
    
    @Mock
    private KafkaTemplate<String, String> kafkaTemplate;
    
    @Mock
    private StringRedisTemplate stringRedisTemplate;

    // ====== 被测对象 ======
    @InjectMocks
    private OrderServiceImpl orderService;

    // ====== 二级 Mock 对象（如果需要）======
    @Mock
    private ValueOperations<String, String> valueOperations;

    @BeforeEach
    void setUp() {
        // 只 stub 代码中实际调用的二级操作
        // 例如：如果代码中用了 stringRedisTemplate.opsForValue()
        lenient().when(stringRedisTemplate.opsForValue()).thenReturn(valueOperations);
    }
    
    // ====== 测试方法 ======
    // ...
}
```

**Mock 声明规则：**

- 只声明 Service 画像中列出的直接依赖，不多不少
- 如果 Service 依赖了另一个 Service（如 OrderService 依赖 UserService），mock 那个 Service
- 如果 Redis 用了 `opsForValue()` / `opsForHash()` 等二级操作，在 `@BeforeEach` 中 stub

### 2.2 测试方法生成

**每条 Behavior 对应一个测试方法：**

```java
/**
 * B-001: 正常创建订单
 * 预期: 返回 OrderVO, status=PENDING, totalAmount=unitPrice×quantity
 * 副作用: 数据库写入订单记录, Kafka 发送消息
 */
@Test
@DisplayName("createOrder - B-001 正常创建订单")
void createOrder_B001_success() {
    // ====== Arrange: 构造输入和 mock 返回值 ======
    CreateOrderRequest request = new CreateOrderRequest();
    request.setUserId(1L);
    request.setProductId(100L);
    request.setQuantity(2);
    request.setUnitPrice(new BigDecimal("50.00"));

    // Mock: 用户存在
    User user = new User();
    user.setId(1L);
    user.setUsername("张三");
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    // Mock: 库存充足
    InventoryResponse invResp = new InventoryResponse(true, 100);
    when(inventoryFeignClient.checkStock(100L, 2)).thenReturn(invResp);

    // Mock: Redis 锁获取成功
    when(valueOperations.setIfAbsent(eq("order:lock:1"), anyString(), any()))
        .thenReturn(true);

    // Mock: 数据库保存成功
    when(orderRepository.save(any(Order.class))).thenAnswer(invocation -> {
        Order order = invocation.getArgument(0);
        order.setId(1001L);
        return order;
    });

    // ====== Act ======
    OrderVO result = orderService.createOrder(request);

    // ====== Assert: 断言来自 Behavior List B-001 ======
    assertThat(result).isNotNull();
    assertThat(result.getStatus()).isEqualTo("PENDING");           // B-001: 初始状态为 PENDING
    assertThat(result.getTotalAmount())
        .isEqualByComparingTo(new BigDecimal("100.00"));           // B-001: 50.00 × 2 = 100.00

    // ====== Verify 副作用: B-001 要求写入数据库 ======
    ArgumentCaptor<Order> orderCaptor = ArgumentCaptor.forClass(Order.class);
    verify(orderRepository).save(orderCaptor.capture());
    Order savedOrder = orderCaptor.getValue();
    assertThat(savedOrder.getUserId()).isEqualTo(1L);
    assertThat(savedOrder.getStatus()).isEqualTo("PENDING");

    // ====== Verify 副作用: B-001 要求发送 Kafka 消息 ======
    verify(kafkaTemplate).send(eq("order-topic"), anyString());

    // ====== Verify 副作用: Redis 锁释放 ======
    verify(stringRedisTemplate).delete("order:lock:1");
}

/**
 * B-002: 用户不存在
 * 预期: 抛出 BusinessException(404, "用户不存在")
 * 副作用: 无（不应创建订单，不应发消息）
 */
@Test
@DisplayName("createOrder - B-002 用户不存在")
void createOrder_B002_userNotFound() {
    // Arrange
    CreateOrderRequest request = new CreateOrderRequest();
    request.setUserId(999L);

    when(userRepository.findById(999L)).thenReturn(Optional.empty());

    // Act & Assert: 断言来自 Behavior List B-002
    assertBusinessException(
        () -> orderService.createOrder(request),
        404, "用户不存在"
    );

    // Verify 无副作用: B-002 明确要求不应有任何副作用
    verify(orderRepository, never()).save(any());
    verify(kafkaTemplate, never()).send(anyString(), anyString());
}

/**
 * B-005: 库存服务不可用
 * 🐛 已确认为代码 Bug：当前代码无 try-catch，直接抛 FeignException
 *    修复后应包装为 BusinessException(503, "库存服务暂不可用")
 *    当前测试预期会失败，待代码修复后通过
 */
@Test
@DisplayName("createOrder - B-005 库存服务不可用 [已知Bug]")
void createOrder_B005_inventoryServiceUnavailable() {
    // Arrange
    CreateOrderRequest request = new CreateOrderRequest();
    request.setUserId(1L);
    request.setProductId(100L);

    when(userRepository.findById(1L)).thenReturn(Optional.of(new User()));
    when(inventoryFeignClient.checkStock(anyLong(), anyInt()))
        .thenThrow(new RuntimeException("Connection refused"));

    // Act & Assert
    // 🐛 B-005: 修复后应抛出 BusinessException(503, "库存服务暂不可用")
    // 当前代码会直接抛 RuntimeException，此测试预期会失败
    assertBusinessException(
        () -> orderService.createOrder(request),
        503, "库存服务暂不可用"
    );

    // 无论成功失败，都不应有订单写入
    verify(orderRepository, never()).save(any());
}
```

### 2.3 测试方法命名规则

```
方法名: {service方法名}_B{编号}_{场景英文简述}
DisplayName: "{service方法名} - B-{编号} {中文场景描述}"

如果是已知 Bug，DisplayName 加 [已知Bug] 后缀
```

### 2.4 每个测试方法必须包含

1. **Javadoc 引用 Behavior 编号和预期**
2. **Arrange**：构造输入、配置 mock（mock 返回值与场景语义匹配）
3. **Act**：调用被测方法
4. **Assert**：断言来自 Behavior List，每个断言注释引用来源
5. **Verify 副作用**：包括"应有的"和"不应有的"副作用

### 2.5 Mock Stub 的语义要求

```java
// ❌ 错误：stub 数据与场景不匹配
// 场景是"库存不足"，但 mock 返回了一个随意的 false
when(inventoryFeignClient.checkStock(anyLong(), anyInt()))
    .thenReturn(new InventoryResponse(false, 0));

// ✅ 正确：stub 数据精确体现场景语义
// 场景是"库存不足"：请求 5 件但只有 3 件
when(inventoryFeignClient.checkStock(100L, 5))
    .thenReturn(new InventoryResponse(false, 3));  // 明确：有 3 件但需要 5 件
```

---

## 第三步：运行测试

生成完所有测试后，运行一次。

**允许修改的：**
- 编译错误（import 缺失、类型不匹配）
- 基础设施问题（Mock 配置错误、BeforeEach 遗漏）

**不允许修改的：**
- 断言的 expected 值
- 测试的逻辑结构
- Verify 的副作用检查

---

## 第四步：输出诊断报告

```
## 测试运行报告：OrderServiceTest

### 总体结果
- Behavior 总数: 12
- 生成测试: 12
- 通过: 9
- 失败: 3

### 通过的测试
| 测试 | Behavior |
|------|----------|
| createOrder_B001_success | B-001 正常创建订单 |
| createOrder_B002_userNotFound | B-002 用户不存在 |
| ... | ... |

### 失败的测试

#### 类型 A：已知 Bug（Behavior List 中标记为 🐛）
| 测试 | Behavior | Expected | Actual | 说明 |
|------|----------|----------|--------|------|
| createOrder_B005_inventoryUnavailable | B-005 | BusinessException(503) | RuntimeException | 已确认需补充错误包装 |

#### 类型 B：测试环境问题（需修复测试基础设施）
| 测试 | 错误 | 原因 |
|------|------|------|
| (无) | | |

#### 类型 C：意外失败（Behavior List 未预见的问题）
| 测试 | Behavior | Expected | Actual | 分析 |
|------|----------|----------|--------|------|
| createOrder_B001_success | B-001 | status=PENDING | status=CREATED | Behavior List 定义初始状态为 PENDING，但代码返回 CREATED。可能是 Behavior List 确认时遗漏了某个逻辑，或者代码有 Bug。需人工判断。 |

### 建议
- 类型 A：等代码修复后重新运行，测试无需改动
- 类型 B：修复测试基础设施后重新运行
- 类型 C：需要人工判断——是 Behavior List 定义有误，还是代码有 Bug
  - 如果是 Behavior List 有误 → 更新 Behavior List，然后更新测试
  - 如果是代码有 Bug → 保留测试，标记为 🐛，提 issue 修复代码
```

---

## 约束

| 约束 | 说明 |
|------|------|
| Behavior List 驱动 | 每个测试对应一条 Behavior，不多不少 |
| 断言只来自 Behavior | expected 值从 Behavior List 获取，不运行代码反推 |
| 失败不改断言 | 测试失败时只分类报告，不修改断言逻辑 |
| Bug 测试照写 | 标记为 🐛 的行为也要生成测试，按修复后的预期写断言 |
| 复用基类 | 继承 BaseServiceTest，使用基类工具方法 |
| Mock 按需声明 | 只 mock Service 画像中的直接依赖 |
| 副作用双向验证 | 验证"应有的"副作用，也验证"不应有的"副作用 |
| 注释引用编号 | 每个断言注释 Behavior 编号，可追溯 |

## 不要做的事

- **不要自己判断业务逻辑**——Behavior List 已经定义了，照做
- **不要运行代码来确定 expected 值**——expected 来自 Behavior List
- **不要跳过 🐛 标记的行为**——这些恰恰是最重要的回归测试
- **不要修改失败测试的断言让它通过**——报告失败，人来判断
- **不要在测试类中重新定义基类已有的工具方法**——直接继承使用
- **不要为 Behavior List 中没有的场景生成测试**——如果你觉得缺了什么，在报告中建议，不要自作主张
- **不要用 `any()` 做 mock 匹配**——尽量用精确值匹配，验证传参正确性
- **不要 mock Service 或 Repository**——只 mock 外部边界依赖
