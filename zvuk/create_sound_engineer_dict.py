#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript pro vytvoření řízeného slovníku zvukařů z CSV souboru.
Seskupuje varianty jmen a vytváří mapování na kanonické názvy.
"""

import csv
import re
from collections import defaultdict

def remove_diacritics(text):
    """Odstraní diakritiku z textu."""
    replacements = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i', 'ň': 'n',
        'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I', 'Ň': 'N',
        'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z',
        'ä': 'a', 'ö': 'o', 'ü': 'u', 'ß': 'ss',
        'Ä': 'A', 'Ö': 'O', 'Ü': 'U'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def normalize_name(name):
    """Normalizuje jméno pro porovnání - odstraní tituly, diakritiku, velikost písmen."""
    if not name or name.strip() in ['-', '', 'zvuk / sound (on box)']:
        return None
    
    # Odstranit uvozovky
    name = name.strip().strip('"').strip("'")
    
    # Odstranit tituly (ing., Ing., p., pí., stř., s., st.)
    name = re.sub(r'^(ing\.|Ing\.|p\.|pí\.|stř\.|s\.|st\.)\s*', '', name, flags=re.IGNORECASE)
    
    # Odstranit zkratky na začátku (J., M., K., atd.)
    name = re.sub(r'^[A-Z]\.\s*', '', name)
    
    # Odstranit mezery a normalizovat
    name = ' '.join(name.split())
    
    # Odstranit diakritiku a převést na malá písmena pro porovnání
    normalized = remove_diacritics(name).lower()
    
    return normalized

def extract_surname(name):
    """Extrahuje příjmení z jména."""
    if not name:
        return None
    
    # Odstranit tituly
    name = re.sub(r'^(ing\.|Ing\.|p\.|pí\.|stř\.|s\.|st\.)\s*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'^[A-Z]\.\s*', '', name)
    name = name.strip().strip('"').strip("'")
    
    # Rozdělit podle čárek, středníků, plusů (pro více osob)
    parts = re.split(r'[,;+\-–]', name)
    if parts:
        # Vzít první část
        first_part = parts[0].strip()
        # Rozdělit podle mezer a vzít poslední slovo (příjmení)
        words = first_part.split()
        if words:
            return words[-1]
    return None

def create_dictionary(input_file, output_file):
    """Vytvoří řízený slovník zvukařů."""
    
    # Načíst všechny záznamy
    all_names = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip() and row[0].strip() not in ['-', '', 'zvuk / sound (on box)']:
                all_names.append(row[0].strip())
    
    # Seskupit podle normalizovaného příjmení
    surname_groups = defaultdict(list)
    for name in all_names:
        surname = extract_surname(name)
        if surname:
            normalized_surname = remove_diacritics(surname).lower()
            surname_groups[normalized_surname].append(name)
    
    # Vytvořit mapování variant -> kanonický název
    variant_to_canonical = {}
    canonical_names = []
    
    for normalized_surname, variants in surname_groups.items():
        # Odstranit duplicity
        unique_variants = list(set(variants))
        
        # Pokud obsahuje čárku nebo středník, je to více osob - nechat jako samostatné
        multi_person = [v for v in unique_variants if ',' in v or ';' in v or '+' in v or '–' in v or '-' in v]
        single_person = [v for v in unique_variants if v not in multi_person]
        
        # Zpracovat jednotlivé osoby
        if single_person:
            # Vybrat kanonický název (nejdelší, s titulem pokud možno, bez zkratek, s diakritikou)
            def has_diacritics(text):
                """Zkontroluje, zda text obsahuje diakritiku."""
                return any(c in text for c in 'áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽäöüÄÖÜ')
            
            canonical = max(single_person, key=lambda x: (
                'Ing.' in x or 'ing.' in x,
                has_diacritics(x),  # Preferovat s diakritikou
                not re.match(r'^[A-Z]\.\s', x),  # Preferovat bez zkratek
                len(x),
                x.count(' ')
            ))
            
            canonical_names.append(canonical)
            
            # Vytvořit mapování pro všechny varianty jednotlivých osob
            for variant in single_person:
                variant_to_canonical[variant] = canonical
        
        # Zpracovat více osob (nechat jako samostatné záznamy)
        for multi in multi_person:
            canonical_names.append(multi)
            variant_to_canonical[multi] = multi
    
    # Seřadit kanonické názvy
    canonical_names.sort(key=lambda x: extract_surname(x) or '')
    
    # Zapsat výsledek
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Variant', 'Kanonický název'])
        
        # Zapsat všechny varianty s jejich kanonickými názvy
        for variant in sorted(set(all_names)):
            if variant and variant not in ['-', '', 'zvuk / sound (on box)']:
                canonical = variant_to_canonical.get(variant, variant)
                writer.writerow([variant, canonical])
    
    # Vytvořit také soubor pouze s kanonickými názvy
    canonical_file = output_file.replace('.csv', '_canonical_only.csv')
    with open(canonical_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Kanonický název'])
        for name in canonical_names:
            writer.writerow([name])
    
    print(f"Vytvořeno {len(canonical_names)} unikátních kanonických názvů")
    print(f"Zpracováno {len(set(all_names))} unikátních variant")
    print(f"Výstupní soubory:")
    print(f"  - {output_file} (mapování variant -> kanonický název)")
    print(f"  - {canonical_file} (pouze kanonické názvy)")

if __name__ == '__main__':
    input_file = 'zvukaři.csv'
    output_file = 'zvukaři_řízený_slovník.csv'
    create_dictionary(input_file, output_file)

