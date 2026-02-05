"""
URL Mapper - Convert medication names to vetisearch.dk product slugs
"""
import re
import requests
from typing import Optional, List


def normalize_danish_text(text: str) -> str:
    """Convert Danish characters to URL-safe equivalents."""
    text = text.lower()
    replacements = {
        'æ': 'ae',
        'ø': 'oe',
        'å': 'aa',
        'ä': 'a',
        'ö': 'o'
    }
    for danish, english in replacements.items():
        text = text.replace(danish, english)
    return text


def clean_medication_name(name: str) -> str:
    """Extract the core medication name, removing dosages and forms."""
    # Remove content in parentheses
    name = re.sub(r'\([^)]*\)', '', name)

    # Remove dosage patterns (e.g., "5 mg/ml", "100 mg", "10%")
    name = re.sub(r'\d+\s*(mg|g|ml|%|mikrog\.|mcg)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\d+\s*mg/ml', '', name, flags=re.IGNORECASE)

    # Remove form indicators
    forms = [r'inj\.?', 'tabletter', r'tbl\.?', 'kapsler', 'spot-on', 'øredråber',
             'øjendråber', 'øresalve', 'øjensalve', 'øjengel', 'salve', 'gel',
             'pulver', 'solvens', 'suspension', 'emulsion', 'opløsning', 'væske',
             r'inj\.væske', 'oral', r'smag\.?', 'smagsatte', 'bløde', 'tyggetabletter',
             'protectorband', 'halsbånd']

    for form in forms:
        name = re.sub(r'\b' + form + r'\b', '', name, flags=re.IGNORECASE)

    # Remove "vet." and similar markers
    name = re.sub(r'\bvet\.?\b', '', name, flags=re.IGNORECASE)

    # Clean up extra whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def medication_to_slug(name: str) -> str:
    """Convert medication name to a URL slug."""
    cleaned = clean_medication_name(name)
    normalized = normalize_danish_text(cleaned)

    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', normalized)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')

    return slug


def generate_slug_variants(name: str) -> List[str]:
    """Generate multiple slug variants to try."""
    variants = []

    # Full cleaned name
    full_slug = medication_to_slug(name)
    if full_slug:
        variants.append(full_slug)

    # First word only
    first_word = clean_medication_name(name).split()[0] if clean_medication_name(name).split() else ""
    if first_word:
        first_word_slug = medication_to_slug(first_word)
        if first_word_slug and first_word_slug not in variants:
            variants.append(first_word_slug)

    # First two words
    words = clean_medication_name(name).split()
    if len(words) >= 2:
        first_two = ' '.join(words[:2])
        first_two_slug = medication_to_slug(first_two)
        if first_two_slug and first_two_slug not in variants:
            variants.append(first_two_slug)

    # Original name with minimal cleaning (just first word)
    original_first = name.split()[0] if name.split() else ""
    if original_first:
        original_slug = normalize_danish_text(original_first.lower())
        original_slug = re.sub(r'[^\w-]', '', original_slug)
        if original_slug and original_slug not in variants:
            variants.append(original_slug)

    return variants


def find_product_url(name: str, timeout: int = 10) -> Optional[str]:
    """
    Try to find a working product URL for the medication.
    Returns the product URL if found, None otherwise.
    """
    base_url = "https://vetisearch.dk/products/"
    headers = {
        'User-Agent': 'Educational Flashcard Generator (Contact: educational-project)'
    }

    variants = generate_slug_variants(name)

    for slug in variants:
        url = f"{base_url}{slug}"
        try:
            response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                return url
        except requests.RequestException:
            continue

    return None


if __name__ == "__main__":
    # Test with some examples
    test_medications = [
        "Metacam inj. 5 mg/ml",
        "Rimadyl Vet. 50 mg, tabletter",
        "Nobivac SHP, inj.væske",
        "Milbemax små hunde/hvalpe, tbl."
    ]

    for med in test_medications:
        print(f"\n{med}")
        print(f"  Cleaned: {clean_medication_name(med)}")
        print(f"  Slug: {medication_to_slug(med)}")
        print(f"  Variants: {generate_slug_variants(med)}")
