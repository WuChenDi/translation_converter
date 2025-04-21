import pandas as pd
import json
import os
import re
from typing import Dict, Any

def unflatten_dict(flat_dict: Dict[str, str], sep: str = '.') -> Dict[str, Any]:
    """
    Convert a flattened dictionary back to a nested dictionary.

    Args:
        flat_dict: Flattened dictionary with keys like 'common.i18n'.
        sep: Separator used in flattened keys (default: '.').

    Returns:
        Nested dictionary.
    """
    nested_dict = {}
    for key, value in flat_dict.items():
        if not value:  # Skip empty values
            continue
        parts = key.split(sep)
        current = nested_dict
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return nested_dict

def read_excel_to_translations(excel_file: str) -> Dict[str, Dict[str, str]]:
    """
    Read translations from an Excel file.

    Args:
        excel_file: Path to the Excel file.

    Returns:
        Dictionary mapping language codes to flattened translation dictionaries.
    """
    if not os.path.isfile(excel_file):
        raise FileNotFoundError(f"Excel file {excel_file} does not exist!")

    # Read Excel file
    try:
        df = pd.read_excel(excel_file, index_col='Key')
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {e}")

    # Extract language codes (columns) and translations
    translations = {}
    for lang_code in df.columns:
        # Create flattened dictionary for each language
        lang_dict = {key: str(value) for key, value in df[lang_code].items() if pd.notna(value)}
        translations[lang_code] = lang_dict

    return translations

def save_translations_to_json(translations: Dict[str, Dict[str, str]], output_dir: str):
    """
    Save translations as JSON files.

    Args:
        translations: Dictionary mapping language codes to flattened translation dictionaries.
        output_dir: Directory to save JSON files.
    """
    os.makedirs(output_dir, exist_ok=True)

    for lang_code in translations:
        # Validate language code
        if not re.match(r'^[a-z]{2}-[A-Z]{2}$', lang_code):
            print(f"Skipping invalid language code: {lang_code}")
            continue
        
        # Convert flattened dictionary to nested structure
        flat_dict = translations[lang_code]
        nested_dict = unflatten_dict(flat_dict)
        
        # Save to JSON file
        output_file = os.path.join(output_dir, f"{lang_code}.json")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(nested_dict, f, ensure_ascii=False, indent=2)
            print(f"Generated JSON file: {output_file}")
        except Exception as e:
            print(f"Failed to write {output_file}: {e}")

def main():
    """
    Main function to read translations from Excel and generate JSON files.
    """
    # Get project root directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(project_dir, 'input', 'translations.xlsx')
    output_dir = os.path.join(project_dir, 'output', 'translations')

    # Read translations from Excel
    try:
        translations = read_excel_to_translations(excel_file)
    except Exception as e:
        print(f"Error: {e}")
        return

    if not translations:
        print("No translations found in Excel file!")
        return

    # Save translations as JSON files
    save_translations_to_json(translations, output_dir)

if __name__ == '__main__':
    main()
