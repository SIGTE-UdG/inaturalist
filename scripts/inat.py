import requests
import json

def fetch_inat_girona():
    base_url = "https://api.inaturalist.org/v1/observations"
    
    # Bounding box aproximada del municipi de Girona
    params = {
        "swlat": 41.9412,
        "swlng": 2.7746,
        "nelat": 42.0363,
        "nelng": 2.8912,
        "has[]": "geo",
        "per_page": 200,
    }

    all_results = []
    page = 1

    while True:
        params["page"] = page
        print(f"Fetching page {page}...")

        r = requests.get(base_url, params=params)
        data = r.json()

        results = data.get("results", [])
        if not results:
            print("No more results. Stopping.")
            break

        all_results.extend(results)
        page += 1

    print(f"Total observations downloaded: {len(all_results)}")
    return all_results


def to_geojson(observations, output_file="girona_inat.geojson"):
    features = []

    for obs in observations:
        if not obs.get("geojson"):
            continue

        point = obs["geojson"]  # { "type": "Point", "coordinates": [...] }

        feature = {
            "type": "Feature",
            "geometry": point,
            "properties": {
                "id": obs.get("id"),
                "species_guess": obs.get("species_guess"),
                "iconic_taxon_name": obs.get("iconic_taxon_name"), 
                "observed_on": obs.get("observed_on"),
                "num_identification_agreements": obs.get("num_identification_agreements"), 
                "photos": obs.get("photos"), 
                "url": obs.get("uri"),
                "taxon_name": (
                    obs.get("taxon", {}).get("name")
                    if obs.get("taxon")
                    else None
                ),
                "common_name": (
                    obs.get("taxon", {}).get("preferred_common_name")
                    if obs.get("taxon")
                    else None
                )
            }
        }

        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"GeoJSON written to {output_file}")


if __name__ == "__main__":
    observations = fetch_inat_girona()
    to_geojson(observations)
