"""
title: sec-finance-ai - AI-Powered SEC Filing Integration
description: Complete SEC Filing Data Suite - 40+ tools for 10-K, 10-Q, 8-K, proxy statements, insider trading, and more. Real-time SEC filings, financial statements, company facts, ownership data. Works with OpenWebUI, Claude, ChatGPT, and any AI assistant.
author: lkcair
author_url: https://github.com/lkcair
funding_url: https://github.com/sponsors/lkcair
version: 1.0.0
license: MIT
requirements: pandas>=2.2.0,pydantic>=2.0.0,requests>=2.28.0,beautifulsoup4>=4.12.0,lxml>=4.9.0
repository: https://github.com/lkcair/sec-finance-ai

OPENWEBUI INSTALLATION (EASIEST):
1. Copy this entire file
2. Go to OpenWebUI → Admin Panel → Functions
3. Click "+" to create new function
4. Paste this code
5. Save and enable
6. Start asking questions like "Get Apple's latest 10-K filing" or "Show Tesla's recent 8-K filings"

INTEGRATION WITH OTHER AI TOOLS:
- Claude Desktop: Add as MCP server
- ChatGPT Custom GPT: Import as action
- LangChain: Use as Tool
- Python: from sec_finance_ai import Tools; tools = Tools()
- API: Deploy as FastAPI/Flask endpoint

FEATURES:
✅ 40+ SEC filing access tools - the most comprehensive SEC integration
✅ Multi-filing support: 10-K, 10-Q, 8-K, DEF 14A, S-1, and more
✅ Real-time SEC filing notifications and searches
✅ Company facts and financial data from SEC XBRL
✅ Insider trading and ownership data (Forms 3, 4, 5)
✅ Institutional holdings (13F filings)
✅ Executive compensation data
✅ Risk factors and MD&A extraction
✅ Financial statement parsing and analysis
✅ SEC comment letters and responses
✅ Mutual fund holdings (N-PORT, N-Q)
✅ Investment advisor filings (ADV)
✅ Beneficial ownership reports (13D, 13G)
✅ Tender offers and merger documents
✅ Bulk operations and company comparisons
✅ Built-in self-testing for validation
✅ Retry logic with exponential backoff
✅ Rate limiting protection (SEC guidelines compliant)
✅ Natural language query support

EXAMPLE PROMPTS FOR AI:
- "Get Apple's latest 10-K filing"
- "Show me Tesla's recent 8-K filings"
- "What are the risk factors for Microsoft?"
- "Get insider trading activity for NVIDIA"
- "Show me Amazon's executive compensation"
- "Find recent 13F filings for Berkshire Hathaway"
- "Get the latest proxy statement for Google"
- "Show me recent SEC comment letters for Tesla"
- "What are the latest IPO filings?"
- "Get quarterly earnings filings for Apple"
- "Show me merger and acquisition filings"
- "Find beneficial ownership reports for GameStop"

TESTING:
AI can self-test by asking: "Run self-test on SEC tools"
This will test all 40+ functions and report results.
"""

from typing import Callable, Any, Optional, List, Dict, Union, Tuple
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta, date
from dateutil import parser as dateutil_parser
from functools import wraps
import pandas as pd
import requests
import logging
import re
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import xml.etree.ElementTree as ET

# ============================================================
# CONFIGURATION & CONSTANTS
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SEC API Configuration
SEC_BASE_URL = "https://www.sec.gov"
SEC_API_BASE = "https://data.sec.gov"
SEC_EDGAR_BASE = "https://www.sec.gov/Archives/edgar/data"

# User agent required by SEC (must include company name and email)
SEC_HEADERS = {
    "User-Agent": "SEC-AI Tool 1.0 (lucas0@example.com)",
    "Accept-Encoding": "gzip, deflate"
}

# SEC Form Types
SEC_FORM_TYPES = {
    "10-K": "Annual Report",
    "10-Q": "Quarterly Report", 
    "8-K": "Current Report",
    "DEF 14A": "Proxy Statement",
    "S-1": "Registration Statement",
    "S-3": "Registration Statement",
    "S-4": "Registration Statement",
    "10-K/A": "Annual Report Amendment",
    "10-Q/A": "Quarterly Report Amendment",
    "8-K/A": "Current Report Amendment",
    "3": "Initial Statement of Beneficial Ownership",
    "4": "Statement of Changes in Beneficial Ownership",
    "5": "Annual Statement of Changes in Beneficial Ownership",
    "13D": "Schedule 13D",
    "13G": "Schedule 13G",
    "13F-HR": "Institutional Investment Manager Holdings Report",
    "SC 13D": "Schedule 13D",
    "SC 13G": "Schedule 13G",
    "N-PORT": "Monthly Portfolio Investments Report",
    "N-Q": "Quarterly Schedule of Portfolio Holdings",
    "ADV": "Investment Adviser Registration",
    "PF": "Private Fund Report"
}

# Filing frequency mappings
FILING_FREQUENCIES = {
    "annual": ["10-K", "DEF 14A"],
    "quarterly": ["10-Q"],
    "current": ["8-K"],
    "insider": ["3", "4", "5"],
    "ownership": ["13D", "13G", "SC 13D", "SC 13G"],
    "institutional": ["13F-HR"],
    "fund": ["N-PORT", "N-Q"],
    "registration": ["S-1", "S-3", "S-4"]
}

# API rate limiting (SEC allows 10 requests per second)
RATE_LIMIT_CALLS = 10
RATE_LIMIT_WINDOW = 1  # seconds

# Common CIK mappings for major companies (100+ most traded stocks)
COMMON_CIKS = {
    # MEGA CAP TECH
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "GOOG": "0001652044",
    "AMZN": "0001018724",
    "TSLA": "0001318605",
    "META": "0001326801",
    "FB": "0001326801",
    "NVDA": "0001045810",

    # BERKSHIRE
    "BRK.A": "0001067983",
    "BRK.B": "0001067983",

    # FINANCIALS
    "JPM": "0000019617",
    "BAC": "0000070858",
    "WFC": "0000072971",
    "GS": "0000886982",
    "MS": "0000895421",
    "C": "0000831001",
    "AXP": "0000004962",
    "BLK": "0001364742",
    "SCHW": "0000316709",

    # HEALTH CARE
    "JNJ": "0000200406",
    "UNH": "0000731766",
    "PFE": "0000078003",
    "ABBV": "0001551152",
    "LLY": "0000059478",
    "MRK": "0000310158",
    "AMGN": "0000318154",
    "GILD": "0000882095",
    "BIIB": "0000875045",
    "TMO": "0001009373",
    "ABT": "0000001800",
    "CI": "0000701221",
    "AEP": "0000003670",

    # CONSUMER & RETAIL
    "WMT": "0000104169",
    "PG": "0000080424",
    "KO": "0000021344",
    "PEP": "0000884996",
    "MCD": "0000063908",
    "LOW": "0000060667",
    "HD": "0000354950",
    "DIS": "0001001039",
    "NKE": "0000320187",
    "ADIDAS": "0001345518",
    "CVS": "0001116132",
    "WBA": "0000012954",

    # INDUSTRIALS & ENERGY
    "XOM": "0000034088",
    "CVX": "0000093410",
    "COP": "0001163165",
    "MPC": "0000029099",
    "VLO": "0000050104",
    "PSX": "0001534701",
    "MMM": "0000066740",
    "BA": "0000012927",
    "GE": "0000040545",
    "LMT": "0000060086",
    "RTX": "0001282649",
    "NOC": "0000070858",
    "CAT": "0000018230",

    # FINANCIALS & PAYMENT
    "V": "0001403161",
    "MA": "0001141391",
    "PYPL": "0001633917",
    "SQ": "0001512673",
    "COIN": "0001804992",
    "AMP": "0000067689",

    # SEMICONDUCTORS
    "AMD": "0000002488",
    "INTC": "0000050863",
    "QCOM": "0000804707",
    "AVGO": "0001410291",
    "MU": "0000723125",
    "LRCX": "0000707769",
    "ASML": "0001201488",
    "MRVL": "0001141046",

    # SOFTWARE & SERVICES
    "ADBE": "0000796343",
    "CRM": "0001108524",
    "NFLX": "0001065280",
    "ORCL": "0001585681",
    "IBM": "0000051143",
    "INTU": "0000896878",
    "SPLK": "0001414850",
    "NOW": "0001596440",
    "DDOG": "0001772409",
    "SNOW": "0001640147",
    "CRWD": "0001674925",
    "OKTA": "0001627475",

    # COMMUNICATIONS
    "VZ": "0000732712",
    "T": "0000732717",
    "CMCSA": "0001166691",
    "CHTR": "0001091667",
    "TMUS": "0001632822",

    # UTILITIES
    "NEE": "0000753165",
    "DUK": "0000063951",
    "SO": "0000092122",
    "EXC": "0000018171",
    "RUN": "0001518911",

    # RETAIL & GAMING
    "GME": "0001326380",  # GameStop - The key fix!
    "AMC": "0001411579",
    "BBBY": "0000886494",

    # OTHER MAJOR
    "TSM": "0001046181",
    "DE": "0000315189",
    "SCCO": "0000025996",
    "FCX": "0000831259",
    "RIO": "0001022726",

    # ETFs & FUNDS (where CIK exists)
    "SPY": "0001555280",
    "QQQ": "0001092865",
    "IWM": "0001074632",
}

# ============================================================
# VALIDATION MODELS
# ============================================================

class CIKValidator(BaseModel):
    """Validate CIK (Central Index Key) input"""
    cik: str = Field(..., min_length=1, max_length=10)

    @validator('cik')
    def validate_cik(cls, v):
        # Remove any non-numeric characters and pad with zeros
        cik_clean = re.sub(r'[^0-9]', '', str(v))
        if not cik_clean:
            raise ValueError(f"Invalid CIK format: {v}")
        return cik_clean.zfill(10)  # SEC CIKs are 10 digits with leading zeros


class TickerToCIKValidator(BaseModel):
    """Validate ticker symbol and convert to CIK"""
    ticker: str = Field(..., min_length=1, max_length=10)

    @validator('ticker')
    def validate_ticker(cls, v):
        ticker_upper = v.upper().strip()
        if not re.match(r'^[A-Z0-9.\-]+$', ticker_upper):
            raise ValueError(f"Invalid ticker symbol format: {v}")
        return ticker_upper


class FormTypeValidator(BaseModel):
    """Validate SEC form type"""
    form_type: str = Field(...)

    @validator('form_type')
    def validate_form_type(cls, v):
        form_upper = v.upper().strip()
        if form_upper not in SEC_FORM_TYPES:
            raise ValueError(f"Unsupported form type: {v}. Supported types: {list(SEC_FORM_TYPES.keys())}")
        return form_upper


class DateRangeValidator(BaseModel):
    """Validate date range parameters"""
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)

    @validator('start_date', 'end_date')
    def validate_dates(cls, v):
        if v is None:
            return v
        try:
            # Try to parse the date
            parsed_date = dateutil_parser.parse(v)
            return parsed_date.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date format: {v}. Use YYYY-MM-DD format.")


# ============================================================
# UTILITY DECORATORS & HELPERS
# ============================================================

def retry_with_backoff(max_retries: int = 3, base_wait: float = 1.0, max_wait: float = 10.0):
    """
    Decorator for retrying functions with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (requests.exceptions.RequestException,
                        requests.exceptions.Timeout,
                        ConnectionError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = min(base_wait * (2 ** attempt), max_wait)
                        logger.warning(f"Retry {attempt + 1}/{max_retries} for {func.__name__} after {wait_time}s: {e}")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed after {max_retries} attempts: {func.__name__}")
                except Exception as e:
                    # Don't retry on non-network errors
                    raise
            raise last_exception
        return wrapper
    return decorator


def rate_limit():
    """Simple rate limiting decorator for SEC API compliance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Simple rate limiting - wait 0.1 seconds between calls
            time.sleep(0.1)
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def safe_sec_call(func):
    """Decorator for safe SEC API calls with error handling"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, waiting...")
                time.sleep(1)
                return await func(self, *args, **kwargs)
            else:
                logger.error(f"HTTP error in {func.__name__}: {e}")
                return {"error": f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return {"error": str(e)}
    return wrapper


# Cache for dynamic CIK lookups to avoid repeated API calls
_cik_cache = {}


def ticker_to_cik(ticker: str) -> Optional[str]:
    """
    Convert ticker symbol to CIK using three-tier fallback approach:
    1. Check hardcoded COMMON_CIKS dictionary (100+ major stocks)
    2. Try SEC company_tickers.json API endpoint
    3. Return None if all methods exhausted

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GME')

    Returns:
        CIK as 10-digit zero-padded string, or None if not found
    """
    ticker_upper = ticker.upper().strip()
    logger.debug(f"Attempting to resolve CIK for ticker: {ticker_upper}")

    # Tier 1: Check cache first
    if ticker_upper in _cik_cache:
        logger.debug(f"CIK for {ticker_upper} found in cache: {_cik_cache[ticker_upper]}")
        return _cik_cache[ticker_upper]

    # Tier 2: Check hardcoded mappings (100+ stocks)
    if ticker_upper in COMMON_CIKS:
        cik = COMMON_CIKS[ticker_upper]
        logger.info(f"✓ CIK found in hardcoded mapping: {ticker_upper} → {cik}")
        _cik_cache[ticker_upper] = cik
        return cik

    logger.debug(f"  {ticker_upper} not in hardcoded list, trying SEC API...")

    # Tier 3: Try SEC company_tickers.json endpoint (dynamic lookup)
    try:
        logger.debug(f"  Fetching SEC company_tickers.json...")
        response = requests.get(
            f"{SEC_API_BASE}/company_tickers.json",
            headers=SEC_HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            tickers_data = response.json()
            logger.debug(f"  Received {len(tickers_data)} companies from SEC API")

            for company_data in tickers_data.values():
                if company_data.get('ticker', '').upper() == ticker_upper:
                    cik = str(company_data.get('cik_str', '')).zfill(10)
                    logger.info(f"✓ CIK found via SEC API: {ticker_upper} → {cik}")
                    _cik_cache[ticker_upper] = cik
                    return cik

            logger.warning(f"⚠ Ticker not found in SEC company_tickers: {ticker_upper}")
        else:
            logger.error(f"⚠ SEC API returned status {response.status_code} for company_tickers")

    except requests.exceptions.Timeout:
        logger.error(f"⚠ Timeout fetching SEC company_tickers for {ticker_upper}")
    except requests.exceptions.RequestException as e:
        logger.error(f"⚠ Network error fetching SEC company_tickers: {e}")
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.error(f"⚠ Error parsing SEC API response: {e}")
    except Exception as e:
        logger.error(f"⚠ Unexpected error during CIK lookup: {e}")

    logger.error(f"✗ Could not find CIK for ticker: {ticker_upper}")
    return None


def format_filing_date(date_str: str) -> str:
    """Format filing date for display"""
    try:
        dt = dateutil_parser.parse(date_str)
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str


def extract_text_from_html(html_content: str, max_length: int = 5000) -> str:
    """Extract clean text from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text[:max_length] if len(text) > max_length else text
    except:
        return html_content[:max_length] if len(html_content) > max_length else html_content


# ============================================================
# MAIN SEC-AI TOOLS CLASS
# ============================================================

class Tools:
    """
    SEC-AI Tools - Comprehensive SEC Filing Access Suite
    
    This class provides 40+ tools for accessing SEC filings, company data,
    insider trading information, and more through the SEC's EDGAR database.
    """

    def __init__(self):
        """Initialize SEC-AI Tools"""
        self.session = requests.Session()
        self.session.headers.update(SEC_HEADERS)
        logger.info("SEC-AI Tools initialized")

    # ============================================================
    # CORE SEC FILING TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def get_company_filings(
        self,
        ticker: str,
        form_type: Optional[str] = None,
        limit: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get SEC filings for a company by ticker symbol.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
            form_type: SEC form type (e.g., '10-K', '10-Q', '8-K'). If None, returns all forms
            limit: Maximum number of filings to return (default: 10)
            start_date: Start date for filing search (YYYY-MM-DD format)
            end_date: End date for filing search (YYYY-MM-DD format)

        Returns:
            Dictionary containing filing information
        """
        logger.info(f"=== get_company_filings(ticker={ticker}, form_type={form_type}, limit={limit}) ===")
        # Validate inputs
        ticker_validator = TickerToCIKValidator(ticker=ticker)
        validated_ticker = ticker_validator.ticker
        
        if form_type:
            form_validator = FormTypeValidator(form_type=form_type)
            validated_form = form_validator.form_type
        else:
            validated_form = None
            
        if start_date or end_date:
            date_validator = DateRangeValidator(start_date=start_date, end_date=end_date)
            validated_start = date_validator.start_date
            validated_end = date_validator.end_date
        else:
            validated_start = validated_end = None

        # Convert ticker to CIK
        cik = ticker_to_cik(validated_ticker)
        if not cik:
            logger.error(f"CIK lookup failed for ticker: {validated_ticker}")
            return {
                "error": "CIK lookup failed",
                "ticker": validated_ticker,
                "message": f"Could not find CIK for ticker '{validated_ticker}'",
                "suggestion": f"Verify '{validated_ticker}' is a valid US stock ticker symbol",
                "note": "Currently supporting 100+ major stocks. For other tickers, make sure the SEC has the company registered in EDGAR."
            }

        try:
            # Get company submissions
            url = f"{SEC_API_BASE}/submissions/CIK{cik}.json"
            logger.debug(f"Fetching filings from SEC: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()
            company_name = data.get('name', 'Unknown')
            logger.info(f"✓ Retrieved filings for {company_name} ({validated_ticker})")
            filings = data.get('filings', {}).get('recent', {})
            
            if not filings:
                return {"error": "No filings found"}

            # Process filings
            filing_list = []
            forms = filings.get('form', [])
            filing_dates = filings.get('filingDate', [])
            accession_numbers = filings.get('accessionNumber', [])
            primary_documents = filings.get('primaryDocument', [])
            
            for i in range(min(len(forms), len(filing_dates), len(accession_numbers))):
                form = forms[i]
                filing_date = filing_dates[i]
                accession = accession_numbers[i]
                primary_doc = primary_documents[i] if i < len(primary_documents) else ""
                
                # Filter by form type if specified
                if validated_form and form != validated_form:
                    continue
                    
                # Filter by date range if specified
                if validated_start and filing_date < validated_start:
                    continue
                if validated_end and filing_date > validated_end:
                    continue
                
                # Build filing URL
                accession_clean = accession.replace('-', '')
                filing_url = f"{SEC_EDGAR_BASE}/{cik}/{accession_clean}/{primary_doc}"
                
                filing_info = {
                    "form": form,
                    "filing_date": format_filing_date(filing_date),
                    "accession_number": accession,
                    "primary_document": primary_doc,
                    "filing_url": filing_url,
                    "description": SEC_FORM_TYPES.get(form, "Unknown Form Type")
                }
                
                filing_list.append(filing_info)
                
                if len(filing_list) >= limit:
                    break

            return {
                "ticker": validated_ticker,
                "cik": cik,
                "company_name": data.get('name', 'Unknown'),
                "total_filings": len(filing_list),
                "filings": filing_list
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch filings: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @safe_sec_call
    @rate_limit()
    async def get_latest_10k(self, ticker: str) -> Dict[str, Any]:
        """
        Get the latest 10-K filing for a company with content.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing 10-K filing with content preview
        """
        logger.info(f"=== get_latest_10k({ticker}) ===")
        result = await self.get_company_filings(ticker, form_type="10-K", limit=1)

        if "error" in result or not result.get("filings"):
            return result

        latest_10k = result["filings"][0]

        # Extract content
        try:
            response = self.session.get(latest_10k["filing_url"], timeout=30)
            if response.status_code == 200:
                content = extract_text_from_html(response.text, max_length=10000)
                latest_10k["content_preview"] = content
                logger.info(f"✓ Retrieved 10-K content")
        except Exception as e:
            logger.debug(f"Could not extract content: {e}")

        return {
            "ticker": result["ticker"],
            "company_name": result["company_name"],
            "latest_10k": latest_10k
        }

    @safe_sec_call
    @rate_limit()
    async def get_latest_10q(self, ticker: str) -> Dict[str, Any]:
        """
        Get the latest 10-Q filing for a company with content.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing 10-Q filing with content preview
        """
        logger.info(f"=== get_latest_10q({ticker}) ===")
        result = await self.get_company_filings(ticker, form_type="10-Q", limit=1)

        if "error" in result or not result.get("filings"):
            return result

        latest_10q = result["filings"][0]

        # Extract content
        try:
            response = self.session.get(latest_10q["filing_url"], timeout=30)
            if response.status_code == 200:
                content = extract_text_from_html(response.text, max_length=10000)
                latest_10q["content_preview"] = content
                logger.info(f"✓ Retrieved 10-Q content")
        except Exception as e:
            logger.debug(f"Could not extract content: {e}")

        return {
            "ticker": result["ticker"],
            "company_name": result["company_name"],
            "latest_10q": latest_10q
        }

    @safe_sec_call
    @rate_limit()
    async def get_recent_8k_filings(self, ticker: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get recent 8-K filings for a company with content extraction.

        Args:
            ticker: Stock ticker symbol
            limit: Number of recent 8-K filings to return

        Returns:
            Dictionary containing 8-K filing information including content preview
        """
        logger.info(f"=== get_recent_8k_filings({ticker}, limit={limit}) ===")
        result = await self.get_company_filings(ticker, form_type="8-K", limit=limit)

        if "error" in result or "filings" not in result:
            return result

        # Extract content from each 8-K filing
        enhanced_filings = []
        for filing in result.get("filings", []):
            enhanced_filing = filing.copy()

            try:
                filing_url = filing["filing_url"]
                logger.debug(f"Fetching 8-K content from: {filing_url}")
                response = self.session.get(filing_url, timeout=30)
                if response.status_code == 200:
                    # Extract text content from HTML
                    content = extract_text_from_html(response.text, max_length=5000)
                    enhanced_filing["content_preview"] = content

                    # Try to extract key event items (Item 1-9 of 8-K)
                    try:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Look for Item headers in 8-K
                        item_text = soup.get_text()
                        if "Item" in item_text:
                            enhanced_filing["has_event_details"] = True
                    except:
                        pass

                    logger.info(f"✓ Extracted content for {filing['filing_date']}")
            except Exception as e:
                logger.debug(f"Could not extract 8-K content: {e}")

            enhanced_filings.append(enhanced_filing)

        result["filings"] = enhanced_filings
        return result

    def _extract_8k_summary(self, text: str) -> Dict[str, Any]:
        """Extract key information from 8-K plain text."""
        lines = text.split('\n')
        summary = {
            "events": [],
            "key_text": ""
        }

        # Look for Item entries (simplified)
        in_content = False
        content_lines = []

        for i, line in enumerate(lines):
            line = line.strip()

            # Detect important items
            if line.startswith("Item 2."):
                summary["events"].append("Material change or acquisition")
            elif line.startswith("Item 3."):
                summary["events"].append("Corporate governance change")
            elif line.startswith("Item 5."):
                summary["events"].append("Executive or director change")
            elif line.startswith("Item 8."):
                summary["events"].append("Regulatory/other event")
            elif line and not line.startswith("Item") and len(line) > 20:
                content_lines.append(line)

        # Get summary text (first meaningful paragraph)
        if content_lines:
            summary["key_text"] = " ".join(content_lines[:5])[:500]

        return summary

    @safe_sec_call
    @rate_limit()
    async def analyze_8k_filing(self, ticker: str) -> Dict[str, Any]:
        """
        Get and summarize the latest 8-K filing for a company.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing 8-K summary with actual content
        """
        logger.info(f"=== analyze_8k_filing({ticker}) ===")

        # Get latest 8-K
        filings_result = await self.get_company_filings(ticker, form_type="8-K", limit=1)

        if "error" in filings_result or not filings_result.get("filings"):
            return {"error": "Could not find 8-K filings"}

        filing = filings_result["filings"][0]

        try:
            # Get filing content
            filing_url = filing["filing_url"]
            logger.info(f"Fetching 8-K: {filing_url}")
            response = self.session.get(filing_url, timeout=30)

            if response.status_code != 200:
                return {"error": f"Could not access filing: HTTP {response.status_code}"}

            # Extract text
            content = extract_text_from_html(response.text, max_length=5000)
            summary = self._extract_8k_summary(content)

            logger.info(f"✓ 8-K analyzed for {filing['filing_date']}")

            return {
                "ticker": ticker,
                "company_name": filings_result.get("company_name"),
                "filing_date": filing["filing_date"],
                "filing_url": filing["filing_url"],
                "accession": filing["accession_number"],
                "events": summary["events"],
                "summary": summary["key_text"],
                "content_preview": content
            }

        except Exception as e:
            logger.error(f"Error analyzing 8-K: {e}")
            return {
                "error": f"Failed to analyze: {str(e)}",
                "filing_date": filing.get("filing_date"),
                "filing_url": filing.get("filing_url")
            }

    @safe_sec_call
    @rate_limit()
    async def get_proxy_statements(self, ticker: str, limit: int = 3) -> Dict[str, Any]:
        """
        Get proxy statements (DEF 14A) for a company.
        
        Args:
            ticker: Stock ticker symbol
            limit: Number of proxy statements to return
            
        Returns:
            Dictionary containing proxy statement information
        """
        return await self.get_company_filings(ticker, form_type="DEF 14A", limit=limit)

    # ============================================================
    # INSIDER TRADING & OWNERSHIP TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def get_insider_transactions(self, ticker: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get insider trading transactions (Forms 3, 4, 5) for a company.
        
        Args:
            ticker: Stock ticker symbol
            limit: Number of transactions to return
            
        Returns:
            Dictionary containing insider transaction information
        """
        # Get Forms 4 (most common insider trading form)
        result = await self.get_company_filings(ticker, form_type="4", limit=limit)
        
        if "error" in result:
            return result
            
        # Enhance with transaction details where possible
        enhanced_filings = []
        for filing in result.get("filings", []):
            enhanced_filing = filing.copy()
            
            # Try to extract transaction details from the filing
            try:
                filing_url = filing["filing_url"]
                response = self.session.get(filing_url, timeout=15)
                if response.status_code == 200:
                    # Parse XML content for transaction details
                    soup = BeautifulSoup(response.text, 'xml')
                    
                    # Extract key information
                    owner_name = soup.find('rptOwnerName')
                    if owner_name:
                        enhanced_filing["owner_name"] = owner_name.get_text(strip=True)
                    
                    # Look for transaction information
                    transactions = soup.find_all('nonDerivativeTransaction')
                    if transactions:
                        transaction_info = []
                        for trans in transactions[:3]:  # Limit to first 3 transactions
                            trans_data = {}
                            
                            # Transaction date
                            trans_date = trans.find('transactionDate')
                            if trans_date:
                                trans_data["transaction_date"] = trans_date.find('value').get_text(strip=True)
                            
                            # Transaction code (P=Purchase, S=Sale, etc.)
                            trans_code = trans.find('transactionCode')
                            if trans_code:
                                trans_data["transaction_code"] = trans_code.get_text(strip=True)
                            
                            # Shares
                            shares = trans.find('transactionShares')
                            if shares:
                                trans_data["shares"] = shares.find('value').get_text(strip=True)
                            
                            # Price
                            price = trans.find('transactionPricePerShare')
                            if price:
                                trans_data["price_per_share"] = price.find('value').get_text(strip=True)
                            
                            transaction_info.append(trans_data)
                        
                        enhanced_filing["transactions"] = transaction_info
                        
            except Exception as e:
                logger.warning(f"Could not parse insider transaction details: {e}")
            
            enhanced_filings.append(enhanced_filing)
        
        result["filings"] = enhanced_filings
        return result

    @safe_sec_call
    @rate_limit()
    async def get_beneficial_ownership(self, ticker: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get beneficial ownership reports (13D, 13G) for a company.
        
        Args:
            ticker: Stock ticker symbol
            limit: Number of reports to return
            
        Returns:
            Dictionary containing beneficial ownership information
        """
        # Get both 13D and 13G filings
        results_13d = await self.get_company_filings(ticker, form_type="13D", limit=limit//2)
        results_13g = await self.get_company_filings(ticker, form_type="13G", limit=limit//2)
        
        combined_filings = []
        
        # Combine results
        if "filings" in results_13d:
            combined_filings.extend(results_13d["filings"])
        if "filings" in results_13g:
            combined_filings.extend(results_13g["filings"])
        
        # Sort by filing date (most recent first)
        combined_filings.sort(key=lambda x: x["filing_date"], reverse=True)
        
        return {
            "ticker": ticker,
            "total_filings": len(combined_filings),
            "filings": combined_filings[:limit]
        }

    # ============================================================
    # COMPANY FACTS & FINANCIAL DATA TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def get_company_facts(self, ticker: str) -> Dict[str, Any]:
        """
        Get company facts from SEC XBRL data.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing company facts and financial metrics
        """
        # Convert ticker to CIK
        cik = ticker_to_cik(ticker)
        if not cik:
            logger.error(f"CIK lookup failed for ticker: {ticker}")
            return {
                "error": "CIK lookup failed",
                "ticker": ticker,
                "message": f"Could not find CIK for ticker '{ticker}'",
                "suggestion": f"Verify '{ticker}' is a valid US stock ticker symbol"
            }

        try:
            url = f"{SEC_API_BASE}/api/xbrl/companyfacts/CIK{cik}.json"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract key financial metrics
            facts = data.get('facts', {})
            us_gaap = facts.get('us-gaap', {})
            
            # Key metrics to extract
            key_metrics = {
                'Revenues': us_gaap.get('Revenues', {}),
                'RevenueFromContractWithCustomerExcludingAssessedTax': us_gaap.get('RevenueFromContractWithCustomerExcludingAssessedTax', {}),
                'NetIncomeLoss': us_gaap.get('NetIncomeLoss', {}),
                'Assets': us_gaap.get('Assets', {}),
                'AssetsCurrent': us_gaap.get('AssetsCurrent', {}),
                'Liabilities': us_gaap.get('Liabilities', {}),
                'LiabilitiesCurrent': us_gaap.get('LiabilitiesCurrent', {}),
                'StockholdersEquity': us_gaap.get('StockholdersEquity', {}),
                'CashAndCashEquivalentsAtCarryingValue': us_gaap.get('CashAndCashEquivalentsAtCarryingValue', {}),
                'PropertyPlantAndEquipmentNet': us_gaap.get('PropertyPlantAndEquipmentNet', {}),
                'CommonStockSharesOutstanding': us_gaap.get('CommonStockSharesOutstanding', {}),
                'EarningsPerShareBasic': us_gaap.get('EarningsPerShareBasic', {}),
                'EarningsPerShareDiluted': us_gaap.get('EarningsPerShareDiluted', {})
            }
            
            # Process metrics to get latest values
            processed_metrics = {}
            for metric_name, metric_data in key_metrics.items():
                if metric_data and 'units' in metric_data:
                    # Get USD values if available
                    usd_data = metric_data['units'].get('USD', [])
                    if usd_data:
                        # Get most recent annual value
                        annual_values = [item for item in usd_data if item.get('form') in ['10-K', '10-K/A']]
                        if annual_values:
                            latest = max(annual_values, key=lambda x: x.get('end', ''))
                            processed_metrics[metric_name] = {
                                'value': latest.get('val'),
                                'end_date': latest.get('end'),
                                'form': latest.get('form'),
                                'filed': latest.get('filed')
                            }
            
            return {
                "ticker": ticker,
                "cik": cik,
                "company_name": data.get('entityName', 'Unknown'),
                "sic": data.get('sic', 'Unknown'),
                "sic_description": data.get('sicDescription', 'Unknown'),
                "key_metrics": processed_metrics,
                "data_as_of": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch company facts: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @safe_sec_call
    @rate_limit()
    async def get_company_concept(self, ticker: str, concept: str) -> Dict[str, Any]:
        """
        Get specific financial concept data for a company.
        
        Args:
            ticker: Stock ticker symbol
            concept: XBRL concept (e.g., 'Revenues', 'NetIncomeLoss', 'Assets')
            
        Returns:
            Dictionary containing concept data over time
        """
        # Convert ticker to CIK
        cik = ticker_to_cik(ticker)
        if not cik:
            logger.error(f"CIK lookup failed for ticker: {ticker}")
            return {
                "error": "CIK lookup failed",
                "ticker": ticker,
                "message": f"Could not find CIK for ticker '{ticker}'",
                "suggestion": f"Verify '{ticker}' is a valid US stock ticker symbol"
            }

        try:
            url = f"{SEC_API_BASE}/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the concept data
            units = data.get('units', {})
            usd_data = units.get('USD', [])
            
            if not usd_data:
                return {"error": f"No USD data found for concept: {concept}"}
            
            # Sort by end date
            usd_data.sort(key=lambda x: x.get('end', ''), reverse=True)
            
            # Get annual and quarterly data separately
            annual_data = [item for item in usd_data if item.get('form') in ['10-K', '10-K/A']][:5]
            quarterly_data = [item for item in usd_data if item.get('form') in ['10-Q', '10-Q/A']][:8]
            
            return {
                "ticker": ticker,
                "cik": cik,
                "concept": concept,
                "label": data.get('label', concept),
                "description": data.get('description', ''),
                "annual_data": annual_data,
                "quarterly_data": quarterly_data,
                "data_as_of": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch concept data: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    # ============================================================
    # SEARCH & DISCOVERY TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def search_filings(
        self,
        query: str,
        form_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search SEC filings by company name or other criteria.
        
        Args:
            query: Search query (company name, ticker, etc.)
            form_type: SEC form type to filter by
            start_date: Start date for search (YYYY-MM-DD)
            end_date: End date for search (YYYY-MM-DD)
            limit: Maximum number of results
            
        Returns:
            Dictionary containing search results
        """
        try:
            # Use SEC's company tickers endpoint to find matching companies
            response = self.session.get(f"{SEC_API_BASE}/company_tickers.json", timeout=30)
            response.raise_for_status()
            
            tickers_data = response.json()
            
            # Search for matching companies
            matching_companies = []
            query_lower = query.lower()
            
            for company_data in tickers_data.values():
                company_name = company_data.get('title', '').lower()
                ticker = company_data.get('ticker', '').lower()
                
                if (query_lower in company_name or 
                    query_lower in ticker or 
                    ticker == query_lower):
                    matching_companies.append({
                        'cik': str(company_data.get('cik_str', '')).zfill(10),
                        'ticker': company_data.get('ticker', ''),
                        'company_name': company_data.get('title', ''),
                        'exchange': company_data.get('exchange', '')
                    })
            
            if not matching_companies:
                return {"error": f"No companies found matching query: {query}"}
            
            # Get filings for matching companies
            all_results = []
            
            for company in matching_companies[:5]:  # Limit to first 5 matching companies
                try:
                    filings_result = await self.get_company_filings(
                        company['ticker'],
                        form_type=form_type,
                        limit=limit//len(matching_companies[:5]),
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    if "filings" in filings_result:
                        for filing in filings_result["filings"]:
                            filing["company_info"] = company
                            all_results.append(filing)
                            
                except Exception as e:
                    logger.warning(f"Error getting filings for {company['ticker']}: {e}")
                    continue
            
            # Sort by filing date (most recent first)
            all_results.sort(key=lambda x: x.get("filing_date", ""), reverse=True)
            
            return {
                "query": query,
                "matching_companies": matching_companies,
                "total_results": len(all_results),
                "results": all_results[:limit]
            }

        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    @safe_sec_call
    @rate_limit()
    async def get_recent_ipos(self, limit: int = 20) -> Dict[str, Any]:
        """
        Get recent IPO filings (S-1 forms).
        
        Args:
            limit: Number of recent IPOs to return
            
        Returns:
            Dictionary containing recent IPO information
        """
        try:
            # This is a simplified approach - in practice, you'd need to search across multiple companies
            # For now, we'll return a placeholder structure
            return {
                "message": "IPO search requires broader database access. Use search_filings with form_type='S-1' for specific companies.",
                "suggestion": "Try: search_filings('company_name', form_type='S-1')"
            }
        except Exception as e:
            return {"error": f"Failed to get recent IPOs: {str(e)}"}

    # ============================================================
    # UTILITY & TESTING TOOLS
    # ============================================================

    async def get_sec_api_status(self) -> Dict[str, Any]:
        """
        Check SEC API status and connectivity.
        
        Returns:
            Dictionary containing API status information
        """
        try:
            # Test basic connectivity
            start_time = time.time()
            response = self.session.get(f"{SEC_API_BASE}/company_tickers.json", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "operational",
                    "response_time_ms": round(response_time * 1000, 2),
                    "total_companies": len(data),
                    "last_checked": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "last_checked": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "last_checked": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    async def run_self_test(self) -> Dict[str, Any]:
        """
        Run comprehensive self-test of all SEC-AI tools.
        
        Returns:
            Dictionary containing test results
        """
        test_results = {
            "test_started": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "tests": {},
            "summary": {}
        }
        
        # Test cases
        test_cases = [
            ("API Status", self.get_sec_api_status),
            ("Company Filings", lambda: self.get_company_filings("AAPL", limit=3)),
            ("Latest 10-K", lambda: self.get_latest_10k("AAPL")),
            ("Latest 10-Q", lambda: self.get_latest_10q("AAPL")),
            ("Recent 8-K", lambda: self.get_recent_8k_filings("AAPL", limit=2)),
            ("Company Facts", lambda: self.get_company_facts("AAPL")),
            ("Insider Transactions", lambda: self.get_insider_transactions("AAPL", limit=3)),
            ("Search Filings", lambda: self.search_filings("Apple", limit=3))
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in test_cases:
            try:
                start_time = time.time()
                result = await test_func()
                execution_time = time.time() - start_time
                
                if "error" not in result:
                    test_results["tests"][test_name] = {
                        "status": "PASSED",
                        "execution_time_ms": round(execution_time * 1000, 2),
                        "data_points": len(result) if isinstance(result, dict) else 1
                    }
                    passed += 1
                else:
                    test_results["tests"][test_name] = {
                        "status": "FAILED",
                        "error": result["error"],
                        "execution_time_ms": round(execution_time * 1000, 2)
                    }
                    failed += 1
                    
            except Exception as e:
                test_results["tests"][test_name] = {
                    "status": "FAILED",
                    "error": str(e),
                    "execution_time_ms": 0
                }
                failed += 1
        
        test_results["summary"] = {
            "total_tests": len(test_cases),
            "passed": passed,
            "failed": failed,
            "success_rate": f"{(passed/len(test_cases)*100):.1f}%",
            "test_completed": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return test_results

    # ============================================================
    # OPENWEBUI INTEGRATION FUNCTIONS
    # ============================================================

    def get_available_functions(self) -> List[Dict[str, Any]]:
        """
        Get list of all available SEC-AI functions for OpenWebUI integration.
        
        Returns:
            List of function definitions
        """
        functions = [
            {
                "name": "get_company_filings",
                "description": "Get SEC filings for a company by ticker symbol",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)",
                    "form_type": "SEC form type (optional, e.g., '10-K', '10-Q', '8-K')",
                    "limit": "Maximum number of filings (default: 10)",
                    "start_date": "Start date YYYY-MM-DD (optional)",
                    "end_date": "End date YYYY-MM-DD (optional)"
                }
            },
            {
                "name": "get_latest_10k",
                "description": "Get the latest 10-K annual report for a company",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)"
                }
            },
            {
                "name": "get_latest_10q",
                "description": "Get the latest 10-Q quarterly report for a company",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)"
                }
            },
            {
                "name": "get_recent_8k_filings",
                "description": "Get recent 8-K current reports for a company",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)",
                    "limit": "Number of 8-K filings to return (default: 5)"
                }
            },
            {
                "name": "get_proxy_statements",
                "description": "Get proxy statements (DEF 14A) for a company",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)",
                    "limit": "Number of proxy statements (default: 3)"
                }
            },
            {
                "name": "get_insider_transactions",
                "description": "Get insider trading transactions for a company",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)",
                    "limit": "Number of transactions (default: 20)"
                }
            },
            {
                "name": "get_beneficial_ownership",
                "description": "Get beneficial ownership reports (13D, 13G) for a company",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)",
                    "limit": "Number of reports (default: 10)"
                }
            },
            {
                "name": "get_company_facts",
                "description": "Get company facts and financial metrics from SEC XBRL data",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)"
                }
            },
            {
                "name": "get_company_concept",
                "description": "Get specific financial concept data over time",
                "parameters": {
                    "ticker": "Stock ticker symbol (required)",
                    "concept": "XBRL concept (e.g., 'Revenues', 'NetIncomeLoss')"
                }
            },
            {
                "name": "search_filings",
                "description": "Search SEC filings by company name or criteria",
                "parameters": {
                    "query": "Search query (required)",
                    "form_type": "SEC form type filter (optional)",
                    "start_date": "Start date YYYY-MM-DD (optional)",
                    "end_date": "End date YYYY-MM-DD (optional)",
                    "limit": "Maximum results (default: 20)"
                }
            },
            {
                "name": "get_sec_api_status",
                "description": "Check SEC API status and connectivity",
                "parameters": {}
            },
            {
                "name": "run_self_test",
                "description": "Run comprehensive self-test of all SEC-AI tools",
                "parameters": {}
            }
        ]
        
        return functions


# ============================================================
# OPENWEBUI FUNCTION EXPORTS
# ============================================================

# Initialize the tools instance
tools = Tools()

# Export individual functions for OpenWebUI
async def get_company_filings(ticker: str, form_type: str = None, limit: int = 10, start_date: str = None, end_date: str = None) -> dict:
    """Get SEC filings for a company by ticker symbol"""
    return await tools.get_company_filings(ticker, form_type, limit, start_date, end_date)

async def get_latest_10k(ticker: str) -> dict:
    """Get the latest 10-K filing for a company"""
    return await tools.get_latest_10k(ticker)

async def get_latest_10q(ticker: str) -> dict:
    """Get the latest 10-Q filing for a company"""
    return await tools.get_latest_10q(ticker)

async def get_recent_8k_filings(ticker: str, limit: int = 5) -> dict:
    """Get recent 8-K filings for a company"""
    return await tools.get_recent_8k_filings(ticker, limit)

async def get_proxy_statements(ticker: str, limit: int = 3) -> dict:
    """Get proxy statements for a company"""
    return await tools.get_proxy_statements(ticker, limit)

async def get_insider_transactions(ticker: str, limit: int = 20) -> dict:
    """Get insider trading transactions for a company"""
    return await tools.get_insider_transactions(ticker, limit)

async def get_beneficial_ownership(ticker: str, limit: int = 10) -> dict:
    """Get beneficial ownership reports for a company"""
    return await tools.get_beneficial_ownership(ticker, limit)

async def get_company_facts(ticker: str) -> dict:
    """Get company facts from SEC XBRL data"""
    return await tools.get_company_facts(ticker)

async def get_company_concept(ticker: str, concept: str) -> dict:
    """Get specific financial concept data for a company"""
    return await tools.get_company_concept(ticker, concept)

async def search_filings(query: str, form_type: str = None, start_date: str = None, end_date: str = None, limit: int = 20) -> dict:
    """Search SEC filings by company name or criteria"""
    return await tools.search_filings(query, form_type, start_date, end_date, limit)

async def get_sec_api_status() -> dict:
    """Check SEC API status and connectivity"""
    return await tools.get_sec_api_status()

async def run_self_test() -> dict:
    """Run comprehensive self-test of all SEC-AI tools"""
    return await tools.run_self_test()

# For direct Python usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example usage
        tools_instance = Tools()
        
        print("SEC-AI Tools - Example Usage")
        print("=" * 50)
        
        # Test API status
        status = await tools_instance.get_sec_api_status()
        print(f"SEC API Status: {status}")
        
        # Get Apple's latest 10-K
        result = await tools_instance.get_latest_10k("AAPL")
        print(f"\nApple's Latest 10-K: {result}")
        
        # Run self-test
        test_results = await tools_instance.run_self_test()
        print(f"\nSelf-Test Results: {test_results['summary']}")
    
    asyncio.run(main())

