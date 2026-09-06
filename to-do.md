# AI-Based Research Paper Review System

## 1. Project Overview

The **AI-Based Research Paper Review System** is a prototype designed to
assist editors and researchers in the early-stage evaluation of academic
research papers.

The system does **not replace human peer reviewers**. Instead, it acts
as an intelligent **pre-review and editorial screening layer**. It
accepts a research paper in PDF format, extracts and preprocesses its
content, sends different aspects of the paper to specialized AI agents,
aggregates their findings, performs plagiarism/similarity analysis,
supports an editorial decision, and finally recommends suitable human
reviewers.

The prototype should visually and functionally represent the complete
workflow shown in the proposed system architecture:

``` text
Research Paper Upload
        ↓
PDF Parsing & Preprocessing
        ↓
Multi-Agent Review Layer
        ↓
Report Aggregation Agent
        ↓
Editorial Decision Agent
        ↓
 ┌──────┼───────────────────────┐
 ↓      ↓                       ↓
Revision Required       Ready for Review
   ↓                           ↓
Author Resubmission       Plagiarism Detection
                               ↓
                    ┌──────────┴──────────┐
                    ↓                     ↓
              High Similarity       Acceptable Similarity
                    ↓                     ↓
                  Alert             Reviewer Assignment
                                          ↓
                                  Human Peer Review
```

------------------------------------------------------------------------

# 2. Main Objective

Build a polished, interactive web prototype that demonstrates how AI can
support the research-paper review pipeline.

The prototype must make it easy for a user to:

1.  Upload a research paper.
2.  See PDF parsing and preprocessing happen.
3.  See individual AI review agents evaluate the paper.
4.  View the combined review report.
5.  See an editorial recommendation.
6.  See whether revision is required or the paper is ready for review.
7.  Run/view plagiarism and similarity analysis.
8.  View an alert when similarity is high.
9.  View recommended human reviewers.
10. Understand that the final peer-review decision remains with humans.

------------------------------------------------------------------------

# 3. Important Product Principle

This is an **AI-assisted review system**, not an autonomous
publication/rejection system.

The AI should provide:

-   Findings
-   Scores
-   Warnings
-   Recommendations
-   Explanations
-   Reviewer suggestions

The system should clearly communicate that:

> **Final publication and peer-review decisions are made by qualified
> human reviewers/editors.**

Do not present the prototype as an actual scientific publishing platform
or claim that its AI decisions are scientifically authoritative.

------------------------------------------------------------------------

# 4. Proposed System Architecture

## 4.1 Research Paper Upload

The user starts by uploading a PDF research paper.

### UI requirements

Create a prominent upload area containing:

-   Drag-and-drop PDF upload
-   Browse/select PDF button
-   Uploaded file name
-   File size
-   Upload status
-   Start Analysis button

Example:

``` text
┌─────────────────────────────────────────────┐
│                                             │
│          Upload Research Paper              │
│                                             │
│       Drag & drop PDF here                  │
│                 or                          │
│             [ Browse PDF ]                  │
│                                             │
│       Supported format: PDF                 │
└─────────────────────────────────────────────┘
```

After upload, show the paper information.

Example:

``` text
Paper:
AI-Driven Carbon Emission Prediction Using
Multi-Agent Systems.pdf

Status: Ready for Analysis
[ Start AI Review ]
```

------------------------------------------------------------------------

# 5. PDF Parsing & Preprocessing

After the user starts analysis, simulate or implement the extraction
pipeline.

The system should identify:

-   Text
-   Figures
-   Tables
-   Equations
-   References
-   Metadata

### Example dashboard

``` text
PDF Parsing & Preprocessing

✓ Text Extraction       Completed
✓ Figures Detection     12 figures
✓ Tables Detection       6 tables
✓ Equations Detection   18 equations
✓ References Extraction 42 references
✓ Metadata Extraction   Completed
```

Use animated progress states where appropriate.

For the prototype, actual PDF parsing can be implemented if practical.
If not, use a realistic mock processing pipeline based on the uploaded
PDF and clearly keep the AI analysis demonstrative.

------------------------------------------------------------------------

# 6. Multi-Agent Review Layer

This is the core of the system.

Create a visually distinct **Multi-Agent Review Layer** containing seven
specialized agents.

## Agent 1 --- Layout Agent

### Responsibility

Evaluate the visual and structural presentation of the paper.

Check:

-   Page consistency
-   Margins
-   Figure placement
-   Table placement
-   Heading consistency
-   Spacing
-   Overall formatting quality

### Example output

``` text
Layout Score: 88/100

✓ Consistent page structure
✓ Figures generally positioned correctly
⚠ Two figures appear too close to section boundaries
```

------------------------------------------------------------------------

## Agent 2 --- Structure Agent

### Responsibility

Evaluate the organization of the research paper.

Check for:

-   Title
-   Abstract
-   Introduction
-   Related Work
-   Methodology
-   Results
-   Discussion
-   Conclusion
-   References

### Example output

``` text
Structure Score: 91/100

✓ Clear section hierarchy
✓ Logical progression
⚠ Related Work section could be better connected to the proposed methodology
```

------------------------------------------------------------------------

## Agent 3 --- Formatting Agent

### Responsibility

Evaluate formatting consistency.

Check:

-   Font consistency
-   Heading styles
-   Figure captions
-   Table captions
-   Numbering
-   References formatting
-   Section formatting

### Example output

``` text
Formatting Score: 84/100

✓ Heading formatting is consistent
⚠ Reference formatting contains inconsistencies
⚠ Two table captions use different formatting
```

------------------------------------------------------------------------

## Agent 4 --- Language Agent

### Responsibility

Evaluate writing quality.

Check:

-   Grammar
-   Spelling
-   Sentence construction
-   Clarity
-   Readability
-   Academic tone
-   Repetition

### Example output

``` text
Language Score: 86/100

✓ Professional academic tone
✓ Generally clear writing
⚠ 7 sentences are overly complex
⚠ Minor grammar issues detected
```

------------------------------------------------------------------------

## Agent 5 --- Citation Agent

### Responsibility

Evaluate citation and reference quality.

Check:

-   Citation presence
-   Citation consistency
-   Reference formatting
-   Uncited claims
-   Reference completeness
-   Citation-reference matching

### Example output

``` text
Citation Score: 79/100

✓ Most major claims are cited
⚠ 4 claims may require citations
⚠ 3 references appear incomplete
```

------------------------------------------------------------------------

## Agent 6 --- Technical Review Agent

### Responsibility

Evaluate the technical quality of the research.

Check:

-   Problem definition
-   Methodology
-   Technical correctness indicators
-   Experimental design
-   Results
-   Discussion
-   Limitations
-   Novelty indicators
-   Reproducibility indicators

### Example output

``` text
Technical Score: 82/100

✓ Problem is clearly defined
✓ Methodology is reasonably detailed
✓ Experimental results are presented
⚠ Dataset limitations are not sufficiently discussed
⚠ Reproducibility information could be improved
```

Important:

The prototype should present these as **AI-generated review findings**,
not as guaranteed scientific truth.

------------------------------------------------------------------------

## Agent 7 --- Scope Matching Agent

### Responsibility

Determine whether the paper fits the target journal/conference scope.

The user should be able to select or enter a target venue.

Example:

``` text
Target Venue:
International Conference on Artificial Intelligence

Scope Match: 92%

✓ AI/ML related topic
✓ Relevant research methodology
✓ Appropriate application domain
```

If no target venue is provided, use a generic research-domain
classification.

------------------------------------------------------------------------

# 7. Multi-Agent Dashboard

Create a central dashboard showing all seven agents.

Example:

``` text
                 MULTI-AGENT REVIEW

┌────────────┐ ┌────────────┐ ┌────────────┐
│ Layout     │ │ Structure  │ │ Formatting │
│    88      │ │    91      │ │    84      │
│  Completed │ │ Completed  │ │ Completed  │
└────────────┘ └────────────┘ └────────────┘

┌────────────┐ ┌────────────┐ ┌────────────┐
│ Language   │ │ Citation   │ │ Technical  │
│    86      │ │    79      │ │    82      │
│ Completed  │ │ Completed  │ │ Completed  │
└────────────┘ └────────────┘ └────────────┘

              ┌───────────────┐
              │ Scope Match   │
              │      92       │
              │   Completed   │
              └───────────────┘
```

Each agent should be clickable to open its detailed findings.

------------------------------------------------------------------------

# 8. Report Aggregation Agent

The **Report Aggregation Agent** combines the outputs from all
specialized agents.

Its purpose is to create one unified review report.

### Dashboard should contain

-   Overall score
-   Strengths
-   Major concerns
-   Minor concerns
-   Agent-wise scores
-   Priority issues
-   Recommended actions

Example:

``` text
Overall AI Review Score
        85 / 100

Strengths
✓ Strong paper structure
✓ Clear methodology
✓ Good scope alignment

Major Concerns
⚠ Citation completeness
⚠ Dataset limitations
⚠ Reference formatting

Minor Concerns
• Sentence complexity
• Figure placement
• Caption consistency
```

------------------------------------------------------------------------

# 9. Editorial Decision Agent

The Editorial Decision Agent consumes the aggregated report and
generates an editorial recommendation.

Possible prototype decisions:

### Ready for Review

``` text
READY FOR REVIEW

The paper satisfies the minimum AI-assisted
screening criteria.

Next Step:
Plagiarism / Similarity Detection
```

### Revision Required

``` text
REVISION REQUIRED

The paper contains issues that should be
addressed before entering human peer review.

[ View Required Revisions ]
[ Return to Author ]
```

### Reject / Do Not Proceed

If implemented, use this only as an editorial screening recommendation
and make it clear that it is not a final scientific rejection.

Example:

``` text
NOT RECOMMENDED FOR CURRENT REVIEW

Significant issues were identified during
automated screening.

[ View Report ]
[ Return to Author ]
```

------------------------------------------------------------------------

# 10. Revision Workflow

If revision is required, the author should be able to see the problems.

Example:

``` text
REVISION REQUIRED

Priority  Issue
High      Missing discussion of dataset limitations
High      4 potentially unsupported claims
Medium    Reference formatting inconsistencies
Medium    Figure caption inconsistency
Low       Sentence readability issues

[ Download Review Report ]
[ Resubmit Revised Paper ]
```

The resubmission flow should return the user to the upload/analysis
stage.

For the prototype, it is acceptable to simulate a revised paper and show
an improved score.

------------------------------------------------------------------------

# 11. Plagiarism / Similarity Detection

Papers that reach the review-ready stage should go through a similarity
check.

Display:

``` text
Similarity Analysis

Overall Similarity
       12%

Direct Matches
       3

Potentially Similar Sources
       5

Status
       ACCEPTABLE
```

The system should visually distinguish between:

### Acceptable Similarity

``` text
✓ Similarity within configured threshold

Continue to Reviewer Assignment
```

### High Similarity

``` text
⚠ HIGH SIMILARITY DETECTED

Similarity: 38%

The paper requires further inspection
before reviewer assignment.

[ View Similarity Report ]
[ Flag for Editor ]
```

Do not claim that the prototype can definitively determine plagiarism.
Use terminology such as:

-   Similarity
-   Potential overlap
-   Matched content
-   Sources requiring inspection

------------------------------------------------------------------------

# 12. Human Reviewer Assignment

Once similarity is acceptable, the system recommends human reviewers.

Create a reviewer-matching dashboard.

Each reviewer card should contain:

-   Reviewer name
-   Research expertise
-   Relevant domains
-   Expertise match percentage
-   Publications/research areas
-   Current workload
-   Conflict-of-interest indicator
-   Recommendation score

Example:

``` text
Recommended Reviewers

┌──────────────────────────────────────────────┐
│ Dr. Ananya Sharma                            │
│ AI • Machine Learning • NLP                  │
│ Expertise Match: 94%                         │
│ Current Workload: Low                        │
│ COI Check: Clear                             │
│                                              │
│ [ View Profile ] [ Assign Reviewer ]        │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ Dr. Rahul Mehta                              │
│ AI • Computer Vision • Deep Learning         │
│ Expertise Match: 89%                         │
│ Current Workload: Medium                     │
│ COI Check: Clear                             │
│                                              │
│ [ View Profile ] [ Assign Reviewer ]        │
└──────────────────────────────────────────────┘
```

Reviewer recommendations should be presented as **AI suggestions**. The
editor should retain control over final assignment.

------------------------------------------------------------------------

# 13. Human Peer Review

After reviewer assignment, show a final stage:

``` text
HUMAN PEER REVIEW

Reviewer Assigned
        ↓
Reviewer Receives Paper
        ↓
Reviewer Evaluates Paper
        ↓
Human Review Decision
```

Possible statuses:

-   Reviewer Assigned
-   Review Pending
-   Review in Progress
-   Review Submitted

The prototype does not need to implement a full real-world peer-review
platform unless required.

------------------------------------------------------------------------

# 14. Main Application Pages

Build the prototype around the following pages/screens.

## Page 1 --- Dashboard

Show:

-   Total papers
-   Papers under analysis
-   Ready for review
-   Revision required
-   Flagged similarity cases
-   Completed reviews

Example:

``` text
Research Review Dashboard

Total Papers              128
AI Reviews Completed       94
Revision Required         21
Ready for Review           17
Similarity Alerts           6
```

------------------------------------------------------------------------

## Page 2 --- Upload Paper

Contains:

-   PDF upload
-   Paper metadata
-   Target journal/conference
-   Start analysis

------------------------------------------------------------------------

## Page 3 --- Analysis Pipeline

Show the complete processing pipeline visually:

``` text
Upload
  ↓
PDF Parsing
  ↓
7 AI Agents
  ↓
Aggregation
  ↓
Editorial Decision
  ↓
Similarity
  ↓
Reviewer Assignment
```

Use progress indicators for each stage.

------------------------------------------------------------------------

## Page 4 --- Agent Review

Display all seven agents and their results.

Allow the user to click an agent and inspect detailed findings.

------------------------------------------------------------------------

## Page 5 --- Unified Review Report

Show:

-   Overall score
-   Agent scores
-   Strengths
-   Weaknesses
-   Critical issues
-   Suggested improvements
-   Editorial recommendation

------------------------------------------------------------------------

## Page 6 --- Similarity Report

Show:

-   Similarity percentage
-   Matched sources
-   Potential overlaps
-   Similarity status
-   Flag/clear action

------------------------------------------------------------------------

## Page 7 --- Reviewer Assignment

Show:

-   Recommended reviewers
-   Expertise matching
-   Workload
-   COI status
-   Assign button

------------------------------------------------------------------------

## Page 8 --- Paper Details

Show the current paper's complete lifecycle:

``` text
Paper Uploaded
      ✓
PDF Parsed
      ✓
AI Review
      ✓
Report Generated
      ✓
Editorial Screening
      ✓
Similarity Check
      ✓
Reviewer Assigned
      ✓
Human Review
    Pending
```

------------------------------------------------------------------------

# 15. UI / UX Requirements

The prototype should look like a modern academic/research management
platform.

## Design style

Use:

-   Professional
-   Clean
-   Minimal
-   Academic
-   Modern SaaS dashboard style

Avoid making it look like a generic chatbot.

## Layout

Use:

-   Left sidebar navigation
-   Top header
-   Main content area
-   Cards
-   Tables
-   Progress indicators
-   Status badges
-   Score cards
-   Charts where useful

## Suggested sidebar

``` text
AI Research Review

Dashboard
Papers
Upload Paper
AI Analysis
Review Reports
Similarity
Reviewers
Settings
```

------------------------------------------------------------------------

# 16. Color / Status Semantics

Use consistent status colors.

### Green

Successful / passed:

-   Completed
-   Ready for Review
-   Acceptable Similarity
-   Clear

### Yellow / Orange

Warning:

-   Revision Required
-   Medium Concern
-   Review Needed

### Red

Critical:

-   High Similarity
-   Critical Issue
-   Flagged

### Blue / Neutral

Processing:

-   Analyzing
-   Parsing
-   AI Agent Running

Do not overuse colors. Keep the overall interface professional.

------------------------------------------------------------------------

# 17. Prototype Technology Stack

Use a modern web stack.

Recommended:

### Frontend

-   React
-   TypeScript
-   Vite
-   Tailwind CSS

### UI

Use a professional component system such as:

-   shadcn/ui

Useful components:

-   Cards
-   Tabs
-   Dialogs
-   Progress
-   Tables
-   Badges
-   Dropdowns
-   Tooltips
-   Toast notifications

### Icons

Use:

-   Lucide React

### Charts

Use:

-   Recharts

### Backend

For a prototype, use either:

-   Python, FastAPI, Uvicorn, Pydantic


### Data

For the initial prototype, use:

-   Local mock JSON/state

No production database is required unless necessary.

If persistence is needed, use:

-   SQLite

------------------------------------------------------------------------

# 18. AI Implementation Strategy

The prototype should be designed so that the AI layer can later be
connected to real LLM APIs.

Create an abstraction such as:

``` text
AIReviewService
    ├── layoutAgent()
    ├── structureAgent()
    ├── formattingAgent()
    ├── languageAgent()
    ├── citationAgent()
    ├── technicalAgent()
    └── scopeMatchingAgent()
```

Each agent should return structured data.

Example:

``` json
{
  "agent": "Language Agent",
  "score": 86,
  "status": "completed",
  "strengths": [
    "Professional academic tone",
    "Generally clear writing"
  ],
  "issues": [
    {
      "severity": "medium",
      "description": "Several sentences are overly complex"
    }
  ],
  "recommendations": [
    "Break long sentences into shorter sentences"
  ]
}
```

------------------------------------------------------------------------

# 19. Mock AI Mode

The prototype MUST work even without an external AI API.

Implement a **Demo / Mock AI mode**.

When enabled:

-   Agent processing is simulated
-   Realistic scores are generated
-   Findings are displayed
-   Progress animation is shown
-   The complete workflow can be demonstrated without an API key

Example:

``` text
AI Engine: Demo Mode

All AI analysis results are simulated
for prototype demonstration.
```

This is important because the prototype should remain fully runnable
during a presentation.

------------------------------------------------------------------------

# 20. Real AI Integration Architecture

Keep the code modular so that a real AI provider can be connected later.

Recommended structure:

``` text
project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── services/
│   │   ├── data/
│   │   ├── types/
│   │   └── utils/
│   └── package.json
│
└── backend/
    ├── main.py
    ├── api/
    ├── agents/
    │   ├── layout_agent.py
    │   ├── structure_agent.py
    │   ├── formatting_agent.py
    │   ├── language_agent.py
    │   ├── citation_agent.py
    │   ├── technical_agent.py
    │   └── scope_agent.py
    ├── services/
    │   ├── ai_service.py
    │   ├── pdf_service.py
    │   ├── similarity_service.py
    │   ├── reviewer_service.py
    │   └── aggregation_service.py
    ├── models/
    ├── schemas/
    ├── data/
    └── requirements.txt
```

------------------------------------------------------------------------

# 21. Data Models

## Paper

``` typescript
interface Paper {
  id: string;
  title: string;
  authors: string[];
  uploadedAt: string;
  status: PaperStatus;
  targetVenue?: string;
  overallScore?: number;
}
```

## Agent Review

``` typescript
interface AgentReview {
  agentName: string;
  score: number;
  status: "pending" | "running" | "completed";
  strengths: string[];
  issues: ReviewIssue[];
  recommendations: string[];
}
```

## Review Issue

``` typescript
interface ReviewIssue {
  severity: "low" | "medium" | "high" | "critical";
  title: string;
  description: string;
}
```

## Reviewer

``` typescript
interface Reviewer {
  id: string;
  name: string;
  expertise: string[];
  matchScore: number;
  workload: "low" | "medium" | "high";
  conflictOfInterest: boolean;
}
```

------------------------------------------------------------------------

# 22. Demo Data

Provide at least one preloaded sample paper.

Example:

``` text
Title:
AI-Driven Carbon Emission Prediction Using
Multi-Agent Systems

Authors:
A. Sharma, R. Mehta, S. Patel

Domain:
Artificial Intelligence / Machine Learning

Target Venue:
International Conference on Artificial Intelligence
```

This allows the complete system to be demonstrated without uploading a
real paper.

------------------------------------------------------------------------

# 23. Complete Demo Flow

The prototype should support this exact presentation flow:

### Step 1

Open Dashboard.

### Step 2

Click:

``` text
Upload Paper
```

### Step 3

Upload/select sample PDF.

### Step 4

Click:

``` text
Start AI Review
```

### Step 5

Show:

``` text
Parsing PDF...
```

Then:

``` text
Text ✓
Figures ✓
Tables ✓
Equations ✓
References ✓
Metadata ✓
```

### Step 6

Start the seven agents.

Display them progressing individually:

``` text
Layout Agent          ✓
Structure Agent       ✓
Formatting Agent      ✓
Language Agent        ✓
Citation Agent        ✓
Technical Agent       ✓
Scope Matching Agent  ✓
```

### Step 7

Show Report Aggregation Agent.

``` text
Aggregating findings...
Generating unified review...
```

### Step 8

Show overall report.

Example:

``` text
Overall Score: 85/100

Decision:
READY FOR REVIEW
```

### Step 9

Run similarity analysis.

Example:

``` text
Similarity: 12%
Status: Acceptable
```

### Step 10

Open Reviewer Assignment.

Show top recommended reviewers.

### Step 11

Assign a reviewer.

### Step 12

Show:

``` text
Human Peer Review
Status: Review Pending
```

This should demonstrate the complete architecture end-to-end.

------------------------------------------------------------------------

# 24. Important Prototype Behavior

The application should NOT merely be a collection of static screens.

Implement interactions for:

-   Uploading a PDF
-   Starting analysis
-   Agent progress
-   Opening agent details
-   Viewing the unified report
-   Viewing issues
-   Triggering revision workflow
-   Running similarity analysis
-   Viewing reviewer recommendations
-   Assigning a reviewer
-   Changing paper status

Use simulated delays where necessary to make the AI workflow visually
understandable.

Example:

``` text
PDF Parsing             1.5 sec
Agent Analysis           2–4 sec
Report Aggregation       1.5 sec
Similarity Analysis      1.5 sec
Reviewer Matching        1.5 sec
```

These delays are only for demonstration and should not make the
application feel slow.

------------------------------------------------------------------------

# 25. Error Handling

Include basic errors.

Examples:

### Invalid file

``` text
Invalid File

Please upload a PDF research paper.
```

### Analysis error

``` text
Analysis Failed

Something went wrong while processing
the paper.

[ Retry Analysis ]
```

### Missing target venue

Allow the user to continue with:

``` text
Generic Scope Analysis
```

instead of blocking the entire workflow.

------------------------------------------------------------------------

# 26. Responsible AI Notice

Include a small notice in the interface:

> **AI-assisted screening:** Results are generated to assist editors and
> reviewers. AI scores and recommendations should be independently
> verified by qualified human reviewers.

This is especially important for:

-   Technical review
-   Plagiarism/similarity
-   Editorial decisions
-   Reviewer assignment

------------------------------------------------------------------------

# 27. Prototype Success Criteria

The prototype is successful if a user can understand the following
without reading the source code:

1.  A research paper is uploaded.
2.  The PDF is parsed.
3.  Seven specialized AI agents analyze different aspects.
4.  Their results are aggregated.
5.  An editorial recommendation is generated.
6.  Papers requiring changes can be sent back for revision.
7.  Review-ready papers undergo similarity detection.
8.  High similarity produces an alert.
9.  Papers with acceptable similarity proceed to reviewer assignment.
10. AI recommends appropriate human reviewers.
11. Human peer review remains the final stage.
12. The entire workflow is visible and understandable.

------------------------------------------------------------------------

# 28. What the Prototype Should NOT Do

Do not unnecessarily build:

-   A complete journal management system
-   Real payment systems
-   Real user authentication unless needed
-   Complex production databases
-   Real plagiarism certification
-   Automatic final paper acceptance/rejection
-   Fully autonomous reviewer assignment
-   A complete publication workflow

Focus on **demonstrating the proposed architecture and user
experience**.

------------------------------------------------------------------------

# 29. Development Priorities

Build in this order:

### Priority 1 --- Core UI

-   Dashboard
-   Sidebar
-   Upload screen
-   Paper details

### Priority 2 --- Analysis Pipeline

-   PDF parsing simulation
-   Seven AI agents
-   Agent status
-   Agent results

### Priority 3 --- Intelligence Layer

-   Report aggregation
-   Editorial decision
-   Revision workflow

### Priority 4 --- Integrity

-   Similarity analysis
-   Similarity alert

### Priority 5 --- Reviewer Matching

-   Reviewer profiles
-   Expertise matching
-   Workload
-   COI indicator
-   Assignment

### Priority 6 --- Polish

-   Animations
-   Loading states
-   Toasts
-   Responsive layout
-   Empty/error states
-   Professional visual design

------------------------------------------------------------------------

# 30.1 Python Backend Requirements

The backend MUST be implemented in **Python**, not Node.js.

Use:

```text
Python
FastAPI
Uvicorn
Pydantic
```

For PDF processing, choose appropriate Python libraries such as:

- PyMuPDF (`fitz`) for PDF text/page extraction
- pdfplumber where useful for structured extraction
- Additional libraries only when genuinely required

Keep the AI agents as independent Python modules so each agent can later be connected to an LLM/API independently.

The frontend should communicate with the FastAPI backend through clean REST endpoints.

Example endpoints:

```text
POST   /api/papers/upload
POST   /api/papers/{paper_id}/analyze
GET    /api/papers/{paper_id}
GET    /api/papers/{paper_id}/agents
GET    /api/papers/{paper_id}/report
POST   /api/papers/{paper_id}/similarity
GET    /api/papers/{paper_id}/reviewers
POST   /api/papers/{paper_id}/assign-reviewer
POST   /api/papers/{paper_id}/resubmit
```

The prototype should still work in **Demo/Mock AI mode** without requiring external AI API keys.

# 30. Final Implementation Instruction for Claude Code

Build this as a **fully working frontend prototype**, not as a static
mockup.

Start by creating the project structure and implementing the dashboard
and navigation.

Then implement the complete paper lifecycle:

``` text
UPLOAD
  ↓
PARSE
  ↓
MULTI-AGENT ANALYSIS
  ↓
AGGREGATION
  ↓
EDITORIAL DECISION
  ↓
REVISION OR READY FOR REVIEW
  ↓
SIMILARITY DETECTION
  ↓
REVIEWER ASSIGNMENT
  ↓
HUMAN PEER REVIEW
```

Use mock data and mock AI services so the application runs without
external API keys.

The code should be modular enough that real PDF extraction, LLM-based
agents, similarity APIs, and reviewer databases can be connected later.

Every major stage must have a clear UI representation.

The most important goal is that when the prototype is demonstrated, an
evaluator can immediately understand:

> **How the uploaded research paper moves through multiple specialized
> AI review agents, how their findings are combined into an editorial
> report, how revision/similarity checks are handled, and how suitable
> human reviewers are finally recommended.**

------------------------------------------------------------------------

# 31. Expected Final Result

The final prototype should feel like a realistic **AI-powered academic
editorial screening platform**.

It should communicate three layers clearly:

### Layer 1 --- AI Understanding

``` text
PDF
 ↓
Parsing
 ↓
7 Specialized AI Agents
```

### Layer 2 --- AI Editorial Screening

``` text
Agent Findings
 ↓
Report Aggregation
 ↓
Editorial Decision
 ↓
Revision / Ready for Review
```

### Layer 3 --- Human Review Support

``` text
Similarity Detection
 ↓
Reviewer Matching
 ↓
Human Peer Review
```

The AI assists throughout the process, but **human experts remain
responsible for the final peer-review judgment.**
