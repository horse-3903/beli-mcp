# AGENTS.md: beli-mcp

MCP server for the Beli app, built on the unofficial API documented in `beli-api-spec`.

## Layout

- `beli_mcp/server.py`: all tools and the HTTP client (login, token refresh, request spacing).

## Run and test

```bash
pip install -e .
BELI_EMAIL=... BELI_PASSWORD=... beli-mcp
```

## Conventions

- Pin `mcp<2`: the code uses `mcp.server.fastmcp.FastMCP`, which v2 renamed.
- Beli needs an `Origin` header and returns 429 on bursts, so calls are spaced about 3 seconds apart. Do not remove that.
- Guide calls need the feature-flag query parameters in `GUIDE_FLAGS`, otherwise Beli returns an empty list.
- Only add tools for endpoints verified in `beli-api-spec` (`x-verified: true`). `add_bookmark` is the only write tool; ask before adding more.

## Rules

- Never commit credentials, tokens, `.env` files or account ids.
- Do not use em dashes in any text. Keep commit messages to one short line, with no Co-Authored-By trailers. Only commit when asked.
