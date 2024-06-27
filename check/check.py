"""
This file is for spellchecker
Created by: Arman Hovhannisyan
Date: 14 June
"""

import argparse
from spellchecker import SpellChecker

def get_arguments():
    """
    Function: get_arguments
    Brief: parses arguments
    Return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="This is input file name")
    parser.add_argument("-o", "--output", required=True, help="This is output file name")
    args = parser.parse_args()
    input_file = args.file
    output_file = args.output
    return input_file, output_file

def get_correct(word, arajark):
    """
    Function: get_correct
    Brief: Shows wrong written words and suggestions and asks to choose right answer
    Params: word: the wrong word
            arajark: suggested word
    Return: the choosen word
    """
    print("Misspelled word: ", word)
    if not arajark:
        print("No suggestions available")
        return word

    print("Suggestion:")
    arajarki_list = list(arajark)
    for i in range(len(arajarki_list)):
        print(f"{i + 1}. {arajarki_list[i]}")
    choice = input(f"Choose the right version (1-{len(arajarki_list)}), otherwise it skips: ")
    if choice.isdigit() and 1 <= int(choice) <= len(arajarki_list):
        return arajarki_list[int(choice) -1]
    else:
        return word

def correct_word(spell, word):
    """
    Fuanction: correct_word
    Brief: checks word and corrects if necessary
    Params: spell: SpellChecker item
            word: the word to check
    Return: corrected word
    """
    if spell.correction(word) == word:
        return word
    arajark = spell.candidates(word)
    return get_correct(word, arajark)

def get_content(input_file):
    """
    Function: get_content
    Brief: function returns the whole content of the file
    Params: input_file: input file name
    Return: file content as a string
    """
    try:
        with open(input_file) as fin:
            return fin.read()
    except FileNotFoundError:
        print("No such file")
    return ""

def write_file(content, output_file):
    """
    Function: write_file
    Brief: writes corrected content to the file
    Params: content: the content of input file
            output_file: output file name
    """
    spell = SpellChecker()
    words = content.split()
    corrected_words = [correct_word(spell, word) for word in words]

    corrected_content = " ".join(corrected_words)

    with open(output_file, "w") as fout:
        fout.write(corrected_content)

def main():
    """
    Fuantion: main
    Brief: Entery point
    """
    input_file, output_file = get_arguments()
    content = get_content(input_file)
    if content:
        write_file(content, output_file)

if __name__ == "__main__":
    main()
