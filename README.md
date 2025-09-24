# Link_Parser_Muinda

A Python script that scrapes journal pages such as RFI or France24, and returns the links of African news articles.

## Features

- Scrapes African news articles from RFI (Radio France Internationale) and France24
- Intelligent content detection using African country names and regional keywords
- Supports both French and English content
- Outputs results in JSON format
- Command-line interface with flexible options
- Duplicate removal and URL normalization

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Beleskuirya/Link_Parser_Muinda.git
cd Link_Parser_Muinda
```

2. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

### Basic Usage

Scrape all sites (RFI and France24):
```bash
python3 link_parser.py
```

### Advanced Options

Scrape only RFI:
```bash
python3 link_parser.py --site rfi
```

Scrape only France24:
```bash
python3 link_parser.py --site france24
```

Save to a custom file:
```bash
python3 link_parser.py --output my_african_news.json
```

Enable verbose logging:
```bash
python3 link_parser.py --verbose
```

### Command Line Options

- `--output`, `-o`: Output JSON file (default: african_news_links.json)
- `--site`: Which site to scrape - options: rfi, france24, all (default: all)
- `--verbose`, `-v`: Enable verbose output
- `--help`, `-h`: Show help message

## Output Format

The script generates a JSON file containing an array of article objects with the following structure:

```json
[
  {
    "title": "Mali : nouvelles du Sahel",
    "url": "https://www.rfi.fr/fr/afrique/20240101-mali-actualites",
    "source": "RFI"
  },
  {
    "title": "Sénégal : élections présidentielles", 
    "url": "https://www.rfi.fr/fr/afrique/20240102-senegal-politique",
    "source": "RFI"
  }
]
```

## African Content Detection

The script identifies African news articles using:

- **Country names**: Algeria, Angola, Benin, Botswana, Burkina Faso, Burundi, Cameroon, Cape Verde, Central African Republic, Chad, Comoros, Congo, Djibouti, Egypt, Eritrea, Ethiopia, Gabon, Gambia, Ghana, Guinea, Kenya, Lesotho, Liberia, Libya, Madagascar, Malawi, Mali, Morocco, Mauritius, Mauritania, Mozambique, Namibia, Niger, Nigeria, Uganda, Rwanda, Senegal, Seychelles, Sierra Leone, Somalia, Sudan, Tanzania, Togo, Tunisia, Zambia, Zimbabwe, Côte d'Ivoire

- **Regional terms**: Maghreb, Sahel, West Africa, Central Africa, East Africa, Southern Africa, Horn of Africa

- **URL patterns**: Articles containing `/afrique/` or `/africa/` in their URLs

## Testing

Run the test suite to verify the parsing logic:
```bash
python3 test_parser.py
```

## Requirements

- Python 3.6+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- urllib3 >= 2.0.0

## License

This project is open source and available under the MIT License.
