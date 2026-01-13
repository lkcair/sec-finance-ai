FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY sec_ai.py .
COPY test_fixes.py .

# Run tests by default
CMD ["python3", "test_fixes.py"]
