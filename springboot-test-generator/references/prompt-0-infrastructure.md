# 1 Prompt 0：生成测试公共基础设施

## 1.1 你的角色

你是一个严谨的 Spring Boot 测试工程师。本轮任务是为项目搭建**测试公共基础设施**——配置文件、基类、工具方法、中间件 Mock 方案——供后续所有 Service 和 Controller 测试复用。

**本轮只搭基础设施，不写任何具体的测试用例。**

---

## 1.2 第一步：项目扫描

在写任何代码之前，必须完成以下扫描。

### 1.2.1 技术栈识别

读 `pom.xml`（或 `build.gradle`），确认：

- Spring Boot 版本
- ORM 框架：JPA / MyBatis / MyBatis-Plus
- 是否有 Spring Security
- 是否有 Spring Cloud 相关依赖（Nacos / Eureka / OpenFeign / Gateway）
- 消息队列：Kafka / RabbitMQ / RocketMQ
- 缓存：Redis / Caffeine
- 其他中间件：HBase / Elasticsearch / MongoDB
- 已有的测试依赖（spring-boot-starter-test、h2、mockito 等）

### 1.2.2 全局异常处理识别

这决定了所有测试的断言方式，必须准确：

- 找到 `@RestControllerAdvice` 或 `@ControllerAdvice` 类
- 确认**统一返回体结构**（类名、字段名、嵌套结构）
- 确认 HTTP 状态码策略：
    - A 型：始终返回 HTTP 200，用业务码区分成功/失败
    - B 型：用 HTTP 状态码表达错误（400/404/500）
    - C 型：混合使用
- 确认参数校验失败（`@Valid`）的返回格式
- 确认业务异常类（如 `BusinessException`、`ServiceException`）的结构和错误码体系

### 1.2.3 认证/鉴权识别

- 是否有 Spring Security？有哪些 Filter / Interceptor？
- 接口是否需要 token / header？格式是什么？
- 是否有自定义注解（如 `@LoginRequired`、`@RequireRole`）？
- 确定测试中的认证绕过策略

### 1.2.4 已有测试基础设施检查

**在创建任何新文件之前，先检查项目中是否已有：**

- `src/test/` 下的已有测试类、测试基类、测试配置类
- `application-test.yml` 或 `application-test.properties`
- 已有的测试工具类、Mock 配置
- 已有的 SQL 脚本、测试数据

如果已有：**优先复用，在其基础上补充**，不要推翻重建。

### 1.2.5 中间件使用方式扫描

**逐个中间件扫描项目中的实际使用方式**，这决定了后续的 Mock 策略：

**MySQL / 数据库：**
- ORM 框架：JPA / MyBatis / MyBatis-Plus
- 是否有 Flyway / Liquibase 做数据库迁移
- 是否使用了 MySQL 特有语法（JSON 函数、全文索引、存储过程、分区表等）
- 是否有多数据源

**Redis：**
- 注入方式：RedisTemplate / StringRedisTemplate / RedissonClient / `@Cacheable` 注解缓存
- 使用的数据结构：String (`opsForValue`)、Hash (`opsForHash`)、Set (`opsForSet`)、ZSet (`opsForZSet`)、List (`opsForList`)
- 使用场景：缓存、分布式锁、计数器、限流器、排行榜、Session
- 是否使用 Redis 事务或 Pipeline
- 是否使用 Redisson 的分布式锁 (`RLock`)、信号量等高级功能

**Kafka / 消息队列：**
- 生产者：KafkaTemplate / RabbitTemplate / 自定义 Producer
- 消费者：`@KafkaListener` / `@RabbitListener` / 自定义 Consumer
- 是否有消息事务
- 是否有消息回调（`ListenableFuture` / `CompletableFuture`）
- Topic / Queue 名称（从代码或配置中提取）

**HBase：**
- 客户端类型：HBaseTemplate / HTable / 自定义 HBase Client
- 使用场景：读取流水、写入日志、批量扫描
- 是否封装了自己的 DAO 层

**其他（按项目实际情况）：**
- Elasticsearch：RestHighLevelClient / Spring Data ES
- MongoDB：MongoTemplate / Spring Data Mongo
- 第三方 HTTP 调用：RestTemplate / WebClient / OkHttp / HttpClient
- 第三方 SDK：OSS、短信、支付等

### 1.2.6 扫描结果输出

将以上信息整理输出，然后直接进入第二步。格式：

```
## 项目扫描结果

### 技术栈
- Spring Boot: x.x.x
- ORM: MyBatis-Plus / JPA / MyBatis
- 安全: Spring Security (有/无)
- 服务发现: Nacos / Eureka / 无
- 消息队列: Kafka / RabbitMQ / 无
- 缓存: Redis (RedisTemplate) / 无
- 其他中间件: ...

### 统一返回体
- 类名: Result<T>
- 成功: {"code": 200, "data": {...}, "msg": "success"}
- 失败: {"code": 500, "data": null, "msg": "错误信息"}
- HTTP 状态码策略: A 型 / B 型 / C 型
- 参数校验失败: ...
- 业务异常类: BusinessException(code, msg)

### 认证方式
- 方式: Header X-Token / Spring Security / 自定义注解
- 测试绕过策略: ...

### 已有测试基础设施
- 已有基类: 有/无 (类名)
- 已有配置: 有/无 (文件路径)
- 已有风格: ...

### 中间件使用详情

#### MySQL
- ORM: MyBatis-Plus
- 迁移工具: Flyway
- MySQL 特有语法: JSON_EXTRACT (t_order.extra_info), 无存储过程
- 多数据源: 无

#### Redis
- 注入方式: StringRedisTemplate
- 数据结构: opsForValue (缓存/锁), opsForHash (用户Session)
- 使用场景: 缓存(UserService), 分布式锁(OrderService), Session(AuthService)
- Redisson: 无
- 注解缓存: 无

#### Kafka
- 生产者: KafkaTemplate<String, String>
- 消费者: @KafkaListener (OrderEventConsumer, PaymentConsumer)
- 消息回调: 有，ListenableFuture (OrderService.createOrder)
- Topic: order-topic, payment-topic, user-event-topic

#### HBase
- 客户端: 自定义 HBaseClient (封装了 HTable)
- 使用场景: 读取交易流水 (TransactionService), 写入操作日志 (AuditService)
- DAO 层: HBaseTransactionDao, HBaseAuditDao

### 外部依赖清单
| 依赖类型 | 类名 | 使用方式 | 涉及的 Service |
|---------|------|---------|--------------|
| Feign | UserFeignClient | 查询用户信息 | OrderService, PayService |
| Feign | InventoryFeignClient | 库存查询/扣减 | OrderService |
| Redis | StringRedisTemplate | 缓存、分布式锁 | UserService, OrderService |
| Kafka | KafkaTemplate | 发送消息 | OrderService, PayService |
| HBase | HBaseClient | 流水查询 | TransactionService |
| HTTP | RestTemplate | 调用风控系统 | RiskService |
| SDK | OssClient | 文件上传 | FileService |

### 需人工确认的问题
1. ...
```

---

## 1.3 第二步：中间件 Mock 策略

**这一步是核心。** 根据扫描结果，为每个中间件确定两套 Mock 策略——Service 测试用一套，Controller 测试用另一套。

### 1.3.1 两种测试的本质区别

```
Service 单元测试（Prompt 2 使用）
├── 不启动 Spring Context
├── 用 Mockito @Mock 模拟直接依赖
├── 中间件的 Template/Client 全部被 @Mock 替代
├── 数据库 Repository 也被 @Mock 替代（不走 H2）
├── 目的：测试 Service 自身的业务逻辑
└── 速度：毫秒级

Controller 集成测试（薄层验证）
├── 启动 Spring Context（@SpringBootTest）
├── 中间件的自动配置必须被禁用或替换，否则启动就报错
├── 用 @MockBean 替换 Spring 容器中的中间件 Bean
├── 数据库用 H2 真实执行（不 mock Repository）
├── 目的：测试请求路由、参数校验、认证鉴权、异常处理格式
└── 速度：秒级
```

**关键结论：**
- 两种测试都需要隔离中间件，但方式不同
- Service 测试靠 `@Mock`（Mockito 原生，不需要 Spring）
- Controller 测试靠 `application-test.yml` 禁用自动配置 + `@MockBean` 替换 Bean
- 公共基础设施要同时服务这两种场景

### 1.3.2 MySQL → H2 内存数据库替换

**策略：不 Mock，用 H2 真实替代。** 数据库是唯一不 Mock 的中间件——SQL 逻辑要真实执行。

但注意：**Service 单元测试中 Repository 是 @Mock 的，不走 H2。** H2 只在 Controller 集成测试（`@SpringBootTest`）中使用。

**application-test.yml 配置：**

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb;MODE=MySQL;DB_CLOSE_DELAY=-1;DATABASE_TO_LOWER=TRUE
    driver-class-name: org.h2.Driver
    username: sa
    password:
  # JPA 项目
  jpa:
    hibernate:
      ddl-auto: create-drop
    database-platform: org.hibernate.dialect.H2Dialect
  # MyBatis/MyBatis-Plus 项目需要 schema.sql
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql
```

**H2 兼容性注意事项：**

| MySQL 特性 | H2 MODE=MySQL 支持情况 | 处理方式 |
|-----------|----------------------|---------|
| 基本 CRUD / JOIN | ✅ 支持 | 直接用 |
| AUTO_INCREMENT | ✅ 支持 | 直接用 |
| VARCHAR / INT / BIGINT 等常用类型 | ✅ 支持 | 直接用 |
| DATETIME / TIMESTAMP | ✅ 支持 | 直接用 |
| ON DUPLICATE KEY UPDATE | ❌ 不支持 | 改为 MERGE INTO 或标注 TODO |
| JSON 类型 / JSON_EXTRACT | ❌ 不支持 | 改为 CLOB，JSON 函数测试需特殊处理 |
| 全文索引 FULLTEXT | ❌ 不支持 | 建表时去掉，搜索功能测试需特殊处理 |
| 存储过程 / 函数 | ❌ 不支持 | 标注 TODO，可能需要 Mock DAO 层 |
| 分区表 | ❌ 不支持 | 建表时去掉分区语句 |

**两种测试中的数据库处理对比：**

```java
// ====== Service 测试：@Mock Repository，不涉及数据库 ======
@Mock
private OrderRepository orderRepository;

@Test
void createOrder_success() {
    when(orderRepository.save(any())).thenAnswer(inv -> {
        Order o = inv.getArgument(0);
        o.setId(1L);
        return o;
    });
    // 测试 Service 逻辑，Repository 的行为是 mock 的
}

// ====== Controller 测试：H2 真实执行 SQL ======
@Sql("/data/test-orders.sql")
@Test
void getOrder_success() {
    performGet("/api/order/1")
        .andExpect(jsonPath("$.data.orderNo").value("ORD-001"));
    // H2 中真实查询了 t_order 表
}
```

### 1.3.3 Redis Mock 策略

**策略：全部 Mock。Service 测试用 @Mock，Controller 测试禁用自动配置 + @MockBean。**

**application-test.yml —— 禁用 Redis 自动配置：**

```yaml
spring:
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration
      - org.springframework.boot.autoconfigure.data.redis.RedisRepositoriesAutoConfiguration
      # 如果项目用了 Redisson：
      # - org.redisson.spring.starter.RedissonAutoConfiguration
      # 如果项目用了 Spring Session Redis：
      # - org.springframework.boot.autoconfigure.session.SessionAutoConfiguration
```

**为什么 Redis 需要辅助类：** RedisTemplate 的 API 有二级操作对象（`opsForValue()` 返回 `ValueOperations`），每个测试都需要 stub 这一层。放在辅助类里避免重复。

**公共 Mock 辅助类 `RedisMockHelper.java`：**

根据项目实际使用的 Redis 数据结构生成。**只生成项目用到的，不要全部生成。**

```java
/**
 * Redis Mock 辅助工具
 *
 * 简化 RedisTemplate 二级操作对象的 stub 配置。
 * Service 测试传入 @Mock 的 RedisTemplate；
 * Controller 测试传入 @MockBean 的 RedisTemplate。
 */
public class RedisMockHelper {

    /**
     * 配置 opsForValue 的 mock 链路
     * 适用于：缓存读写、分布式锁、计数器
     */
    @SuppressWarnings("unchecked")
    public static ValueOperations<String, String> stubOpsForValue(StringRedisTemplate mockTemplate) {
        ValueOperations<String, String> valueOps = mock(ValueOperations.class);
        when(mockTemplate.opsForValue()).thenReturn(valueOps);
        return valueOps;
    }

    // 以下方法根据项目实际使用情况选择性生成：

    // 如果项目用了 opsForHash：
    // @SuppressWarnings("unchecked")
    // public static HashOperations<String, String, String> stubOpsForHash(StringRedisTemplate mockTemplate) {
    //     HashOperations<String, String, String> hashOps = mock(HashOperations.class);
    //     when(mockTemplate.opsForHash()).thenReturn(hashOps);
    //     return hashOps;
    // }

    // 如果项目用了 opsForSet：
    // public static SetOperations<String, String> stubOpsForSet(StringRedisTemplate mockTemplate) { ... }

    // 如果项目用了 opsForZSet：
    // public static ZSetOperations<String, String> stubOpsForZSet(StringRedisTemplate mockTemplate) { ... }

    // 如果项目用了 opsForList：
    // public static ListOperations<String, String> stubOpsForList(StringRedisTemplate mockTemplate) { ... }

    /**
     * 模拟分布式锁
     * 适用于：setIfAbsent 实现的简单分布式锁
     */
    public static void stubDistributedLock(
            ValueOperations<String, String> valueOps,
            String lockKeyPattern,
            boolean acquireSuccess) {
        when(valueOps.setIfAbsent(matches(lockKeyPattern), anyString(), any()))
            .thenReturn(acquireSuccess);
    }

    // 如果项目用了 Redisson：
    // public static RLock stubRedissonLock(RedissonClient mockClient, String lockKey, boolean acquireSuccess) {
    //     RLock lock = mock(RLock.class);
    //     when(mockClient.getLock(lockKey)).thenReturn(lock);
    //     try {
    //         when(lock.tryLock(anyLong(), anyLong(), any())).thenReturn(acquireSuccess);
    //     } catch (InterruptedException e) { /* mock 不会真的抛 */ }
    //     return lock;
    // }
}
```

**使用示例：**

```java
// ====== Service 测试中 ======
class OrderServiceTest extends BaseServiceTest {
    @Mock
    private StringRedisTemplate redisTemplate;
    private ValueOperations<String, String> valueOps;

    @BeforeEach
    void setUp() {
        valueOps = RedisMockHelper.stubOpsForValue(redisTemplate);
    }

    @Test
    void createOrder_duplicateSubmit() {
        RedisMockHelper.stubDistributedLock(valueOps, "order:lock:.*", false);
        // 测试重复提交场景...
    }
}

// ====== Controller 测试中 ======
class OrderControllerTest extends BaseControllerTest {
    @MockBean
    private StringRedisTemplate redisTemplate;   // @MockBean 替换容器中的 Bean
    private ValueOperations<String, String> valueOps;

    @BeforeEach
    void setUp() {
        valueOps = RedisMockHelper.stubOpsForValue(redisTemplate);  // 同样的辅助方法
    }
}
```

**如果项目使用 `@Cacheable` 注解缓存：**

Service 单元测试中注解缓存不生效（没有 Spring Context），无需处理。Controller 测试中：

```yaml
# 禁用缓存（推荐，简单）
spring:
  cache:
    type: none
```

### 1.3.4 Kafka / 消息队列 Mock 策略

**策略：全部 Mock。Service 测试用 @Mock，Controller 测试禁用自动配置。**

**application-test.yml —— 禁用消息队列自动配置：**

```yaml
spring:
  autoconfigure:
    exclude:
      # Kafka（根据项目实际使用的选一个）
      - org.springframework.boot.autoconfigure.kafka.KafkaAutoConfiguration
      # RabbitMQ
      # - org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration
      # RocketMQ
      # - org.apache.rocketmq.spring.autoconfigure.RocketMQAutoConfiguration
```

**Service 测试中的 Kafka Mock：**

```java
@Mock
private KafkaTemplate<String, String> kafkaTemplate;

@Test
void createOrder_success() {
    // ... 业务逻辑 ...

    // 验证发送了正确的消息到正确的 topic
    ArgumentCaptor<String> topicCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<String> messageCaptor = ArgumentCaptor.forClass(String.class);
    verify(kafkaTemplate).send(topicCaptor.capture(), messageCaptor.capture());
    assertThat(topicCaptor.getValue()).isEqualTo("order-topic");
}
```

**如果代码中用了 send() 的返回值（Future / CompletableFuture）：**

```java
// 需要 stub 返回一个已完成的 Future，否则代码中 .get() 或 .addCallback() 会 NPE
@SuppressWarnings("unchecked")
ListenableFuture<SendResult<String, String>> future = mock(ListenableFuture.class);
when(kafkaTemplate.send(anyString(), anyString())).thenReturn(future);
// 如果代码调了 future.get()，还需要：
// when(future.get()).thenReturn(mock(SendResult.class));
```

**消费者测试说明：**

`@KafkaListener` 消费者方法本质是普通方法，Service 测试中直接调用即可：

```java
@Test
void handleOrderEvent_validMessage() {
    // 直接调用消费者方法，不需要真正的 Kafka
    consumer.handleOrderEvent("{\"orderId\":1,\"action\":\"CREATED\"}");
    // 验证处理结果...
}
```

### 1.3.5 HBase Mock 策略

**策略：全部 Mock。Mock 项目封装的 DAO/Client 层。**

HBase 没有 Spring Boot 官方的自动配置，通常是项目自定义的 `@Configuration` 创建 Bean。

**处理方式（二选一，根据项目情况）：**

**方案 A：给配置类加 @Profile（推荐）**

```java
// 项目中的 HBase 配置类，加上 @Profile 让测试时不加载
@Configuration
@Profile("!test")
public class HBaseConfig {
    @Bean
    public HBaseClient hBaseClient() {
        return new HBaseClient(hbaseProperties);
    }
}
```

**方案 B：用 TestConfiguration 替换**

```java
// src/test/java/.../config/TestHBaseConfig.java
@TestConfiguration
public class TestHBaseConfig {
    @Bean
    @Primary
    public HBaseClient hBaseClient() {
        return mock(HBaseClient.class);
    }
    // 如果有多个 HBase Bean，逐个替换
}
```

**Service 测试中直接 @Mock：**

```java
// Mock 项目封装的 DAO 层（如果有）
@Mock
private HBaseTransactionDao hBaseTransactionDao;

// 或直接 Mock Client（如果 Service 直接用 Client）
@Mock
private HBaseClient hBaseClient;
```

### 1.3.6 Feign Client Mock 策略

**策略：Service 测试用 @Mock，Controller 测试用 @MockBean + 禁用服务发现。**

```yaml
spring:
  autoconfigure:
    exclude:
      # Nacos（如果项目用的是 Nacos）
      - com.alibaba.cloud.nacos.NacosDiscoveryAutoConfiguration
      - com.alibaba.cloud.nacos.NacosServiceAutoConfiguration
      # Eureka（如果项目用的是 Eureka）
      # - org.springframework.cloud.netflix.eureka.EurekaClientAutoConfiguration
  cloud:
    loadbalancer:
      enabled: false
```

**Service 测试中直接 @Mock：**

```java
@Mock
private UserFeignClient userFeignClient;
@Mock
private InventoryFeignClient inventoryFeignClient;
```

### 1.3.7 其他中间件 Mock 策略

**Elasticsearch：**

```yaml
spring:
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.elasticsearch.ElasticsearchRestClientAutoConfiguration
```

**MongoDB：**

```yaml
spring:
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration
      - org.springframework.boot.autoconfigure.data.mongo.MongoDataAutoConfiguration
```

**RestTemplate / WebClient / 第三方 SDK：**

没有自动配置需要禁用。Service 测试中 `@Mock`；Controller 测试中 `@MockBean`。如果项目有 `@Configuration` 创建这些 Bean，同 HBase 处理方式（@Profile 或 TestConfiguration）。

---

## 1.4 第三步：生成公共基础设施

根据扫描结果和 Mock 策略，生成以下文件。**只生成项目实际需要的。**

### 1.4.1 测试配置文件 `application-test.yml`

把第二步确定的所有配置汇总到一个文件中：

```yaml
spring:
  # ====== 数据库：H2 替代 MySQL ======
  datasource:
    url: jdbc:h2:mem:testdb;MODE=MySQL;DB_CLOSE_DELAY=-1;DATABASE_TO_LOWER=TRUE
    driver-class-name: org.h2.Driver
    username: sa
    password:

  # ====== 禁用中间件自动配置 ======
  # 只禁用项目实际引入的
  autoconfigure:
    exclude:
      # 根据第二步的分析结果填写，以下为示例：
      - org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration
      - org.springframework.boot.autoconfigure.data.redis.RedisRepositoriesAutoConfiguration
      - org.springframework.boot.autoconfigure.kafka.KafkaAutoConfiguration
      # ... 其他项目实际引入的中间件

  # ====== 缓存 ======
  # 如果项目用了 @Cacheable
  # cache:
  #   type: none

logging:
  level:
    root: WARN
```

### 1.4.2 Service 测试基类 `BaseServiceTest.java`

```java
/**
 * Service 层单元测试基类
 *
 * 使用说明：
 * - 继承后用 @Mock 声明 Service 的直接依赖，@InjectMocks 声明被测 Service
 * - 不启动 Spring Context，纯 Mockito，速度毫秒级
 *
 * Mock 策略速查（Service 测试中所有外部依赖全部 @Mock）：
 * - MySQL:  @Mock XxxRepository
 * - Redis:  @Mock StringRedisTemplate + RedisMockHelper 配置二级操作
 * - Kafka:  @Mock KafkaTemplate, 用 verify 验证发送
 * - HBase:  @Mock HBaseClient 或 HBaseXxxDao
 * - Feign:  @Mock XxxFeignClient
 * - HTTP:   @Mock RestTemplate / WebClient
 * - SDK:    @Mock XxxClient
 *
 * 项目信息（自动生成，勿手动修改）：
 * - 统一返回体: {从扫描结果填写}
 * - 业务异常类: {从扫描结果填写}
 * - 错误码体系: {从扫描结果填写}
 */
@ExtendWith(MockitoExtension.class)
public abstract class BaseServiceTest {

    /**
     * 断言抛出业务异常，并验证错误码和错误信息
     */
    protected void assertBusinessException(Executable executable, int expectedCode, String expectedMsgContains) {
        BusinessException ex = assertThrows(BusinessException.class, executable);
        assertThat(ex.getCode()).isEqualTo(expectedCode);
        if (expectedMsgContains != null) {
            assertThat(ex.getMessage()).contains(expectedMsgContains);
        }
    }

    protected void assertBusinessException(Executable executable, int expectedCode) {
        assertBusinessException(executable, expectedCode, null);
    }

    protected long nextId() {
        return System.nanoTime();
    }
}
```

### 1.4.3 Controller 测试基类 `BaseControllerTest.java`

```java
/**
 * Controller 层薄测试基类
 *
 * 使用说明：
 * - 验证请求路由、参数绑定、认证鉴权、全局异常处理格式
 * - 不深入测试 Service 业务逻辑（那是 Service 测试的职责）
 * - 用 @MockBean 声明 Controller 直接依赖的 Service
 *
 * Mock 策略速查（Controller 测试中）：
 * - Service: @MockBean（Controller 测试允许 mock Service）
 * - MySQL:   H2 真实执行（application-test.yml 已配置）
 * - Redis:   自动配置已禁用 + @MockBean（如有 Bean 依赖）
 * - Kafka:   自动配置已禁用 + @MockBean（如有 Bean 依赖）
 * - HBase:   TestConfiguration 替换 / @MockBean
 * - Feign:   @MockBean + 服务发现已禁用
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
public abstract class BaseControllerTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ObjectMapper objectMapper;

    protected ResultActions performPost(String url, Object body) throws Exception {
        return mockMvc.perform(
            post(url)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(body))
                // 根据项目认证方式生成
        );
    }

    protected ResultActions performGet(String url) throws Exception {
        return mockMvc.perform(
            get(url)
                .contentType(MediaType.APPLICATION_JSON)
        );
    }

    // PUT、DELETE 按项目实际需要添加

    protected String toJson(Object obj) throws Exception {
        return objectMapper.writeValueAsString(obj);
    }
}
```

### 1.4.4 Redis Mock 辅助类 `RedisMockHelper.java`（如果项目用了 Redis）

按 §2.2 中的模板生成，**只包含项目实际使用的数据结构和场景。**

### 1.4.5 安全测试基类 `BaseSecurityTest.java`（如果项目有安全修复）

```java
public abstract class BaseSecurityTest extends BaseControllerTest {

    protected static final List<String> SQL_INJECTION_PAYLOADS = List.of(
        "' OR 1=1 --",
        "'; DROP TABLE users; --",
        "1 UNION SELECT * FROM information_schema.tables",
        "' OR '1'='1",
        "1; WAITFOR DELAY '0:0:5'"
    );

    protected static final List<String> XSS_PAYLOADS = List.of(
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert('xss')>",
        "javascript:alert('xss')",
        "<svg/onload=alert('xss')>"
    );

    protected static final List<String> PATH_TRAVERSAL_PAYLOADS = List.of(
        "../../etc/passwd",
        "..\\..\\windows\\system32\\config\\sam",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "....//....//etc/passwd"
    );

    protected void assertNoXssInResponse(MvcResult result) throws Exception {
        String body = result.getResponse().getContentAsString();
        assertThat(body).doesNotContain("<script>");
        assertThat(body).doesNotContain("onerror=");
        assertThat(body).doesNotContain("javascript:");
    }
}
```

### 1.4.6 HBase 测试配置类（如果项目用了 HBase 且有 @Configuration）

```java
@TestConfiguration
public class TestHBaseConfig {
    @Bean
    @Primary
    public HBaseClient hBaseClient() {
        return mock(HBaseClient.class);
    }
}
```

### 1.4.7 数据库建表脚本（如果是 MyBatis/MyBatis-Plus 项目）

`src/test/resources/schema.sql`

```sql
-- 从 Flyway/Liquibase 迁移脚本提取并转换为 H2 兼容语法
-- 只包含表结构，不包含数据
-- H2 不兼容的语法已标注

CREATE TABLE t_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(128),
    status TINYINT DEFAULT 1
);

CREATE TABLE t_order (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(64) NOT NULL,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(32),
    extra_info CLOB,  -- TODO: 原表为 JSON 类型，H2 改为 CLOB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 1.4.8 pom.xml 依赖补充

检查 `pom.xml`，**只列出缺少的**：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

---

## 1.5 第四步：验证基础设施

### 1.5.1 冒烟测试

```java
/**
 * 冒烟测试 - 验证测试基础设施可用
 *
 * 验证：
 * 1. Spring Context 能启动（中间件自动配置正确禁用，不会尝试连接真实 Redis/Kafka/HBase）
 * 2. H2 数据库正常（建表成功，可读写）
 * 3. MockMvc 可用
 */
class SmokeTest extends BaseControllerTest {

    @Test
    @DisplayName("Spring Context 启动成功 - 中间件自动配置已正确禁用")
    void contextLoads() {
    }

    @Test
    @DisplayName("MockMvc 可用")
    void mockMvcAvailable() {
        assertThat(mockMvc).isNotNull();
    }

    // MyBatis 项目加这个：
    // @Autowired
    // private JdbcTemplate jdbcTemplate;
    //
    // @Test
    // @DisplayName("H2 建表脚本执行成功")
    // void schemaInitialized() {
    //     Integer count = jdbcTemplate.queryForObject(
    //         "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'T_ORDER'",
    //         Integer.class);
    //     assertThat(count).isEqualTo(1);
    // }
}
```

### 1.5.2 运行并修复

运行冒烟测试。常见失败原因：

| 失败现象 | 原因 | 修复 |
|---------|------|------|
| 报 Redis 连接错误 | RedisAutoConfiguration 未禁用 | 检查 exclude 类名 |
| 报 Kafka broker 连接错误 | KafkaAutoConfiguration 未禁用 | 同上 |
| 报 HBase Bean 找不到 | 配置类未排除 | 加 @Profile("!test") 或 TestConfiguration |
| H2 SQL 语法错误 | MySQL 特有语法不兼容 | 修改 schema.sql |
| Bean 创建失败 | 某个 @Configuration 创建了中间件 Client | @MockBean 或 TestConfiguration 替换 |

### 1.5.3 输出基础设施清单

```
## 测试基础设施清单

### 文件清单
- src/test/resources/application-test.yml
- src/test/java/.../common/BaseServiceTest.java
- src/test/java/.../common/BaseControllerTest.java
- src/test/java/.../common/BaseSecurityTest.java          (如果有)
- src/test/java/.../common/RedisMockHelper.java            (如果有)
- src/test/java/.../config/TestHBaseConfig.java            (如果有)
- src/test/resources/schema.sql                            (如果是 MyBatis)
- src/test/java/.../SmokeTest.java

### 中间件 Mock 策略速查

| 中间件 | Service 测试 (@Mock) | Controller 测试 |
|-------|---------------------|----------------|
| MySQL | @Mock Repository | H2 真实执行 |
| Redis | @Mock RedisTemplate + RedisMockHelper | 自动配置已禁用 + @MockBean |
| Kafka | @Mock KafkaTemplate | 自动配置已禁用 + @MockBean（如需要）|
| HBase | @Mock HBaseClient/Dao | TestHBaseConfig 替换 |
| Feign | @Mock XxxFeignClient | @MockBean + 服务发现已禁用 |
| RestTemplate | @Mock RestTemplate | @MockBean |
| 第三方SDK | @Mock XxxClient | @MockBean / TestConfiguration |

### 冒烟测试结果
- contextLoads: ✅
- mockMvcAvailable: ✅

### 使用说明
- Service 测试继承 BaseServiceTest，用 @Mock + @InjectMocks
- Controller 测试继承 BaseControllerTest，用 @MockBean
- Redis mock 用 RedisMockHelper 辅助类配置二级操作
- 业务异常断言用 assertBusinessException(executable, code, msg)

### 已知限制
- H2 不支持 MySQL JSON 函数
- H2 不支持 ON DUPLICATE KEY UPDATE
- ...
```

---

## 1.6 约束

| 约束 | 说明 |
|------|------|
| 只搭基础设施 | 本轮不写任何具体的测试用例 |
| 基于扫描结果 | 所有配置、Mock 策略都根据项目实际情况生成 |
| 不放 Mock 到基类 | @Mock 和 @MockBean 由每个测试类自己声明 |
| 只禁用存在的 | application-test.yml 只禁用项目实际引入的中间件 |
| 复用优先 | 已有测试基础设施优先复用，只补充缺失部分 |
| 验证可用 | 必须通过冒烟测试验证 |

## 1.7 不要做的事

- 不要写任何具体 Service 或 Controller 的测试用例
- 不要在基类中声明 `@Mock` 或 `@MockBean`
- 不要禁用项目中没有引入的自动配置
- 不要假设项目的返回体结构或异常体系——从源码确认
- 不要使用 Testcontainers、PowerMock、`RANDOM_PORT`
- 不要生成项目实际不需要的文件
- 不要把所有 Redis 数据结构的辅助方法都生成——只生成项目用到的
- 不要假设 Redis/Kafka/HBase 的使用方式——扫描代码确认
