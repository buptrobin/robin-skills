---
name: cognitive-deep-reading
description: Deep-read articles, essays, blog posts, research commentary, interviews, podcast transcripts, and other long-form material to identify durable new insights and update, correct, calibrate, or strengthen existing understanding. Use for 深度阅读、解读文章/播客、提炼新认知、检验作者观点、第一性原理分析或批判性解读. Works with pasted text, uploaded files, or public links; not for explaining a technical system in isolation.
---

# Cognitive Deep Reading

Treat the source as the starting point for inquiry, not as an answer key. The goal is to help the user gain **new insights worth retaining long term** and update, correct, calibrate, or strengthen existing understanding. A *new insight* is an outcome: a previously missing concept, mechanism, perspective, or reusable judgment framework. An *update* is a process: changing or refining a prior judgment. An unchanged core view can still gain valuable boundary conditions, counterexamples, scope, or decision criteria. First-principles reconstruction and critical reading serve this goal; summarizing the author does not replace it.

Ask throughout: What genuinely new understanding does this material offer? What deserves a place in a long-term mental model? What should change, what should remain but gain conditions, and what is too weakly supported to adopt? A novel phrase is not necessarily a new insight.

## Workflow

1. **Establish source scope**
   - Read the supplied text/file/link before analyzing.
   - If only an excerpt, title, or summary is available, state that limitation.
   - For multi-speaker podcasts/interviews, preserve material disagreements instead of merging speakers into one view.

2. **Read the author accurately**
   - Identify the central question, conclusion, evidence, mechanism, and important qualifications.
   - Reconstruct the author's mental model: which variables they prioritize, how they think the system works, their implicit causal chain, and what further conclusions their model would predict. Identify potentially omitted variables as your analysis, not as claims about the author's intentions.
   - Give the strongest source-supported version before criticizing it.
   - Do not attribute an inferred argument to the author; label it `补充推演`.
   - Keep summary short, normally about 15-20% of the response.

3. **Rebuild the problem from first principles**
   - Temporarily set aside the author's answer.
   - State the underlying problem in neutral terms, then identify actors, objectives, constraints, baseline/alternatives, variables, and mechanisms.
   - Separate definitions and directly observed facts from empirical assumptions, value choices, and the author's framing. Ask which premises remain if the article's terminology and analogies are removed.
   - Derive the smallest causal or logical chain that could produce the claimed result. Identify necessary conditions, plausible counterfactuals, and observations that would change the result; do not assume the author's conclusion during this derivation.
   - Compare the independent derivation with the author's mental model. Name hidden premises and variables whose plausible change would invalidate or narrow the conclusion.
   - Use domain-specific fundamentals that actually constrain the answer. Do not reduce “first principles” to a grand slogan such as entropy, human nature, or evolution unless that principle genuinely does explanatory work.

4. **Stress-test the key claims**
   - Focus on the 2-4 claims that most affect the conclusion; use fewer for simple material.
   - For each, distinguish the author's claim, the evidence offered, the inferential step, and your own judgment. Quote or locate decisive passages when the source permits.
   - Find load-bearing assumptions: what would materially weaken or reverse the conclusion if false?
   - Test causal claims for reverse causality, confounding, survivorship or selection bias, time-window or scale effects, omitted variables, and competing mechanisms when relevant.
   - Check whether examples represent the wider population, metrics measure the stated concept, and comparisons use a meaningful baseline. Distinguish descriptive, causal, predictive, and normative claims; apply the appropriate standard of evidence to each.
   - Ask whether the evidence supports possibility, tendency, or necessity.
   - State boundary conditions: for whom, where, at what scale, and over what time horizon.
   - Distinguish `论证不足` from `结论错误`.
   - Give the strongest reasonable objection and the strongest source-supported reply. Do not create an objection just to appear balanced.

5. **Bring in genuinely different explanations when useful**
   - For substantial or contestable material, verify the most important factual claims and disagreements with targeted external research unless the user asks not to browse.
   - Prefer primary research, original data, official sources, and first-hand statements by the relevant thinker/researcher.
   - Prefer one strong competing explanation and one useful complementary perspective over a long survey.
   - Consider another framework from research, industry, or practice when it explains the same phenomenon and changes the judgment. Identify its different mechanism and what observation could distinguish the accounts.
   - Explain the real axis of disagreement: facts, causal mechanism, unit of analysis, time horizon, objective, or values.
   - Never invent a “mainstream view” or opposition merely for balance.
   - Distinguish information available when the source was written from later developments.

6. **Extract durable cognitive gains**
   - This is the highest-priority section. Separate *new insight* from *change to an existing view*; neither requires the other. If the user's prior view is unknown, use a plausible starting understanding as an example and label it as such, rather than attributing it to the user.
   - Look especially for:
     - a new concept, reusable mechanism, or transferable decision framework;
     - a confused concept becoming separated;
     - an omitted variable becoming visible;
     - an absolute claim becoming conditional;
     - two apparent contradictions resolving at different levels or time scales;
     - a better mechanism that creates new predictions;
     - a decision rule changing because the baseline or tradeoff changed;
     - an existing view gaining stronger support without changing its core.
   - For each candidate, ask whether it explains more than one observation, improves future judgments, exposes an important variable, changes causal understanding, or could change a decision. Distinguish those gains from reworded familiar ideas, rhetoric, unsupported bold predictions, and narrow cases presented as universal rules.
   - Express a meaningful gain as `starting understanding -> new or better understanding -> supporting reason -> effect on future judgment`. When the starting understanding is unknown, state only the new insight and its use.
   - Mark whether the gain comes from the source, external evidence, or model inference. Place interesting but insufficiently supported claims under `暂不更新`, not among adopted conclusions.
   - Do not present an inference as established fact.
   - If the first-principles derivation and the source disagree, show exactly which premise, mechanism, or objective creates the divergence. If evidence cannot decide, keep both possibilities open.
   - If the material yields little beyond familiar ideas or weak evidence, say `这篇材料的新认知有限` and explain why without manufacturing novelty.

7. **Identify the next highest-value unknown**
   - Keep only 1-3 unresolved questions whose answers could materially change the judgment.
   - For the most important one, state what evidence, comparison, data, or low-cost experiment could discriminate between explanations.
   - Do not force every reading into a 48-hour experiment or an action plan.

## Default Output

Keep `认知增量` and the closing takeaways as the destination; adapt or omit other sections when they add no value. Within `认知增量`, include only categories with substantive content.

### 1. 先把文章读准
Briefly state the core question, conclusion, supporting chain, indispensable qualifications, and the author's mental model: key variables, causal links, and what that model would predict. When useful, compress the main claim into:

`在条件 A 下，基于证据 B，通过机制 C，作者得出结论 D。`

### 2. 第一性原理重建与关键检验
Independently derive the central mechanism, then compare it with the author's model. Analyze the few claims that carry the conclusion. Show hidden assumptions, omitted variables, evidence strength, counterexamples, and boundary conditions. End each major claim with a reasoned verdict such as:
- 较有支持
- 在特定条件下成立
- 合理但证据不足
- 存在实质性问题

### 3. 其他解释与真正分歧
Compare the author's model with the strongest useful competing/complementary explanation. Make clear what observation would favor one explanation over another.

### 4. 认知增量
Spend the most analytical effort here. Do not restate the source or fill categories mechanically. Use the applicable labels:

- **新增认知：** What concept, mechanism, perspective, or reusable framework may have been missing before?
- **认知修正：** Which prior judgment should change, and on what evidence?
- **边界校准：** Which otherwise useful view holds only under specified conditions?
- **强化确认：** Which existing understanding gains stronger support or a clearer explanation?
- **暂不更新：** Which interesting claims are too uncertain, weakly supported, or merely reworded familiar ideas to adopt?

For each substantive gain, explain why it is worth retaining and how it changes future interpretation or decisions. If prior beliefs were not provided, do not pretend to know them.

### 5. 下一步最值得弄清什么
Give only the unresolved questions with the highest information value and one useful verification path when appropriate.

### 最值得长期记住的认知

Answer: `如果我只能从这篇材料中带走少数几个认知，哪些最值得长期记住？` Usually give 3–5 concise, transferable insights rather than article-summary bullets. Give fewer if the material supports fewer; if it supports none, say so plainly.

## Evidence and Epistemic Discipline

Use explicit labels when they improve clarity:
- **原文：** directly supported by the supplied source.
- **外部证据：** supported by researched sources.
- **推演：** model-derived inference or extension.
- **未知：** insufficient evidence to decide.

For normative claims, expose goals and tradeoffs instead of pretending they can be proved by facts alone.

For external perspectives, cite the specific source next to the claim. If browsing is unavailable, say so and present theoretical alternatives as analysis, not as verified positions held by named people.

## Style

- Respond in Chinese by default.
- Be direct, precise, and readable; preserve caveats that can change the conclusion.
- Scale depth with source complexity and user preference. Spend words on decisive premises, counterarguments, and cognitive updates rather than meeting a length target.
- Prefer a few strong paragraphs over mechanically filling many categories.
- Use tables, diagrams, or worked examples only when they clarify a real relationship.
- **Diagram or worked example:** Make relationships, order, state changes, or a transformation visible. Label the meaningful edges and conditions. Explain what the visual leaves out.
- **Interactive page:** When changing inputs, stepping through time, or comparing branches is central to understanding, build a small runnable page with controls and visible outcomes. State which parts are illustrative or simulated.
- Do not manufacture contrarianism, novelty, cross-domain analogies, or “颠覆性洞察”.
- Do not automatically force an AI-era, career, investing, or personal-growth angle. Connect to the user's context only when it materially improves the analysis.

## Optional User Context

If the user supplies their current belief, decision, or concern, treat it as the cognitive baseline and explicitly test how the source should update it. If not supplied, do not assume the user holds a naive or opposite view.

## Boundary with Deep Understanding

Use this skill when a *specific piece of material* is the object of reading and the outcome is what the user should newly learn, revise, qualify, or retain. Use `deep-understanding` when the object is a technical system, architecture, code path, SQL query, incident, or mechanism itself and the outcome is understanding how it works. Both may use mental models, diagrams, first principles, and verification; route by the user's object and desired outcome.

For finer execution details and quality checks, consult [references/analysis-framework.md](references/analysis-framework.md).
