# ReqLint Architecture Overview

## Executive Summary
ReqLint is an automated Software Requirement Specifications (SRS) linting and quality assurance platform based on **ISO/IEC/IEEE 29148** standards and **INVEST** criteria for Agile teams.

## System Architecture Diagram
```
+-------------------------------------------------------------------------------+
|                             FRONTEND + QA LAYER                               |
| Next.js 14 + Tailwind CSS + Monaco Editor (Live SRS Highlight & Diff Viewer)  |
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
|  ├── Rule-Based Linting (spaCy POS/Passive voice & IEEE/INVEST rubrics)       |
|  └── Semantic Rewriting (Groq / LLaMA-3 / LangChain SLM Reasoning)            |
+-------------------------------------------------------------------------------+
```

## Team Workspaces
1. `pm-docs/`: Project Manager & Architect documentation and metric rubrics.
2. `ai-engine/`: AI / NLP Engineer pipeline, language models, rule matchers, LLM rewriter.
3. `backend/`: Backend Engineer API service, database persistence, task queues.
4. `frontend-qa/`: Frontend UI & QA Engineer editor, audit visualization, E2E tests.
