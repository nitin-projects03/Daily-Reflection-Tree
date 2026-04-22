# Write-Up: Daily Reflection Tree — Design Rationale

**Assignment:** DT Fellowship — Daily Reflection Tree (Part A)
**Submitted by:** Tarun Ayitam

---

## 1. Why These Specific Questions

### The core design problem

The hardest thing about this assignment is not building a tree. It's writing questions that a tired employee at 7pm would actually stop and think about — rather than click through in 30 seconds without reading.

I approached every question with one test: *would a real person need to pause before answering this?* If the "right" answer was too obvious, I rewrote the question.

### Axis 1 — Locus of Control

I opened with a metaphor ("if today were a road") rather than a direct question about control. Direct questions like "did you feel in control today?" are too transparent — the employee immediately knows what the "healthy" answer is and picks it. A metaphor is more disarming. Choosing between "smooth," "bumpy," "winding," and "blocked" requires actual recall of the day, not self-presentation.

The follow-up questions (A1_Q_AGENCY_HIGH and LOW) were designed around one insight from Rotter (1954): locus of control is most visible not in outcomes, but in *attributions*. When things went well, did you point to your own behavior or to circumstance? When things went badly, did you look for a micro-choice you still had, or did you wait for someone else to fix it?

The third question per branch (A1_Q_CHOICE_*) deliberately asks about one specific moment, because the psychology literature (Dweck, 2006) shows that mindset is domain-specific — a person can have a growth mindset at work and a fixed mindset in personal life. One concrete moment is more honest than a generalised self-assessment.

### Axis 2 — Contribution vs Entitlement

Entitlement is nearly impossible to ask about directly — the entitlement-oriented employee doesn't experience themselves as entitled, they experience themselves as *underappreciated*. So the opening question (A2_OPEN) is framed neutrally: "giving or receiving focus?" This surfaces the orientation without attaching a moral charge.

For the entitlement branch (A2_Q_ENTITLE), I followed Campbell et al. (2004)'s observation that entitlement usually has a *trigger* — a felt injustice or deficit of recognition. Asking "what drove that focus today?" is more useful than reflecting their answer back as a flaw. If the employee feels unseen, that's real data about the team environment, not just about their character.

The contribution branch includes A2_Q_EXPECTATION — asking what they expected back after giving. This is the most important question in Axis 2, because contribution without expectation (Organ, 1988 — OCB) is qualitatively different from contribution-as-transaction. The question makes that distinction real for the employee.

### Axis 3 — Radius of Concern

The opening question asks "who is in the frame?" — not "how many people did you think about?" The word *frame* is deliberate. It triggers spatial, visual thinking rather than abstract counting, which tends to produce more honest answers.

I designed the three branches (self, dyad, wide) to feel non-judgmental at every level. The self-centric branch doesn't shame narrow focus — it gently asks whether the problem will ripple outward. The dyad branch rewards the specific, concrete form of empathy (thinking about one colleague) over the abstract "I care about the team." The wide branch acknowledges that broad perspective-taking is cognitively expensive — because Batson (2011) shows that perspective-taking fatigues under stress — and names that cost explicitly in the reflection.

---

## 2. How I Designed the Branching

### Routing philosophy

The decision nodes use the minimum information needed to branch. I avoided over-branching early (before the tree has enough signal) and over-merging late (when the tree has enough signal to say something specific).

**Key trade-off: depth vs. breadth.** Each axis has 2-3 levels of branching, not 4-5. Deeper branching creates more personalized paths but also more dead-ends and harder maintenance. At 36 nodes covering 3 axes, the tree is already complex enough to feel responsive without becoming a maze.

**The mixed path (A1_Q_CHOICE_MIXED)** is shared between two branches (high agency who attributed success to luck, and low agency who still found one thing to control). This was a deliberate convergence — both of these employee states are psychologically similar: they've partially internalized agency and partially externalized it. The same question serves both, and the reflection they land on is appropriately nuanced.

### Axis transitions

The bridge nodes (BRIDGE_1_2, BRIDGE_2_3) are not decorative. They do psychological work: they signal to the employee that the conversation is *moving*, not looping. "Now let's move from how you handled today — to what you put into it" marks a clear shift from cognitive/behavioral reflection (Axis 1) to social/relational reflection (Axis 2). This sequencing mirrors the progression in Maslow's hierarchy from personal efficacy to social contribution to transcendence.

### Summary interpolation

The summary node uses three stored signals (`axis1.dominant`, `axis2.dominant`, `axis3.dominant`) plus the employee's literal opening answer (`A1_OPEN.answer`) to produce a reflection that feels personal. The goal was to avoid a generic closing — the summary should say something the employee couldn't have predicted when they started.

---

## 3. Psychological Sources

| Source | How it shaped the design |
|--------|--------------------------|
| Rotter (1954) — Locus of Control | Axis 1 structure; attribution-based questions (not outcome-based) |
| Dweck (2006) — Growth vs Fixed Mindset | Axis 1 follow-up design; asking about one specific moment rather than a generalised self-assessment |
| Campbell et al. (2004) — Psychological Entitlement | Axis 2 entitlement branch; framing "what drove that focus?" rather than naming entitlement directly |
| Organ (1988) — Organizational Citizenship Behavior | Axis 2 contribution questions; distinguishing OCB (discretionary, uncharged) from strategic giving |
| Maslow (1969) — Self-Transcendence | Axis 3 structure; the progression from self → dyad → wide mirrors Maslow's transcendence arc |
| Batson (2011) — Perspective-Taking | Axis 3 wide-radius reflection; acknowledging the cognitive cost of holding others' experience under stress |

---

## 4. What I Would Improve With More Time

**a) More branching within Axis 2 entitlement**
The current entitlement branch has only one follow-up question before the reflection. A longer path would ask a second question — for example, whether the felt unfairness was about *this specific interaction* or a pattern over weeks. That distinction changes the quality of the reflection significantly.

**b) Cross-axis memory**
Currently, the summary uses each axis's dominant signal independently. A better summary would notice *combinations* — for example, someone who is external on Axis 1 (low agency) but contribution-oriented on Axis 2 is a very different profile from someone who is external on both. Cross-axis signals would make the summary sharper.

**c) A "return" question**
The tree currently ends without asking the employee what they will do differently tomorrow. Adding one optional question at the summary stage — "One thing you'd carry into tomorrow?" with 3-4 grounded options — would close the loop between reflection and action, which is the gap between awareness and change.

**d) Validation testing with real employees**
The questions were designed on paper. Real testing would reveal which options are too similar to distinguish (leading to arbitrary clicks) and which questions feel intrusive rather than insightful. I'd iterate at least two rounds before considering the question design stable.

---

*Total nodes: 36 | Axes covered: 3 | Deterministic: yes | LLM at runtime: none*
