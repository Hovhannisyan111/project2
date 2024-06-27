Spell Checker

Created by: Arman Hovhannisyan
Date: 14.06.2024

Description

This script is a spellchecker that reades a input file checks for misspelled words and provides suggestions for corrections.The user can choose the correct version or skip leaving unchanged. Then corrected content is written to an output file.

Requirments

Python 3.x
SpellChecker module(0.8.1) - "pip install pyspellchecker"

run the script

python3 check.py -f input.txt -o out.txt

Arguments

"-f", "--file": Input file name
"-o". "--output": Output file name

Files

check.py: Python script
r.txt: File contaning text with mispelled words
