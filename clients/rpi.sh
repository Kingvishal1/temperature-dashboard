#!/bin/bash
PI_IP="192.168.1.90"
TOKEN="G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb"
DEVICE="rpi"
# read millidegrees
if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
  raw=$(cat /sys/class/thermal/thermal_zone0/temp)
  # many RPis report in millideg
  temp_c=$(awk "BEGIN{printf \"%.2f\", $raw/1000}")
else
  # fallback to vcgencmd if present
  temp_c=$(vcgencmd measure_temp 2>/dev/null | sed -E "s/temp=([0-9.]+)'C/\1/")
fi
ts=$(date -Iseconds)
curl -s -X POST http://$PI_IP:5000/api/temps \
  -H "Content-Type: application/json" \
  -d "{\"device\":\"${DEVICE}\",\"battery\":100,\"temp_c\":${temp_c},\"ts\":\"${ts}\",\"token\":\"${TOKEN}\"}"
