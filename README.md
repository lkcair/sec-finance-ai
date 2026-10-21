# sec-finance-ai 📊💼

### AI-Powered SEC Filing Integration for Your AI Assistant

**23 SEC EDGAR tools** for any AI assistant: 10-K, 10-Q, 8-K, 20-F and proxy filings, the full text of any filing read in pages or searched, XBRL company facts, insider trades, 13D/13G ownership, 13F institutional holdings, IPOs and EDGAR full-text search, through plain-language questions.

Use it as an **MCP server** (Claude, Cursor, VS Code and any MCP client), an **OpenClaw skill** or an **OpenWebUI tool**.

[![PyPI](https://img.shields.io/pypi/v/sec-finance-ai)](https://pypi.org/project/sec-finance-ai/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Also try [yfinance-ai](https://github.com/lkcair/yfinance-ai) for stocks, crypto and market data. ⭐ Star the repo or the skill if you like it.

---

# 🚀 Thousands of downloads on ClawHub and OpenWebUI

# 🚀 Quick Start

## 🔌 MCP server (Claude, Cursor, VS Code, any MCP client)

Needs [uv](https://docs.astral.sh/uv/getting-started/installation/). No API key.

**Claude Code**
```bash
claude mcp add sec-ai -e SEC_USER_AGENT="Your Name you@example.com" -- uvx sec-finance-ai@latest
```

**Claude Desktop, Cursor and other clients** (`claude_desktop_config.json`, `.cursor/mcp.json`, ...)
```json
{
  "mcpServers": {
    "sec-ai": {
      "command": "uvx",
      "args": ["sec-finance-ai@latest"],
      "env": { "SEC_USER_AGENT": "Your Name you@example.com" }
    }
  }
}
```

Without uv: `pip install sec-finance-ai`, then use `"command": "sec-finance-ai"` with no args.

All tools are exposed over MCP, each marked read-only. Listed in the [MCP Registry](https://registry.modelcontextprotocol.io) as `io.github.lkcair/sec-ai`. MCP server source: [lkcair/sec-ai-mcp](https://github.com/lkcair/sec-ai-mcp).

## 🦞 OpenClaw (ClawHub): thousands of downloads

```bash
openclaw skills install @lkcair/sec
```
Skill page: [clawhub.ai/lkcair/sec](https://clawhub.ai/lkcair/sec). You can also download the skill there and upload it to your OpenClaw skills folder.

## 🌐 OpenWebUI: thousands of downloads

1. Open sec-finance-ai on the [OpenWebUI website](https://openwebui.com/posts/sec_finance_ai_data_pull_8e017585) and click **Get**.
2. Select your OpenWebUI instance and click **Save** inside it.
3. **Enable** the tool on the model or in the chat.

Manual install: copy [sec_finance_ai.py](https://github.com/lkcair/sec-finance-ai/blob/main/sec_finance_ai.py), go to **Workspace → Tools → +**, paste, **Save**, then enable it.

## 🐍 Python

```python
import asyncio
from sec_finance_ai import Tools
print(asyncio.run(Tools().get_latest_10k("AAPL")))  # every tool is an async method
```

---

## 🪪 SEC User-Agent

The SEC asks every program to identify itself with a name and contact e-mail. Set `SEC_USER_AGENT` (as in the examples above, e.g. `"MyResearchApp admin@example.com"`). If you don't, a built-in default is sent and everything still works, but your own keeps you clear of the SEC's fair-access limits.

---

## ✨ Why sec-finance-ai

✅ **23 tools straight on the official EDGAR APIs**, no third-party data service and no API key

✅ **One file, three platforms**: the same `sec_finance_ai.py` runs as MCP server, OpenClaw skill and OpenWebUI tool

✅ **Read, search or link**: filing size checked first; read any filing in pages, search inside it for a phrase, or get the link for filings over 25 MB

✅ **Full-text search** of every EDGAR filing since 2001 by word or exact phrase

✅ **13F holdings** of any institutional manager (e.g. Berkshire Hathaway) with weights

✅ **Cross-company XBRL**: rank all companies by one metric for one period (e.g. 2024 revenue)

✅ **Ownership and insiders**: 13D/13G with amendments, Forms 3, 4 and 5

✅ **Foreign issuers**: 20-F, 6-K and 40-F

✅ **Recent IPOs**: priced offerings (424B4) and new S-1/F-1 registrations

✅ **Every release checked against real data**: each tool is called and its numbers compared with the filings

✅ **Self-test**: ask the AI to "run self-test on SEC tools" (28 checks)

---

## 📋 Supported SEC Forms

| Form | Description | Use case |
|------|-------------|----------|
| **10-K / 20-F / 40-F** | Annual report (US / foreign / Canadian) | Business, financials, risks |
| **10-Q** | Quarterly report | Quarterly financials and updates |
| **8-K / 6-K** | Current report (US / foreign) | Material events |
| **DEF 14A** | Proxy statement | Executive pay, shareholder votes |
| **S-1 / F-1 / 424B4** | Registration and final prospectus | IPOs and offerings |
| **S-8, S-3, S-4, 425** | Registrations and mergers | Employee plans, shelf offerings, combinations |
| **D, 144** | Exempt offerings and sales | Private placements, proposed insider sales |
| **3, 4, 5** | Insider trading | Officer and director transactions |
| **13D / 13G** | Beneficial ownership | Positions above 5% |
| **13F** | Institutional holdings | Quarterly manager portfolios |
| **N-PORT** | Fund holdings | Monthly fund portfolios |
| **ADV** | Investment adviser | RIA registrations |

---

## 💬 Example prompts

- "Get Apple's latest 10-K" / "What does it say about Greater China?"
- "Show Tesla's recent 8-K filings" / "Taiwan Semiconductor's latest 20-F"
- "Apple's revenue from SEC facts" / "Which companies had the highest revenue in 2024?"
- "Recent insider trading for NVIDIA" / "Beneficial ownership reports for GameStop"
- "Berkshire Hathaway's top holdings in its latest 13F"
- "Search all 8-Ks from this year that mention \"going concern\""
- "Show recent IPOs"

---

## 🛠️ Available Tools (23)

### Filings and text
- get_company_filings - Filings of a company, filtered by form and date
- get_latest_10k - Latest annual report with a preview and how to read the rest
- get_latest_10q - Latest quarterly report
- get_recent_8k_filings - Recent current reports
- analyze_8k_filing - What an 8-K reports, item by item
- get_proxy_statements - Proxy statements (DEF 14A)
- get_filing_documents - Every document inside a filing
- get_filing_size - Size of a filing before downloading
- download_filing_text - Read a filing in pages, search inside it, or get the link
- get_filing_content - Content of a filing document
- search_filings - Filings across companies by form and date
- full_text_search - EDGAR full-text search since 2001
- get_recent_ipos - Priced IPOs and new registrations

### Financial data (XBRL)
- get_company_facts - Key financial facts of a company
- get_company_concept - One metric over time
- get_available_metrics - Which metrics a company reports
- get_xbrl_frames - One metric across all companies for a period

### Ownership and insiders
- get_insider_transactions - Forms 3, 4 and 5
- get_beneficial_ownership - 13D and 13G with amendments
- get_13f_holdings - Institutional manager portfolio

### Utility
- get_sec_api_status - EDGAR API status
- get_available_functions - List of every function
- run_self_test - Self-test of all tools (28 checks)

---

## 🔗 Related

- [yfinance-ai](https://github.com/lkcair/yfinance-ai): Yahoo Finance in 68 tools
- [SEC EDGAR API documentation](https://www.sec.gov/edgar/sec-api-documentation)

MIT license. Author: lucas0.

*sec-finance-ai is not affiliated with the U.S. Securities and Exchange Commission. All data comes from public SEC databases.*
