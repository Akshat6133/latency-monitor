command -v python3 >/dev/null ||
{
    echo "python3 is required."
    exit 1
}

python3 -m pip --version >/dev/null ||
{
    echo "pip is required."
    exit 1
}

if [[ ! -d env ]]; then
    python3 -m venv .latency-collector-env
fi

source .latency-collector-env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

 #!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

exec "${PROJECT_DIR}/.latency-collector-env/bin/python" \
     "${PROJECT_DIR}/tools/latency.py" "$@"
     
 python3 tools/latency.py     --input logs/2026-07-15.csv     --target Google     --target NSE     --from-time 09:00     --to-time 16:00     --output report

