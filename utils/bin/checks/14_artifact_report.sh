#!/usr/bin/env bash
# Description: Report old browser artifacts; age never causes failure or deletion
set -e
python utils/lib/artifacts.py

