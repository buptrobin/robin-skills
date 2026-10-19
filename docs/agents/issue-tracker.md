# Issue tracker: Local Markdown

Issues and specs for this repo live as Markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is a `Status:` line near the top of each issue file; use the roles in `triage-labels.md`
- Append conversation history under `## Comments`

## When a skill says "publish to the issue tracker"

Create a file under `.scratch/<feature-slug>/`, creating directories as needed.

## When a skill says "fetch the relevant ticket"

Read the referenced file. The user normally supplies its path or issue number.

## Wayfinding operations

- Map: `.scratch/<effort>/map.md`, containing Notes, Decisions-so-far, and Fog.
- Child ticket: `.scratch/<effort>/issues/NN-<slug>.md`; `Type:` records `research`, `prototype`, `grilling`, or `task`; `Status:` records `claimed` or `resolved`.
- Blocking: `Blocked by: NN, NN`; all listed tickets must be resolved.
- Frontier: first numbered open, unblocked, unclaimed ticket.
- Claim: set `Status: claimed` before work.
- Resolve: add `## Answer`, set `Status: resolved`, and add a context pointer to the map.
