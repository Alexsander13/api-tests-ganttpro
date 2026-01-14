#!/usr/bin/env bash

# GanttPRO API Test Runner
# Unified test execution for local and CI environments
# Generates: junit.xml, report.html, allure-results/

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create reports directory
mkdir -p reports

echo -e "${YELLOW}Running GanttPRO API Tests...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run pytest with all report generators
python -m pytest \
  --tb=short \
  --junitxml=reports/junit.xml \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  tests/

TEST_EXIT_CODE=$?

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed or were skipped${NC}"
    echo -e "Exit code: $TEST_EXIT_CODE"
fi

echo ""
echo "📊 Reports generated:"
echo "  • JUnit XML: reports/junit.xml"
echo "  • HTML Report: reports/report.html"
echo "  • Allure Results: reports/allure-results/"
echo ""

exit $TEST_EXIT_CODE
