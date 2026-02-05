# Setup Guide

## Prerequisites

- Python 3.8 or higher
- Git (for deployment)
- A modern web browser

## Installation Steps

### 1. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r scraper/requirements.txt
```

**Important:** Always activate the virtual environment before running the scraper:
```bash
source venv/bin/activate
```

### 2. Test the Scraper (Optional)

Test with 3 medications first:

```bash
cd scraper
python3 scraper.py --test
cd ..
```

This will:
- Scrape the first 3 medications from the list
- Create `data/medications_scraped.json`
- Generate `data/scraping_report.txt`

Review the results to ensure the scraper is working correctly.

### 3. Run Full Scrape

```bash
cd scraper
python3 scraper.py
cd ..
```

**Duration:** 5-10 minutes for 75 medications

**What happens:**
- Scrapes all 75 medications from vetisearch.dk
- 1.5 second delay between requests (respectful crawling)
- Shows progress with emoji indicators:
  - ✓ = Exact match found
  - ~ = Approximate match (shows warning on card)
  - ❌ = Failed to scrape
  - ⚠️ = No SPC variants found

### 4. Transform Data for Frontend

```bash
python3 transform_data.py
```

This converts `data/medications_scraped.json` to `docs/data/medications.json` in the format needed by the frontend.

### 5. Test Locally

```bash
python3 server.py
```

Open your browser to: **http://localhost:8000**

**Test checklist:**
- [ ] Flash cards display correctly
- [ ] Click to flip cards works
- [ ] Keyboard navigation works (← → Space)
- [ ] Progress bar updates
- [ ] All 75 cards are accessible
- [ ] Missing data shows appropriate message

### 6. Deploy to GitHub Pages

#### Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `med-flash-cards` (or your choice)
3. Make it Public
4. Don't initialize with README (we already have one)
5. Create repository

#### Push Your Code

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Danish veterinary medication flash cards"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/med-flash-cards.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Pages** in the left sidebar
4. Under "Source":
   - Select **Deploy from a branch**
   - Branch: **main**
   - Folder: **/public**
5. Click **Save**

#### Wait for Deployment

- GitHub will build and deploy your site (2-3 minutes)
- Refresh the Pages settings page to see the URL
- Your site will be at: `https://YOUR_USERNAME.github.io/med-flash-cards/`

## Troubleshooting

### Virtual Environment Issues

**Problem:** `venv` not found
```bash
# Install python3-venv
sudo apt install python3-venv  # On Debian/Ubuntu
```

**Problem:** Forgot to activate virtual environment
```bash
# You'll see errors about missing modules
# Solution: Activate the venv
source venv/bin/activate
```

### Scraper Issues

**Problem:** Network timeouts
```bash
# Increase delay between requests
cd scraper
python3 scraper.py --delay 2.5
```

**Problem:** Many medications failing
- Check your internet connection
- Verify vetisearch.dk is accessible
- Review `data/scraping_report.txt` for specific errors

**Problem:** Specific medication not found
- Search manually on vetisearch.dk
- If it exists, check the URL pattern
- May need to adjust `url_mapper.py` slug generation
- Or manually add data to `medications_scraped.json`

### Frontend Issues

**Problem:** "Failed to load medications"
- Check browser console for errors
- Verify `docs/data/medications.json` exists
- Check JSON is valid: `python3 -m json.tool docs/data/medications.json`

**Problem:** Cards not flipping
- Hard refresh browser: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Check browser console for JavaScript errors

**Problem:** Styling looks broken
- Clear browser cache
- Check that `styles.css` is loading (Network tab in dev tools)

### Deployment Issues

**Problem:** GitHub Pages shows 404
- Wait 2-3 minutes after configuring Pages
- Verify folder is set to `/public` not `/root`
- Check that `docs/index.html` exists in your repository

**Problem:** Site loads but shows errors
- Check browser console
- Verify `docs/data/medications.json` exists in repo
- Ensure all files were committed and pushed

## Directory Structure After Setup

```
med-flash-cards/
├── venv/                            # Virtual environment (not in git)
├── data/
│   ├── medications_input.json       # ✅ Input medications
│   ├── medications_scraped.json     # ✅ After scraping
│   └── scraping_report.txt          # ✅ After scraping
├── scraper/
│   ├── scraper.py
│   ├── url_mapper.py
│   ├── parser.py
│   └── requirements.txt
├── docs/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data/
│       └── medications.json         # ✅ After transform_data.py
├── server.py
├── transform_data.py
└── README.md
```

## Quick Start Commands

```bash
# Full setup from scratch
python3 -m venv venv
source venv/bin/activate
pip install -r scraper/requirements.txt

# Scrape and build
cd scraper && python3 scraper.py && cd ..
python3 transform_data.py

# Test
python3 server.py

# Deploy
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/med-flash-cards.git
git push -u origin main
```

## Need Help?

1. Check `IMPLEMENTATION_SUMMARY.md` for technical details
2. Review `README.md` for usage documentation
3. Check `data/scraping_report.txt` for scraping issues
4. Look at browser console for frontend errors

## What's Next?

After successful deployment:
1. Share the GitHub Pages URL with students
2. Review failed medications in the report
3. Consider manually adding missing data
4. Optionally add more medications to the input list
