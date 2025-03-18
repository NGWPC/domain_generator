#!/bin/bash
set -e

source /opt/venv/bin/activate

if [ "$VERBOSE" = "true" ]; then
  echo "Python $(python --version)"
  echo "Using project virtual environment: /opt/venv"
  echo "UV available at: /opt/uv_venv/bin/uv"
  echo "Working directory: $(pwd)"
  echo "Installed packages in project venv:"
  pip list
fi

exec "$@"
