#!/usr/bin/env python3
"""
Transform scraped data to frontend format.
Reads from data/medications_scraped.json and writes to public/data/medications.json
"""
import json
import os


def transform_data():
    """Transform scraped data for frontend consumption."""
    input_file = 'data/medications_scraped.json'
    output_file = 'public/data/medications.json'

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        print("Please run the scraper first: python3 scraper/scraper.py")
        return False

    # Load scraped data
    print(f"📖 Reading scraped data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        scraped = json.load(f)

    # Transform to frontend format
    print(f"🔄 Transforming {len(scraped)} medications...")
    frontend_data = []

    for med in scraped:
        card = {
            'input_name': med['input_name'],
            'varenr': med['varenr'],
            'found': med['found']
        }

        if med['found']:
            card.update({
                'exact_match': med['exact_match'],
                'variant_name': med['variant_name'],
                'spc_url': med['spc_url'],
                'aktivt_stof': med['aktivt_stof'],
                'indikationer': med['indikationer']
            })

        frontend_data.append(card)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save to public directory
    print(f"💾 Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, ensure_ascii=False, indent=2)

    # Print summary
    successful = sum(1 for m in frontend_data if m['found'])
    failed = len(frontend_data) - successful

    print("\n" + "=" * 60)
    print("✅ Data transformation complete!")
    print("=" * 60)
    print(f"Total medications: {len(frontend_data)}")
    print(f"Successfully scraped: {successful}")
    print(f"Failed/missing: {failed}")
    print(f"\n📁 Frontend data saved to: {output_file}")
    print("\nNext step: Run 'python3 server.py' to test locally")
    print("=" * 60)

    return True


if __name__ == "__main__":
    transform_data()
