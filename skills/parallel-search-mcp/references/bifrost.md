# Parallel Search MCP in Bifrost

Bifrost needs both an MCP connection for executable tools and a published skill for the agent instructions.

## Connect the MCP server

In Bifrost's MCP Gateway, add an HTTP client named `parallel-search`. Use the endpoint and authentication appropriate to the deployment:

| Use | Endpoint | Authentication |
| --- | --- | --- |
| Anonymous exploration | `https://search.parallel.ai/mcp` | None; lower limits |
| Account-backed access | `https://search.parallel.ai/mcp` | Headers: `Authorization: Bearer <Parallel API key>` |
| Enforced authentication | `https://search.parallel.ai/mcp-oauth` | Bearer API key or OAuth |

For production, configure account-backed authentication. Store credentials in Bifrost's connection settings or supported secret references. Never include them in published skill files. Bifrost management credentials and downstream client/virtual keys are separate from the Parallel credential used on this upstream connection.

For anonymous exploration, this entry can be merged into the existing `mcp.client_configs` array in Bifrost's `config.json`:

```json
{
  "name": "parallel-search",
  "connection_type": "http",
  "connection_string": "https://search.parallel.ai/mcp",
  "auth_type": "none",
  "is_ping_available": false,
  "tools_to_execute": ["web_search", "web_fetch"]
}
```

Keep existing clients. For authenticated configuration, use Headers auth and the Bearer header in the dashboard; OAuth uses the `/mcp-oauth` endpoint and requires completing Bifrost's verification/sign-in flow.

Confirm the connection is healthy and discovers `web_search` and `web_fetch`. Allow these tools for the intended downstream client or virtual key. Connect the agent to Bifrost's MCP gateway using the deployment's configured authentication and verify the agent can see both tools. Tool names may be prefixed by Bifrost. Preserve the deployment's tool approval settings.

## Publish the skill

Open **Skills Repository → New Skill**. Copy the name and description from `SKILL.md`, paste only its Markdown body into the body editor, and attach `references/bifrost.md` with that relative path. Bifrost generates YAML frontmatter from the details fields. For an existing skill, use its new-version flow rather than creating a duplicate.

Publish version `1.0.0` for a new skill, then use **Register as Marketplace** and the dashboard's client-specific install commands. The plugin is `bifrost-parallel-search-mcp`. Creation immediately serves the first version; marketplace/download routes are documented as public, so published files must contain no credentials or private customer data.

Installing this skill provides instructions. The MCP connection above supplies the tools. Both must be available in the agent client.

## Verify end to end

1. Inspect the agent's tool list and confirm both Parallel tools are present through Bifrost.
2. Ask: "Use Parallel Search MCP to find official Python asyncio cancellation guidance and cite the sources." Confirm it calls `web_search` and returns evidence-backed links.
3. Ask it to read `https://docs.python.org/3/library/asyncio-task.html` with `web_fetch` and summarize cancellation cleanup. Confirm successful page content and inspect any per-URL errors.
4. Verify Bifrost records the tool calls on the intended connection. For authenticated use, verify the connection is using the configured Parallel account.

Direct calls to the hosted MCP endpoint verify Parallel availability, but do not prove Bifrost routing, authentication, tool filtering, or skill installation. Run these checks in the target deployment before declaring setup complete.

## Sources

- [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)
- [Bifrost MCP connections](https://docs.getbifrost.ai/mcp/connecting-to-servers)
- [Bifrost Skills Repository](https://docs.getbifrost.ai/features/skills-repository)
