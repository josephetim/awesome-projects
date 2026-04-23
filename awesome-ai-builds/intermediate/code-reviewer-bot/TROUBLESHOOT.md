# TROUBLESHOOT

## Webhook returns 401

- Confirm `GITHUB_WEBHOOK_SECRET` in `.env` matches the GitHub webhook secret exactly.
- Verify your tunnel forwards raw payloads without modification.

## Bot does not post comments

- Ensure `GITHUB_TOKEN` has repository comment/write permissions.
- Verify webhook action is `opened`, `reopened`, or `synchronize`.

## Empty or weak reviews

- Large diffs are truncated for prompt safety; split PRs into focused changes.
- Improve PR description quality to give the model better intent context.
