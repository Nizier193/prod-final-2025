#!/bin/sh

case "$1" in
    "e2e")
        echo "Starting e2e tests. Have fun :)\n"
        python -m pytest e2e_tests/test_flows/test_creation_flow.py -v
        ;;
    "unit")
        echo "Starting unit_tests. Good luck =)\n"
        python -m pytest unit_tests -v
        ;;
    "all"|*)
        echo "Starting all tests. Good luck and have fun =D\n"
        python -m pytest e2e_tests/test_flows/test_creation_flow.py &&
        python -m pytest unit_tests -v
        ;;
esac
