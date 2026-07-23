#!/bin/bash

##############################################
# Configuration
##############################################

START_TIME="09:00"
END_TIME="16:05"

INTERVAL=5          # seconds

TARGET_FILE="targets.conf"
LOG_DIR="logs"

mkdir -p "$LOG_DIR"

##############################################

LOG_FILE="$LOG_DIR/$(date +%F).csv"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "timestamp,target,host,port,rtt_ms,loss_percent,status" > "$LOG_FILE"
fi

echo "==========================================="
echo "Latency Collector Started"
echo "Logging to $LOG_FILE"
echo "Sampling every $INTERVAL seconds"
echo "==========================================="

while true
do
    now=$(date +%H:%M)

    if [[ "$now" < "$START_TIME" ]]; then
        sleep 30
        continue
    fi

    if [[ "$now" > "$END_TIME" ]]; then
        echo "Finished for today."
        exit 0
    fi

    timestamp=$(date +"%Y-%m-%dT%H:%M:%S")

    while IFS=',' read -r name host port
    do
        [[ -z "$name" ]] && continue
        [[ "$name" =~ ^# ]] && continue

        output=$(sudo nping \
            --tcp \
            --count 1 \
            -p "$port" \
            "$host" 2>/dev/null)

        #####################################################
        # Extract RTT
        #####################################################

        rtt=$(echo "$output" |
            sed -n 's/.*Avg rtt: \([0-9.]*\)ms.*/\1/p')

        #####################################################
        # Extract packet loss
        #####################################################

        loss=$(echo "$output" |
            grep -oP 'Lost: \d+ \(\K[0-9.]+' )

        #####################################################
        # Determine status
        #####################################################

        if [[ -n "$rtt" ]]; then
            status="OK"
        else
            status="FAIL"
        fi

        echo "$timestamp,$name,$host,$port,$rtt,$loss,$status" \
            >> "$LOG_FILE"

        printf "%-8s %-16s:%-5s RTT=%-8s Loss=%-6s %s\n" \
            "$name" "$host" "$port" \
            "${rtt:-N/A}" "${loss:-100}%" "$status"

    done < "$TARGET_FILE"

    sleep "$INTERVAL"

done
