# Contributing

Contributions are welcome.

For new features, please start with an issue
so we can discuss the potential feature first.
I don't want to waste your time
and reject code
for a feature that I was never going to accept.

No code will be merged unless CI is passing. This means:

* Free of lint errors
* Includes type annotations
* 100% test coverage

## Tools

To develop locally:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
pytest
```

## Release checklist

These are notes for my release process,
so I don't have to remember all the steps.

1. Update `CHANGELOG.md`.
2. Update version in `setup.cfg`.
3. `rm -rf dist && python -m build`
4. `twine upload dist/*`
5. `git tag -a vX.X -m "Version X.X"`
6. `git push --tags`
