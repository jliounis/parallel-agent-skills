# Gateway-level search controls

Configure Parallel's search behavior on Bifrost's authenticated upstream MCP connection. These settings apply to every `web_search` call on that connection and do not affect `web_fetch`.

## Search mode and response limits

Search MCP calls the processing preset `mode`, not `processor`. Supported modes are `turbo`, `fast`, `basic`, and `advanced`. Select the mode according to the deployment's quality, latency, and cost requirements; do not invent a `processor` field or copy Task API processors into this configuration.

Add `x-parallel-search-config` to the same Bifrost Headers configuration as the Authorization header. The header's value is a JSON string. For example, a connection with an explicit fast preset and a small result budget:

```json
{
  "Authorization": "env.PARALLEL_MCP_AUTHORIZATION",
  "x-parallel-search-config": "{\"mode\":\"fast\",\"max_chars_total\":12000,\"advanced_settings\":{\"max_results\":5}}"
}
```

In the dashboard header-value field, enter the JSON object text without the outer string escaping:

```json
{
  "mode": "fast",
  "max_chars_total": 12000,
  "advanced_settings": {
    "max_results": 5
  }
}
```

Keep the Authorization header present when adding or changing search controls. For OAuth connections, preserve OAuth authentication and configure the search header through the connection's supported static-header settings.

## Other controls

Use only the settings the deployment needs. The header follows the current Search API request schema:

| Setting | Purpose |
| --- | --- |
| `mode` | Search processing preset |
| `max_chars_total` | Total excerpt character budget |
| `advanced_settings.max_results` | Maximum number of results |
| `advanced_settings.excerpt_settings.max_chars_per_result` | Per-result excerpt budget |
| `advanced_settings.source_policy.include_domains` | Restrict returned sources to specified domains or supported paths |
| `advanced_settings.source_policy.exclude_domains` | Exclude sources when no include list is set |
| `advanced_settings.source_policy.after_date` | Publication-date filter |
| `advanced_settings.location` | Two-letter country code for geographic relevance |
| `advanced_settings.fetch_policy` | Live-fetch/cache policy; can increase latency |

An include list takes precedence over exclusions. Domain/path prefixes require `fast`, `basic`, or `advanced`; they are unsupported in `turbo`. Source filters constrain search results, not which URLs `web_fetch` can read; do not treat them as a gateway-wide network access boundary.

## URL alternative and precedence

For short settings, use the connection URL instead:

```text
https://search.parallel.ai/mcp-oauth?mode=advanced&advanced_settings.max_results=5
```

Nested fields use dotted paths. URL parameters override the same fields in `x-parallel-search-config`; unrelated header settings remain. Prefer one location for each setting to avoid an old URL parameter silently overriding a new header value. An existing Bifrost client's URL is immutable, so header changes are preferable for tuning an established connection.

`objective` and `search_queries` remain per-call tool inputs and cannot be pinned in the connection. Unknown fields, unsupported modes, malformed JSON, or attempts to pin those inputs cause a handshake 400. Reconnect/verify after changes and check the effective settings in available request logs without exposing credentials.

## References

- [Search MCP configuration and precedence](https://docs.parallel.ai/integrations/mcp/search-mcp#configure-search-behavior)
- [Search API schema](https://docs.parallel.ai/api-reference/search/search)
- [Bifrost header configuration](https://docs.getbifrost.ai/mcp/auth/headers)
