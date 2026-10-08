# PromptOps Studio

**A local-first control plane for versioning, testing, comparing, and safely reviewing prompts used in LLM, RAG, and agent workflows.**

PromptOps matters because prompt changes behave like code changes: they can improve one scenario while silently breaking formatting, grounding, safety, or another scenario. Teams need repeatable evidence before approval—not a folder of prompt snippets.

## Problem statement

AI teams often lack a single audit trail connecting prompt intent, version history, synthetic test cases, output quality signals, regressions, and approval decisions. PromptOps Studio makes those relationships explicit while remaining runnable without paid APIs.

## Architecture

```text
Prompt template
      |
      v
Prompt version registry
      |
      v
Evaluation test cases
      |
      v
Rule-based evaluator
      |
      v
Regression comparison
      |
      v
Scorecard + approval recommendation
      |
      v
Audit log + dashboard
```

FastAPI serves the API and static dashboard, SQLite stores registries and audit runs, and the `promptops` package contains deterministic evaluation logic.

## Core features

- Prompt registry with use case, status, notes, tags, and timestamps
- Immutable numbered versions with change rationale and expected improvement
- Structured evaluation cases for keywords, forbidden phrases, JSON fields, RAG context, safety, and ideal behavior
- Offline deterministic simulator—no key or paid API required
- Quality checks for keyword coverage, forbidden phrases, citations, JSON validity/fields, length, context overlap, unsupported-claim risk, safety patterns, and formatting
- Regression reports listing improved/regressed cases, formatting breaks, safety regressions, and `approve`/`needs_review`/`reject` recommendations
- SQLite audit trail, metrics API, premium responsive dashboard, pytest suite, and GitHub Actions CI

## Prompt versioning

Creating a prompt establishes v1. `POST /prompts/{prompt_id}/versions` records a new candidate alongside what changed, why it changed, and the expected improvement. Versions remain independently evaluable; workflow status (`draft`, `testing`, `approved`, `archived`) is visible rather than inferred.

## Evaluation strategy

The evaluator combines transparent deterministic checks instead of hiding quality behind a single model judgment. Scores are decision support, not truth: every result carries `human_review_required: true`.

## Regression testing

The same selected cases run against baseline and candidate versions. The report compares mean scores and case-level outcomes, explicitly escalating new safety flags or broken structured output.

## Safety checks

Prompt-injection-like text, secret-extraction language, forbidden output, unsupported context claims, formatting failures, and unsafe-request behavior are surfaced for review. There is no auto-deployment and real LLM support is disabled by default.

## Example version comparison

| Signal | v1 | v2 |
|---|---:|---:|
| Overall score | 0.72 | 0.86 |
| Citations | inconsistent | passed |
| JSON schema | passed | passed |
| Recommendation | baseline | approve for review |

## Example evaluation output

```json
{
  "prompt_name": "RAG Answer Generator",
  "version": "v2",
  "overall_score": 0.86,
  "keyword_coverage": 0.9,
  "citation_check": "passed",
  "json_validity": "not_applicable",
  "safety_flags": [],
  "regression_status": "improved",
  "recommendation": "approve_for_review"
}
```

## API endpoints

`GET /health`, `POST/GET /prompts`, `GET /prompts/{prompt_id}`, `POST/GET /prompts/{prompt_id}/versions`, `POST/GET /test-cases`, `POST /runs/evaluate`, `POST /runs/regression`, `GET /runs`, `GET /runs/{run_id}`, and `GET /dashboard`. Interactive documentation is at `/docs`.

## Setup and local use

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
# or: uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. Use a different local port with `PORT=8001 python run.py` if another demo is already running. Run tests with `pytest`.

## Screenshots / demo

Add a reviewed dashboard screenshot or short local demo recording here after release. The dashboard includes a safe synthetic demo loader.

## Privacy and safety

Only fictional prompts, contexts, and outputs are included. Never commit API keys, `.env`, private prompts, real conversations, customer/company data, documents, logs, or generated application material. Optional provider variables are placeholders and `LLM_ENABLED=false`; this repository does not claim production, client, enterprise, or commercial use.

## Limitations

SQLite is intended for local demonstration; authentication and multi-user controls are out of scope. Heuristic evaluation can produce false positives/negatives, simulated responses do not represent a real model, and approval always requires human judgment.

## Future improvements

Add pluggable local models, richer diff visualization, configurable weighted policies, dataset import validation, signed approval records, role-based access, and evaluator calibration reports.

## License

Portfolio demonstration project. No warranty or production-use claim.
