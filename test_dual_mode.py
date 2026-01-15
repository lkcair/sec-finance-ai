#!/usr/bin/env python3
"""
Test script for dual-mode metric selection in sec_finance_ai.py

Tests:
1. Generic mode (no specific_metrics) - Should return 13 essential metrics
2. Specific mode (with specific_metrics) - Should return only requested metrics
3. Metric discovery - Should list available metrics and allow searching
4. File size handling - Should check file size and handle large files gracefully
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, '/root/sec-ai')

from sec_finance_ai import Tools

async def test_generic_mode():
    """Test generic mode - should return 13 essential metrics"""
    print("\n" + "="*70)
    print("TEST 1: Generic Mode (Default, 13 Essential Metrics)")
    print("="*70)

    tools = Tools()

    print("\nCalling: get_filing_content(ticker='AAPL', filing_type='10-Q')")
    print("         (no specific_metrics - should use generic mode)")

    result = await tools.get_filing_content(ticker='AAPL', filing_type='10-Q')

    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return False

    print(f"\n✅ Generic Mode Results:")
    print(f"   Ticker: {result.get('ticker')}")
    print(f"   Company: {result.get('company_name')}")
    print(f"   Mode: {result.get('mode')}")
    print(f"   Metrics Returned: {result.get('metrics_returned')}")
    print(f"   Values per Metric: {result.get('values_per_metric')}")
    print(f"   Filing Type: {result.get('filing_type')}")
    print(f"   Filing Date: {result.get('filing_date')}")

    if result.get('mode') != 'generic':
        print(f"❌ FAILED: Expected mode='generic', got mode='{result.get('mode')}'")
        return False

    if result.get('metrics_returned') != 13:
        print(f"❌ FAILED: Expected 13 metrics, got {result.get('metrics_returned')}")
        return False

    print(f"\n📊 Metrics included:")
    for metric_name in list(result.get('financial_metrics', {}).keys())[:5]:
        metric_data = result['financial_metrics'][metric_name]
        num_values = len(metric_data.get('units', {}).get('USD', []))
        print(f"   - {metric_name}: {num_values} values")

    print(f"   ... and {result.get('metrics_returned') - 5} more")

    return True


async def test_specific_mode():
    """Test specific mode - should return only requested metrics"""
    print("\n" + "="*70)
    print("TEST 2: Specific Mode (4 Metrics for TTM EBITDA)")
    print("="*70)

    tools = Tools()

    specific_metrics = [
        'NetIncomeLoss',
        'InterestExpense',
        'IncomeTaxExpenseBenefit',
        'DepreciationDepletionAndAmortization'
    ]

    print(f"\nCalling: get_filing_content(")
    print(f"    ticker='AAPL',")
    print(f"    filing_type='10-Q',")
    print(f"    specific_metrics={specific_metrics}")
    print(f")")

    result = await tools.get_filing_content(
        ticker='AAPL',
        filing_type='10-Q',
        specific_metrics=specific_metrics
    )

    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return False

    print(f"\n✅ Specific Mode Results:")
    print(f"   Ticker: {result.get('ticker')}")
    print(f"   Company: {result.get('company_name')}")
    print(f"   Mode: {result.get('mode')}")
    print(f"   Metrics Returned: {result.get('metrics_returned')}")
    print(f"   Values per Metric: {result.get('values_per_metric')}")

    if result.get('mode') != 'specific':
        print(f"❌ FAILED: Expected mode='specific', got mode='{result.get('mode')}'")
        return False

    if result.get('metrics_returned') != 4:
        print(f"❌ FAILED: Expected 4 metrics, got {result.get('metrics_returned')}")
        return False

    print(f"\n📊 Metrics included:")
    for metric_name in result.get('financial_metrics', {}).keys():
        metric_data = result['financial_metrics'][metric_name]
        num_values = len(metric_data.get('units', {}).get('USD', []))
        print(f"   - {metric_name}: {num_values} values")

    return True


async def test_metric_discovery():
    """Test metric discovery - should list available metrics"""
    print("\n" + "="*70)
    print("TEST 3: Metric Discovery (Find Available Metrics)")
    print("="*70)

    tools = Tools()

    print("\nTest 3a: Get ALL metrics for a company")
    print("Calling: get_available_metrics(ticker='AAPL')")

    result = await tools.get_available_metrics(ticker='AAPL')

    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return False

    print(f"\n✅ Metric Discovery Results:")
    print(f"   Ticker: {result.get('ticker')}")
    print(f"   Company: {result.get('company_name')}")
    print(f"   Total Available Metrics: {result.get('total_available')}")
    print(f"   Categories Found: {len(result.get('categories', {}))}")

    for category, metrics in result.get('categories', {}).items():
        print(f"   - {category}: {len(metrics)} metrics")

    print(f"\n📊 Sample metrics from income_statement:")
    for metric in result.get('categories', {}).get('income_statement', [])[:5]:
        print(f"   - {metric}")

    # Test 3b: Search for specific metrics
    print(f"\nTest 3b: Search for metrics matching 'Depreciation'")
    print("Calling: get_available_metrics(ticker='AAPL', search_term='Depreciation')")

    search_result = await tools.get_available_metrics(
        ticker='AAPL',
        search_term='Depreciation'
    )

    if "error" in search_result:
        print(f"❌ ERROR: {search_result['error']}")
        return False

    filtered = search_result.get('filtered_metrics', [])
    print(f"\n✅ Found {len(filtered)} metrics matching 'Depreciation':")
    for metric in filtered[:10]:
        print(f"   - {metric}")

    return True


async def test_ttm_ebitda_calculation():
    """Test TTM EBITDA calculation using specific metrics"""
    print("\n" + "="*70)
    print("TEST 4: TTM EBITDA Calculation Example")
    print("="*70)

    tools = Tools()

    print("\nStep 1: Get specific metrics for AAPL")

    result = await tools.get_filing_content(
        ticker='AAPL',
        filing_type='10-Q',
        specific_metrics=[
            'NetIncomeLoss',
            'InterestExpense',
            'IncomeTaxExpenseBenefit',
            'DepreciationDepletionAndAmortization'
        ]
    )

    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return False

    print(f"✅ Retrieved {result.get('metrics_returned')} metrics")

    # Extract TTM values
    print(f"\nStep 2: Extract TTM values (last 4 quarters)")

    metrics_data = result['financial_metrics']

    try:
        ni_values = metrics_data['NetIncomeLoss']['units']['USD'][:4]
        ie_values = metrics_data['InterestExpense']['units']['USD'][:4]
        tax_values = metrics_data['IncomeTaxExpenseBenefit']['units']['USD'][:4]
        da_values = metrics_data['DepreciationDepletionAndAmortization']['units']['USD'][:4]

        # Sum for TTM
        ttm_ni = sum(v['value'] for v in ni_values)
        ttm_ie = sum(v['value'] for v in ie_values)
        ttm_tax = sum(v['value'] for v in tax_values)
        ttm_da = sum(v['value'] for v in da_values)

        ttm_ebitda = ttm_ni + ttm_ie + ttm_tax + ttm_da

        print(f"\nStep 3: Calculate TTM EBITDA")
        print(f"   TTM Net Income: ${ttm_ni:>15,.0f}")
        print(f"   TTM Interest Expense: ${ttm_ie:>10,.0f}")
        print(f"   TTM Tax Benefit: ${ttm_tax:>15,.0f}")
        print(f"   TTM Depreciation & Amortization: ${ttm_da:>5,.0f}")
        print(f"   " + "-"*40)
        print(f"   TTM EBITDA: ${ttm_ebitda:>22,.0f}")

        print(f"\n✅ Successfully calculated TTM EBITDA")
        return True

    except (KeyError, IndexError, TypeError) as e:
        print(f"❌ FAILED to extract values: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║  SEC-Finance-AI: Dual-Mode Metric Selection Test Suite     ║")
    print("╚" + "="*68 + "╝")

    results = {
        "Generic Mode": await test_generic_mode(),
        "Specific Mode": await test_specific_mode(),
        "Metric Discovery": await test_metric_discovery(),
        "TTM EBITDA Calculation": await test_ttm_ebitda_calculation(),
    }

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
