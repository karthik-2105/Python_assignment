
import os
import sys
import pandas as pd
from urllib.parse import urlparse, parse_qs

def xlsx_to_csvs(xlsx_path):
    """
    Converts all sheets in an XLSX file into individual CSV files.
    """
    # Create output folder (same name as file, without extension)
    base_name = os.path.splitext(os.path.basename(xlsx_path))[0]
    output_dir = os.path.join(os.getcwd(), base_name)
    os.makedirs(output_dir, exist_ok=True)

    # Read all sheets
    print(f"Reading {xlsx_path} ...")
    sheets = pd.read_excel(xlsx_path, sheet_name=None)  # returns dict: {sheet_name: DataFrame}

    print(f"Found {len(sheets)} sheets:")
    for sheet_name in sheets:
        print(f"  - {sheet_name}")

    # Export each sheet as CSV
    for sheet_name, df in sheets.items():
        csv_name = f"{sheet_name}.csv".replace("/", "_")  # avoid invalid file chars
        csv_path = os.path.join(output_dir, csv_name)
        df.to_csv(csv_path, index=False)
        print(f"Saved → {csv_path}")

    print(f"\nAll sheets converted successfully! Output directory: {output_dir}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python converter.py <excel_file.xlsx>")
        sys.exit(1)

    input_arg = sys.argv[1]

    if not os.path.exists(input_arg):
        print(f"File not found: {input_arg}")
        sys.exit(1)
    xlsx_to_csvs(input_arg)


if __name__ == "__main__":
    main()
