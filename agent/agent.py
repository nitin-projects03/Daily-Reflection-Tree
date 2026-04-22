"""
Daily Reflection Tree — CLI Agent
Loads reflection-tree.json and walks the employee through the conversation.
No LLM calls at runtime. Fully deterministic.
"""
 
import json
import os
import sys
import time
 
# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
BLUE    = "\033[94m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
MAGENTA = "\033[95m"
WHITE   = "\033[97m"
 
def c(color, text):
    return f"{color}{text}{RESET}"
 
def clear():
    os.system("cls" if os.name == "nt" else "clear")
 
def slow_print(text, delay=0.018):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()
 
def divider():
    print(c(DIM, "─" * 60))
 
 
# ── TREE LOADER ───────────────────────────────────────────────────────────────
 
def load_tree(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    nodes = {n["id"]: n for n in data["nodes"]}
    return nodes
 
 
# ── STATE ─────────────────────────────────────────────────────────────────────
 
def fresh_state():
    return {
        "axis1": {"internal": 0, "external": 0},
        "axis2": {"contribution": 0, "entitlement": 0},
        "axis3": {"self": 0, "dyad": 0, "wide": 0},
        "answers": {}
    }
 
def apply_signal(state, signal):
    if not signal:
        return
    axis, pole = signal.split(":")
    if axis in state and pole in state[axis]:
        state[axis][pole] += 1
 
def dominant(state, axis):
    counts = state[axis]
    return max(counts, key=counts.get)
 
def axis3_label(state):
    d = dominant(state, "axis3")
    labels = {
        "self":  "yourself primarily",
        "dyad":  "yourself and a specific colleague",
        "wide":  "your team and beyond"
    }
    return labels.get(d, "yourself")
 
 
# ── INTERPOLATION ─────────────────────────────────────────────────────────────
 
def interpolate(text, state):
    if not text:
        return text
    text = text.replace("{axis1.dominant}", dominant(state, "axis1"))
    text = text.replace("{axis2.dominant}", dominant(state, "axis2"))
    text = text.replace("{axis3.dominant}", dominant(state, "axis3"))
    text = text.replace("{axis3.label}",    axis3_label(state))
    for node_id, answer in state["answers"].items():
        text = text.replace(f"{{{node_id}.answer}}", answer)
    return text
 
 
# ── ROUTING ───────────────────────────────────────────────────────────────────
 
def resolve_decision(node, state):
    """
    Parse routing rules from a decision node's options list.
    Format: "answer=Opt A|Opt B:TARGET_NODE;answer=Opt C:OTHER_NODE"
    Returns the target node id.
    """
    last_answer_id = node["parentId"]
    last_answer = state["answers"].get(last_answer_id, "")
 
    for rule_block in node["options"]:
        for rule in rule_block.split(";"):
            rule = rule.strip()
            if not rule:
                continue
            condition, target = rule.split(":")
            _, options_str = condition.split("=", 1)
            options = [o.strip() for o in options_str.split("|")]
            if last_answer in options:
                return target.strip()
    return None
 
 
# ── NODE RENDERERS ────────────────────────────────────────────────────────────
 
def render_start(node, state):
    clear()
    print()
    divider()
    slow_print(c(BLUE, BOLD + "  🌙  Daily Reflection" + RESET))
    divider()
    print()
    slow_print(c(WHITE, "  " + interpolate(node["text"], state)))
    print()
    input(c(DIM, "  Press Enter to begin..."))
    return node.get("target")
 
 
def render_question(node, state):
    clear()
    print()
    divider()
    slow_print(c(CYAN, BOLD + "  Question" + RESET))
    divider()
    print()
    slow_print(c(WHITE, "  " + interpolate(node["text"], state)))
    print()
 
    options = node["options"]
    for i, opt in enumerate(options, 1):
        print(c(YELLOW, f"    {i}.") + f" {opt}")
    print()
 
    while True:
        raw = input(c(DIM, "  Your choice (number): ")).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            chosen = options[int(raw) - 1]
            state["answers"][node["id"]] = chosen
            apply_signal(state, node.get("signal"))
            print()
            print(c(DIM, f"  ✓  \"{chosen}\""))
            time.sleep(0.6)
            return node.get("target")
        print(c(MAGENTA, f"  Please enter a number between 1 and {len(options)}."))
 
 
def render_decision(node, state):
    target = resolve_decision(node, state)
    return target
 
 
def render_reflection(node, state):
    clear()
    print()
    divider()
    slow_print(c(MAGENTA, BOLD + "  Reflection" + RESET))
    divider()
    print()
    slow_print(c(WHITE, "  " + interpolate(node["text"], state)), delay=0.012)
    print()
    apply_signal(state, node.get("signal"))
    input(c(DIM, "  Press Enter to continue..."))
    return node.get("target")
 
 
def render_bridge(node, state):
    clear()
    print()
    divider()
    slow_print(c(YELLOW, BOLD + "  ───" + RESET))
    print()
    slow_print(c(WHITE, "  " + interpolate(node["text"], state)))
    print()
    time.sleep(1.2)
    return node.get("target")
 
 
def render_summary(node, state):
    clear()
    print()
    divider()
    slow_print(c(GREEN, BOLD + "  Today's Reflection" + RESET))
    divider()
    print()
    summary_text = interpolate(node["text"], state)
    for line in summary_text.split("\n"):
        slow_print(c(WHITE, "  " + line), delay=0.010)
    print()
    input(c(DIM, "  Press Enter to finish..."))
    return node.get("target")
 
 
def render_end(node, state):
    clear()
    print()
    divider()
    slow_print(c(BLUE, BOLD + "  " + node["text"] + RESET))
    divider()
    print()
    return None
 
 
# ── WALK ──────────────────────────────────────────────────────────────────────
 
RENDERERS = {
    "start":      render_start,
    "question":   render_question,
    "decision":   render_decision,
    "reflection": render_reflection,
    "bridge":     render_bridge,
    "summary":    render_summary,
    "end":        render_end,
}
 
def walk(nodes, state, start_id="START"):
    current_id = start_id
    visited = []
 
    while current_id:
        node = nodes.get(current_id)
        if not node:
            print(c(MAGENTA, f"[ERROR] Node '{current_id}' not found in tree."))
            break
 
        visited.append(current_id)
        renderer = RENDERERS.get(node["type"])
        if not renderer:
            print(c(MAGENTA, f"[ERROR] Unknown node type: {node['type']}"))
            break
 
        next_id = renderer(node, state)
 
        # If no explicit target/return, find next sibling by parentId chain
        if not next_id and node["type"] not in ("end", "decision"):
            # Look for a node whose parentId matches current node id
            children = [n for n in nodes.values() if n.get("parentId") == current_id]
            if children:
                next_id = children[0]["id"]
 
        current_id = next_id
 
    return visited, state
 
 
# ── TRANSCRIPT ────────────────────────────────────────────────────────────────
 
def save_transcript(visited, state, nodes, filename):
    lines = []
    lines.append("# Reflection Session Transcript\n")
    lines.append(f"**Path:** {' → '.join(visited)}\n")
    lines.append("\n---\n")
 
    for node_id in visited:
        node = nodes.get(node_id)
        if not node:
            continue
        ntype = node["type"].upper()
        text = interpolate(node.get("text") or "", state)
        if ntype in ("DECISION",):
            continue  # internal, skip
        lines.append(f"### [{ntype}] {node_id}")
        if text:
            lines.append(f"\n{text}\n")
        answer = state["answers"].get(node_id)
        if answer:
            lines.append(f"\n> **Employee chose:** {answer}\n")
        lines.append("")
 
    lines.append("\n---\n")
    lines.append("## Session Summary\n")
    lines.append(f"- **Axis 1 (Locus):** {dominant(state, 'axis1')}")
    lines.append(f"- **Axis 2 (Orientation):** {dominant(state, 'axis2')}")
    lines.append(f"- **Axis 3 (Radius):** {dominant(state, 'axis3')} ({axis3_label(state)})")
    lines.append(f"\n**Full answer log:**")
    for k, v in state["answers"].items():
        lines.append(f"- {k}: {v}")
 
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(c(GREEN, f"\n  Transcript saved → {filename}"))
 
 
# ── MAIN ──────────────────────────────────────────────────────────────────────
 
def main():
    # Resolve tree file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tree_path = os.path.join(script_dir, "..", "tree", "reflection-tree.json")
 
    if not os.path.exists(tree_path):
        # Try same directory
        tree_path = os.path.join(script_dir, "reflection-tree.json")
 
    if not os.path.exists(tree_path):
        print(c(MAGENTA, f"[ERROR] Could not find reflection-tree.json"))
        print(c(DIM, "Expected at: ../tree/reflection-tree.json"))
        sys.exit(1)
 
    nodes = load_tree(tree_path)
    state = fresh_state()
 
    try:
        visited, state = walk(nodes, state)
    except KeyboardInterrupt:
        print(c(DIM, "\n\n  Session interrupted.\n"))
        sys.exit(0)
 
    # Ask to save transcript
    print()
    save = input(c(DIM, "  Save transcript? (y/n): ")).strip().lower()
    if save == "y":
        transcript_dir = os.path.join(script_dir, "..", "transcripts")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(transcript_dir, f"session_{timestamp}.md")
        save_transcript(visited, state, nodes, filename)
    print()
 
 
if __name__ == "__main__":
    main()
 
