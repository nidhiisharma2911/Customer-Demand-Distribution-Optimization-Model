# Contributing

Thank you for contributing! Quick checklist for PRs:

- [ ] The branch is up-to-date with `main`.
- [ ] Code follows project style and includes minimal, focused changes.
- [ ] New code includes tests where appropriate (run `pytest`).
- [ ] Notebooks either include a top cell that installs dependencies or are accompanied by `requirements.txt` updates.
- [ ] Documentation updated (`README.md`, `dashboard/README.md`, or other files).
- [ ] If adding data files, avoid committing large binaries; use `outputs/` for generated example outputs only.

CI will run the scenario runner, execute notebooks, and run tests on PRs.
