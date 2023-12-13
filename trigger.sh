#!/bin/bash

set -e


curl --location --request PUT 'django:8000/api/v1/checkout/products/inventory-accuracy/' \
--header 'Content-Type: application/json' \
--header 'Cookie: session_id=Z4z9rppEXqNYLEJKWaG9ifs4Wiq8sR' \
--data-raw '{
    "analyst_email": "bbereoff@gmail.com"
}'

$@