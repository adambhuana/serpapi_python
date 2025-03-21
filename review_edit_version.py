import os, csv
from urllib.parse import urlsplit, parse_qsl
from serpapi import SerpApiClient

params = {
    "engine": "google_maps",
    "q": "coffee",
    "type": "search",
    "ll": "@40.7455096,-74.0083012,14z",
    "api_key": os.getenv("YOUR API KEY"),
}

search = SerpApiClient(params, timeout=90)

fieldnames = set()
results_to_write = []

pages = search.pagination()

for page_number, page in enumerate(pages):
  print(f"\nCurrent page: {page_number}")

  if not "local_results" in page:
    break

  local_results = page.get("local_results", [])
  results_to_write.extend(local_results)

  for result in page.get("local_results", []):
    fieldnames.update(result.keys())

    print(f"""
Title: {result.get('title')}
Address: {result.get('address')}
Rating: {result.get('rating')}
Reviews: {result.get('reviews')}""")

  if "ads_results" in page:
    print("Ads")

  for result in page.get("ads_results", []):
    print(f"""
Title: {result.get('title')}
Address: {result.get('address')}""")

with open(f'test.csv', 'w', encoding='utf8', newline='') as output_file:
  fc = csv.DictWriter(output_file, fieldnames=fieldnames)

  fc.writeheader()
  fc.writerows(results_to_write)
