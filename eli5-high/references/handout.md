# 讲义版版式 · 落地配方

`eli5-high` 与 `eli5` 共用同一套**工程**规范（`interactive.md`：适配性判断、几何 helper、
交互四件套、单一 render、五坑、验证链、手机适配）。

这份文档只管一件事：**怎么让它看起来、读起来像一份精编讲义，而不是一本绘本。**

参考成品：`../examples/handout-demo.html`（酶 · 必修一第 5 章，含全部六区块）。

---

## 0. 两张脸：什么时候它是 eli5，什么时候它是 eli5-high

| 症状 | 说明你写成了绘本 | 讲义版应该这样 |
|---|---|---|
| 一张图配一句话，下面是 60px 留白 | 字太少，读者拿不走东西 | 每图配 2–3 行，且要出现课本术语 |
| 出现"就像……一样"作为主措辞 | 比喻替代了定义 | 定义在前，比喻放进 `.aside` 附注 |
| 全页没有一个数字 | 没有可核对的东西 | 至少 3 处带来源的数值 |
| 没有题目 | 看完不会做 | 必须有「一道题走一遍」 |
| 标题是「原来……是这样」 | 目标错了 | 标题是术语本身，或者一句要考的判断 |
| 段落之间靠大留白分隔 | 节奏太慢 | 靠**编号 + 徽章 + 分隔线**分隔 |

> 一句话：eli5 让人**恍然大悟**，eli5-high 让人**不再丢分**。

---

## 1. 页面骨架与宽度分层

```
<div class="wrap">
  kicker        「ELI5-HIGH · 讲给要考试的人」
  h1            术语 + 一句要考的判断
  .meta         教材出处 · 适用年级 · 预计 12 分钟
  .lede         3–4 行：这一节在整章里的位置 + 最容易错的那件事
  .toc          章节锚点（一条横向 chip 列表，手机上可横滑）

  section A   .quote        课本原话（引用卡）+ .aside 翻译
  section B   figure ×2-5   拆开看
  section C   figure.wide   自己拖一下（B 级互动）
  section D   .ex           一道题走一遍（分步揭示）
  section E   .qa           考你会怎么考（迷你图）
  section F   .errs         易错清单（两栏对错）
  footer                    数据来源与口径声明
</div>
```

宽度分层（比 eli5 略宽，容许单行放更多字）：

```css
.wrap{max-width:1080px;margin:0 auto;padding:44px 24px 72px}
h1{max-width:880px}
.lede,.note,footer{max-width:860px}
figure{max-width:940px}
figure.wide{max-width:1040px}
svg{display:block;width:100%;height:auto}
```

字号 / 行高（讲义版整体压紧一档，别用 eli5 那套 1.6 + 大段留白）：

| 元素 | eli5 | eli5-high |
|---|---|---|
| h1 | 34px | 32px（长标题可 30px） |
| .lede | 18px / 1.6 | 17px / 1.78 |
| 图说明 | 14.5px 一行 | 15px / 1.75，2–3 行 |
| 正文段落 | — | 15px / 1.78，段距 14px |
| 卡片内文 | 13px | 13.5px / 1.75 |
| figure padding | 26px 28px | 22px 26px 20px |

---

## 2. 考点徽章

四种，颜色语义固定，**不要新增第五种**：

```html
<span class="bdg bdg-must">必考</span>   <!-- 琥珀：反复出现的题型 -->
<span class="bdg bdg-warn">易错</span>   <!-- 红：一考就错 -->
<span class="bdg bdg-diff">辨析</span>   <!-- 蓝：和相近概念对比 -->
<span class="bdg bdg-ext">延伸</span>    <!-- 绿：超出课本但对理解有帮助 -->
```

```css
.bdg{display:inline-block;font-size:11.5px;font-weight:700;line-height:1;
  padding:4px 9px;border-radius:6px;letter-spacing:.04em;vertical-align:2px}
.bdg-must{background:var(--amber-soft);color:#8a5c14;border:1px solid #f0dcb4}
.bdg-warn{background:var(--red-soft);color:#8f3226;border:1px solid #f0cbc4}
.bdg-diff{background:var(--blue-soft);color:#1f4f96;border:1px solid #bcd4f5}
.bdg-ext {background:var(--green-soft);color:#1e6640;border:1px solid #bfe0cd}
```

用法规矩：**一张图最多一个徽章**，挂在 `fig-t` 后面。满页都是徽章等于没有徽章。

---

## 3. 课本原话卡片

左侧 3px 竖条 + 极浅底色。**正文用楷体/衬线感更"教材"**，但要保持可读：

```html
<section class="quote">
  <p class="q-t">课本原话 <span class="q-src">人教版必修1 P78</span></p>
  <p class="q-b">酶是活细胞产生的具有催化作用的有机物，其中绝大多数酶是蛋白质。</p>
  <p class="q-n">→ 翻成人话：酶有三个条件同时成立——<b>活细胞产生</b>、<b>有催化作用</b>、<b>是有机物</b>。</p>
</section>
```

```css
.quote{border-left:3px solid var(--amber);background:#fffaf2;border-radius:0 14px 14px 0;
  padding:14px 18px;margin:0 0 20px;max-width:880px}
.q-t{font-size:12.5px;color:var(--mid);margin:0 0 8px;font-weight:600}
.q-src{font-family:var(--mono);font-weight:400;margin-left:6px}
.q-b{margin:0;font-size:16px;line-height:1.85;color:#2b2a26;
  font-family:"Kaiti SC","KaiTi","STKaiti",Georgia,serif}
.q-n{margin:10px 0 0;font-size:13.5px;color:#3a3a35;line-height:1.75;
  padding-top:9px;border-top:1px dashed #f0dcb4}
```

⚠️ `.q-n` 里那句"翻成人话"必须**点出条件的个数**（三个条件 / 两个前提 / 一个前提一个结果）。
这是学生丢分最多的地方：记住内容、记不住"几个条件"。

---

## 4. 图块头（比 eli5 多三样东西）

```html
<figure>
  <div class="fig-cap">
    <span class="fig-no">图 2</span>
    <span class="fig-t">温度对酶活性的影响</span>
    <span class="bdg bdg-warn">易错</span>
  </div>
  <p class="fig-s">横轴是温度，纵轴是<b>相对活性</b>……（2–3 行，出现术语）</p>
  <div class="svgbox"> … </div>
  <p class="take">结论：低温只<b>抑制</b>活性、酶不失活；高温使酶<b>变性失活</b>，不可恢复。</p>
</figure>
```

`.take` 是讲义版新增的**结论条**：一条虚线分隔 + 一句可以直接背的结论。
eli5 用 `.note`（补充说明），讲义版用 `.take`（必须记住的判断语），两者不要混用。

```css
.take{margin:14px 0 0;padding-top:12px;border-top:1px dashed var(--line);
  font-size:13.5px;color:#3a3a35;line-height:1.75}
.take::before{content:"结论 ";font-weight:700;color:var(--amber);letter-spacing:.06em}
.note{font-size:13px;color:var(--mid);margin:12px 0 0;padding-top:10px;
  border-top:1px dashed var(--line)}
```

---

## 5. 一道题走一遍（分步揭示）

**这个区块决定这页有没有用。** 结构是：题干 → 步骤（默认只显示第一步）→ 标准答案。

```html
<section class="ex">
  <p class="ex-t">例题 <span class="bdg bdg-must">必考</span></p>
  <p class="ex-q">某酶在 20℃ 时活性为最适值的 60%。若把温度从 20℃ 升到 37℃……
    <b>请判断并说明理由。</b></p>

  <ol class="steps" id="steps">
    <li class="step">
      <p class="s-h">第 1 步 · 找变量</p>
      <p class="s-b">自变量是<b>温度</b>，因变量是<b>酶活性</b>，其余（pH、底物浓度）必须相同。</p>
      <p class="s-k">用到：单一变量原则</p>
    </li>
    <li class="step" hidden> … </li>
  </ol>

  <button id="next" type="button">下一步</button>

  <div class="ans" id="ans" hidden>
    <p class="ans-t">标准答案（可抄）</p>
    <p class="ans-b">① 上升过程中活性逐渐增大，在 37℃ 达到最适；<br>
      ② 超过最适温度后活性下降，因为<b>高温使酶的空间结构被破坏</b>，这种失活<b>不可逆</b>。</p>
  </div>
</section>
```

```css
.ex{border:1px solid var(--line);border-radius:16px;padding:20px 22px;background:#fbfaf7;margin:0 0 18px}
.ex-q{font-size:15px;line-height:1.8;margin:0 0 16px;color:#2b2a26}
.steps{list-style:none;margin:0;padding:0;counter-reset:s}
.step{position:relative;padding:0 0 14px 34px;margin:0 0 14px;border-bottom:1px dashed var(--line)}
.step[hidden]{display:none}                 /* 必须补，否则 hidden 被 li 的 display 顶掉 */
.s-h{font-size:13.5px;font-weight:700;margin:0 0 5px;color:var(--blue)}
.step::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:-1px;
  width:22px;height:22px;border-radius:50%;background:var(--blue-soft);color:#1f4f96;
  font-size:12px;font-weight:700;text-align:center;line-height:22px}
.s-b{font-size:14px;line-height:1.78;margin:0;color:#3a3a35}
.s-k{font-size:12px;color:var(--mid);margin:6px 0 0;font-family:var(--mono)}
.ans{margin-top:16px;border:1px dashed #bfe0cd;background:#f6fbf8;border-radius:12px;padding:14px 16px}
.ans[hidden]{display:none}
.ans-t{font-size:12.5px;font-weight:700;color:var(--green);margin:0 0 8px;letter-spacing:.06em}
.ans-b{font-size:14px;line-height:1.85;margin:0;color:#2b2a26}
```

JS（就这几行，别写状态机）：

```js
var steps = document.querySelectorAll("#steps .step");
var ans = document.getElementById("ans"), btn = document.getElementById("next"), i = 1;
if (steps.length) steps[0].hidden = false;          // 第一步默认展开
btn.addEventListener("click", function () {
  if (i < steps.length) { steps[i].hidden = false; i++; }
  if (i >= steps.length) { ans.hidden = false; btn.textContent = "已全部展开"; btn.disabled = true; }
});
```

写步骤的四条规矩：

1. 每步只推进一个判断。跨三跳的一步等于没讲。
2. 每步末尾必须有 `.s-k`，写明"这一步用到哪个概念"——这是学生最缺的连接。
3. 最后一定要有 `.ans`，且**分行编号**，可以直接抄进答题卡。
4. 题干里要留一个"陷阱点"（例：把"20℃ 升到 37℃"写出来，暗示会到最适），
   但不要说出来，让读者自己踩。

---

## 6. 易错清单（两栏对错）

```html
<div class="errs">
  <div class="er">
    <p class="er-x">✗ 低温使酶变性失活</p>
    <p class="er-v">✓ 低温只<b>抑制</b>酶的活性，酶的空间结构未被破坏，回升温度后活性可恢复</p>
    <p class="er-w">错在哪：把"活性低"当成了"酶死了"。只有高温、强酸强碱才会破坏空间结构。</p>
  </div>
  …
</div>
```

```css
.errs{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.er{border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:#fff}
.er-x{margin:0 0 8px;font-size:14px;color:#a04437;background:var(--red-soft);
  border-radius:8px;padding:8px 11px;line-height:1.6}
.er-v{margin:0 0 8px;font-size:14px;color:#1e6640;background:var(--green-soft);
  border-radius:8px;padding:8px 11px;line-height:1.7}
.er-w{margin:0;font-size:13px;color:var(--mid);line-height:1.7}
```

⚠️ 左边必须是**学生真的会写的错句**，不是"正确说法的反面"。
获取方式：教材课后题的错误选项、历年真题的干扰项、教案里的典型错例。自己编的错句没有价值。

---

## 7. 辨析表（两个相近概念）

宽屏两列、窄屏上下堆叠。**中间那一列是"判据"，不是形容词。**

```html
<table class="cmp">
  <thead><tr><th></th><th>酶</th><th>无机催化剂</th></tr></thead>
  <tbody>
    <tr><td>化学本质</td><td>绝大多数是蛋白质，少数是 RNA</td><td>无机物</td></tr>
    <tr class="key"><td>作用机理</td><td>显著降低活化能</td><td>也能降低活化能，但幅度小</td></tr>
    <tr><td>条件</td><td>需适宜温度、pH</td><td>耐受范围宽</td></tr>
  </tbody>
</table>
```

```css
.cmp{width:100%;border-collapse:collapse;font-size:13.5px;margin:0 0 14px;
  background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.cmp th,.cmp td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);
  line-height:1.65;vertical-align:top}
.cmp thead th{background:#f4f3ee;font-size:13px;font-weight:700}
.cmp tbody td:first-child{color:var(--mid);font-weight:600;width:88px;white-space:nowrap}
.cmp tr.key td{background:var(--amber-soft)}   /* 只高亮那一行"真正的区别" */
```

规矩：**整张表只允许高亮 1 行**——那才是"这两个东西真正的差别"。
全部高亮 = 没有差别。

---

## 8. 章节目录（.toc）

```html
<nav class="toc">
  <a href="#a">① 课本怎么说</a><a href="#b">② 拆开看</a><a href="#c">③ 自己拖一下</a>
  <a href="#d">④ 一道题</a><a href="#e">⑤ 会怎么考</a><a href="#f">⑥ 易错清单</a>
</nav>
```

```css
.toc{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 30px}
.toc a{font-size:13px;color:#3a3a35;text-decoration:none;background:#f1f0ea;
  border:1px solid var(--line);border-radius:999px;padding:6px 13px}
.toc a:hover{border-color:#bcd4f5;color:#1f4f96;background:#f5f9ff}
```
手机上允许换行（上面就是 `flex-wrap:wrap`），不要做成横向滚动——横向滚动藏东西。

---

## 9. 数据的写法（讲义版特有）

三个位置必须写清来源，否则读者不会信：

1. **图里的关键数值** → 在图说明里加 `（教材值）` 或 `（实验值，某年某文献）`
2. **模型/公式的假设** → 在 `footer` 里写清口径与误差
3. **超出课本的补充** → 挂 `bdg-ext` 徽章，并注明"不要求掌握"

页脚模板：

```html
<footer>
  对应 人教版必修1 第5章第1节 · 生成自 <code>eli5-high</code> skill（单文件零依赖）<br>
  数据口径：最适温度取 37℃（人体酶）；活性曲线为教学示意模型 f(T)=exp(−(T−37)²/2σ²)，
  σ 左 18 / 右 6.5 —— 只是为了复现"低温缓降、高温陡降"的形状，<b>不是实测值</b>。
</footer>
```

⚠️ **宁可写"示意值"，也不要让读者以为那是实测。** 一旦被拿去当实验数据，这页就是错的。

---

## 10. 交互区的三个可读数值

eli5 的互动面板常只有一个大数字。讲义版必须给**三个**，且第三个是"判断"：

| 位置 | 内容 | 例 |
|---|---|---|
| 数值卡 1 | 你正在调的那个量 | 温度 37.0 ℃ |
| 数值卡 2 | 被它决定的量 | 相对活性 100.0% |
| 数值卡 3 | **状态判断（文字）** | 最适温度 · 结构完好 |

第三个卡片是讲义版独有的：高中生要的不是"数值是多少"，而是"**现在是哪种状态**"。
状态文案要直接对应课本的四个判据（低温抑制 / 最适 / 高温变性 / 完全失活），
并且用一个颜色块表达（绿=正常，琥珀=偏离，红=失活）。

---

## 11. 交付前清单（讲义版追加项）

在 `interactive.md` §11 全部条目之外，再逐条勾：

- [ ] 有 `.quote` 课本原话，且写了教材版本 + 页码
- [ ] `.q-n` 点明了"几个条件"
- [ ] 每张图有 `.take` 结论条，且结论是**判断句**不是描述句
- [ ] 有「一道题走一遍」，步骤 ≥3，最后有 `.ans` 标准答案
- [ ] 每步都有 `.s-k`（用到哪个概念）
- [ ] 易错清单 ≥5 条，左边是**真实错句**（有出处）
- [ ] 辨析表只高亮 1 行
- [ ] 互动区有第三个"状态判断"卡片
- [ ] footer 写清数据口径，示意值必须标注"不是实测值"
- [ ] 全文数字前后一致（同一个量不许出现两个值）
- [ ] 全文搜一遍「简单来说 / 众所周知 / 只要记住」，出现即删
- [ ] 手机 390px 下 `.toc` 换行正常、`.cmp` 表单列可读、`.errs` 单列
