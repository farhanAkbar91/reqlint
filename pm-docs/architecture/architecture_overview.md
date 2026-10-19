# ReqLint Architecture Overview

## Executive Summary
ReqLint is an automated **Agile User Story Linting and Quality Assurance platform** based on the **INVEST criteria** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*) and the **Connextra User Story standard** (*Role - Action - Benefit*).

## System Architecture Diagram
```
+-------------------------------------------------------------------------------+
|                             FRONTEND + QA LAYER                               |
| Next.js 14 + Tailwind CSS + User Story Editor (Live Smells & INVEST Score)    |
+---------------------------------------+---------------------------------------+
                                        | HTTP / REST API (JSON)
                                        v
+-------------------------------------------------------------------------------+
|                             BACKEND API LAYER                                 |
| FastAPI (Python 3.11) + Pydantic v2 + PostgreSQL (Audit History) + Redis      |
+---------------------------------------+---------------------------------------+
                                        | Internal Python Module Call / Async Task
                                        v
+-------------------------------------------------------------------------------+
|                            AI / NLP ENGINE LAYER                              |
| Bilingual Language Detector (ID / EN)                                         |
|  ├── User Story Structure & INVEST Rule Matcher (spaCy POS + Regex)           |
|  └── INVEST & Gherkin Acceptance Criteria Rewriter (Groq / LLaMA-3 / Fallback)|
+-------------------------------------------------------------------------------+
```

## Team Workspaces
1. `pm-docs/`: Project Manager & Architect documentation, INVEST rubrics, and agile quality guidelines.
2. `ai-engine/`: AI / NLP Engineer pipeline, User Story syntax verifier, INVEST smell matchers, and LLM rewriter.
3. `backend/`: Backend Engineer REST API service, audit persistence, and task queues.
4. `frontend-qa/`: Frontend UI & QA Engineer user story editor, INVEST audit scorecard, and Cypress E2E tests.

