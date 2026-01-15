# SEC-Finance-AI: Dual-Mode Financial Metrics Guide

## Overview

The enhanced `sec_finance_ai.py` now supports **smart dual-mode metric selection** that allows AI to:
1. **Generic Mode**: Get 13 essential metrics for any financial analysis (token-efficient)
2. **Specific Mode**: Request ONLY the metrics needed for targeted analysis (minimal token usage)

This solves the token limit problem by allowing AI to fetch only what's needed instead of downloading massive financial datasets.

---

## Quick Start

### Example 1: Generic Mode (Default, Recommended for General Analysis)

**Use this when you don't know what metrics you'll need:**

```python
# Call without specific_metrics parameter
result = await get_filing_content(
    ticker='GME',
    filing_type='10-Q'
)

# Returns 13 essential metrics with last 5 values each:
# - NetIncomeLoss
# - Revenues
# - InterestExpense
# - IncomeTaxExpenseBenefit
# - OperatingIncomeLoss
# - GrossProfit
# - Assets
# - Liabilities
# - StockholdersEquity
# - DepreciationDepletionAndAmortization
# - CommonStockSharesOutstanding
# - CashAndCashEquivalentsAtCarryingValue
# - LongTermDebt
```

**Response Structure (Generic Mode):**
```json
{
  "ticker": "GME",
  "company_name": "GameStop Corp.",
  "mode": "generic",
  "metrics_returned": 13,
  "values_per_metric": 5,
  "financial_metrics": {
    "NetIncomeLoss": {
      "units": {
        "USD": [
          {"value": -524000000, "end": "2025-11-01", "form": "10-Q"},
          {"value": -312000000, "end": "2025-08-02", "form": "10-Q"},
          // ... 3 more values
        ]
      }
    },
    "Revenues": { ... },
    // ... 11 more essential metrics
  }
}
```

---

### Example 2: Specific Mode (For TTM Calculations)

**Use this for targeted analysis like TTM EBITDA calculation:**

```python
# Step 1: Discover available metrics
metrics = await get_available_metrics(
    ticker='GME',
    search_term='Depreciation'
)

# Step 2: Request only the metrics you need
result = await get_filing_content(
    ticker='GME',
    filing_type='10-Q',
    specific_metrics=[
        'NetIncomeLoss',
        'InterestExpense',
        'IncomeTaxExpenseBenefit',
        'DepreciationDepletionAndAmortization'
    ]
)

# Returns ONLY 4 metrics (not 13)
# - NetIncomeLoss (for operating income)
# - InterestExpense (to add back)
# - IncomeTaxExpenseBenefit (to add back after-tax adjustments)
# - DepreciationDepletionAndAmortization (to add back)
```

**Response Structure (Specific Mode):**
```json
{
  "ticker": "GME",
  "company_name": "GameStop Corp.",
  "mode": "specific",
  "metrics_returned": 4,
  "values_per_metric": 5,
  "financial_metrics": {
    "NetIncomeLoss": { ... },  // Last 5 quarters
    "InterestExpense": { ... },
    "IncomeTaxExpenseBenefit": { ... },
    "DepreciationDepletionAndAmortization": { ... }
  }
}
```

**TTM Calculation from Response:**
```python
# Extract TTM values (last 4 quarters)
net_income_ttm = sum([
    -524_000_000,  # Q3 2025
    -312_000_000,  # Q2 2025
    -156_000_000,  # Q1 2025
    89_000_000     # Q4 2024
])

interest_expense_ttm = sum([...])
tax_benefit_ttm = sum([...])
depreciation_ttm = sum([...])

# Calculate EBITDA: NI + Interest + Taxes + D&A
ttm_ebitda = net_income_ttm + interest_expense_ttm + tax_benefit_ttm + depreciation_ttm
```

---

## Discovering Available Metrics

### Use `get_available_metrics()` to Find What's Available

```python
# Get ALL available metrics for GME
all_metrics = await get_available_metrics(ticker='GME')

# Response includes:
# - all_metrics: Complete list of 100+ metrics
# - categories: Organized by type (income_statement, balance_sheet, cash_flow, etc)
# - usage_tips: Examples of how to use specific_metrics mode
```

**Response Structure:**
```json
{
  "ticker": "GME",
  "company_name": "GameStop Corp.",
  "total_available": 245,
  "categories": {
    "income_statement": [
      "Revenues",
      "NetIncomeLoss",
      "OperatingIncomeLoss",
      "GrossProfit",
      "InterestExpense"
    ],
    "balance_sheet": [
      "Assets",
      "Liabilities",
      "StockholdersEquity",
      "CashAndCashEquivalentsAtCarryingValue",
      "LongTermDebt"
    ],
    "cash_flow": [
      "DepreciationDepletionAndAmortization",
      "CashFlow"
    ]
  },
  "usage_tips": {
    "generic_mode": "Call get_filing_content() without specific_metrics for 13 essentials",
    "specific_mode": "Use get_filing_content() with specific_metrics list",
    "ttm_calculation": "For TTM, use specific_metrics with income statement and adjustment items",
    "metric_search": "Search by keyword to find related metrics"
  }
}
```

### Search for Specific Metrics

```python
# Find all depreciation-related metrics
results = await get_available_metrics(
    ticker='GME',
    search_term='Depreciation'
)

# Returns metrics matching the search term:
# - DepreciationDepletionAndAmortization
# - AccumulatedDepreciation
# - etc.
```

---

## File Handling

The tool intelligently handles large SEC filings:

### Small Files (<1MB)
```python
result = await get_filing_content(
    ticker='GME',
    filing_type='10-Q',
    get_full_content=True  # Download and read full text
)

# Response includes:
# - full_content: Complete filing text for AI analysis
# - content_size_kb: "245.3 KB"
```

### Large Files (≥1MB)
```python
result = await get_filing_content(
    ticker='AAPL',
    filing_type='10-K',
    get_full_content=True  # Try to download but will link if too large
)

# Response includes:
# - filing_url: "https://www.sec.gov/Archives/edgar/..."
# - file_size_mb: 2.5
# - file_too_large: true
# - ai_note: "⚠️ NOTICE: The 10-K filing for Apple Inc. is 2.5MB,
#            which exceeds our 1MB processing limit. We've sent the user
#            a link to download the full filing directly from SEC EDGAR.
#            The user should download and analyze it manually..."
```

**Always check for `ai_note` field** - if present, inform user that they need to download the filing manually.

---

## Real-World Example: GME TTM EBITDA Calculation

```python
import asyncio

async def calculate_gme_ttm_ebitda():
    # Step 1: Discover what metrics are available
    print("Step 1: Discovering available metrics...")
    metrics = await get_available_metrics(
        ticker='GME',
        search_term='NetIncomeLoss'
    )
    print(f"Found {metrics['total_available']} total metrics")

    # Step 2: Request specific metrics for TTM calculation
    print("\nStep 2: Fetching financial data for TTM calculation...")
    filing = await get_filing_content(
        ticker='GME',
        filing_type='10-Q',
        specific_metrics=[
            'NetIncomeLoss',
            'InterestExpense',
            'IncomeTaxExpenseBenefit',
            'DepreciationDepletionAndAmortization'
        ]
    )

    print(f"Mode: {filing['mode']}")
    print(f"Metrics returned: {filing['metrics_returned']}")
    print(f"Historical values per metric: {filing['values_per_metric']}")

    # Step 3: Extract TTM values
    print("\nStep 3: Calculating TTM EBITDA...")

    metrics_data = filing['financial_metrics']

    # Get last 4 quarters for each metric
    net_income_values = metrics_data['NetIncomeLoss']['units']['USD'][:4]
    interest_values = metrics_data['InterestExpense']['units']['USD'][:4]
    tax_values = metrics_data['IncomeTaxExpenseBenefit']['units']['USD'][:4]
    depreciation_values = metrics_data['DepreciationDepletionAndAmortization']['units']['USD'][:4]

    # Sum to get TTM
    ttm_net_income = sum(v['value'] for v in net_income_values)
    ttm_interest = sum(v['value'] for v in interest_values)
    ttm_taxes = sum(v['value'] for v in tax_values)
    ttm_depreciation = sum(v['value'] for v in depreciation_values)

    # Calculate EBITDA
    ttm_ebitda = ttm_net_income + ttm_interest + ttm_taxes + ttm_depreciation

    print(f"TTM Net Income: ${ttm_net_income:,.0f}")
    print(f"TTM Interest Expense: ${ttm_interest:,.0f}")
    print(f"TTM Tax Benefit: ${ttm_taxes:,.0f}")
    print(f"TTM Depreciation & Amortization: ${ttm_depreciation:,.0f}")
    print(f"\nTTM EBITDA: ${ttm_ebitda:,.0f}")

    return ttm_ebitda

# Run it
ttm_ebitda = asyncio.run(calculate_gme_ttm_ebitda())
```

---

## API Reference

### `get_filing_content()`

**Parameters:**
- `ticker` (str, required): Stock ticker (e.g., 'GME', 'AAPL')
- `filing_type` (str, optional): '10-Q', '10-K', '8-K', etc. Default: latest
- `get_full_content` (bool, optional): If True, try to download full filing text. Default: False
- `specific_metrics` (list, optional): List of metric names to fetch. Default: None (returns 13 essentials)

**Returns:** Dict with financial metrics, filing metadata, and optionally full content or link

---

### `get_available_metrics()`

**Parameters:**
- `ticker` (str, required): Stock ticker (e.g., 'GME', 'AAPL')
- `search_term` (str, optional): Keyword to filter metrics (e.g., 'Depreciation', 'Revenue', 'Debt')

**Returns:** Dict with all_metrics, categories, and usage tips

---

## Token Efficiency Comparison

| Scenario | Mode | Metrics | Values | Approx. Tokens |
|----------|------|---------|--------|----------------|
| "Tell me about GME's financials" | Generic | 13 | 5 each | ~8,000 |
| "Calculate GME TTM EBITDA" | Specific | 4 | 5 each | ~2,400 |
| "Full 10-K analysis" | With content | 13 + full text | Variable | 50,000-150,000 |
| "Full 10-K too large" | With content | 13 + link | N/A | ~8,000 + user downloads |

---

## Common Use Cases

### 1. Quick Financial Overview
```python
# Generic mode - 13 essential metrics
await get_filing_content(ticker='AAPL', filing_type='10-Q')
```

### 2. Specific Ratio Calculation
```python
# Current ratio: Current Assets / Current Liabilities
await get_filing_content(
    ticker='AAPL',
    specific_metrics=['AssetsCurrent', 'LiabilitiesCurrent']
)
```

### 3. Debt Analysis
```python
# Debt-to-equity: Total Debt / Equity
await get_filing_content(
    ticker='TSLA',
    specific_metrics=['LongTermDebt', 'ShortTermBorrowings', 'StockholdersEquity']
)
```

### 4. Full Filing Review (for small filings)
```python
# Get content if <1MB, else link
await get_filing_content(
    ticker='GME',
    filing_type='10-Q',
    get_full_content=True
)
```

---

## Workflow Best Practices

1. **Start with metric discovery** if you're unsure what metrics exist
   ```python
   metrics = await get_available_metrics(ticker='GME')
   ```

2. **Use specific mode for custom analysis** to minimize tokens
   ```python
   filing = await get_filing_content(
       ticker='GME',
       specific_metrics=['NetIncomeLoss', 'Revenues']
   )
   ```

3. **Use generic mode for general questions** (default behavior)
   ```python
   filing = await get_filing_content(ticker='GME')
   ```

4. **Check ai_note for large files** and inform user to download manually
   ```python
   if 'ai_note' in filing:
       print(filing['ai_note'])
       print(f"Download from: {filing['filing_url']}")
   ```

5. **Always use 5 values for TTM calculations** (last 4 quarters + 1 prior)

---

## Known Limitations

- **Max metrics in response**: Limited by token budget (200K tokens for OpenRouter)
- **Historical depth**: 5 most recent values per metric (sufficient for TTM over 4 quarters)
- **File size limit**: 1MB for automatic download; larger files require user manual download
- **Data source**: SEC XBRL (standardized financial data from 10-K/10-Q filings)

---

## Troubleshooting

**Issue**: Too many tokens in response
**Solution**: Use specific mode with fewer metrics, or use generic mode instead

**Issue**: "file_too_large" warning
**Solution**: Check the `filing_url` provided and share with user for manual download

**Issue**: Metric not found in specific_metrics
**Solution**: Use `get_available_metrics(search_term='...')` to find exact metric name

**Issue**: 5 values not enough for TTM
**Solution**: Use `get_company_concept()` for deeper historical data

---

## Files Modified

- `/root/sec-ai/sec_finance_ai.py`: Added metric discovery function and enhanced docstrings
- `/root/sec-ai/DUAL_MODE_GUIDE.md`: This guide

---

## Version

- Version: 1.0.1
- Enhanced: January 2026
- Feature: Dual-mode metric selection with metric discovery

---

## Questions?

Refer to the inline docstrings in `sec_finance_ai.py` for detailed parameter explanations and return value structures.
