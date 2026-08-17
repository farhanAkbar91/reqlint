# ReqLint AI Engine Workspace

Welcome, **AI / NLP Engineer**! This directory contains the complete self-contained NLP & SLM reasoning pipeline for auditing software requirements in both **Indonesian** and **English**.

## Quickstart

1. **Install Dependencies**:
   ```bash
   pip install -r requirements-ai.txt
   ```

2. **Download Language Models**:
   ```bash
   python setup_models.py
   ```

3. **Run Benchmark Evaluation**:
   ```bash
   python benchmarks/evaluate.py
   ```

4. **Run Unit Tests**:
   ```bash
   pytest tests/
   ```

## Architecture Summary
- `ai_module/detector/`: Language detector (ID vs EN).
- `ai_module/rules/indonesian/`: Indonesian spaCy POS rules, passive voice prefixes (`di-`, `ter-`), and weak directive dictionaries.
- `ai_module/rules/english/`: English spaCy POS rules, passive voice patterns, and weak directive dictionaries.
- `ai_module/llm/`: Rewriter using Groq / LLaMA-3 with prompt templates for ID and EN.
