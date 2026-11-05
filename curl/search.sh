#!/usr/bin/env bash
set -eu
if [ -z "$GEOCODING_API_KEY" ]; then echo "Set GEOCODING_API_KEY"; exit 1; fi
curl --fail --silent --show-error --get 'https://api.geocoding.info/search' --data-urlencode 'q=Paris, France' --data-urlencode 'format=json' --data-urlencode "key=$GEOCODING_API_KEY"
