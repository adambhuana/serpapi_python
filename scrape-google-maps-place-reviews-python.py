# video: https://www.youtube.com/watch?v=HQAWQPNjw_k

from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import json
import pandas as pd

params = {
  "api_key": "28631dd982fd40c01eac0bfe5b600ae7653360d85434bd1c1d1d800418169e0d",                   # your api key
  "engine": "google_maps_reviews",                    # serpapi search engine
  "hl": "id",                                         # language of the search
  "data_id": "0x2e69f5c4552c7473:0x8b7a429bd29969a2"  # place id data located inside Google Maps Place URL: located inside `data=` query parameter. 
}

search = GoogleSearch(params)


reviews = []

page_num = 0
while True:
    page_num += 1
    results = search.get_dict()

    print(f"Extracting reviews from {page_num} page.")

    if not "error" in results:
        for result in results.get("reviews", []): # return an empty list [] if no reviews from the place
            reviews.append({
                "page": page_num,
                "name": result.get("user").get("name"),
                "link": result.get("user").get("link"),
                "thumbnail": result.get("user").get("thumbnail"),
                "rating": result.get("rating"),
                "date": result.get("date"),
                "snippet": result.get("snippet"),
                "images": result.get("images"),
                "local_guide": result.get("user").get("local_guide"),
                # other data
            })
    else:
        print(results["error"])
        break

    if results.get("serpapi_pagination").get("next") and results.get("serpapi_pagination").get("next_page_token"):
        # split URL in parts as a dict and update search "params" variable to a new page that will be passed to GoogleSearch()
        search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
        #search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
    else:
        break


print(json.dumps(reviews, indent=2, ensure_ascii=False))
df = pd.DataFrame(reviews)
df.to_csv(f"data.csv", index=False)