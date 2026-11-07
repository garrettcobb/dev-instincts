#!/bin/sh
# Run Dev Instincts' own tests (tests/test_*.py): one line per test, PASS or FAIL,
# then why each failure failed. Exits 1 if any test fails.
#   sh tools/check.sh          (from Git Bash; set PYTHON to pick the interpreter)
# Standard library only. Tests write only in scratch folders in the system temp dir.
here=$(cd "$(dirname "$0")/.." && pwd)
py=${PYTHON:-}
if [ -z "$py" ]; then
    # On Windows "python3" can be the Microsoft Store stub, so each candidate must run.
    for c in python3 python; do
        if command -v "$c" >/dev/null 2>&1 && "$c" -I -c 'import sys; sys.exit(sys.version_info < (3, 9))' >/dev/null 2>&1; then
            py=$c
            break
        fi
    done
fi
[ -n "$py" ] || { echo "FAIL  no working Python 3.9 or later (tried python3, python; set PYTHON)"; exit 1; }
cd "$here" || exit 1
"$py" -I -B tests/run.py
