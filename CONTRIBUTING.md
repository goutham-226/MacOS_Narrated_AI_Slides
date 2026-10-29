# Contributing

Thanks for your interest in improving Lisa!

1. Fork the repo and create a branch: `git checkout -b my-change`.
2. Set up the project as described in the [README](README.md).
3. Make your change and run `python v_ai.py` to check it end to end.
4. Open a pull request describing what you changed and why.

## Rules for secrets

- Never commit API keys or tokens. Put them in `.env`, which is git-ignored.
- If you add a new secret, read it with `os.getenv(...)` and add a placeholder
  to `.env.example`.
- If a key is ever committed by mistake, revoke it with the provider right
  away. Deleting it in a later commit does not remove it from git history.
