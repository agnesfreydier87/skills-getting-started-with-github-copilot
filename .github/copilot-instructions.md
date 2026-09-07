# Copilot Instructions

## Project overview

This is a small FastAPI app ("Mergington High School Activities API") that lets students view and
sign up for extracurricular activities. It's a teaching exercise repo (GitHub Skills), not a
production system — keep changes simple and self-contained.

## Architecture

- `src/app.py` — the entire backend: a single FastAPI `app` with two endpoints (`GET /activities`,
  `POST /activities/{activity_name}/signup`). All activity data lives in an in-memory Python dict
  (`activities`), keyed by activity name; there is no database. Data resets whenever the server
  restarts.
- `src/static/` — vanilla JS/HTML/CSS frontend served by FastAPI's `StaticFiles` mount at
  `/static`. `app.js` fetches `/activities` and posts to the signup endpoint directly via `fetch`;
  there is no build step or framework.
- `GET /` redirects to `/static/index.html`.
- Students are identified by email (not stored as separate entities) and simply appended to an
  activity's `participants` list on signup — there's no duplicate-signup or capacity check against
  `max_participants` currently enforced in the signup handler.

## Running the app

```bash
pip install -r requirements.txt
python src/app.py          # or: uvicorn src.app:app --reload --reload-include "src/static/*"
```

- App: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

The VS Code launch config (`.vscode/launch.json`, "Launch Mergington WebApp") runs uvicorn with
`--reload-include src/static/*` so static file edits also trigger reload.

## Tests

`pytest.ini` sets `pythonpath = .` but there is currently no test suite in the repo. If adding
tests, put them where pytest can discover them (e.g. a top-level `tests/` dir) and run with:

```bash
pytest                       # full suite
pytest tests/test_x.py::test_name   # single test
```

## Notes

- `.github/steps/` and `.github/workflows/0-start-exercise.yml` through `5-step.yml` are scaffolding
  for the GitHub Skills exercise flow — not part of the application itself.
