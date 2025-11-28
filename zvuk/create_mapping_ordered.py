#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript pro vytvoření mapování s původním pořadím.
Sloupec 1 = původní hodnoty v původním pořadí
Sloupec 2 = kanonický název (ontologie)
"""

import csv

def create_ordered_mapping(original_file, dictionary_file, output_file):
    """Vytvoří mapování s původním pořadím."""
    
    # Načíst mapování variant -> kanonický název
    variant_to_canonical = {}
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant = row['Variant']
            canonical = row['Kanonický název']
            variant_to_canonical[variant] = canonical
    
    # Načíst původní CSV v původním pořadí
    original_values = []
    with open(original_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():
                original_values.append(row[0].strip())
    
    # Vytvořit mapování s původním pořadím
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['zvuk / sound (on box)', 'Kanonický název'])
        
        for original_value in original_values:
            # Přeskočit hlavičku a prázdné hodnoty
            if original_value in ['zvuk / sound (on box)', '-', '']:
                continue
            
            # Najít kanonický název
            canonical = variant_to_canonical.get(original_value, original_value)
            writer.writerow([original_value, canonical])
    
    print(f"Vytvořeno mapování pro {len(original_values)} hodnot v původním pořadí")
    print(f"Výstupní soubor: {output_file}")

if __name__ == '__main__':
    original_file = 'zvukaři.csv'
    dictionary_file = 'zvukaři_řízený_slovník.csv'
    output_file = 'zvukaři_mapping_ordered.csv'
    create_ordered_mapping(original_file, dictionary_file, output_file)

