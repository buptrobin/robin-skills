# Autopilot · 互动页「自走」规范

**一句话：B 级互动页的默认态不该是静止等人，而是一段自己在演的循环。**

起因是一个反复出现的失效点：读者根本不知道那张图能拖。写「请拖动滑块」没人看；
真正有效的是**让滑块的圆点自己动起来**。

---

## 0. 什么时候用（默认就用，例外三种）

B 级互动页**默认带 Autopilot**。三类例外：

| 例外 | 为什么 | 改用什么 |
|---|---|---|
| 需要读者**先猜**再揭晓 | 自走会把答案先演完 | 静止 + 一个明确的「开始」按钮 |
| 一页里有 **2 个以上**互动点 | 全都在动 = 全都在抢注意力 | 只让当前段落对应的那个自走，其余静止 |
| **工具型**页面（计算器、查询） | 用户带着目的来，自走是噪音 | 不加 |

还有一条隐藏代价，判断时常被忽略：

> **自走会把「最好的那一帧」变成「平均的一帧」。** 读者随机停留 3 秒，可能正好撞上最平淡的中间状态。

所以循环里**必须有一个"值得停 2–3 秒"的关键帧**。写不出这个关键帧，说明这个主题不适合 Autopilot，
退回静止的互动页反而更好。

---

## 1. 四条硬规则（违反任何一条都会退化）

1. **不写「请拖动滑块」**，让滑块圆点在空闲时自己移动（引擎负责回写 `follow.value`）。
2. **永远不停下来等人**：静置就是循环动画。互动是「打断」，不是「被要求参与」。
3. **松手 5 秒自动交还**：`nearestPhase()` 找循环里最接近的相位平滑接回，不跳帧。
4. **点击门槛低于拖动**：点画面跳到下一个关键值。手机上拖 17px 的圆点很别扭，点击没有这个问题。

配套：**状态徽标必须可见**（自动演示中 / 你接管了）。否则读者分不清"它在动"和"它坏了"。

---

## 2. API

文件：`assets/autopilot.js`（约 250 行，无依赖，ES5）。
**产出单文件 HTML 时必须把全文内联**，不允许外链。

```js
var ap = AutoPilot.create({
  mount:  document.getElementById('board'),      // 点这里换关键帧
  follow: document.getElementById('angle'),      // 拖动 = 接管
  loop:   [{t:0,v:0}, {t:3,v:120}, {t:4.5,v:180}, {t:6,v:360}],
  keys:   [0, 90, 180, 270, 360],
  value:  0, min: 0, max: 360, step: 1,
  idle:   5000,
  prefer: [3, 6],                                // 交还时优先落回这一段
  onChange: function (v) { alpha = v; render(); },   // 你只管画
  onMode:   function (m) { badge.textContent = m === 'auto' ? '自动演示中' : '你接管了'; },
  onKey:    function (v) { toast(v); }
});
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `value` | 0 | 初始值；循环存在时会立刻转 auto |
| `min` / `max` / `step` | 0 / 1 / 0.01 | 范围与步长；`step` 同时决定显示几位小数 |
| `loop` | null | 自走关键帧 `[{t,v}]`，`t` 秒、必须递增；总长建议 10–15 秒 |
| `keys` | null | 点击循环的关键值（3–5 个，按叙事顺序，不是均匀采样） |
| `idle` | 5000 | 松手后多久交还（ms） |
| `rate` | 14 | 数值追赶速率，越大越跟手；不要低于 8，会显得迟钝 |
| `prefer` | null | `[t0,t1]`，交还时优先落回这段相位，避免跳回起点 |
| `mount` | null | 点击切关键帧的区域；不传则不响应点击 |
| `follow` | null | 需要跟着动的 `<input type=range>` |
| `keyboard` | true | ← → 步进（焦点在 input 内时不抢键） |
| `reducedMotion` | null | 默认读 `prefers-reduced-motion`，为真则不自动播放 |

方法：`take()` 接管 / `release()` 交还 / `setValue(v, fromUser)` / `pulse(dt)` 手动步进 /
`destroy()`；只读属性 `value` `mode` `decimals`。

---

## 3. 循环怎么设计（最花心思的一步）

关键帧不是"把区间切几段"，而是**一次微型叙事**：

```
0.0  0.45   ← 平常状态出场
3.2  0.92   ← 慢慢逼近临界
4.6  1.00   ┐
7.4  1.00   ┘ 停留 2.8 秒：这是全篇最值钱的一帧
10.0 1.45   ← 跨过去，形态质变
13.0 0.45   ← 回到起点，闭环
```

三条经验：

- **停留帧**：两个相同 `v` 的相邻关键帧就是停留。放在"结论出现的瞬间"，不是放在结尾。
- **总长 10–15 秒**：短于 8 秒像抽搐，长于 18 秒轮不到关键帧。
- **回程可以快**：从极值回到起点用 2–3 秒即可，读者已经看过了。

---

## 4. 和 SVG 版页面怎么接（本 skill 的主线）

引擎只管数值，不管画。**把页面里所有输入入口接成 `take()` + `setValue()`，把所有显示接成 `onChange`。**

```js
// 原来的拖拽 / 滑块 / 键盘三处入口，都要先 take()
stage.addEventListener('pointerdown', function (ev) {
  ap.take();
  dragging = true;
  alpha = Math.round(angleFromEvent(ev));
  ap.setValue(alpha, false);          // false = 不重复 take
  render();
});
slider.addEventListener('input', function () {
  ap.take();
  alpha = parseFloat(this.value);
  ap.setValue(alpha, false);
  render();
});
```

⚠️ **`onChange` 里只做 `alpha = v; render();`**，不要在里面再写回 `slider.value` ——
引擎已经在自动态下回写了，页面再写一遍会和拖动打架（血泪：圆点被拽回去）。

单一真值仍然是 `alpha`，Autopilot 只是它的驱动器。

---

## 5. 八个坑

1. **自己再写一条 rAF / setInterval 去改数值** → 两套时钟打架，画面抖动。全部交给引擎。
2. **在 `onChange` 里回写滑块** → 自动态下会把用户刚拖的值顶回去。
3. **`keys` 用均匀采样**（0/25/50/75/100）→ 没有叙事，点起来和拖动没区别。
4. **循环里没有停留帧** → 最关键的那一格一闪而过，等于没讲。
5. **交还后数值跳回起点** → 传 `prefer:[t0,t1]` 收窄落点。
6. **一页多个图都开自走** → 用 `IntersectionObserver` 只让可见的那个跑：
   ```js
   new IntersectionObserver(function (es) {
     es.forEach(function (e) { e.isIntersecting ? ap.release() : ap.take(); });
   }, { threshold: 0.15 }).observe(board);
   ```
7. **`pointer-events` 误挡**：点击切关键帧的 `mount` 不能盖住滑块；它应该在画布/舞台上，不是整页。
8. **拖完浏览器还会补一个 `click`** → 引擎把它当成"点了一下画面"，每次拖完都多跳一个关键帧。
   在同一节点上、`AutoPilot.create` **之前**注册一个 click 监听，拖过就在里面 `stopImmediatePropagation()`
   （同节点按注册顺序触发，晚注册的挡不住早注册的）：

   ```js
   var suppressTap = false;
   stage.addEventListener("pointerup", function () { if (moved) suppressTap = true; });
   stage.addEventListener("click", function (ev) {          // 必须在 create 之前
     if (!suppressTap) return;
     suppressTap = false;
     ev.stopImmediatePropagation();                          // 别让引擎接管这一次 click
   });
   ```

   配套：按画面横向位置直接取值的拖拽，要和"点"区分开——pointerdown 只记起点，走够 5px 才算拖，
   没走够就留给引擎的 click 去跳关键帧。`examples/handout-demo.html` 就是这么写的。

---

## 6. 验证链（在原有验证基础上加三条）

把实例挂到 `window` 上再断言：

```js
window.__ap = ap;   // 只为测试
```

```json
[
  ["scroll", "#board"],
  ["eval", "({mode: __ap.mode, v: +__ap.value.toFixed(2)})"],
  ["wait", 3000],
  ["eval", "({mode: __ap.mode, v: +__ap.value.toFixed(2)})"],
  ["click", "#board"],
  ["wait", 200],
  ["eval", "({mode: __ap.mode, v: +__ap.value.toFixed(2)})"],
  ["wait", 5600],
  ["eval", "({mode: __ap.mode})"]
]
```

必须成立：

- [ ] 初次进入 `mode === "auto"`，且 3 秒后 `v` 发生了变化（证明真的在演）
- [ ] 点击后 `mode === "manual"`，`v` 跳到某个 `keys` 值上
- [ ] 再等 5.6 秒，`mode` 回到 `"auto"`（证明交还不坏）
- [ ] `prefers-reduced-motion: reduce` 下初次进入就是 `"manual"`（可用 drive.mjs 的 emulation 手测一次）
- [ ] 自动态下数值面板里至少有一项在持续变化（不能只有滑块在动、图没动）

---

## 7. 交付时怎么说

按 SKILL.md 第八步的四句话，其中**判断结论**那句要额外点明：

> 这页用了 Autopilot：空闲时循环 e 从 0.45 到 1.45，在 e=1.00 停 2.8 秒；读者拖动或点击即接管，松手 5 秒交还。

如果**没用** Autopilot，必须说明命中第 0 节三条例外里的哪一条。
