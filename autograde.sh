#!/bin/bash
# ============================================================
# Project: Kahoot to Classroom
# Script: autograde.sh
# Purpose: Run autograding workflow (with --autograde)
# Author: jesus.loport
# ============================================================

# Usage:
#   ./autograde.sh -c config/ISW17.ini
#   ./autograde.sh -h
#
# Notes:
#   - Requires Python 3 and pandas installed.
#   - The -c (config) flag is mandatory unless -h is used.
#   - Reports (-r) are optional in autograde mode, since grading
#     will be handled via Google Classroom API.

# Parse arguments
while getopts "c:r:h" opt; do
  case $opt in
    c) CONFIG_FILE="$OPTARG" ;;
    r) REPORT_FILE="$OPTARG" ;;   # optional, but allowed
    h) python3 src/main.py -h; exit 0 ;;
    \?) python3 src/main.py -h; exit 1 ;;
  esac
done

# Validate arguments
if [ -z "$CONFIG_FILE" ]; then
  echo "error: -c <config.ini> must be provided"
  python3 src/main.py -h
  exit 1
fi

# Run Python script in autograde mode
if [ -z "$REPORT_FILE" ]; then
  python3 src/main.py -c "$CONFIG_FILE" --autograde
else
  python3 src/main.py -c "$CONFIG_FILE" -r "$REPORT_FILE" --autograde
fi