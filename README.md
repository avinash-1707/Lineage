# Adaptive Code Review Agent

AI-powered code review system that learns your team's standards over time and delivers context-aware PR feedback.

Listens to GitHub PR webhooks, analyzes diffs semantically, retrieves similar past reviews from a vector store, and generates structured file-level feedback with severity rankings. Improves continuously from accepted/dismissed feedback.

**Stack:** Next.js (web) + FastAPI (api)
