
import os
import re
from datetime import datetime
import pdfplumber
import pandas as pd

def to_float(val): return float(val.replace(" ", "")) if val else None

def extract_transactions_from_pdf(pdf_path):
    transactions = []
    previous_balance= None
    current_year = None

    transaction_regex = re.compile(
        r"(?P<date>\d{1,2}\.\d{2})\s+\d{1,2}\.\d{2}\s+(?P<description>.+?)\s+(?P<amount>\d{1,3}(?: \d{3})*\.\d{2})\s+(?P<balance>\d{1,3}(?: \d{3})*\.\d{2})$"
    )
    header_regex = re.compile(r"EXTRATO DE (\d{4})/(\d{2})/\d{2}")
    initial_balance_regex = re.compile(
        r"SALDO INICIAL\s+(\d{1,3}(?: \d{3})*\.\d{2})"
    )    

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")

            for line in lines:
                match = initial_balance_regex.search(text)
                if match:
                    previous_balance = float(match.group(1).replace(" ", ""))

                # Update current year/month
                header_match = header_regex.search(line)
                if header_match:
                    current_year = int(header_match.group(1))
                    continue

                # Parse transaction line
                match = transaction_regex.search(line)
                if match and current_year is not None and previous_balance is not None:
                    try:
                        date = match.group("date").split(".")
                        month = int(date[0])
                        day = int(date[1])
                        date = datetime(current_year, month, day).strftime("%Y-%m-%d")
                        desc = match.group("description").strip()
                        balance = to_float(match.group("balance"))
                        amount = balance - previous_balance
                        amount = round(amount, 2)
                        previous_balance = balance

                        transactions.append((date, desc, amount))
                    except ValueError as e:
                        print(f"Error parsing date or amount: {e} in line: {line}")
                        continue  # skip invalid dates

    return pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])

def export_transactions_to_csv(pdf_path, output_path):
    transactions_df = extract_transactions_from_pdf(pdf_path)
    transactions_df.to_csv(output_path, index=False)
    print(f"Exported to {output_path}")

def export_lines_to_csv(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_path, "w", encoding="utf-8") as f:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    f.write(text + "\n")
    print(f"Exported lines to {output_path}")

pdf_files = [f for f in os.listdir('files') if f.endswith('.pdf')]
for pdf_path in pdf_files:
    print(f"Processing {pdf_path}...")
    export_transactions_to_csv(pdf_path, f"{pdf_path}_transactions.csv")
    # export_lines_to_csv(pdf_path, f"{pdf_path}_lines.txt")