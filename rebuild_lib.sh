#!/bin/bash

set -e

echo "rebuilding box_auto package, hold on..."

pip3 uninstall -y box_auto
echo "--- package removed ---"

python3 setup.py sdist bdist_wheel
echo "--- rebuild successful ---"

pip3 install box_auto --no-index --find-links ./dist/
echo "--- package reinstalled ---"
