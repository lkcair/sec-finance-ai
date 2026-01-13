#!/usr/bin/env python3
"""
Simple test script to verify sec-ai fixes work correctly
"""
import asyncio
import sys
from sec_ai import Tools

async def main():
    print("=" * 70)
    print("SEC-AI FIXES TEST SUITE")
    print("=" * 70)

    tools = Tools()

    # Test cases
    test_cases = [
        ("GME (was broken)", "GME", "8-K", 3),
        ("AAPL (common)", "AAPL", "8-K", 3),
        ("GOOGL (common)", "GOOGL", "8-K", 2),
        ("TSLA (common)", "TSLA", "10-K", 1),
    ]

    passed = 0
    failed = 0

    for test_name, ticker, form_type, limit in test_cases:
        try:
            print(f"\n{'─' * 70}")
            print(f"Test: {test_name} - get_recent_8k_filings({ticker}, limit={limit})")
            print(f"{'─' * 70}")

            result = await tools.get_recent_8k_filings(ticker, limit=limit)

            # Check for success
            if "error" in result:
                print(f"❌ FAILED - Error returned:")
                print(f"   {result}")
                failed += 1
            elif "filings" in result and len(result["filings"]) > 0:
                print(f"✅ PASSED")
                print(f"   Ticker: {result.get('ticker')}")
                print(f"   Company: {result.get('company_name')}")
                print(f"   Filings found: {result.get('total_filings')}")
                for i, filing in enumerate(result["filings"][:2], 1):
                    print(f"   [{i}] {filing['form']} - {filing['filing_date']}")
                passed += 1
            else:
                print(f"⚠️  PARTIAL - No filings returned")
                print(f"   Result: {result}")
                failed += 1

        except Exception as e:
            print(f"❌ FAILED - Exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Test invalid ticker
    print(f"\n{'─' * 70}")
    print(f"Test: Invalid ticker - get_recent_8k_filings(INVALID999)")
    print(f"{'─' * 70}")
    try:
        result = await tools.get_recent_8k_filings("INVALID999")
        if "error" in result:
            print(f"✅ PASSED - Error handling works")
            print(f"   Error: {result.get('message', result.get('error'))}")
            passed += 1
        else:
            print(f"❌ FAILED - Should have returned error for invalid ticker")
            print(f"   Result: {result}")
            failed += 1
    except Exception as e:
        print(f"❌ FAILED - Exception: {e}")
        failed += 1

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"TEST SUMMARY")
    print(f"{'=' * 70}")
    print(f"✅ Passed:  {passed}")
    print(f"❌ Failed:  {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print(f"{'=' * 70}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
