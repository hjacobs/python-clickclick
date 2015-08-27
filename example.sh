#!/bin/bash
set -x

# Print Usage
./example.py

# Print Message 'too many matches'
./example.py l

# Print Localtime
./example.py lo

# Print listing with multiple outputformats
./example.py li
./example.py li -o tsv
./example.py li -o json
./example.py li -o yaml

# Print Action messages
./example.py work-

# print Choice prompt
echo 2 | ./example.py work_ 15.4
echo 3 | ./example.py work_ 15.4

# Print Action messages with multiple output format
./example.py output
./example.py output -o tsv
./example.py output -o json
./example.py output -o yaml

exit 0
