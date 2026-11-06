# Reverse geocode GPS coordinates in Python

Disclosure: I operate Geocoding.info.

Register at https://geocoding.info/Signup.aspx , verify your email if requested, and create a key in the dashboard. Set GEOCODING_API_KEY on your server. The example requires Python 3.10+ and no external dependencies.

~~~python
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

~~~

Run: python geocode.py reverse 48.8584 2.2945

Search returns candidate locations as a list; reverse lookup returns an object. Empty results are possible. Handle authentication errors (401), rate/quota limits (429) and temporary failures (5xx). Send requests sequentially and avoid unlimited retries. Never log full request URLs or publish your real API key.

Coverage varies with OpenStreetMap/Nominatim; reverse lookup can return a nearby mapped feature rather than an exact postal address. Preserve required attribution: https://www.openstreetmap.org/copyright . Current allowances: https://geocoding.info/Pricing.aspx .
