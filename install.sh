#!/usr/bin/env bash

set -euo pipefail

if [[ ! -x collector.sh ]]; then
    chmod +x collector.sh
fi

if [[ ! -x analyze.sh ]]; then
    chmod +x analyze.sh
fi

SERVICE_NAME="latency-collector"
SYSTEMD_DIR="/etc/systemd/system"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER="$(id -un)"

echo "Installing ${SERVICE_NAME}..."
echo "Project directory : ${PROJECT_DIR}"
echo "User              : ${CURRENT_USER}"

#cat > "${PROJECT_DIR}/${SERVICE_NAME}.service" <<EOF
cat > /tmp/${SERVICE_NAME}.service <<EOF
[Unit]
Description=Network Latency Collector
After=network-online.target
Wants=network-online.target

[Service]
Type=simple

User=${CURRENT_USER}
WorkingDirectory=${PROJECT_DIR}

ExecStart=${PROJECT_DIR}/collector.sh

Restart=on-failure
RestartSec=5

StandardOutput=null
StandardError=append:${PROJECT_DIR}/collector.log

[Install]
WantedBy=multi-user.target
EOF

sudo install -m 644 /tmp/${SERVICE_NAME}.service \
    ${SYSTEMD_DIR}/${SERVICE_NAME}.service

#rm /tmp/${SERVICE_NAME}.service

#sudo ln -sf "${PROJECT_DIR}/${SERVICE_NAME}.service" \
#        /etc/systemd/system/${SERVICE_NAME}.service
        
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}

echo
echo "Installation complete."
echo
systemctl status ${SERVICE_NAME} --no-pager
