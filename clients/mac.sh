#!/bin/bash
PI_IP="192.168.1.90"
TOKEN="G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb"
DEVICE="mac"

# Requires `brew install osx-cpu-temp`
raw_temp=$(osx-cpu-temp)               # e.g. "57.8°C"
temp_c=$(echo "$raw_temp" | tr -d '°C')

# Battery info from pmset
batt_info=$(pmset -g batt)
batt_percent=$(echo "$batt_info" | grep -Eo '[0-9]+%' | tr -d '%')
batt_status=$(echo "$batt_info" | grep -Eo 'charging|discharging|charged')

# Handle missing values safely
batt_percent=${batt_percent:-0}
batt_status=${batt_status:-unknown}

# Timestamp in UTC ISO8601
ts=$(date -u -Iseconds)

# Send to Pi API
curl -s -X POST "http://${PI_IP}:5000/api/temps" \
 -H "Content-Type: application/json" \
 -d "{
  \"device\": \"${DEVICE}\",
  \"temp_c\": ${temp_c},
  \"battery\": {\"percent\": ${batt_percent}, \"status\": \"${batt_status}\"},
  \"ts\": \"${ts}\",
  \"token\": \"${TOKEN}\"
}"
