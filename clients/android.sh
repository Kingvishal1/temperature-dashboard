raw=$(cat /sys/class/thermal/thermal_zone0/temp)
temp=$(awk "BEGIN{printf \"%.2f\", $raw/1000}")
curl -X POST http://192.168.1.90:5000/api/temps -H "Content-Type: application/json" \
  -d "{\"device\":\"phone\",\"temp_c\":${temp},\"ts\":\"$(date -Iseconds)\",\"token\":\"G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb\"}"
