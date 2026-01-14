# Quick Start

## OpenWebUI (Recommended)

1. Copy `sec_finance_ai.py` entire file
2. OpenWebUI → Admin Panel → Functions → Create New
3. Paste code
4. Save and enable
5. Start asking questions!

## Example Questions for AI

- "Get Apple's latest 10-K filing"
- "Show me Tesla's recent 8-K filings"
- "What are Microsoft's quarterly reports?"
- "Get insider trading for NVIDIA"
- "Show GameStop's recent filings"
- "Find beneficial ownership reports for Amazon"

## Python Usage

```python
from sec_finance_ai import Tools
import asyncio

async def main():
    tools = Tools()

    # Get recent 8-K filings
    result = await tools.get_recent_8k_filings("GME", limit=5)
    print(result)

    # Get latest 10-K
    result = await tools.get_latest_10k("AAPL")
    print(result)

asyncio.run(main())
```

## Supported Tickers (105+)

AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, JPM, JNJ, V, PG, WMT, DIS, PYPL, BA, GE, XOM, CVX, T, VZ, AMD, QCOM, CRM, NFLX, ORCL, IBM, **GME**, AMC, and 75+ more!

## Common Filings

- **10-K** - Annual Report
- **10-Q** - Quarterly Report
- **8-K** - Current Report (material events)
- **DEF 14A** - Proxy Statement
- **4** - Insider Trading
- **13D/13G** - Beneficial Ownership

## Troubleshooting

**"Could not find CIK for ticker"**
- Verify ticker is correct
- Check if it's a valid US stock symbol

**"No filings found"**
- Try different date range
- Check form_type is valid (10-K, 10-Q, 8-K, etc.)

## Learn More

See README.md for complete API reference and examples.
