# Project Status

## Build status

Complete local portfolio build; no production or client-use claim.

## Completed features

Registry, versions, test cases, deterministic simulation, ten rule-based quality signals, regression recommendations, SQLite audit runs, dashboard, API, tests, and CI.

## Testing status

Pytest covers API health/workflow/dashboard plus keyword, JSON, citation, forbidden phrase, safety, and regression logic.

## Known limitations

Single-user local storage; heuristic quality signals; synthetic simulator; human approval required; real LLM execution disabled by default.

## Safety boundaries

Synthetic examples only. No secrets, private/customer/company data, auto-deployment, or real-world usage claims. Outputs remain human-reviewable.

## Files excluded from Git

Environment files, databases, logs, PDFs, caches, virtual environments, uploads, generated outputs, private prompts/data/documents, real conversations/company data, secrets, and credentials.

## What must be checked before making public

- Tests and dependency installation pass.
- Tracked files contain no secrets, personal/private data, or production claims.
- `.env`, databases, logs, generated output, and caches remain untracked.
- Samples are synthetic and the final diff and visibility are reviewed.
