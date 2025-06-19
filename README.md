# Extractos Parser

A Python tool for extracting transaction data from PDF bank statements (extractos) and converting them to CSV format.

## Features

- Extracts transaction data from PDF bank statements
- Parses transaction dates, descriptions, and amounts
- Calculates transaction amounts based on balance changes
- Exports data to CSV format for further analysis
- Handles Portuguese bank statement formats

## Requirements

- Python 3.x
- pandas
- pdfplumber

## Installation

1. Clone the repository:
```bash
git clone https://github.com/psousa50/extractos-parser.git
cd extractos-parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF bank statements in the `files/` directory
2. Run the script:
```bash
python extract_transactions_from_pdf.py
```

The script will process all PDF files in the `files/` directory and generate corresponding CSV files with the extracted transaction data.

## Output Format

The generated CSV files contain the following columns:
- **Date**: Transaction date (YYYY-MM-DD format)
- **Description**: Transaction description
- **Amount**: Transaction amount (positive for credits, negative for debits)

## File Structure

```
extractos-parser/
├── extract_transactions_from_pdf.py  # Main extraction script
├── requirements.txt                  # Python dependencies
├── files/                           # Directory for PDF files (ignored by git)
└── README.md                        # This file
```

## Notes

- The script is designed for Portuguese bank statement formats
- PDF files and generated CSV files in the `files/` directory are ignored by git
- Transaction amounts are calculated based on balance differences between consecutive transactions