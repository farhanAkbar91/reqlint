# ReqLint: Requirement Analyzer via NLP

Automated Quality Assurance & Ambiguity Detection Tool for Software Requirement Specifications (SRS) based on **ISO/IEC/IEEE 29148 Standard** and **INVEST Criteria for Agile**.

---

## 👥 Role-Based Project Workspaces (4 Team Members)

Each team member has a dedicated, isolated workspace directory:

| Member & Role | Workspace Directory | Quickstart Guide |
|---|---|---|
| **Member 1: PM & Architect** | `pm-docs/` | [pm-docs/architecture/architecture_overview.md](file:///d:/portfolio/AI/reqlint/pm-docs/architecture/architecture_overview.md) |
| **Member 2: AI / NLP Engineer** | `ai-engine/` | [ai-engine/README.md](file:///d:/portfolio/AI/reqlint/ai-engine/README.md) |
| **Member 3: Backend Engineer** | `backend/` | [backend/README.md](file:///d:/portfolio/AI/reqlint/backend/README.md) |
| **Member 4: Frontend + QA Engineer** | `frontend-qa/` | [frontend-qa/README.md](file:///d:/portfolio/AI/reqlint/frontend-qa/README.md) |

---

## 🌐 Bilingual Support (Indonesian & English)

ReqLint's AI engine automatically detects whether the input SRS or User Story is written in **Indonesian (`id`)** or **English (`en`)** and applies tailored NLP rule matchers and SLM rewrites.

### Example Indonesian Audit
- **Input**: *"Sistem sebaiknya dapat memproses data transaksi pengguna dengan cepat."*
- **Flaws Flagged**: `WEAK_DIRECTIVE_ID` (*sebaiknya/dapat*), `SUBJECTIVE_ADJECTIVE_ID` (*cepat*).
- **Suggested Rewrite**: *"Sistem HARUS memproses data transaksi pengguna dengan waktu respon < 200 ms."*

### Example English Audit
- **Input**: *"The system should allow users to search for documents easily."*
- **Flaws Flagged**: `WEAK_DIRECTIVE_EN` (*should*), `SUBJECTIVE_ADJECTIVE_EN` (*easily*).
- **Suggested Rewrite**: *"The system SHALL allow users to search for documents within 3 clicks."*

---

## 🚀 Running Full Stack with Docker Compose

```bash
docker-compose up --build
```

- **Frontend UI**: http://localhost:3000
- **FastAPI Docs**: http://localhost:8000/docs
