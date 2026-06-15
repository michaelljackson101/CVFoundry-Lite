#!/bin/bash
# Unified Streamlit Launcher Pattern for CVFoundry-Lite

PORT=""

# Parse args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --port) PORT="$2"; shift ;;
        *) ;;
    esac
    shift
done

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ -z "$PORT" ]; then
    # Try to resolve port via NetOps, fallback to 8566 if it fails or netops isn't available
    if command -v python3 &> /dev/null && python3 -c "import netops" &> /dev/null; then
        # Actually parse the port from resolve-port output. Here we assume JSON output.
        NETOPS_OUTPUT=$(python3 -m netops.cli resolve-port \
          --service-id foundry/cvfoundry-lite/ui \
          --repo CVFoundry-Lite \
          --type streamlit 2>/dev/null)
        
        # Simple extraction if jq isn't available
        PORT=$(echo "$NETOPS_OUTPUT" | grep -o '"port": *[0-9]*' | grep -o '[0-9]*')
    fi
    
    if [ -z "$PORT" ]; then
        PORT=8566
    fi
fi

echo "Starting Streamlit UI on port $PORT..."
python3 -m streamlit run ui.py --server.port "$PORT" --server.headless true
