# Translation Converter

This project contains two Python scripts to convert between JSON translation files and an Excel spreadsheet for multilingual applications.

## Directory Structure
```
translation_converter/
├── scripts/
│   ├── json_to_excel.py        # Convert JSON files to Excel
│   └── excel_to_json.py        # Convert Excel to JSON files
├── input/
│   ├── en-US.json              # Input JSON translation files
│   ├── zh-CN.json
│   ├── zh-TW.json
│   ├── ko-KR.json
│   ├── ja-JP.json
│   └── translations.xlsx       # Input Excel file
├── output/
│   ├── translations.xlsx       # Output Excel file
│   └── translations/           # Output JSON files
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Prerequisites
- Python 3.6 or higher
- Required libraries:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
1. **Convert JSON to Excel**:
   - Place JSON translation files (e.g., `en-US.json`, `zh-CN.json`) in the `input/` directory.
   - Run:
     ```bash
     python scripts/json_to_excel.py
     ```
   - Output: `output/translations.xlsx`

2. **Convert Excel to JSON**:
   - Place the Excel file (`translations.xlsx`) in the `input/` directory.
   - Run:
     ```bash
     python scripts/excel_to_json.py
     ```
   - Output: JSON files in `output/translations/` (e.g., `en-US.json`, `zh-CN.json`)

## Notes
- Ensure all JSON files use UTF-8 encoding.
- The Excel file must have a `Key` column with translation keys (e.g., `common.i18n`) and columns for each language code.
- Empty cells in the Excel file are ignored in the JSON output.

## License
MIT License
