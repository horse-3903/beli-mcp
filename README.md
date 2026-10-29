<div align="center">

# Beli MCP Server

Unofficial Beli MCP server: let Claude and other AI assistants search restaurants, manage bookmarks and read guides on your Beli account.

[![Python](https://img.shields.io/badge/Python_3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-000000?style=flat-square&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/github/license/horse-3903/beli-mcp?style=flat-square)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/horse-3903/beli-mcp?style=flat-square)](../../commits)

</div>

---

## Overview

**beli-mcp** is a Model Context Protocol server for the Beli restaurant ranking app. It wraps the unofficial Beli API documented in [beli-api-spec](https://github.com/horse-3903/beli-api-spec), so an AI assistant can search restaurants, bookmark places and read your guides. It signs in with your own Beli account and spaces requests to stay under Beli's rate limit.

---

## Features

- **Search** - find restaurants in a city and get their Beli business ids
- **Bookmarks** - list bookmarks, check a place and add new ones
- **Guides** - list your guides and read their places
- **Referral link** - fetch your referral link
- **Read-only escape hatch** - `beli_get` calls any GET endpoint from the spec
- **Rate limit aware** - requests are spaced about 3 seconds apart

Tools: `whoami`, `search_restaurants`, `get_bookmarks`, `add_bookmark`, `bookmark_status`, `list_my_guides`, `get_my_guide_items`, `get_guide`, `referral_link`, `beli_get`. `add_bookmark` is the only tool that writes.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-000000?style=for-the-badge&logo=anthropic&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-0A66C2?style=for-the-badge)

---

## Getting Started

### Prerequisites

- Python 3.10+
- A Beli account with an email and password login

### Installation

```bash
git clone https://github.com/horse-3903/beli-mcp
cd beli-mcp
pip install .
```

### Run locally

```bash
BELI_EMAIL=you@example.com BELI_PASSWORD=your-password beli-mcp
```

### Add to Claude Desktop or Claude Code

```json
{
  "mcpServers": {
    "beli": {
      "command": "beli-mcp",
      "env": { "BELI_EMAIL": "you@example.com", "BELI_PASSWORD": "your-password" }
    }
  }
}
```

---

## Project Structure

```
beli-mcp/
├── beli_mcp/
│   ├── __init__.py
│   └── server.py        # MCP tools and Beli API client
├── pyproject.toml
├── AGENTS.md            # instructions for AI coding agents
└── README.md
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BELI_EMAIL` | none | Beli account email |
| `BELI_PASSWORD` | none | Beli account password |
| `BELI_REFRESH_TOKEN` | none | Optional refresh token, used instead of the password while valid (7 days) |

---

## FAQ

**Is there an official Beli MCP server?** No. This one is unofficial and uses the reverse engineered Beli API.

**Does it work with Claude?** Yes, with any MCP client such as Claude Desktop, Claude Code or Cursor.

---

## Disclaimer

Unofficial and not affiliated with Beli. **Use at your own risk.** Calling the API outside the official app may violate Beli's terms and can lead to rate limiting, a suspended or banned account, or loss of data. The authors accept no responsibility for any consequences to your account. Use only your own account, and never share your credentials or tokens.
