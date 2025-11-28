# Databáze zvukových materiálů českého filmu

Webová aplikace pro prohlížení a filtrování databáze zvukových materiálů.

## Jak zobrazit stránku

### Z GitLabu (raw soubory)

1. Otevři soubor `index.html` přímo z GitLabu:
   ```
   https://git.digilab.nfa.cz/jonas.kucharsky/databaze-zvukovych-materialu/-/raw/main/public/index.html
   ```

2. Nebo použij službu jako [raw.githack.com](https://raw.githack.com):
   ```
   https://raw.githack.com/git.digilab.nfa.cz/jonas.kucharsky/databaze-zvukovych-materialu/main/public/index.html
   ```

### Lokálně

1. Naklonuj repozitář:
   ```bash
   git clone https://git.digilab.nfa.cz/jonas.kucharsky/databaze-zvukovych-materialu.git
   cd databaze-zvukovych-materialu
   ```

2. Spusť lokální server (kvůli CORS):
   ```bash
   python3 -m http.server 8000
   ```

3. Otevři v prohlížeči:
   ```
   http://localhost:8000/public/
   ```

## Funkce

- **Vyhledávání** - textové vyhledávání ve filmech a materiálech
- **Filtrování** - podle obsahu, typu, zvukaře, formátu atd.
- **Řazení** - podle abecedy, počtu materiálů, rozmanitosti, data
- **Rozbalovací detaily** - zobrazení materiálů pro každý film
- **Stránkování** - pro snadnější procházení velkého množství dat

## Struktura souborů

- `index.html` - hlavní HTML soubor
- `unique_normalized_titles_ais - final.csv` - datový soubor s filmy a materiály
- `public/` - složka pro GitLab Pages (pokud je dostupné)

