#!/bin/bash

# Generate a sample JSON payload
payload='{"key1":"value1", "key2":"value2"}'

# Send the payload using curl
curl -X POST http://localhost:2525/inbound -H "Content-Type: application/json" -d "$payload"
