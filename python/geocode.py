import json, os, sys
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

def build_url(operation, values, key):
    if operation not in ("search", "reverse"): raise ValueError("Use search or reverse.")
    if not key: raise ValueError("Set GEOCODING_API_KEY.")
    params = {"format": "json", "accept-language": "en", "key": key}
    if operation == "search":
        if len(values) != 1 or not values[0].strip(): raise ValueError("Provide one quoted address.")
        params["q"] = values[0]
    else:
        if len(values) != 2: raise ValueError("Provide latitude and longitude.")
        lat, lon = map(float, values)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180): raise ValueError("Invalid coordinates.")
        params.update(lat=str(lat), lon=str(lon))
    return "https://api.geocoding.info/" + operation + "?" + urlencode(params)

def geocode(operation, values, key):
    url = build_url(operation, values, key)
    try:
        with urlopen(url, timeout=20) as response: return json.load(response)
    except HTTPError as error:
        raise RuntimeError("API returned HTTP " + str(error.code) + ". Check your key and limits.") from None
    except (URLError, TimeoutError):
        raise RuntimeError("Could not reach the API.") from None

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3: raise ValueError("Usage: geocode.py search 'Paris, France' OR reverse 48.8584 2.2945")
        print(json.dumps(geocode(sys.argv[1], sys.argv[2:], os.getenv("GEOCODING_API_KEY", "")), indent=2))
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr);sys.exit(1)
