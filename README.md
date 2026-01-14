# sec-finance-ai 📊💼

**AI-Powered SEC Filing Integration for Your AI Assistant**

40+ tools for accessing SEC filings directly from OpenWebUI, Claude, ChatGPT, or any AI assistant. Get 10-K, 10-Q, 8-K filings, insider trading data, company facts, and more with natural language queries.

From the same creators of **[yfinance-ai](https://github.com/lkcair/yfinance-ai)**.


## 🛠️ Installation

### OpenWebUI Automatic (Recommended)

**🚀 Easiest way - works exactly like yfinance-ai:**

    1. Download sec-finance-ai on the OpenWebUI Website
    2. Click on Get
    3. Write your OpenWebUI address for import to work.
    4. Click on Save inside your OpenWebUI installation.
    5. Enable on Model or on Chat (VERY IMPORTANT - Either enable the sec-finance-ai TOOL on the model itself via Admin Panel; or enable everytime on every new chat).
    
    6. Start asking questions like:
        "What's Apple's latest 8K about?"
        "Compare AAPL 10K with AMZN"

🚀 (Alternative) OpenWebUI Manual Installation

1. Copy the entire file content: `sec_finance_ai.py`
2. OpenWebUI → Admin Panel → Functions → Create New
3. Paste the code
4. Save and enable
5. Ask: *"Get Apple's latest 10-K"* or *"Show GameStop's recent 8-K filings"*

Done! All functions available in your AI assistant.




[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SEC EDGAR API](https://img.shields.io/badge/SEC-EDGAR%20API-green.svg)](https://www.sec.gov/edgar)

## 🚀 Features

- **40+ SEC Filing Tools** - Most comprehensive SEC integration available
- **Multi-Filing Support** - 10-K, 10-Q, 8-K, DEF 14A, S-1, and more
- **Real-time Data** - Direct access to SEC EDGAR database
- **Insider Trading** - Forms 3, 4, 5 with transaction details
- **Ownership Reports** - 13D, 13G beneficial ownership tracking
- **Company Facts** - XBRL financial data and metrics
- **Executive Compensation** - Proxy statement analysis
- **Institutional Holdings** - 13F filings tracking
- **SEC Compliance** - Rate limiting and proper attribution
- **AI Integration** - Works with all major AI platforms

## 📋 Supported SEC Forms

| Form Type | Description | Use Case |
|-----------|-------------|----------|
| **10-K** | Annual Report | Complete business overview, financials, risks |
| **10-Q** | Quarterly Report | Quarterly financials and updates |
| **8-K** | Current Report | Material events and corporate changes |
| **DEF 14A** | Proxy Statement | Executive compensation, shareholder voting |
| **S-1** | Registration Statement | IPO filings and new securities |
| **3, 4, 5** | Insider Trading | Officer and director transactions |
| **13D/13G** | Beneficial Ownership | Large shareholder positions (>5%) |
| **13F** | Institutional Holdings | Quarterly institutional positions |
| **N-PORT** | Fund Holdings | Monthly mutual fund portfolios |
| **ADV** | Investment Advisor | RIA registrations and updates |


### Python Direct Usage
```bash
pip install pandas pydantic requests beautifulsoup4 lxml python-dateutil
```

```python
from sec_finance_ai import Tools
import asyncio

async def example():
    tools = Tools()
    result = await tools.get_recent_8k_filings("GME")
    print(result)

asyncio.run(example())
```

## 📖 Usage Examples

### Basic Company Filings
```python
# Get all recent filings for Apple
filings = await tools.get_company_filings("AAPL", limit=10)

# Get specific form type
quarterly_reports = await tools.get_company_filings("TSLA", form_type="10-Q", limit=5)

# Filter by date range
recent_8ks = await tools.get_company_filings(
    "MSFT", 
    form_type="8-K", 
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### Financial Data & Company Facts
```python
# Get comprehensive company facts from XBRL data
facts = await tools.get_company_facts("AAPL")

# Get specific financial concept over time
revenue_data = await tools.get_company_concept("AAPL", "Revenues")
net_income = await tools.get_company_concept("AAPL", "NetIncomeLoss")
```

### Insider Trading & Ownership
```python
# Get insider trading transactions
insider_trades = await tools.get_insider_transactions("TSLA", limit=20)

# Get beneficial ownership reports (13D/13G)
ownership = await tools.get_beneficial_ownership("GME", limit=10)
```

### Search & Discovery
```python
# Search filings by company name
results = await tools.search_filings("Apple Inc", form_type="10-K")

# Search across multiple criteria
proxy_search = await tools.search_filings(
    "Tesla", 
    form_type="DEF 14A",
    start_date="2023-01-01"
)
```

## 🤖 AI Assistant Prompts

### For OpenWebUI/ChatGPT/Claude:

**Basic Queries:**
- *"Get Apple's latest 10-K filing"*
- *"Show me Tesla's recent 8-K filings"*
- *"What are Microsoft's quarterly reports?"*

**Financial Analysis:**
- *"Get Apple's revenue data from SEC filings"*
- *"Show me Tesla's financial metrics over time"*
- *"Compare Amazon's assets vs liabilities"*

**Insider Trading:**
- *"Show me recent insider trading for NVIDIA"*
- *"Get beneficial ownership reports for GameStop"*
- *"Who are the major shareholders of Apple?"*

**Advanced Searches:**
- *"Find all proxy statements filed this year"*
- *"Search for recent IPO filings"*
- *"Get merger and acquisition documents"*

## 🔧 API Reference

### Core Filing Functions

#### `get_company_filings(ticker, form_type=None, limit=10, start_date=None, end_date=None)`
Get SEC filings for a company by ticker symbol.

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA')
- `form_type` (str, optional): SEC form type filter
- `limit` (int): Maximum number of filings to return
- `start_date` (str, optional): Start date (YYYY-MM-DD)
- `end_date` (str, optional): End date (YYYY-MM-DD)

#### `get_latest_10k(ticker)`
Get the latest 10-K annual report for a company.

#### `get_latest_10q(ticker)`
Get the latest 10-Q quarterly report for a company.

#### `get_recent_8k_filings(ticker, limit=5)`
Get recent 8-K current reports for a company.

### Financial Data Functions

#### `get_company_facts(ticker)`
Get company facts and financial metrics from SEC XBRL data.

#### `get_company_concept(ticker, concept)`
Get specific financial concept data over time.

**Common Concepts:**
- `Revenues` - Total revenue
- `NetIncomeLoss` - Net income
- `Assets` - Total assets
- `StockholdersEquity` - Shareholders' equity
- `CashAndCashEquivalentsAtCarryingValue` - Cash position

### Ownership & Trading Functions

#### `get_insider_transactions(ticker, limit=20)`
Get insider trading transactions (Forms 3, 4, 5).

#### `get_beneficial_ownership(ticker, limit=10)`
Get beneficial ownership reports (13D, 13G).

### Search Functions

#### `search_filings(query, form_type=None, start_date=None, end_date=None, limit=20)`
Search SEC filings by company name or criteria.

### Utility Functions

#### `get_sec_api_status()`
Check SEC API status and connectivity.

#### `run_self_test()`
Run comprehensive self-test of all SEC-AI tools.

## 📊 Data Sources

SEC-AI uses official SEC data sources:

- **SEC EDGAR Database** - Primary filing repository
- **SEC XBRL API** - Structured financial data
- **Company Tickers API** - Ticker to CIK mapping
- **Company Facts API** - Standardized financial metrics

All data is sourced directly from the SEC with proper attribution and rate limiting compliance.

## ⚡ Performance & Compliance

- **Rate Limiting** - Complies with SEC's 10 requests/second limit
- **Retry Logic** - Exponential backoff for failed requests
- **Error Handling** - Comprehensive error management
- **Caching** - Intelligent caching to reduce API calls
- **User Agent** - Proper SEC-compliant user agent headers

## 🧪 Testing

Run the built-in self-test:

```python
# Test all functions
results = await tools.run_self_test()
print(f"Tests passed: {results['summary']['success_rate']}")
```

Or ask your AI assistant: *"Run self-test on SEC tools"*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SEC EDGAR Team** - For providing comprehensive public access to corporate filings
- **SEC XBRL Program** - For standardized financial data formats
- **Open Source Community** - For the foundational libraries that make this possible

## 📞 Support

- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - General questions and community support
- **Sponsor** - Support development at [GitHub Sponsors](https://github.com/sponsors/lkcair)

## 🔗 Related Projects

- **[yfinance-ai](https://github.com/lkcair/yfinance-ai)** - Yahoo Finance integration for AI assistants
- **[SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)** - Official SEC API documentation

---

**Built with ❤️ for the AI and Finance communities**

*SEC-AI is not affiliated with the U.S. Securities and Exchange Commission. All data is sourced from public SEC databases with proper attribution.*
