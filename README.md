# Danish Veterinary Medication Flash Cards

Interactive flash cards for 75 veterinary medications with data scraped from vetisearch.dk.

## Features

- Interactive flip cards with medication information
- Active substances (Aktivt stof) and indications (Indikationer)
- Keyboard navigation (← / → / Space)
- Progress tracking
- Mobile responsive
- Links to official product summaries

## Project Structure

```
med-flash-cards/
├── data/
│   ├── medications_input.json       # Input: 75 medications
│   ├── medications_scraped.json     # Scraped data (after running scraper)
│   └── scraping_report.txt          # Scraping report
├── scraper/
│   ├── scraper.py                   # Main scraper
│   ├── url_mapper.py                # URL mapping logic
│   ├── parser.py                    # HTML parsing
│   └── requirements.txt             # Python dependencies
├── docs/                            # Frontend (GitHub Pages)
│   ├── index.html                   # Main UI
│   ├── styles.css                   # Styling
│   ├── app.js                       # Flash card logic
│   └── data/
│       └── medications.json         # Production data
├── server.py                        # Local testing server
├── transform_data.py                # Data transformation
└── README.md
```

## Setup and Usage

### 1. Install Python Dependencies

```bash
cd scraper
pip install -r requirements.txt
cd ..
```

### 2. Run the Scraper

**Test mode (first 3 medications):**
```bash
cd scraper
python3 scraper.py --test
cd ..
```

**Full scrape (all 75 medications):**
```bash
cd scraper
python3 scraper.py
cd ..
```

This will create:
- `data/medications_scraped.json` - Raw scraped data
- `data/scraping_report.txt` - Summary report

### 3. Transform Data for Frontend

```bash
python3 transform_data.py
```

This copies the scraped data to `docs/data/medications.json` in the format needed by the frontend.

### 4. Test Locally

```bash
python3 server.py
```

Open http://localhost:8000 in your browser.

### 5. Deploy to GitHub Pages

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit: Danish vet med flashcards"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/med-flash-cards.git
git branch -M main
git push -u origin main
```

Then configure GitHub Pages:
1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, Folder: `/docs`
4. Save

Your site will be available at: `https://YOUR_USERNAME.github.io/med-flash-cards/`

## Keyboard Shortcuts

- `←` / `→` - Navigate between cards
- `Space` / `Enter` - Flip card
- Click card to flip

## Scraper Details

### How It Works

1. **URL Discovery**: Converts medication names to vetisearch.dk product URLs
2. **Variant Matching**: Finds the best matching product variant (e.g., specific concentration)
3. **Data Extraction**: Scrapes active substances and indications from SPC pages
4. **Rate Limiting**: 1.5 second delay between requests

### Handling Missing Data

Some medications may not be found on vetisearch.dk. These are:
- Included in the flash cards with "Data ikke tilgængelig" message
- Listed in `data/scraping_report.txt` for manual review

### Manual Data Entry

If medications fail to scrape, you can manually add data to `data/medications_scraped.json`:

```json
{
  "input_name": "Medication Name",
  "varenr": "123456",
  "found": true,
  "exact_match": true,
  "variant_name": "Full Product Name",
  "product_url": "https://vetisearch.dk/products/...",
  "spc_url": "https://vetisearch.dk/spcs/...",
  "aktivt_stof": ["Active Substance 1", "Active Substance 2"],
  "indikationer": ["Indication 1", "Indication 2"]
}
```

Then run `python3 transform_data.py` again.

## Development

### Testing Changes

After modifying frontend files (HTML/CSS/JS):
1. Reload the page in your browser
2. Hard refresh with Ctrl+Shift+R to clear cache

### Adding More Medications

1. Add entries to `data/medications_input.json`
2. Run scraper: `cd scraper && python3 scraper.py`
3. Transform data: `python3 transform_data.py`
4. Test locally: `python3 server.py`

## License

Educational project for veterinary students.

## Credits

Data source: https://vetisearch.dk
