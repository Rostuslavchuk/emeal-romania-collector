# Job Scraper

A Python-based web scraper that collects job listings from company career websites.

## Features

- Extracts job listing URLs from career pages.
- Collects job details such as title, company, location, and job URL.
- Uses asynchronous requests for efficient data collection.
- Parses HTML using XPath.
- Validates extracted data with Pydantic.
- Stores results in JSON format.

## Tech Stack

- Python
- asyncio
- curl_cffi
- lxml
- XPath
- Pydantic

## Project Structure

```text
.
├── config/
├── fetcher/
├── parser/
├── storage/
├── utils/
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:

```bash
python -m  piplines.main_pipline -u "https://careers.nttdata.ro/sitemap.xml"
```

## Output

The scraper exports collected job listings to JSON.

Example:

```json
[
  {
    "CompanyName": "NTT DATA",
    "JobTitle": "Quality Assurance Engineer with German (Playwright)",
    "Country": "Romania",
    "City": "Cluj",
    "url": "https://careers.nttdata.ro/job/..."
  }
]
```

## License

This project is for educational purposes.
