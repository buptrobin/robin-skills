# Representation Guide

Choose by what the reader must mentally simulate. A richer format is useful only if it reduces that work or enables a check the simpler one cannot.

| Reader's task | Useful form | What to show |
| --- | --- | --- |
| Understand a claim or cause | Prose | Actor, action, reason, consequence |
| Compare options or evidence | Table | Stable comparison criteria and important exceptions |
| See components or branches | Flowchart or image | Boundaries, directions, decision conditions |
| Follow calls, retries, or time | Sequence diagram | Actors, order, waits, failures |
| Follow legal states | State diagram | States, transition triggers, invalid paths |
| Understand a transformation | Worked example | Small input, intermediate step, output |
| Explore changing inputs or paths | Interactive page | Controls, immediate feedback, representative presets |
| See motion or narration explain a process | Video | Scene-by-scene causal progression, readable labels |

Use Mermaid for a compact technical diagram when it renders well in the user's destination. Use another drawing format when spatial layout or visual detail matters. Keep labels short and put nuance beside the diagram. A diagram must make at least one relationship easier to check than prose would.

For an interactive page, define the one question each control answers. Show the current input and resulting state together. Test the initial view and meaningful control paths. Mark toy data, approximations, and simulated behavior so the page does not appear to prove more than it does.

For a video, first identify what must change on screen to make the mechanism clear. Check pacing, label legibility, narration alignment, and final playback. A video can teach a process, but important claims and limitations should remain accessible as text or captions for inspection.

Combine formats only when they answer different questions. Respect a requested format even when another might also work.
