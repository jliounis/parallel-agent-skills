# Parallel Search for Bifrost

This package contains a standard Agent Skill and a Python 3 helper using Parallel's Search API. No third-party Python dependencies are needed.

## Runtime requirements

The installed agent needs Python 3, outbound HTTPS to `api.parallel.ai`, and `PARALLEL_API_KEY` supplied through its runtime environment or secret manager. Bifrost hosts and distributes the skill; the helper executes in the agent client and calls Parallel directly. An inference-only application needs a tool integration instead.

## Add to Bifrost Skills Repository

In the target Bifrost dashboard, open **Skills Repository → New Skill**. Enter the name and description from `SKILL.md`. Paste only the Markdown body into the SKILL.md editor; Bifrost generates frontmatter from the details fields. Add `scripts/search.py` and `references/bifrost.md` with their relative paths preserved. Publish version `1.0.0` for a new skill.

Creation immediately serves the first version. Bifrost documents marketplace/download routes as public: this package intentionally contains no credentials or customer-specific content.

Use **Register as Marketplace** in the dashboard and follow its client-specific installation commands. The resulting plugin is `bifrost-parallel-search-api`.

## Verify after installation

Run from the installed skill folder:

```bash
python3 scripts/search.py --query 'Python asyncio task cancellation' --dry-run
python3 scripts/search.py --query 'Python asyncio task cancellation' --mode fast
```

The first command needs no credentials and prints the request. The second makes a billable Search API call using the runtime key. Confirm a successful exit and a JSON response containing `search_id`, `session_id`, and `results`. Then explicitly ask the agent to use `parallel-search-api` to research Python task cancellation with official source citations and confirm it activates this skill, executes the helper, and cites returned URLs.

## Sources

- [Bifrost Skills Repository](https://docs.getbifrost.ai/features/skills-repository)
- [Bifrost create-skill API](https://docs.getbifrost.ai/api-reference/skills/create-skill)
- [Parallel Search API](https://docs.parallel.ai/api-reference/search/search)
- [Parallel Search quickstart](https://docs.parallel.ai/search/search-quickstart)
