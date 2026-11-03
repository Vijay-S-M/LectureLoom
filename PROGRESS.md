# Progress

Commit after every class. Tag every Friday: `git tag week-N && git push origin week-N`.

## Week 1 (tag week-1 by Fri 23 Oct)
- [x] Repo created from the Examate template and registered on the form
- [x] README top section filled from my project card
- [x] /health runs locally
- [x] docs/QUESTIONS.md: 10 real questions
- [x] 50+ pages collected, DATASET.md filled, sample in data/sample/
- [x] Tag week-1 pushed

## Week 2 (tag week-2 by Fri 30 Oct)
- [ ] POST /chat calls an LLM and returns structured JSON
- [ ] Streaming, timeouts, retry and a fallback model
- [ ] Cost log + GET /usage
- [ ] Docker Compose (API + Postgres/pgvector) runs
- [ ] CI green, live link in README
- [ ] Tag week-2 pushed

## Week 3 (tag week-3 by Fri 6 Nov)
- [ ] Parser keeps page numbers and headings
- [ ] 500+ pages chunked, embedded and stored in pgvector
- [ ] POST /ask answers with [document, page] citations
- [ ] docs/EVAL_v0.md with my 10 questions scored
- [ ] Tag week-3 pushed

## Daily log
| Date | What I did today | Commit |
|---|---|---|
| 2026-10-21 | Created repository from Examate template, verified FastAPI /health endpoint and CI configuration | `38345b7` |
| 2026-10-22 | Filled project card in README: product, target users, problem statement, signature feature, and hardest problem | `a83ccef` |
| 2026-10-23 | Collected 54 pages of NPTEL lecture transcripts across CSE & ECE courses, added sample files in data/sample/, populated DATASET.md and data/manifest.csv, defined 10 real evaluation questions with document-page citations in docs/QUESTIONS.md, passed health test, tagged and pushed week-1 | `week-1` |
