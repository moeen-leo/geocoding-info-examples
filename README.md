# Geocoding.info API examples

Python, Node.js, cURL and Postman examples for address search and reverse geocoding.

[Demo](https://geocoding.info/?utm_source=github&utm_medium=examples&utm_campaign=launch) | [Sign up](https://geocoding.info/Signup.aspx) | [Pricing](https://geocoding.info/Pricing.aspx) | [Guide](https://geocoding.info/Geocoding.aspx) | [Postman](https://www.postman.com/sparetime-8550009/geocoding-info-api/overview)

## Run

Create and verify your account, create a key in the dashboard, and set GEOCODING_API_KEY in your server environment. On PowerShell use $env:GEOCODING_API_KEY = 'YOUR_API_KEY'. On Bash use export GEOCODING_API_KEY='YOUR_API_KEY'.

~~~bash
python python/geocode.py search 'Paris, France'
python python/geocode.py reverse 48.8584 2.2945
node node/geocode.mjs search 'Paris, France'
node node/geocode.mjs reverse 48.8584 2.2945
~~~

Requires Python 3.10+ or Node.js 20+. No third-party dependencies.

## API

Base URL: https://api.geocoding.info. Supply the key query parameter on authenticated requests.

| Endpoint | Purpose |
|---|---|
| /status | Public health check, no key |
| /search?q=...&format=json | Address to candidate coordinates |
| /reverse?lat=...&lon=...&format=json | Coordinates to a suitable nearby mapped place |
| /lookup?osm_ids=...&format=json | OpenStreetMap object lookup |
| /usage | Read account usage |

Search/lookup return lists; reverse returns an object. Use format=xml on geocoding requests for XML. English is the default unless accept-language is supplied.

Fork the public Postman collection or import postman/Geocoding.info.postman_collection.json. Set api_key locally; its shared value is empty. Never publish real keys. Do not embed a secret key in frontend JavaScript. Redact query URLs in logs.

Daily and 30-day limits both apply. Send requests sequentially and respect the current rate limit in your account. Handle 401, 429 and temporary 5xx errors; do not retry indefinitely.

OpenStreetMap/Nominatim coverage varies. A reverse result can describe a nearby feature rather than the exact street address. This is not postal-address validation. Preserve [OSM attribution](https://www.openstreetmap.org/copyright).

## Offline tests

~~~bash
python -m unittest discover -s tests
node --test tests/geocode.test.mjs
~~~

## License

Example code is MIT licensed. Geocoding.info branding and third-party map data are not relicensed by this repository.
