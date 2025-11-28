#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript pro vytvoření mapování kanonických názvů na varianty z původního CSV.
"""

import csv
from collections import defaultdict

def create_mapping_to_original(original_file, dictionary_file, output_file):
    """Vytvoří mapování kanonických názvů na varianty z původního CSV."""
    
    # Načíst mapování variant -> kanonický název
    variant_to_canonical = {}
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant = row['Variant']
            canonical = row['Kanonický název']
            variant_to_canonical[variant] = canonical
    
    # Načíst původní CSV a seskupit varianty podle kanonických názvů
    canonical_to_variants = defaultdict(list)
    
    with open(original_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip() and row[0].strip() not in ['-', '', 'zvuk / sound (on box)']:
                original_variant = row[0].strip()
                # Najít kanonický název
                canonical = variant_to_canonical.get(original_variant, original_variant)
                canonical_to_variants[canonical].append(original_variant)
    
    # Odstranit duplicity v seznamech variant
    for canonical in canonical_to_variants:
        canonical_to_variants[canonical] = sorted(list(set(canonical_to_variants[canonical])))
    
    # Zapsat výsledek - kanonický název a všechny jeho varianty
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Kanonický název', 'Varianty (z původního CSV)'])
        
        # Seřadit podle kanonického názvu
        for canonical in sorted(canonical_to_variants.keys()):
            variants = canonical_to_variants[canonical]
            # Zapsat kanonický název a všechny varianty
            writer.writerow([canonical, '; '.join(variants)])
    
    # Vytvořit také soubor ve formátu původního CSV (každá varianta na řádku s kanonickým názvem)
    output_original_format = output_file.replace('.csv', '_original_format.csv')
    with open(output_original_format, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['zvuk / sound (on box)'])  # Hlavička jako v původním
        
        # Zapsat všechny varianty s jejich kanonickými názvy
        for canonical in sorted(canonical_to_variants.keys()):
            for variant in canonical_to_variants[canonical]:
                writer.writerow([variant])
    
    # Vytvořit také soubor s kanonickými názvy ve formátu původního CSV
    output_canonical_format = output_file.replace('.csv', '_canonical_format.csv')
    with open(output_canonical_format, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['zvuk / sound (on box)'])  # Hlavička jako v původním
        
        # Zapsat kanonické názvy (každý jednou)
        for canonical in sorted(canonical_to_variants.keys()):
            writer.writerow([canonical])
    
    print(f"Vytvořeno mapování pro {len(canonical_to_variants)} kanonických názvů")
    print(f"Výstupní soubory:")
    print(f"  - {output_file} (mapování kanonický název -> varianty)")
    print(f"  - {output_original_format} (všechny varianty ve formátu původního CSV)")
    print(f"  - {output_canonical_format} (kanonické názvy ve formátu původního CSV)")

if __name__ == '__main__':
    original_file = 'zvukaři.csv'
    dictionary_file = 'zvukaři_řízený_slovník.csv'
    output_file = 'zvukaři_mapping_na_původní.csv'
    create_mapping_to_original(original_file, dictionary_file, output_file)

