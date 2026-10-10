# sec-finance-ai 📊💼

### AI-Powered SEC Filing Integration for Your AI Assistant

**Natural Language SEC Integration** - Access 23 SEC filing tools directly from OpenWebUI, Claude, ChatGPT, or any AI assistant. Get 10-K, 10-Q, 8-K filings, 13D/13G beneficial ownership, insider trading data, company facts (XBRL), and institutional holdings via simple natural language queries.

**Author**: lucas0

**Github**: [Github](https://github.com/lkcair/)

**Version**: 1.3.1

**License**: MIT

**Requirements**: pandas>=2.2.0, pydantic>=2.0.0, requests>=2.28.0, beautifulsoup4>=4.12.0, lxml>=4.9.0, python-dateutil>=2.8.0

**Repository**: https://github.com/lkcair/sec-finance-ai

**OpenWebUI Page**: Download sec-finance-ai on the [OpenWebUI Website](https://openwebui.com/posts/fc928bb1-1ae8-462d-a4c1-ae5ede39aaa7)

**OpenClaw Page**: [https://clawhub.ai/lkcair/sec](https://clawhub.ai/lkcair/sec)

---
# Star the [Github](https://github.com/lkcair/sec-finance-ai) or the Skill if you like it.
**Repository**: https://github.com/lkcair/sec-finance-ai

# Also, try [yfinance-ai](https://github.com/lkcair/yfinance-ai) for stocks and crypto data.


# 🚀 Quick Start
## 🦞 (Main) Installation with OpenClaw
```bash
openclaw skills install @lkcair/sec
```
On OpenClaw, start asking questions like:
   - "What's Apple's latest 10-K about?"
   - "Get beneficial ownership reports for GME"

Skill page: [Openclaw SEC](https://clawhub.ai/lkcair/sec)

- **(Alternative) OpenClaw Manual**: Download Skill at [https://clawhub.ai/lkcair/sec](https://clawhub.ai/lkcair/sec) and upload manually to OpenClaw skills location.

## 🚀 OpenWebUI (Main) Automatic Installation
1. Download `sec-finance-ai` on the [OpenWebUI Website](https://openwebui.com/posts/fc928bb1-1ae8-462d-a4c1-ae5ede39aaa7)
2. Click on **Get**
3. Select your OpenWebUI instance.
4. Click on **Save** inside your OpenWebUI installation.
5. **Enable** the tool on the Model or Chat.
6. Start asking questions like:
   - "Get Apple's latest 10-K"
   - "Show GameStop's recent 8-K filings"

---

## 🚨 CRITICAL: SEC User-Agent Requirement
The SEC requires all programmatic requests to identify the user/company and provide a contact email. **Requests without a proper User-Agent will be blocked (403 Forbidden).**

Set the `SEC_USER_AGENT` environment variable (for example `SEC_USER_AGENT="MyResearchApp admin@example.com"`), or, if you are using this as a standalone script, locate `SEC_HEADERS` in `sec_finance_ai.py` and update it:
```python
SEC_HEADERS = {
    "User-Agent": "MyResearchApp admin@example.com", # <--- UPDATE THIS
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*"
}
```

---

## ✨ Features

✅ **Monolithic Codebase:** Single-file script allowing easy integration

✅ **23 SEC Filing Tools** - Full access to EDGAR database

✅ **Read, Search or Link** - Exact filing size checked before download; read filings in 50,000-character pages, search inside a filing for a word or phrase, or get the link only for filings over 25MB

✅ **Full-Text Search** - Search the text of every EDGAR filing since 2001 by word or exact phrase

✅ **13F Holdings** - Latest portfolio of any institutional manager (e.g. Berkshire Hathaway) with weights

✅ **Cross-Company XBRL** - Rank all companies by one metric for one period (e.g. 2024 revenue)

✅ **Recent IPOs** - Priced offerings (424B4) and new S-1/F-1 registrations

✅ **Foreign Issuer Support** - Full support for **20-F** and **6-K** filings

✅ **Enhanced Ownership Tracking** - Comprehensive **13D/13G** monitoring including all amendments

✅ **Financial Facts** - XBRL financial data and 500+ metrics

✅ **Insider Trading** - Forms 3, 4, 5 tracking

✅ **Smart Mode** - Generic (13 essential metrics) or Specific (custom metrics) modes for token efficiency

✅ **Built-in testing** function for validation

✅ **Comprehensive error handling** and rate limiting protection

✅ **Natural language** query support

---

## 📋 Supported SEC Forms

| Form Type | Description | Use Case |
|-----------|-------------|----------|
| **10-K** | Annual Report (US) | Complete business overview, financials, risks |
| **20-F** | Annual Report (Foreign) | Annual financials for international companies (e.g. TSM, ASML) |
| **10-Q** | Quarterly Report (US) | Quarterly financials and updates |
| **8-K** | Current Report (US) | Material events and corporate changes |
| **6-K** | Current Report (Foreign) | Material events for international companies |
| **DEF 14A** | Proxy Statement | Executive compensation, shareholder voting |
| **S-1 / F-1** | Registration Statement | IPO filings and new securities |
| **424B4** | Final Prospectus | Priced IPOs and offerings |
| **40-F** | Annual Report (Canadian) | Annual financials for Canadian issuers |
| **S-8, S-3, S-4, 425** | Registrations and Mergers | Employee plans, shelf offerings, business combinations |
| **D, 144** | Exempt Offerings and Sales | Private placements, proposed insider sales |
| **3, 4, 5** | Insider Trading | Officer and director transactions |
| **13D/13G** | Beneficial Ownership | Large shareholder positions (>5%) & merger alerts |
| **13F** | Institutional Holdings | Quarterly institutional positions |
| **N-PORT** | Fund Holdings | Monthly mutual fund portfolios |
| **ADV** | Investment Advisor | RIA registrations and updates |

---

## 💬 Example Prompts for AI

### Basic Queries
- "Get Apple's latest 10-K filing"
- "Show me Tesla's recent 8-K filings"
- "What is Taiwan Semiconductor's latest 20-F?"

### Financial Analysis
- "Get Apple's revenue data from SEC facts"
- "Show me Microsoft's assets and liabilities"

### Insider Trading & Ownership
- "Show me recent insider trading for NVIDIA"
- "Get beneficial ownership reports for GameStop"

### Advanced Searches
- "Find all 6-K filings for Alibaba"
- "Get Schedule 13D for EBAY"
- "Search all 8-Ks from this year that mention \"going concern\""
- "What are Berkshire Hathaway's top holdings in its latest 13F?"
- "Which companies had the highest revenue in 2024?"
- "What does Apple's latest 10-K say about Greater China?"
- "Show recent IPOs"

---

## 🧪 Testing

AI can self-test by asking:

```
"Run self-test on SEC tools"
```

This runs 28 checks across all 23 functions and reports results with **100% pass rate**.

---

## 🔗 Related Projects
- **[yfinance-ai](https://github.com/lkcair/yfinance-ai)** - Yahoo Finance integration
- **[SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)** - Official SEC API documentation

---

**Built with ❤️ for the AI and Finance communities**

*SEC-AI is not affiliated with the U.S. Securities and Exchange Commission. All data is sourced from public SEC databases with proper attribution.*

*Version: 1.3.1*
*Status: Production Ready ✅*
