# Instructor runbook

## Recommended timing

| Segment | Time |
|---|---:|
| Coding agent concepts and Issue -> PR demo | 25 min |
| Lab 1 | 35 min |
| Break | 10 min |
| Security/review concepts and demo | 20 min |
| Lab 2 | 30 min |
| End-to-End Agent Guardrails concepts and demo | 20 min |
| Lab 3: End-to-End Agent Guardrails | 35 min |
| Wrap-up | 5 min |

## 48-hour preflight

- [ ] Repository is created from this starter and `main` is protected as intended.
- [ ] Copilot coding agent is enabled for a test student account.
- [ ] GitHub Actions can run in the organization.
- [ ] Advanced CodeQL setup is accepted for this repository; default setup is not enabled.
- [ ] Copilot code review is available in the PR reviewer menu.
- [ ] `copilot-setup-steps.yml` succeeds from the Actions tab.
- [ ] A complete Lab 1 agent run has been recorded as backup.
- [ ] A prepared Lab 2 PR produces the expected CodeQL alerts.
- [ ] Students have repository admin access for creating a repository ruleset.
- [ ] The `validate` and `analyze` checks have completed at least once so they are selectable.
- [ ] Venue network reaches GitHub and Python package hosting.

## Validate the repository

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/preflight.py
python scripts/validate.py
```

The Lab 1 acceptance suite should fail on the starter and pass only after implementation:

```bash
pytest -q -m lab1
```

## Prepare the Lab 2 demonstration PR

```bash
git switch main
git pull
git switch -c lab2-insecure-report
python scripts/prepare_lab2.py
git diff
python scripts/validate.py
```

Commit, push, and open a PR. Confirm CodeQL catches at least the SQL construction and
dynamic execution paths before the event. If a query pack changes, retain screenshots or
SARIF excerpts of the verified findings as the fallback.

## Facilitation guidance

- Pair students when the class has more than 20 participants to reduce agent queue pressure.
- At minute 15 of each lab, move blocked students to an instructor-prepared PR/session.
- Demonstrate one imperfect agent result; do not present the agent as infallible.
- Require students to cite acceptance criteria or findings when giving follow-up feedback.
- Never merge the intentionally vulnerable Lab 2 PR.
- Do not use real secrets to demonstrate secret scanning.

## Hosted-feature fallback

Prepare these before the event outside the student starter branch:

- screen recording of a successful Coding Agent session
- screenshot/SARIF excerpt of the Lab 2 CodeQL findings
- completed Lab 1 and remediated Lab 2 PRs in an instructor-only repository or branch

Do not place completed solution source files in the student default branch because the
coding agent can read the repository.
