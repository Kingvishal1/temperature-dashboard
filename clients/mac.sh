#!/bin/bash
PI_IP="192.168.1.90"
TOKEN="G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb
DEVICE="mac"
# needs `brew install osx-cpu-temp`
raw=$(osx-cpu-temp) # e.g. "57.8°C"
temp_c=$(echo "$raw" | tr -d '°C' )
ts=$(date -u -Iseconds)
curl -s -X POST http://$PI_IP:5000/api/temps \
 -H "Content-Type: application/json" \
 -d "{\"device\":\"${DEVICE}\",\"temp_c\":${temp_c},\"ts\":\"${ts}\",\"token\":\"${TOKEN}\"}"
