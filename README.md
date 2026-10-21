# sec-finance-ai

AI-powered SEC EDGAR integration: 23 tools on the official sec.gov APIs, in one Python file.

🚀 **Thousands of downloads on ClawHub and OpenWebUI**

10-K, 10-Q, 8-K, 20-F and proxy filings, the full text of any filing read in pages or searched, XBRL company facts and cross-company rankings, Form 4 insider trades, 13D/13G ownership, 13F fund portfolios, IPOs, and full-text search of every filing since 2001.

| Use it in | Install | Repo |
|---|---|---|
| Claude, Cursor, VS Code and other MCP clients | `uvx sec-finance-ai@latest` | [sec-ai-mcp](https://github.com/lkcair/sec-ai-mcp) |
| ClawHub skill for OpenClaw 🚀 Thousands of downloads | `openclaw skills install @lkcair/sec` | [sec-ai-skill](https://github.com/lkcair/sec-ai-skill) |
| OpenWebUI tool 🚀 Thousands of downloads | [Get it on openwebui.com](https://openwebui.com/posts/sec_finance_ai_data_pull_8e017585) | [sec-finance-ai](https://github.com/lkcair/sec-finance-ai) |
| Python | `from sec_finance_ai import Tools` | [sec-finance-ai](https://github.com/lkcair/sec-finance-ai) |


## Install

**MCP**
```bash
claude mcp add sec-ai -e SEC_USER_AGENT="Your Name you@example.com" -- uvx sec-finance-ai@latest
```
Setup for VS Code, Claude Desktop, Cursor and other clients: [sec-ai-mcp](https://github.com/lkcair/sec-ai-mcp).

**ClawHub (OpenClaw)**
```bash
openclaw skills install @lkcair/sec
```
Skill page: [clawhub.ai/lkcair/sec](https://clawhub.ai/lkcair/sec).

**OpenWebUI**
1. Open the [OpenWebUI page](https://openwebui.com/posts/sec_finance_ai_data_pull_8e017585), click **Get** and save it in your OpenWebUI.
2. Enable the tool on the model or in the chat.

Or copy [`sec_finance_ai.py`](https://github.com/lkcair/sec-finance-ai/blob/main/sec_finance_ai.py) into **Workspace > Tools > +** and save.

**Python**
```python
import asyncio
from sec_finance_ai import Tools
print(asyncio.run(Tools().get_latest_10k("AAPL")))
```

Set `SEC_USER_AGENT` (for example `"Your Name you@example.com"`) to identify yourself to the SEC. If it is not set, a default is sent.

## Tools (23)

**Filings**
- `get_company_filings`: Get SEC filings for a company by ticker symbol
- `get_latest_10k`: Latest 10-K with a short preview of its text
- `get_latest_10q`: Latest 10-Q with a short preview of its text
- `get_recent_8k_filings`: Recent 8-K filings with a short preview of each
- `analyze_8k_filing`: Get and summarize the latest 8-K filing for a company
- `get_proxy_statements`: Get proxy statements (DEF 14A) for a company
- `get_recent_ipos`: Get recent IPO activity from EDGAR

**Reading inside a filing**
- `get_filing_size`: Exact size of a filing document before downloading it
- `download_filing_text`: Read a filing in 50,000-character pages, search inside it, or get the link when it is over 25 MB
- `get_filing_documents`: List every document in a filing (main document, exhibits, XBRL, XML) with sizes and links
- `get_filing_content`: Key financial figures from XBRL, or the full filing text in pages

**Search**
- `full_text_search`: Search the full text of every EDGAR filing since 2001 (words or "exact phrase")
- `search_filings`: Search SEC filings by company name or other criteria

**Ownership and insiders**
- `get_insider_transactions`: Get insider trading transactions (Forms 3, 4, 5) for a company
- `get_beneficial_ownership`: Get beneficial ownership reports (13D, 13G) for a company
- `get_13f_holdings`: Get the latest 13F portfolio of an institutional investment manager

**Financial data (XBRL)**
- `get_company_facts`: Get company facts from SEC XBRL data
- `get_company_concept`: Get specific financial concept data for a company
- `get_available_metrics`: Discover available financial metrics for a company from SEC XBRL data
- `get_xbrl_frames`: One financial concept across all reporting companies for one period, ranked

**Utility**
- `get_sec_api_status`: Check SEC API status and connectivity
- `get_available_functions`: List of every function
- `run_self_test`: Run comprehensive self-test of all SEC-AI tools

## Example questions

- What does Apple's latest 10-K say about Greater China?
- What are Berkshire Hathaway's top holdings in its latest 13F?
- Find every 8-K this year that mentions 'going concern'.
- Which companies had the highest revenue in 2024?

See also [yfinance-ai](https://github.com/lkcair/yfinance-ai) for stocks, crypto and market data.

## License

MIT. All data comes from public SEC EDGAR databases. Not affiliated with the U.S. Securities and Exchange Commission.
