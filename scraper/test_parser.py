import requests
from parser import parse_spc_page

# Test with Metacam SPC page
url = "https://vetisearch.dk/spcs/191-metacam"
response = requests.get(url)
result = parse_spc_page(response.text)

print("Aktivt stof:", result['aktivt_stof'])
print("Indikationer:", result['indikationer'][:2] if len(result['indikationer']) > 2 else result['indikationer'])
