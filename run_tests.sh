#!/bin/bash

coverage erase
# if no arguments are given, run all tests
if [ "$#" -eq  "0" ];
then coverage run -m pytest

# if a pattern argument is given, run tests with names matching the pattern
elif [ "$#" -eq  "1" ];
then coverage run -m pytest -k $1 --setup-show

else echo Too many arguments!
fi

echo -e '\v'
echo "Checking code style"
flake8 --ignore None
echo -e '\v'

coverage report
