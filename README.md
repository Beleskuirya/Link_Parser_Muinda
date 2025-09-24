# Link_Parser_Muinda

Un script Python qui récupère les articles africains les plus récents sur des sites
comme RFI et France24, puis exporte les liens dans un fichier JSON exploitable
(par exemple pour ensuite alimenter Google Sheets).

## Fonctionnalités

- Scrapping d'articles africains sur RFI (Radio France Internationale) et France24
- Détection intelligente du contenu via des mots-clés de pays et de régions
- Suppression des doublons et normalisation des URL
- Interface en ligne de commande (`python -m link_parser`)
- Export JSON prêt à l'emploi

## Prérequis

- Python 3.8 ou plus récent
- `pip` et `virtualenv` disponibles sur la machine

## Installation rapide

```bash
python3 -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer le script

Une fois l'environnement virtuel actif, deux possibilités :

```bash
# Option 1 : via le module directement
python -m link_parser --site all --output african_news_links.json

# Option 2 : via le script de confort
./scripts/run_parser.sh --site france24 --verbose
```

Le paramètre `--site` accepte `rfi`, `france24` ou `all`. Utilisez `--output` pour
changer le nom du fichier généré et `--verbose` pour des logs détaillés.

## Sortie JSON

Le fichier produit contient un tableau d'objets `{title, url, source}` :

```json
[
  {
    "title": "Mali : nouvelles du Sahel",
    "url": "https://www.rfi.fr/fr/afrique/20240101-mali-actualites",
    "source": "RFI"
  },
  {
    "title": "Cameroun : football africain",
    "url": "https://www.france24.com/fr/afrique/20240201-cameroun-sport",
    "source": "France24"
  }
]
```

## Tests automatisés

Des tests (basés sur du HTML fictif) valident la détection du contenu africain,
la suppression des doublons et l'enregistrement JSON.

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt  # installe pytest
pytest
```

## Aller plus loin

- Planifier l'exécution avec `cron`, GitHub Actions ou tout autre orchestrateur.
- Étendre la liste des sites à analyser en ajoutant de nouvelles méthodes
  similaires à `scrape_rfi_links` ou `scrape_france24_links`.
- Remplacer la sortie JSON par une intégration directe Google Sheets.
