import json
import os
from typing import Dict, Any
import pandas as pd
from collections import defaultdict
import re

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, str]:
    """
    Flatten a nested dictionary, joining keys with a separator.

    Args:
        d: Nested dictionary to flatten.
        parent_key: Parent key for recursive calls (default: '').
        sep: Separator for joining keys (default: '.').

    Returns:
        Flattened dictionary with string values.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            value = str(v).strip('"')  # Remove extra quotes if any
            items.append((new_key, value))
    return dict(items)

def load_json_files(lang_dir: str, valid_langs: set = None) -> Dict[str, Dict[str, str]]:
    """
    Load all JSON translation files from a directory.

    Args:
        lang_dir: Directory containing JSON files.
        valid_langs: Set of valid language codes to load (optional).

    Returns:
        Dictionary mapping language codes to flattened translation dictionaries.
    """
    if not os.path.isdir(lang_dir):
        print(f"Directory {lang_dir} does not exist!")
        return {}

    translations = {}
    lang_pattern = re.compile(r'^[a-z]{2}-[A-Z]{2}\.json$')
    for file in os.listdir(lang_dir):
        if file.endswith('.json') and lang_pattern.match(file):
            lang_code = file.replace('.json', '')
            if valid_langs is None or lang_code in valid_langs:
                try:
                    with open(os.path.join(lang_dir, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        flattened = flatten_dict(data)
                        if not flattened:
                            print(f"Warning: {file} is empty or contains no valid translations")
                        translations[lang_code] = flattened
                except UnicodeDecodeError:
                    print(f"Encoding error in {file}: File must be UTF-8 encoded")
                except json.JSONDecodeError as e:
                    print(f"Error loading {file}: {e}")
    return translations

def create_excel(translations: Dict[str, Dict[str, str]], output_file: str, priority_lang: str = 'en-US'):
    """
    Create an Excel file from translation dictionaries.

    Args:
        translations: Dictionary mapping language codes to flattened translation dictionaries.
        output_file: Path to the output Excel file.
        priority_lang: Language code to prioritize in column order (default: 'en-US').
    """
    # Collect all unique translation keys
    all_keys = set()
    for lang_dict in translations.values():
        all_keys.update(lang_dict.keys())
    
    # Build data for DataFrame
    df_data = defaultdict(dict)
    for key in sorted(all_keys):
        for lang_code, lang_dict in translations.items():
            df_data[key][lang_code] = lang_dict.get(key, '')  # Use empty string for missing keys
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(df_data, orient='index')
    
    # Sort columns with priority language first
    cols = df.columns.tolist()
    if priority_lang in cols:
        cols.remove(priority_lang)
        cols = [priority_lang] + sorted(cols)
    else:
        cols = sorted(cols)
    df = df[cols]
    
    # Save to Excel
    try:
        df.to_excel(output_file, index=True, index_label='Key')
        print(f"Excel file created: {output_file}")
    except PermissionError:
        print(f"Permission denied when writing to {output_file}")
    except Exception as e:
        print(f"Failed to create Excel file: {e}")

def main():
    """
    Main function to load translation files and generate Excel output.
    """
    # Get project root directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(project_dir, 'input')
    output_file = os.path.join(project_dir, 'output', 'translations.xlsx')
    
    # Load translation files
    translations = load_json_files(input_dir)
    
    if not translations:
        print("No translation files found!")
        return
    
    # Generate Excel file
    create_excel(translations, output_file)

if __name__ == '__main__':
    main()
