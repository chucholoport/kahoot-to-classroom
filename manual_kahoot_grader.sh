#!/bin/bash
# ============================================================
# Project: Kahoot to Classroom
# Script: autograde.sh
# Purpose: Run autograding workflow (with --autograde)
# Author: jesus.loport
# ============================================================

# Usage:
#   ./autograde.sh -c config/ISW17.ini -r reports/ISW17_Kahoot.xlsx
#   ./autograde.sh -h
#
# Notes:
#   - Requires Python 3 and pandas installed.
#   - The -c (config) and -r (report) flags are mandatory unless -h is used.
#   - Multiple reports can be passed after -r.

# Parse arguments
while getopts "c:r:h" opt; do
  case $opt in
    c) CONFIG_FILE="$OPTARG" ;;
    r) REPORT_FILE="$OPTARG" ;;
    h) python3 src/main.py -h; exit 0 ;;
    \?) python3 src/main.py -h; exit 1 ;;
  esac
done

# Validate arguments
if [ -z "$CONFIG_FILE" ] || [ -z "$REPORT_FILE" ]; then
  echo "error: both -c <config.ini> and -r <report.xlsx> must be provided"
  python3 src/main.py -h
  exit 1
fi

# Run Python script in autograde mode
python3 src/main.py -c "$CONFIG_FILE" -r "$REPORT_FILE"