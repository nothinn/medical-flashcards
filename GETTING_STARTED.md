# Getting Started - Quick Reference

## 🚀 Fast Track (5 Steps)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r scraper/requirements.txt

# 3. Test scraper (optional but recommended)
cd scraper && python3 scraper.py --test && cd ..

# 4. Run full scrape and transform
cd scraper && python3 scraper.py && cd ..
python3 transform_data.py

# 5. Test locally
python3 server.py
# Open http://localhost:8000
```

## 📁 Project Files

### Essential Files You'll Use
- **scraper/scraper.py** - The web scraper (run this first)
- **transform_data.py** - Converts scraped data to frontend format
- **server.py** - Local testing server
- **data/medications_input.json** - Your 75 medications (already populated)

### Files You'll Get After Scraping
- **data/medications_scraped.json** - Raw scraped data
- **data/scraping_report.txt** - Success/failure report
- **public/data/medications.json** - Frontend-ready data

### Frontend Files (already complete)
- **public/index.html** - Flash card interface
- **public/styles.css** - Styling
- **public/app.js** - Interactive logic

### Documentation
- **README.md** - Main documentation
- **SETUP_GUIDE.md** - Detailed setup with troubleshooting
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **PROJECT_STATUS.md** - Current status

## 🎯 What Each Command Does

### `python3 scraper.py --test`
- Scrapes **first 3 medications** only
- Takes ~10 seconds
- Good for testing before full run
- Creates: `data/medications_scraped.json` and `data/scraping_report.txt`

### `python3 scraper.py`
- Scrapes **all 75 medications**
- Takes 5-10 minutes
- Shows progress with emoji indicators:
  - ✓ = Perfect match
  - ~ = Approximate match
  - ❌ = Failed
- Creates: `data/medications_scraped.json` and `data/scraping_report.txt`

### `python3 transform_data.py`
- Converts scraped data to frontend format
- Takes < 1 second
- Creates: `public/data/medications.json`
- Shows summary statistics

### `python3 server.py`
- Starts local web server on port 8000
- Serves files from `public/` directory
- Open http://localhost:8000 to test
- Press Ctrl+C to stop

## 📊 What to Expect

### Scraping Results
- **Expected success:** 85-95% (64-71 medications)
- **Common failures:**
  - Generic drugs (Gabapentin, Trazodone, Tramadol)
  - Products not in veterinary database
  - Discontinued products

### Frontend
- All 75 medications included (even failed ones)
- Failed medications show "Data ikke tilgængelig"
- Approximate matches show warning "⚠️ Viser: [variant name]"

## 🎮 Using the Flash Cards

### Navigation
- **Click card** - Flip to see answer
- **← →** - Previous/Next card
- **Space/Enter** - Flip card

### Front of Card Shows
- Medication name
- Varenr (product number)
- Warning if approximate match

### Back of Card Shows
- Active substances (Aktivt stof)
- Indications (Indikationer)
- Link to official product summary

## 🔧 Troubleshooting Quick Fixes

### "Module not found" error
```bash
# Make sure you activated the virtual environment!
source venv/bin/activate
```

### Scraper failing for many medications
```bash
# Increase delay between requests
cd scraper
python3 scraper.py --delay 2.5
```

### "Failed to load medications" in browser
```bash
# Check that the JSON file exists
ls -l public/data/medications.json

# Validate the JSON
python3 -m json.tool public/data/medications.json
```

### GitHub Pages shows 404
- Wait 2-3 minutes after configuring
- Ensure folder is set to `/public` in settings
- Check that files were pushed: `git push origin main`

## 📦 Deployment to GitHub Pages

```bash
# One-time setup
git init
git add .
git commit -m "Initial commit: Danish vet med flashcards"
git remote add origin https://github.com/YOUR_USERNAME/med-flash-cards.git
git push -u origin main

# Then on GitHub.com:
# Settings → Pages → Deploy from branch → main → /public → Save
```

Your site will be at: `https://YOUR_USERNAME.github.io/med-flash-cards/`

## 🔄 Making Updates

### Re-scraping Data
```bash
source venv/bin/activate
cd scraper && python3 scraper.py && cd ..
python3 transform_data.py
```

### Adding More Medications
1. Edit `data/medications_input.json`
2. Run scraper again
3. Run transform again
4. Git commit and push

### Updating Frontend
1. Edit files in `public/`
2. Test with `python3 server.py`
3. Git commit and push
4. GitHub Pages updates automatically

## 📚 File Sizes

- **Input data:** ~5 KB (75 medications)
- **Scraped data:** ~50-100 KB (depends on success rate)
- **Frontend total:** ~100 KB (HTML + CSS + JS + data)
- **Very fast loading** - no frameworks, pure vanilla JS

## ✅ Success Checklist

Before deployment, verify:
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Test scrape worked
- [ ] Full scrape completed
- [ ] Reviewed scraping report
- [ ] Transform script ran successfully
- [ ] Local server works
- [ ] Flash cards display and flip correctly
- [ ] Keyboard navigation works
- [ ] All 75 cards accessible
- [ ] Tested on mobile (or DevTools mobile view)

## 🎓 Next Steps After Deployment

1. **Share URL** with veterinary students
2. **Review failed medications** in report
3. **Consider manual data entry** for important failed medications
4. **Gather feedback** on usability
5. **Iterate** as needed

## 💡 Pro Tips

- Always activate `venv` before running Python scripts
- Test scrape first to catch any issues early
- Review `scraping_report.txt` to see what failed
- Keep `data/medications_scraped.json` as backup
- Hard refresh browser (Ctrl+Shift+R) if changes don't show
- Use browser DevTools to test mobile responsiveness

## 🆘 Need More Help?

1. **Setup issues:** See `SETUP_GUIDE.md`
2. **Technical details:** See `IMPLEMENTATION_SUMMARY.md`
3. **General info:** See `README.md`
4. **Current status:** See `PROJECT_STATUS.md`

## 🎉 You're Ready!

The project is fully implemented and ready to use. Follow the 5-step Fast Track above to get started.

Good luck with your Danish veterinary medication flash cards! 🏥🐕🐈
