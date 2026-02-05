#!/usr/bin/env python3
"""
Main scraper orchestration for vetisearch.dk
"""
import json
import time
import argparse
from typing import Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from url_mapper import find_product_url, generate_slug_variants
from parser import parse_spc_page, extract_variant_links


class VetSearchScraper:
    def __init__(self, delay: float = 1.5):
        self.delay = delay
        self.base_url = "https://vetisearch.dk"
        self.session = self._create_session()
        self.failed_medications = []

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()

        # Retry strategy
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.headers.update({
            'User-Agent': 'Educational Flashcard Generator (Educational project)'
        })

        return session

    def calculate_match_score(self, input_name: str, variant_name: str) -> int:
        """
        Calculate how well a variant matches the input name.
        Returns score 0-100.
        """
        input_lower = input_name.lower()
        variant_lower = variant_name.lower()

        score = 0

        # Extract concentration patterns
        import re
        concentration_pattern = r'\d+\s*(mg|g|ml|%|mikrog|mcg)'

        input_concentrations = set(re.findall(concentration_pattern, input_lower))
        variant_concentrations = set(re.findall(concentration_pattern, variant_lower))

        # Bonus for matching concentrations
        if input_concentrations and variant_concentrations:
            matches = input_concentrations & variant_concentrations
            score += len(matches) * 30

        # Extract form patterns
        forms = ['inj', 'tablet', 'kapsel', 'spot-on', 'øredråber', 'øjendråber',
                 'salve', 'gel', 'suspension', 'emulsion', 'opløsning']

        for form in forms:
            if form in input_lower and form in variant_lower:
                score += 20

        # Check for word overlap
        input_words = set(input_lower.split())
        variant_words = set(variant_lower.split())
        common_words = input_words & variant_words

        score += len(common_words) * 10

        return min(score, 100)

    def select_best_variant(self, variants: List[Dict], input_name: str) -> Dict:
        """
        Select the best matching variant from a list.
        Returns the variant dict with added 'exact_match' boolean.
        """
        if not variants:
            return None

        # Calculate scores
        scored_variants = [
            (variant, self.calculate_match_score(input_name, variant['name']))
            for variant in variants
        ]

        # Sort by score (highest first)
        scored_variants.sort(key=lambda x: x[1], reverse=True)

        best_variant, best_score = scored_variants[0]

        return {
            **best_variant,
            'exact_match': best_score > 60,  # Threshold for "close enough"
            'match_score': best_score
        }

    def scrape_medication(self, name: str, varenr: str) -> Dict:
        """
        Scrape data for a single medication.

        Returns:
            Dict with medication data or error information
        """
        print(f"Scraping: {name}...", end=" ")

        result = {
            'input_name': name,
            'varenr': varenr,
            'found': False
        }

        try:
            # Step 1: Find product URL
            product_url = find_product_url(name)

            if not product_url:
                print("❌ Product not found")
                result['error'] = "Product not found on vetisearch.dk"
                self.failed_medications.append((name, varenr, "Product not found"))
                return result

            # Step 2: Get product page to find variants
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()

            # Step 3: Extract variant links
            variants = extract_variant_links(response.text, self.base_url)

            if not variants:
                print("⚠️  No SPC variants found")
                result['error'] = "No SPC variants found"
                self.failed_medications.append((name, varenr, "No SPC variants"))
                return result

            # Step 4: Select best matching variant
            best_variant = self.select_best_variant(variants, name)

            if not best_variant:
                print("❌ No suitable variant")
                result['error'] = "No suitable variant found"
                self.failed_medications.append((name, varenr, "No suitable variant"))
                return result

            # Step 5: Scrape the SPC page
            spc_response = self.session.get(best_variant['url'], timeout=10)
            spc_response.raise_for_status()

            # Step 6: Parse the SPC page
            parsed_data = parse_spc_page(spc_response.text)

            # Step 7: Build result
            result.update({
                'found': True,
                'exact_match': best_variant['exact_match'],
                'variant_name': best_variant['name'],
                'product_url': product_url,
                'spc_url': best_variant['url'],
                'aktivt_stof': parsed_data['aktivt_stof'],
                'indikationer': parsed_data['indikationer']
            })

            match_indicator = "✓" if best_variant['exact_match'] else "~"
            print(f"{match_indicator} Success (score: {best_variant.get('match_score', 0)})")

        except requests.RequestException as e:
            print(f"❌ Network error: {str(e)[:50]}")
            result['error'] = f"Network error: {str(e)}"
            self.failed_medications.append((name, varenr, f"Network error: {str(e)}"))

        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
            result['error'] = str(e)
            self.failed_medications.append((name, varenr, str(e)))

        return result

    def scrape_all(self, medications: List[Dict], test_mode: bool = False) -> List[Dict]:
        """
        Scrape all medications.

        Args:
            medications: List of medication dicts with 'name' and 'varenr'
            test_mode: If True, only scrape first 3 medications

        Returns:
            List of scraped medication data
        """
        if test_mode:
            medications = medications[:3]
            print(f"🧪 TEST MODE: Scraping first {len(medications)} medications\n")
        else:
            print(f"🚀 Starting scrape of {len(medications)} medications\n")

        results = []

        for i, med in enumerate(medications, 1):
            print(f"[{i}/{len(medications)}] ", end="")

            result = self.scrape_medication(med['name'], med['varenr'])
            results.append(result)

            # Rate limiting
            if i < len(medications):
                time.sleep(self.delay)

        return results

    def generate_report(self, results: List[Dict]) -> str:
        """Generate a summary report of the scraping results."""
        total = len(results)
        successful = sum(1 for r in results if r['found'])
        failed = total - successful

        report = "=" * 50 + "\n"
        report += "SCRAPING REPORT\n"
        report += "=" * 50 + "\n\n"
        report += f"Total medications: {total}\n"
        report += f"Successfully scraped: {successful}\n"
        report += f"Failed: {failed}\n\n"

        if self.failed_medications:
            report += "Failed medications (need manual data entry):\n"
            report += "-" * 50 + "\n"
            for i, (name, varenr, reason) in enumerate(self.failed_medications, 1):
                varenr_str = varenr if varenr else "N/A"
                report += f"{i}. {name}\n"
                report += f"   Varenr: {varenr_str}\n"
                report += f"   Reason: {reason}\n\n"

        # Stats on exact matches
        exact_matches = sum(1 for r in results if r.get('found') and r.get('exact_match'))
        approximate_matches = successful - exact_matches

        report += f"\nMatch quality:\n"
        report += f"  Exact matches: {exact_matches}\n"
        report += f"  Approximate matches: {approximate_matches}\n"

        return report


def main():
    parser = argparse.ArgumentParser(description='Scrape vetisearch.dk for medication data')
    parser.add_argument('--test', action='store_true', help='Test mode: scrape first 3 medications only')
    parser.add_argument('--delay', type=float, default=1.5, help='Delay between requests in seconds')
    args = parser.parse_args()

    # Load input medications
    with open('../data/medications_input.json', 'r', encoding='utf-8') as f:
        medications = json.load(f)

    # Create scraper
    scraper = VetSearchScraper(delay=args.delay)

    # Scrape
    results = scraper.scrape_all(medications, test_mode=args.test)

    # Save results
    output_file = '../data/medications_scraped.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Results saved to {output_file}")

    # Generate and save report
    report = scraper.generate_report(results)
    report_file = '../data/scraping_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 Report saved to {report_file}\n")
    print(report)


if __name__ == "__main__":
    main()
