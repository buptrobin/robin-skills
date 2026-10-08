---
name: deep-understanding
description: "Explain and help inspect complex model outputs, technical proposals, code paths, or research findings. Use when the user needs to understand a mechanism, judge a result, or explore its behavior through prose, a diagram, an example, an interactive page, or a video."
---

# Deep Understanding

Make a complex result easier to understand **and check**. Inspired by [Karpathy's post on understanding model outputs](https://x.com/karpathy/status/2105819303471976479). The post suggests clear technical writing, diagrams, interactive pages, and custom explainer videos as increasingly expressive options. Treat these as choices, not a required sequence or a ranking that overrides the user's requested format.

## Work out what the reader needs to see

- Identify the question or decision behind the request and the reader's likely knowledge gap. If the user asks for a specific format, honor it.
- Inspect the supplied material and relevant evidence. Build a small internal model of the actors, flow, state, assumptions, and causal links that matter to this question. Do not present inferred behavior as observed behavior.
- Preserve the details that could change the reader's judgment: correctness conditions, limitations, tradeoffs, failure paths, and uncertainty. Skip details that do not help them predict or assess the result.

## Choose and make the explanation

Use the simplest format that lets the reader understand and inspect the important behavior. Follow [the representation guide](references/representation-guide.md) when a visual or artifact might help.

- **Prose:** Explain the core mechanism and its consequence in plain language. For dense English technical writing, use the ASD-STE100-inspired principles in [clear writing](references/clear-writing.md). This is a readability style, not a claim of standard compliance. Apply the same clarity principles in the user's language.
- **Diagram or worked example:** Make relationships, order, state changes, or a transformation visible. Label the meaningful edges and conditions. Explain what the visual leaves out.
- **Interactive page:** When changing inputs, stepping through time, or comparing branches is central to understanding, build a small runnable page with controls and visible outcomes. State which parts are illustrative or simulated.
- **Explainer video:** When the user asks for video, or motion and narration would materially clarify a changing process, make a video if the available tools permit it. Keep the explanation tied to the actual source, and verify the rendered output. If a paid service or missing credential is required, use an available local route or explain the specific blocker.

Do the artifact work when the request calls for an artifact. Do not substitute a description of a diagram, page, or video for the deliverable. Avoid making a larger artifact merely because it is possible.

## Check that the model is usable

- Can the reader use the explanation to predict what happens in one representative case and one important edge case?
- Are claims supported by the supplied source, code, or observations? Mark consequential inferences and unknowns; give a focused way to check them.
- If reviewing an AI-generated plan or result, surface the few issues that could change the decision. Do not invent problems or turn every explanation into a full audit.
- Check artifacts in the form the reader will use: render diagrams, operate interactive controls, and inspect video playback where applicable. Fix broken labels, missing states, and misleading examples.

Start with the answer or the smallest useful model. Add depth only where it resolves a real question. Use headings and a final takeaway only when they help this reader; do not force a fixed report template.
