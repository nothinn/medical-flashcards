"""
HTML Parser - Extract active substances and indications from SPC pages
"""
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text - collapse multiple spaces/newlines into single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def parse_spc_page(html: str) -> Dict[str, any]:
    """
    Parse an SPC page and extract active substances and indications.

    Returns:
        {
            'aktivt_stof': List[str],
            'indikationer': List[str]
        }
    """
    soup = BeautifulSoup(html, 'lxml')

    result = {
        'aktivt_stof': [],
        'indikationer': []
    }

    # Find active substances
    aktivt_stof = extract_aktivt_stof(soup)
    if aktivt_stof:
        result['aktivt_stof'] = aktivt_stof

    # Find indications
    indikationer = extract_indikationer(soup)
    if indikationer:
        result['indikationer'] = indikationer

    return result


def extract_aktivt_stof(soup: BeautifulSoup) -> List[str]:
    """Extract active substances from the page."""
    aktivt_stof = []

    # Look for heading containing "Aktivt stof" or "Aktive stoffer"
    headings = soup.find_all(['h2', 'h3', 'h4'])

    for heading in headings:
        heading_text = heading.get_text(strip=True).lower()

        if 'aktivt stof' in heading_text or 'aktive stoffer' in heading_text or 'active substance' in heading_text:
            # Get the next sibling elements until we hit another heading
            current = heading.find_next_sibling()

            while current and current.name not in ['h1', 'h2', 'h3', 'h4']:
                # Check for list items (both in <ul> and standalone <li>)
                if current.name == 'ul':
                    for li in current.find_all('li'):
                        text = normalize_whitespace(li.get_text())
                        if text:
                            aktivt_stof.append(text)
                elif current.name == 'li':
                    # Handle standalone <li> elements (not in <ul>)
                    text = normalize_whitespace(current.get_text())
                    if text:
                        aktivt_stof.append(text)
                elif current.name == 'p':
                    text = normalize_whitespace(current.get_text())
                    if text and len(text) > 0:
                        # Sometimes substances are in paragraphs
                        aktivt_stof.append(text)

                current = current.find_next_sibling()

            break

    return aktivt_stof


def extract_indikationer(soup: BeautifulSoup) -> List[str]:
    """Extract indications from the page."""
    indikationer = []

    # Look for heading containing "Indikationer" or "Terapeutiske indikationer"
    headings = soup.find_all(['h2', 'h3', 'h4'])

    for heading in headings:
        heading_text = heading.get_text(strip=True).lower()

        if 'indikation' in heading_text or 'therapeutic indication' in heading_text:
            # Get the next sibling elements until we hit another heading
            current = heading.find_next_sibling()

            while current and current.name not in ['h1', 'h2', 'h3', 'h4']:
                # Collect paragraphs
                if current.name == 'p':
                    text = normalize_whitespace(current.get_text())
                    if text and len(text) > 10:  # Filter out very short text
                        indikationer.append(text)
                elif current.name == 'ul':
                    # Sometimes indications are in list format
                    for li in current.find_all('li'):
                        text = normalize_whitespace(li.get_text())
                        if text and len(text) > 10:
                            indikationer.append(text)
                elif current.name == 'div':
                    # Check for nested paragraphs
                    for p in current.find_all('p', recursive=False):
                        text = normalize_whitespace(p.get_text())
                        if text and len(text) > 10:
                            indikationer.append(text)

                current = current.find_next_sibling()

            break

    return indikationer


def extract_variant_links(html: str, base_url: str = "https://vetisearch.dk") -> List[Dict[str, str]]:
    """
    Extract all variant links from a product page.

    Returns:
        List of dicts with 'name', 'url', and 'spc_id'
    """
    soup = BeautifulSoup(html, 'lxml')
    variants = []

    # Look for links that point to SPC pages
    # Typically these are in the format /spcs/{id}-{slug}
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']

        # Check if this is an SPC link
        if '/spcs/' in href or '/spc/' in href:
            # Extract variant name from link text or nearby text
            variant_name = link.get_text(strip=True)

            # Build full URL
            if href.startswith('http'):
                full_url = href
            else:
                full_url = base_url + href if href.startswith('/') else base_url + '/' + href

            # Extract SPC ID from URL
            spc_id = href.split('/')[-1] if '/' in href else href

            variants.append({
                'name': variant_name,
                'url': full_url,
                'spc_id': spc_id
            })

    # Remove duplicates based on URL
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant['url'] not in seen:
            seen.add(variant['url'])
            unique_variants.append(variant)

    return unique_variants


if __name__ == "__main__":
    # Test HTML parsing
    test_html = """
    <html>
        <h3>Aktivt stof</h3>
        <ul>
            <li>Meloxicam : 5 mg/ml</li>
        </ul>

        <h3>Indikationer</h3>
        <p>Kvæg: Akut mastitis i kombination med antibiotikabehandling.</p>
        <p>Gris: Behandling af fødselsbetingede sygdomme.</p>

        <h3>Dosering</h3>
        <p>Some other content...</p>
    </html>
    """

    result = parse_spc_page(test_html)
    print("Parsed result:")
    print(f"  Aktivt stof: {result['aktivt_stof']}")
    print(f"  Indikationer: {result['indikationer']}")
