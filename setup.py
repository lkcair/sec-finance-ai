from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sec-ai",
    version="1.0.0",
    author="lucas0",
    author_email="lucas0@example.com",
    description="World's Best AI-Powered SEC Filing Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucas0/sec-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.2.0",
        "pydantic>=2.0.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "python-dateutil>=2.8.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0"
        ]
    }
)