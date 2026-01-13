# SEC-AI Quick Start Guide

Get started with SEC-AI in 5 minutes!

## 🚀 Installation

### Option 1: OpenWebUI (Fastest)
1. Copy `sec_ai.py`
2. OpenWebUI → Admin Panel → Functions → "+"
3. Paste code → Save → Enable
4. Done! Ask: *"Get Apple's latest 10-K"*

### Option 2: Python
```bash
pip install pandas pydantic requests beautifulsoup4 lxml python-dateutil
python3 -c "from sec_ai import Tools; print('✓ Ready!')"
```

## 💡 Common Tasks

### Get Recent 8-K Filings
```python
from sec_ai import Tools
import asyncio

async def example():
    tools = Tools()
    result = await tools.get_recent_8k_filings("GME", limit=5)
    print(result)

asyncio.run(example())
```

### Get Latest 10-K Annual Report
```python
result = await tools.get_latest_10k("AAPL")
print(f"Company: {result['company_name']}")
print(f"Filing: {result['latest_10k']['filing_url']}")
```

### Get Insider Trading
```python
insider_trades = await tools.get_insider_transactions("TSLA", limit=10)
for filing in insider_trades['filings']:
    print(f"{filing['filing_date']} - {filing.get('owner_name', 'Unknown')}")
```

### Search Filings
```python
results = await tools.search_filings("Tesla", form_type="10-K")
for result in results['results'][:3]:
    print(f"{result['company_info']['company_name']}: {result['filing_date']}")
```

## 📊 Supported Tickers (100+)

**Big Tech**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA
**Finance**: JPM, BAC, GS, WFC, MS, AXP, BLK
**Healthcare**: JNJ, UNH, PFE, ABBV, LLY, MRK
**Consumer**: WMT, PG, KO, MCD, NKE, DIS
**Energy**: XOM, CVX, COP
**Other**: GME, AMC, AMD, QCOM, NFLX, CRM, IBM, ORCL
... and **100+ more!**

## 🔧 Advanced Usage

### Filter by Date
```python
filings = await tools.get_company_filings(
    "AAPL",
    form_type="10-K",
    start_date="2023-01-01",
    end_date="2023-12-31"
)
```

### Get Financial Data
```python
facts = await tools.get_company_facts("AAPL")
revenues = facts['key_metrics']['Revenues']
print(f"Revenue: ${revenues['value']:,.0f}")
```

### Search Across Companies
```python
results = await tools.search_filings(
    "Tesla",
    form_type="DEF 14A",
    limit=20
)
```

## ❓ Troubleshooting

**"Could not find CIK for ticker"**
- Verify ticker is correct (e.g., "AAPL" not "Apple")
- Check if ticker is in hardcoded 100+ list or SEC EDGAR

**"No filings found"**
- Check form_type is valid (10-K, 10-Q, 8-K, etc.)
- Try increasing date range

**Slow responses**
- Normal! SEC API needs 0.1-1s per request
- Results are cached to speed up repeated queries

## 📚 More Examples

### Get Company Concept Over Time
```python
revenue_history = await tools.get_company_concept("AAPL", "Revenues")
for data_point in revenue_history['annual_data']:
    print(f"{data_point['end']}: ${data_point['val']:,}")
```

### Check API Status
```python
status = await tools.get_sec_api_status()
print(f"SEC API Status: {status['status']}")
print(f"Response time: {status['response_time_ms']}ms")
```

### Run Self-Tests
```python
results = await tools.run_self_test()
print(results['summary'])
# Output:
# {
#   'total_tests': 8,
#   'passed': 8,
#   'failed': 0,
#   'success_rate': '100.0%'
# }
```

## 🎯 Common Form Types

| Code | Meaning |
|------|---------|
| 10-K | Annual Report |
| 10-Q | Quarterly Report |
| 8-K | Current Report (major events) |
| DEF 14A | Proxy Statement (voting & compensation) |
| S-1 | IPO Registration |
| 4 | Insider Trading |
| 13D | Large shareholder (5%+) |
| 13F | Institutional holdings |

## 🔗 Resources

- [SEC EDGAR](https://www.sec.gov/edgar) - Official database
- [Full API Reference](./README.md#-api-reference) - Complete documentation
- [GitHub Issues](https://github.com/lucas0/sec-ai/issues) - Report bugs

---

**Ready to go!** Start exploring SEC filings with AI assistance. 🚀
