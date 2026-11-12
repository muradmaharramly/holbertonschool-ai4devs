# User Stories - AI Decision Helper

This document defines the user requirements, user stories, acceptance criteria, and delivery priorities for the **AI Decision Helper** MVP, translating the concepts defined in [`team_ideation.md`](./team_ideation.md) into concrete engineering specifications.

---

## User Story 1: Submit Decision Problem and Context
As a user facing decision fatigue,  
I want to submit a dilemma with background context and constraints,  
so that the AI can understand my situation and formulate a structured decision evaluation.

**Acceptance Criteria**:
- The user can input a decision title (e.g., "Should our team adopt Microservices or remain with a Modular Monolith?") and detailed background description (minimum 20 characters, up to 2,000 characters).
- The user can optionally specify key constraints (e.g., budget limits, timeline, team skill level, risk tolerance).
- The system validates input non-emptiness and sanitizes text prior to submission.
- Upon submission, a new decision session is initialized with status `DRAFT` and assigned a unique identifier.

**Priority**: MVP (Must Have)

---

## User Story 2: Define Candidate Options
As a decision maker,  
I want to input explicit alternatives or have the AI automatically suggest viable choices,  
so that the evaluation covers all realistic paths forward.

**Acceptance Criteria**:
- The user can manually define two or more discrete decision options (e.g., Option A vs. Option B).
- If the user provides an open dilemma without explicit options, the system provides an "Auto-Detect Options" button that extracts distinct alternatives from the scenario description.
- Each option contains a concise title (maximum 100 characters) and an optional description.
- The interface allows adding, editing, and removing options before analysis execution.

**Priority**: MVP (Must Have)

---

## User Story 3: Generate Structured Pros and Cons
As a user evaluating alternatives,  
I want the AI to generate balanced, categorized pros and cons for each option,  
so that I can objectively compare trade-offs without personal cognitive bias.

**Acceptance Criteria**:
- The system sends a structured prompt to the AI provider requesting between 3 and 5 pros and 3 and 5 cons per candidate option.
- Each generated point includes a category tag (e.g., `Financial`, `Technical`, `Operational`, `Strategic`) and an objective explanation.
- The AI output is returned in validated JSON format conforming to the expected schema.
- The UI renders pros in positive/green visual containers and cons in warning/red visual containers under each option.
- If the AI call fails or times out, an informative error message is displayed with a one-click retry trigger.

**Priority**: MVP (Must Have)

---

## User Story 4: Impact and Urgency Weighting
As an analytical decision maker,  
I want each pro and con to indicate an estimated impact weight and risk level,  
so that minor trivial points do not skew the comparison against critical factors.

**Acceptance Criteria**:
- The AI assigns a default impact weight (`Low`, `Medium`, `High`, `Critical`) to each generated pro and con based on context.
- The user can interactively adjust or override the impact weight of any item using an intuitive UI selector.
- The system visually highlights `Critical` and `High` impact factors to emphasize major trade-offs.
- Adjusted weights immediately update the computed aggregate score for the corresponding option.

**Priority**: MVP (Must Have)

---

## User Story 5: Cast User Preference Votes
As a user or team member,  
I want to vote for my preferred option and record confidence levels,  
so that my qualitative preference is formally captured in the decision record.

**Acceptance Criteria**:
- The user can select their preferred option and optionally submit an agreement/confidence rating from 1 to 5 stars.
- The user can attach an optional rationale note explaining their vote.
- Multiple team members can record independent votes against the same decision session.
- The interface displays the live vote distribution and current consensus percentage across all options.

**Priority**: MVP (Must Have)

---

## User Story 6: Synthesize Recommendation and Summary
As a busy stakeholder,  
I want the AI to synthesize the weighted arguments and votes into a clear recommendation,  
so that I have an actionable conclusion to act upon.

**Acceptance Criteria**:
- The system provides a "Generate Recommendation" action that evaluates options, weighted pros/cons, and recorded votes.
- The AI produces a concise 2–3 paragraph executive summary outlining the recommended option, key rationale, trade-off compromises, and immediate next steps.
- The recommendation explicitly references the highest-weighted pros and mitigation strategies for identified cons.
- The decision record status updates to `DECIDED`.

**Priority**: MVP (Must Have)

---

## User Story 7: Decision History and Retrieval
As a returning user,  
I want to view a historical log of past decisions and their final rationales,  
so that I can review past reasoning and prevent decision rework.

**Acceptance Criteria**:
- The dashboard displays a chronological list of all saved decisions with status badges (`DRAFT`, `ANALYZED`, `DECIDED`).
- Each entry shows the title, creation date, chosen option, and total options evaluated.
- The user can filter past decisions by keyword, status, or date range.
- Clicking any decision loads the complete interactive breakdown, including options, arguments, and vote outcomes.

**Priority**: High (Should Have)

---

## User Story 8: Export and Share Decision Report
As a team collaborator,  
I want to export the complete decision matrix as Markdown or PDF,  
so that I can share the rationale with leadership or archive it in team documentation.

**Acceptance Criteria**:
- The user can click an "Export" action and select Markdown (`.md`) or printable HTML/PDF format.
- The exported report contains the dilemma statement, options comparison table, all categorized pros and cons with weights, voting tally, and final AI recommendation.
- The export retains clean formatting suitable for pasting directly into Notion, GitHub Discussions, or Confluence.
- The action completes client-side or via an API endpoint in under 2 seconds.

**Priority**: High (Should Have)

---

## Summary Matrix

| ID | User Story Title | User Role | Core Value | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **US-01** | Submit Decision Problem & Context | Decision Maker | Define problem boundary and constraints | MVP |
| **US-02** | Define Candidate Options | Decision Maker | Establish discrete alternatives to compare | MVP |
| **US-03** | Generate Structured Pros & Cons | Decision Maker | Eliminate bias with objective AI trade-offs | MVP |
| **US-04** | Impact & Urgency Weighting | Analytical User | Separate critical trade-offs from noise | MVP |
| **US-05** | Cast User Preference Votes | Team Member | Capture human consensus and confidence | MVP |
| **US-06** | Synthesize Recommendation | Stakeholder | Produce actionable next steps from analysis | MVP |
| **US-07** | Decision History & Retrieval | Returning User | Audit trail of past reasoning and outcomes | Should Have |
| **US-08** | Export & Share Decision Report | Collaborator | Seamless handoff to team documentation | Should Have |
