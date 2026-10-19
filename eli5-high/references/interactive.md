# 单文件交互页 · 落地配方

`eli5` 在主题**合适**时产出 B 级「参数联动」页。这份文档是全部工程细节，照着抄就能做出质量一致的成品。
参考实现：`../examples/trig-page-full.html`（完整页：6 张静态讲解图 + 互动面板 + 窄屏堆叠布局）。

---

## 0. 先判断：这个主题合适吗？

**动手画之前必须先做完这一步。** 问自己：*这个主题里有没有「改一个量，图形就会跟着变」？*

### ✅ 适合做 B 级

命中任意 2 条就可以做：

| 判据 | 例子 |
|---|---|
| 有一个**连续可调的量** | 角度、时间、频率、半径、比例、阈值、权重、浓度、速度 |
| 图形会**随它改变形态** | 曲线弯法、线段长短、面积、位置、颜色深浅 |
| 存在**反直觉、要自己试才信**的结论 | 「转过去为什么冒出负号」「周期为什么减半」 |
| 有**多层依赖**：A 变 → B 变 → C 变 | 静态图说不清这条链 |
| 有**值得看的临界 / 极端情形** | 趋近 0 或无穷、断点、相变、刚好失效的那一刻 |
| 读者的真实疑问是「**如果我改成 X 会怎样**」 | 调参、权衡、敏感度 |

### ❌ 不适合（命中任意 1 条就退回 A 级或静态）

| 判据 | 为什么 | 该怎么做 |
|---|---|---|
| 清单 / 分类 / 术语对照 | 没有「量」，拖什么 | A：hover 高亮、点击展开 |
| 时间线 / 历史 / 流程叙事 | 顺序固定，拖拽很怪 | A 或 B+ 步骤机 |
| 并列对比几个离散选项 | 读者要同时看全，不是拖 | 静态对照表 + hover 高亮 |
| 数据是外部给定的真值 | 不随任何参数变 | 静态 |
| 参数本身不连续（只有几个合法取值） | 滑块会撒谎 | 改成按钮切换 |
| 一页里已经有互动点 | 注意力是有限资源 | 保持静态 |

### 判断记录（写不出来 = 不合适）

> 读者拖「＿＿」→ 看到「＿＿」变 → 因此相信「＿＿」。

这句话写不出来，说明这个主题没有可拖的量，别硬做。

### 混搭通常最好

一页 = **静态讲解打底 + 1 个互动收尾**。绝大多数好页面都是这个结构，一页最多 1–2 个动手点。
负面样板：每个知识点都做成滑块 → 读者疲于操作，什么都记不住。

### 主题档次速查（含反面判断示例）

| 主题 | 判据命中 | 结论 |
|---|---|---|
| 三角函数：单位圆与正弦曲线 | 角度连续可调 + 反直觉 + 多层依赖 | **B** ✅ |
| 复利 / 利率 | 利率、年限连续可调 | **B** ✅ |
| 二进制搜索 | 数组规模可调 + 命中次数 | **B** ✅ |
| 排序算法 | 规模可调，但"过程"才是重点 | **B+ 步骤机** |
| 光的三原色叠加 | 三个量互相影响 | **C** 多图联动 |
| HTTP 状态码分类 | 纯清单，没有量 | **A**（hover 分区） |
| 一个公司的历史 | 时间线固定 | **A / 静态** |
| 三种数据库选型对比 | 离散选项，要同时看全 | **静态对照表** |
| 某个国家的人口数字 | 外部真值，不随参数变 | **静态** |
| 布尔代数真值表 | 取值不连续（0/1） | **按钮切换**，不用滑块 |

---

## 1. 页面骨架

```
<wrap max-width:1060px>
  kicker 小标签：固定写「ELI5 · 讲给想探知的人」（不写「完全不懂」——是好奇，不是无知）
  h1      一句话说清这页在讲什么（关键词上色）
  .lede   2–3 行，把核心洞察点破；正文 max-width 820px
  figure        讲解图（max-width 900px）
  figure.wide   互动区（max-width 1012px，右侧详情面板/图表更宽才放得下）
  footer  来源与说明
```

关键 CSS 约定（宽度分层，别让正文行长超过 820px）：

```css
.wrap{max-width:1060px;margin:0 auto;padding:48px 24px 72px}
h1,.lede,.note,footer{max-width:820px}
figure{max-width:900px}
figure.wide{max-width:1012px}
svg{display:block;width:100%;height:auto}
```

**注意**：把 figure 做宽以后，里面 SVG 的实际渲染宽度 = figure 宽 − 56px 内边距。
`viewBox` 宽度要按这个反推字号，否则文字会缩得看不见。经验值：
渲染宽度 950px + viewBox 1100 → 缩放 0.87，SVG 里写 `font-size:14` 实际显示约 12px。

## 2. 配色语义（固定，别随意换）

| 变量 | 值 | 用途 |
|---|---|---|
| `--ink` / `--mid` / `--faint` | `#1b1b19` / `#6b6a64` / `#c9c7bf` | 正文 / 次要 / 轴与网格 |
| `--line` | `#e3e1d9` | 卡片描边、分隔虚线 |
| `--blue` / `--blue-soft` | `#2f6fd0` / `#dce9fb` | 主色；**横坐标 / cos** |
| `--green` / `--green-soft` | `#2f8a5b` / `#dcefe5` | **纵坐标 / sin** |
| `--amber` / `--amber-soft` | `#c8862a` / `#fbeed7` | 高亮、雷达/角标记、重点背景 |
| `--red` / `--red-soft` | `#c04a3c` / `#f8e2df` | **风险 / tan / 反向量** |

背景一律 `--paper:#faf9f6`，卡片 `#fff`，**light 主题为默认**。

## 3. 几何 helper（照抄这五个就够）

```js
var RAD = Math.PI / 180, NS = "http://www.w3.org/2000/svg";

// 圆上一点；y 轴朝下所以 sin 要减
function pt(r, deg){ var a = deg*RAD; return [CX + r*Math.cos(a), CY - r*Math.sin(a)]; }

// 圆弧路径。数学逆时针 → sweep-flag 0（SVG 的 y 轴朝下，这一点最反直觉）
function arcD(r, a1, a2){
  var p1 = pt(r,a1), p2 = pt(r,a2);
  var span = Math.abs(a2-a1) % 360, large = span > 180 ? 1 : 0;
  return "M "+p1[0].toFixed(2)+" "+p1[1].toFixed(2)+
         " A "+r+" "+r+" 0 "+large+" 0 "+p2[0].toFixed(2)+" "+p2[1].toFixed(2);
}

// 数据坐标 → 像素坐标
function xOf(t){ return X0 + W*(t/TWO_PI); }
function yOf(t){ return CY - AMP*Math.sin(t); }

// 建元素的小工具，省掉一堆 createElementNS 样板
function el(tag, attrs, parent){
  var n = document.createElementNS(NS, tag);
  for (var k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}
```

**箭头**（要画运动方向时）：逆时针运动在角度 θ 处的切线方向 = θ+90，**顺时针 = θ−90**。
`arrow(px, py, deg, size)` 用 `(cos deg, −sin deg)` 作方向向量。

曲线：不用手摆点，循环取样即可（n=200 就足够平滑）：

```js
var d = ""; for (var i=0;i<=n;i++){ var t=i/n*TWO_PI; d += (i?" L ":"M ")+xOf(t)+" "+yOf(t); }
```

## 4. 交互四件套

### 4.1 拖拽（带跨 0°/360° 解缠）

```js
function angleFromEvent(ev){
  var box = stage.getBoundingClientRect();
  var vb = VIEW_W / box.width;                    // 视口像素 → viewBox 单位
  var x = (ev.clientX - box.left)*vb - CX;
  var y = CY - (ev.clientY - box.top)*vb;
  return Math.atan2(y, x) / RAD;
}

// ⚠️ 监听必须挂在 SVG 根节点上，不能挂手柄图形（见坑 2）
stage.addEventListener("pointerdown", function(ev){
  if ((ev.clientX - stage.getBoundingClientRect().left)*(VIEW_W/stage.getBoundingClientRect().width) > PANEL_SPLIT) return;
  dragging = true;
  try { stage.setPointerCapture(ev.pointerId); } catch(e){}
  alpha = Math.round(angleFromEvent(ev));
  render();
});
stage.addEventListener("pointermove", function(ev){
  if (!dragging) return;
  ev.preventDefault();
  var raw = angleFromEvent(ev);
  var base = Math.floor((alpha + 180) / 360) * 360;   // 选择离当前值最近的等价角，避免跳变
  var cand = base + raw;
  if (cand - alpha > 180) cand -= 360;
  if (alpha - cand > 180) cand += 360;
  alpha = Math.round(cand);
  render();
});
["pointerup","pointercancel"].forEach(function(e){
  stage.addEventListener(e, function(){ dragging = false; });
});
window.addEventListener("blur", function(){ dragging = false; });   // 切窗口时别卡住状态
```

抓取面：在最上层铺一张 `fill="transparent"` 的 rect 盖满整个面板，
并在 CSS 里给 `.hit{cursor:grab}` —— 比让用户精确点中一个小圆点友好得多。

### 4.2 滑块

```js
slider.addEventListener("input", function(){
  var th = parseFloat(this.value);
  alpha = Math.floor(alpha/360)*360 + th;      // 保留已转的整圈数
  if (alpha < 0) alpha += 360;
  render();
});
```

### 4.3 键盘

```html
<svg id="stage" tabindex="0" role="application" aria-label="...">
```
```js
document.addEventListener("keydown", function(ev){
  if (ev.target.tagName === "INPUT") return;      // 别抢滑块的键
  var step = ev.shiftKey ? 15 : 1;
  if (ev.key === "ArrowRight" || ev.key === "ArrowUp") { alpha += step; render(); ev.preventDefault(); }
  else if (ev.key === "ArrowLeft" || ev.key === "ArrowDown") { alpha -= step; render(); ev.preventDefault(); }
});
```
焦点可见性：`svg:focus-visible{box-shadow:0 0 0 3px var(--blue-soft);border-radius:12px}`

### 4.4 自动演示（rAF）

```js
var playing = false, raf = null;
playBtn.addEventListener("click", function(){
  playing = !playing;
  this.textContent = playing ? "❚❚ 暂停" : "▶ 自动旋转";
  if (!playing) { if (raf) cancelAnimationFrame(raf); return; }
  (function loop(){
    if (!playing) return;
    alpha += 0.7;                      // 每帧 0.7°，约 24 秒一圈
    render();
    raf = requestAnimationFrame(loop);
  })();
});
```
**必须在切换时 `cancelAnimationFrame`**，否则会有多个循环叠加、越来越快。

## 5. 单一 render() 收敛所有状态

只留一个 `render()`，读全局状态 → 更新 DOM。别在多处散着改属性。
所有图形元素在初始化时建好并持有引用，render 里只 `setAttribute`，**不重建节点**。

里面对齐的规矩：

- `alpha` 是**唯一的真值**（单位：度，可正可负可超 360）。
  显示用 `th = ((alpha % 360) + 360) % 360`，弧度用 `th * RAD`。
- 数值一律 `toFixed(3)`；角度 `toFixed(1)` 加 `°`。
- 弧度写成 `(rad/Math.PI).toFixed(3) + "π"`，比小数更符合课本习惯。
- **一切"第几圈 / 累计"的显示都按 `Math.abs(alpha)` 算**（见坑 5）。
- 退化情形要兜住：`cos ≈ 0` 时 tan 不存在（隐藏线段 + 显示"不存在"）；
  角度正好落在坐标轴上时，象限口诀失效（显示"坐标轴上，要单独判断"）。

## 6. 五个必查的坑

1. **SVG 圆弧方向**
   y 轴朝下 ⇒ 数学逆时针 = `sweep-flag 0`；顺时针运动在 θ 处的箭头方向 = θ−90。
   写反了图会朝反方向转，而且不容易一眼看出来。

2. **`pointerdown` 必须挂 SVG 根节点**
   挂到手柄 `<circle>` 上会**静默失效**：手柄中心被后画的半径线/圆点盖住，
   事件落在兄弟节点上，不会冒泡回手柄。改成整块面板铺透明抓取 rect + 监听挂根节点。

3. **`hidden` 属性会被类里的 `display` 顶掉**
   `.sym{display:flex}` + `hidden` → 元素照样显示。必须补 `.cls[hidden]{display:none}`。

4. **浮动文字要白色光晕**
   角度值、标签压在射线/曲线上会看不清：
   `.halo{stroke:#fff;stroke-width:3.6;paint-order:stroke;stroke-linejoin:round}`

5. **反向拖拽让角度变成负数**
   显示圈数时 `Math.floor(alpha/360)` 会算出 −1 → 出现「第 0 圈（已转 -1 整圈）」。
   一律用 `Math.floor(Math.abs(alpha)/360)`。

## 7. 验证链（做完必须跑，不许只看截图）

截图只能证明"画出来了"，证明不了 JS 有没有跑。用 anatomy skill 的 drive.mjs **真跑一遍**：

```bash
cd C:/Users/robin/.workbuddy/skills/anatomy
node scripts/drive.mjs <page.html> --actions <steps.json> --width 1280 --height 900
```

actions JSON 示例（**eval 字符串必须放文件里，内联 JSON 的引号会炸**）：

```json
[
  ["eval", "({figs: document.querySelectorAll('figure').length, deg: vDeg.textContent})"],
  ["scroll", "#stage"],
  ["drag", "#stage", 0.30, 0.4978, 0.10, 0.60, 28],
  ["wait", 200],
  ["eval", "({deg: vDeg.textContent, cos: vCos.textContent, sin: vSin.textContent, tan: vTan.textContent, q: vQ.textContent})"],
  ["shot", "out.png", "figure:nth-of-type(7)"],
  ["scroll", "#play"], ["click", "#showSym"], ["wait", 200],
  ["eval", "getComputedStyle(document.getElementById('symLegend')).display"]
]
```

规矩：

- **页面长时必须先 `["scroll", sel]`**。否则指针事件落在视口外，`drag` / `click` 会**静默失败**
  —— 现象是数值完全没变，很容易误判成代码 bug。
- 动作：`["drag", sel, fx0,fy0, fx1,fy1, steps]`、`["click", sel]`、`["key","ArrowRight",sel]`、
  `["eval","JS"]`、`["shot", out, sel]`、`["until","JS"]`。分数 0..1 相对元素盒子。
- **`eval` 读回数值面板做算术断言**，跟几何真值比。例：224° → cos −0.719 / sin −0.695 /
  tan +0.966 / 第Ⅲ象限；40° → cos 0.766 / sin 0.643 / tan 0.839。
  这一步能抓住弧方向、象限、符号之类的**数学错误**，比看截图可靠得多。
- 最后一行必须 `console: clean`（同时报告 console 错误与未捕获异常）。
- 每张 SVG 单独截图读一遍（`Read` 工具直接看 png）：
  ```bash
  node scripts/capture.mjs <page> --select "figure:nth-of-type(N)" --width 940 --height 900 --out x.png
  ```
  整页缩略图看不清标签压线、文字溢出这类问题。

---

### ⚠️ CSS 注入后的结构自检（血泪教训）

往 `<style>` 里追加 CSS 时，**只要多带一个 `</style>`，它后面的规则就会变成正文文本跑到页面顶上**。
实测症状：两段媒体查询整段泄漏成可见文字，而 `console: clean`、`hOverflow: 0`、逐图截图**全都正常** ——
常规检查抓不到。所以每次动过 CSS，编译期 + 运行期各查一次：

```python
# 编译期：标签必须配平，且 </style> 到 <body> 之间不能有残留
assert html.count("<style>") == html.count("</style>") == 1
assert html[html.index("</style>"):html.index("<body>")].strip() == "</style>\n</head>"
```

```js
// 运行期：样式表要真的解析成功，body 顶部不能有文本节点
({ sheets: document.styleSheets.length,
   rules: document.styleSheets[0] ? document.styleSheets[0].cssRules.length : -1,
   topOfBody: document.body.firstChild.nodeType === 3
              ? document.body.firstChild.textContent.trim().slice(0, 40) : "(元素)" })
```
`sheets` 必须是 1，`rules` 别是 0，`topOfBody` 必须是空串。

另外**首屏一定要单独截一张图看** —— 逐图截图（`--select "figure:nth-of-type(N)"`）看不到页面顶部，
这类问题会整个漏掉。

还有个纯属自找的坑：测试脚本里**别复用同一个截图文件名**，后跑的那次会静默覆盖前一次
（我就因此把 390px 的截图当成 1280px 的看，差点误判成布局回归）。

## 8. 手机窄屏适配（默认假设会被转发到手机上）

不做适配的话，宽 viewBox 的图缩到 390px 后文字只剩 4–6px，等于没画。
**这不是可选项**：单文件 HTML 最常见的用途就是发到微信里让人在手机上看。

### 9.1 宽度分层

| 层 | 宽屏 | 窄屏（≤760px） |
|---|---|---|
| `.wrap` | max-width 1060，padding `48px 24px 72px` | padding `28px 14px 56px` |
| 正文 | `max-width:820px` | 100% |
| 普通讲解图 | `max-width:900px` | 100%，padding `18px 14px 16px` |
| 互动图 | `max-width:1012px` | 100% |
| 数值卡 | `auto-fit minmax(140px,1fr)` | `repeat(2,1fr)` |
| 公式卡 | `auto-fit minmax(358px,1fr)`（两列） | 1 列 |

字号一律 `clamp()`，别用断点跳变（跳变时中间宽度会很难看）。

### 9.2 静态宽图：点击放大浮层

宽 viewBox 的讲解图在手机上必然缩到看不清。两种做法：

- ❌ **横向滚动条**：读者不知道能滑，而且每张图都要滑一遍
- ✅ **默认缩到全宽看整体 + 点一下弹浮层放大看细节**

```css
.svgbox{position:relative}
.zoomchip{display:none}                       /* 宽屏不显示提示 */
.zoom{position:fixed;inset:0;z-index:60;background:#fff;overflow:auto;padding:58px 12px 36px}
.zoom[hidden]{display:none}
.zoom svg{width:720px;max-width:none;height:auto;display:block;margin:0 auto}
@media (max-width:760px){ .zoomchip{display:inline-block} }
```
```js
Array.prototype.forEach.call(document.querySelectorAll(".svgbox"), function (box) {
  box.addEventListener("click", function () {
    if (window.innerWidth > 760) return;        // 宽屏本来就看得很清，别乱弹
    var svg = box.querySelector("svg");
    if (!svg) return;
    inner.innerHTML = ""; inner.appendChild(svg.cloneNode(true));
    zoom.hidden = false; document.body.style.overflow = "hidden";
  });
});
```
要点：关闭按钮用 `position:fixed` 才会滚动时一直可见；支持 **Esc** 和点背景关闭；
**关掉时必须把 `body.style.overflow` 还原**，否则整页再也滚不动；给手机放一个看得见的提示胶囊。

### 9.3 互动图：换布局，不是缩放

窄屏下把「并排」改成「上下堆叠」——读者必须**同时看到拖的东西和变化的东西**，横向滚动会毁掉这个关系。
（反过来，静态图可以滚动，因为它是「看」不是「拖」。）

实现：把几何常量收进 `WIDE` / `NARROW` 两个对象，一个 `applyLayout()` 切换 viewBox、clipPath、抓取面，
并**重建静态层**；`render()` 每次按当前常量重新定位，不改结构。

```js
var WIDE   = { VW:1100, viewBox:"0 0 1100 462", CX:190, CY:230, R:140,
               X0:470, W:600, AMP:140, AY:230,
               hit:{x:22,y:62,w:336,h:336}, cClip:{...}, wClip:{...}, breakpoint:860 };
var NARROW = { VW:430,  viewBox:"0 0 430 830",  CX:215, CY:180, R:132,
               X0:40,  W:350, AMP:132, AY:620,
               hit:{x:55,y:24,w:312,h:312}, cClip:{...}, wClip:{...}, breakpoint:860 };
var L = WIDE;
var CX = L.CX, CY = L.CY, /* … */;            // 仍是普通变量，applyLayout 里重新赋值

function applyLayout() {
  CX = L.CX; CY = L.CY; R = L.R; X0 = L.X0; W = L.W; AMP = L.AMP; AY = L.AY;
  stage.setAttribute("viewBox", L.viewBox);
  setRect(grip, L.hit);                        // 抓取面
  setRect($("circleClip").querySelector("rect"), L.cClip);
  setRect($("waveClip").querySelector("rect"), L.wClip);
  stage.parentElement.classList.toggle("stacked", L !== WIDE);
  buildStatic();                               // 静态层必须可重建
  render();
}
function pickLayout() {                        // 断点看容器宽，不是窗口宽
  var w = stage.parentElement.getBoundingClientRect().width;
  return w >= WIDE.breakpoint ? WIDE : NARROW;
}
```

三条硬经验：

1. **断点看容器宽度**。board 宽 ≥860 才够放 1100 单位的并排图（缩到 860 时 14px 字 ≈ 11px），再窄就该堆叠。
2. **堆叠版要限制渲染宽度**：`.board.stacked svg{max-width:460px;margin:0 auto}`，
   否则在平板上会被放大成巨图（430 单位 × 1.6 倍 → 22px 的字）。
3. **两套布局必须分别验证**。拖拽的落点分数是按 viewBox 算的——宽屏分数放到窄屏会落到曲线面板上被门禁挡掉，
   现象是「数值完全没变」。**只用一套分数测，一定会漏掉另一套。**

### 9.4 其他必做

- 可拖拽的 SVG 加 `touch-action:none`，否则手机上拖动会变成页面滚动
- 触控目标 ≥44px：`@media (pointer:coarse){ button{min-height:44px} }`
- 窄屏下按钮 `flex:1 1 auto`、滑块 `width:100%`、`.hint` 独占一行
- **验证横向溢出**：`document.documentElement.scrollWidth - innerWidth === 0`
- **多宽度回归**：390 / 768 / 1024 / 1280 各跑一遍 drive.mjs，检查
  `window.__layout()` 的切换点、拖拽数值、以及有没有横滑

## 9. 「别人会怎么问你」——每次都要有的一节

听懂 ≠ 扛得住追问。这一节替读者**预演他会被怎么问**，每问配一句话答案 + 一张小图。

### 六个必覆盖的角度

| 角度 | 长什么样 | 三角函数页的例子 |
|---|---|---|
| 定义追问 | 「为什么偏偏是它？」 | sin 30° 为什么正好是 1/2？ |
| 概念混淆 | 「A 和 B 到底差在哪？」 | 角度用得好好的，为什么要发明弧度？ |
| **反直觉** | 「为什么加了 π 反而变号？」 | sin 不变号、cos 却变号 |
| **易错点** | 「能不能写成……？」 | sin²α 和 sin(α²) 一样吗？ |
| 边界 / 极端 | 「能大于 1 吗？」 | sin 的值域为什么是 [−1, 1] |
| 有什么用 | 「学它干嘛？」 | JPEG / MP3 / 5G 都在拆正弦波 |

挑 4–8 个最可能被问到的。不必凑满六类，但**反直觉**和**易错点**两类优先——
那正是读者自己也没想通、又最容易被问到的地方。

### 形式：问答卡 + 迷你图

```html
<div class="qa">                       /* auto-fit minmax(336px,1fr)；窄屏 1 列 */
  <div class="qac">
    <p class="q">「问题原话」</p>        /* 15px / 700 */
    <p class="a">一句话答案，<b>关键词加粗</b></p>   /* 14px / 行高 1.72 */
    <svg viewBox="0 0 240 132">…</svg>   /* 迷你图：白底 + 细边框 */
  </div>
  …
</div>
```

迷你图的规矩：

- viewBox 统一 `0 0 240 132`（约 1.8:1），卡内 `width:100%`，外框 `1px` 细边 + 白底
- 字号用**独立的小号类**（`.ms` 10px / `.mm` 10.5px mono / `.mh` 11px），
  **别复用正文图的 `.ts`/`.tm`** —— 迷你图渲染会放大 1.2–1.4 倍，12.5px 会撑爆版面
- 一图只说一件事：一条线 + 一个点 + 一个标注就够，不要塞第二层信息
- 图里不要重复文字答案（答案已经在 `<p class="a">` 里）

**收尾在 note 里点明「这 N 问其实是同一件事」**，例如：
「这六问背后其实只有一句：一切都回到单位圆上那个点。」

---

## 10. 「它从哪来」——有料才写，宁缺毋滥

历史能让抽象知识点突然变得有人味，但**只写真实、可查的东西**。

### 怎么写

- **只写有人、有年份、有动机的节点**。「某位古人研究过它」没有信息量；
  「喜帕恰斯为了算星星的位置造出第一张弦表」才有。
- **优先挖「意外的转折」**，别铺成流水账。最好的历史段落几乎都是转折：
  - 它最初不是为了这个目的发明的（三角函数来自**天文**，不是几何）
  - 中途改过形态（从「整条弦」改成「半条弦」才成为 sin）
  - 名字来自一场误会（`jya（梵语“弦”）→ jiba → jaib（“衣褶”）→ sinus → sine`）
- **时间轴用 CSS 竖排**（左侧一条线 + 圆点），不用 SVG：条目数和文字长度都不定，竖排最省心也最适合手机。
  节点分三档颜色：普通（蓝）、关键转折（琥珀）、当下（绿实心）。
- 词源 / 掌故单独做个高亮框（`.etym`，左侧琥珀粗边），比塞进时间轴更容易被记住。

### ⚠️ 「最新发现」：没有就不写，别硬凑

**数学 / 理论类主题多数没有时效性新闻** —— 定理不会过期，也没有「上个月有新发现」这回事。遇到这种情况：

- **明确不写这一节**，在交付说明里讲一句为什么（「这是定理，不存在时效性」）
- **绝对不要**用「近年来研究者不断探索」之类的话充版面
- 确实有近期进展时（新技术、新应用、新定理）才写，并交代清楚**是哪一年的什么事**
- 退一步的诚实写法：不写「最新」，改写成「**它今天长到哪去了**」，
  把当代应用作为时间轴的最后一站（例：「傅里叶之后：JPEG / MP3 / 5G 都在拆正弦波」）

---

## 11. 交付前清单

- [ ] 有「别人会怎么问你」一节：4–8 问，每问配一句话答案 + 迷你图，note 里点明「其实是同一件事」
- [ ] 历史一节：只写有人 / 年份 / 动机的真实节点；**没有真进展就不写「最新发现」**，并在交付说明里讲清
- [ ] **动手前已写下判断记录**（拖什么 → 看到什么变 → 因此相信什么）；判断为 A / 静态时能指出第 0 节命中哪一条，并在交付说明里讲清理由
- [ ] **标签配平**：`<style>`/`</style>` 各 1 个、`<script>`/`</script>` 配平；`body` 顶部无文本节点（见 §7 自检）
- [ ] **首屏单独截图看过**（逐图截图看不到页面顶部）
- [ ] 单文件，`grep -c "http" page.html` 除 w3.org 命名空间外无外链
- [ ] 鼠标拖 / 触摸拖 / 键盘 三种输入都能改状态
- [ ] 数值面板 6 项全部实时更新，退化情形（tan 不存在、坐标轴上）有兜底文案
- [ ] 每个可切换元素的**默认状态**正确（该隐藏的真的隐藏了）
- [ ] drive.mjs 全流程 `console: clean`，且数值断言与真值一致
- [ ] 逐图截图肉眼过一遍，无标签压线 / 溢出 / 被裁
- [ ] 生成器（如有）与产物同步，改参数能一键重生
