# Daily Reflection Tree — README

## What This Is

An end-of-day deterministic reflection tool for employees. It walks through a structured conversation using a decision tree across three psychological axes. No LLM is called at runtime — the entire conversation is driven by lookups, tallies, and string templates.

---

## Repository Structure

```
/tree/
  reflection-tree.json          ← Part A: full tree data (36 nodes)
  tree-diagram.md               ← Part A: visual Mermaid diagram + statistics
/agent/
  agent.py                      ← Part B: CLI agent (Python, no dependencies)
/transcripts/
  persona-1-victor-transcript.md   ← Part B: Victor + Contribution + Wide path
  persona-2-victim-transcript.md   ← Part B: Victim + Entitlement + Self path
write-up.md                     ← Part A: design rationale (2 pages)
README.md                       ← This file
```

---

## How to Run the Agent (Part B)

**Requirements:** Python 3.7+ — no external libraries needed.

```bash
# From the repo root
python agent/agent.py
```

The agent will:
1. Load `tree/reflection-tree.json` automatically
2. Walk you through the session interactively in the terminal
3. Offer to save a transcript at the end

**Controls:**
- At `question` nodes: type the number (1–4) and press Enter
- At `start`, `reflection`, `bridge`, `summary` nodes: press Enter to continue
- `Ctrl+C` at any time to exit

---

## How to Read the Tree

The tree is in `reflection-tree.json`. Every node has this structure:

```json
{
  "id": "NODE_ID",
  "parentId": "PARENT_NODE_ID",
  "type": "start | question | decision | reflection | bridge | summary | end",
  "text": "What the employee sees (may contain {placeholders})",
  "options": ["Option A", "Option B", ...],
  "target": "NODE_ID to jump to (overrides parent-child traversal)",
  "signal": "axis:pole — what this node records in state"
}
```

### Node Types

| Type | Visible to employee | Interaction |
|------|--------------------|-|
| `start` | Yes | None — auto-advances |
| `question` | Yes | Employee picks one option |
| `decision` | No | Auto-routes based on prior answer |
| `reflection` | Yes | Employee reads, clicks Continue |
| `bridge` | Yes | None — auto-advances |
| `summary` | Yes | Reads interpolated synthesis |
| `end` | Yes | Session closes |

### How Decision Nodes Route

Decision node `options` contain routing rules, not user-visible choices:

```
"answer=Option A|Option B:TARGET_NODE_A;answer=Option C:TARGET_NODE_B"
```

This means: if the previous answer was "Option A" or "Option B", go to TARGET_NODE_A. If it was "Option C", go to TARGET_NODE_B.

### How State Accumulates

Each `signal` field on a node tallies toward the state object:

```
"axis1:internal"      →  state.axis1.internal += 1
"axis2:contribution"  →  state.axis2.contribution += 1
"axis3:wide"          →  state.axis3.wide += 1
```

The `dominant` value per axis is whichever pole has the higher count. This drives summary interpolation.

### How Placeholders Work

Reflection and summary nodes use `{node_id.answer}` and `{axis.dominant}` syntax:

```
"You described today as \"{A1_OPEN.answer}\"..."
```

At runtime, these are replaced with the stored answer from that node.

---

## Tracing a Path Manually

To trace any path without running code:

1. Start at node `id: "START"`
2. At `question` nodes: pick an option, store it as `answers[node_id]`
3. At `decision` nodes: match stored answer against routing rules, jump to the matched target
4. At `reflection` and `bridge` nodes: follow `target` field if present, otherwise follow `parentId` chain
5. At `summary`: substitute `{placeholders}` with stored answers and axis tallies
6. End at `id: "END"`

Three pre-traced example paths are included in the `possible_paths` array inside the JSON.

---

## Tree Statistics

| Metric | Count | Requirement |
|--------|-------|-------------|
| Total nodes | 36 | 25+ ✅ |
| Question nodes | 12 | 8+ ✅ |
| Decision nodes | 6 | 4+ ✅ |
| Reflection nodes | 9 | 4+ ✅ |
| Bridge nodes | 2 | 2+ ✅ |
| Summary nodes | 1 | 1+ ✅ |
| Axes covered | 3/3 | All 3 ✅ |
| Options per question | 4 (all) | 3–5 ✅ |

---

## Psychological Framework

| Axis | Spectrum | Sources |
|------|----------|---------|
| Axis 1: Locus | Victim ↔ Victor | Rotter (1954) Locus of Control; Dweck (2006) Growth Mindset |
| Axis 2: Orientation | Entitlement ↔ Contribution | Campbell et al. (2004); Organ (1988) OCB |
| Axis 3: Radius | Self-Centric ↔ Altrocentric | Maslow (1969) Self-Transcendence; Batson (2011) Perspective-Taking |

---

## Design Constraints Met

- ✅ No LLM at runtime — fully deterministic
- ✅ Fixed options only — no free text input
- ✅ Same answers always produce same path
- ✅ Reflections use interpolation, not generated text
- ✅ Tree is readable as data without running code
- ✅ Three axes flow in sequence with psychological progression
