Speech Rcognition

Creted by: Arman Hovhannisyan
Date: 05.06.2024

Description

This script uses speech recognition to perform various file and browser operations based on voice commands. It can open Firefox, search the web, create, open, read, and delete files, and create and list directories.

Requirments

Python 3.x
SpeechRecognition module(3.10.4) - "pip install SpeechRecognition"
PyAudio module(0.2.14) - "pip install PyAudio"
Firefox browser

Run the script

python3 speech.py

Voice Commands

open firefox: Opens the Firefox browser.
search for <term>: Searches the specified term in Firefox.
create file <filename>: Creates a file with the specified name.
open file <filename>: Opens the specified file in current directory.
read file <filename>: Reads and prints the contents of the specified file.
delete file <filename>: Deletes the specified file in current directory.
create directory <directory>: Creates a directory with the specified path.
list directory <directory>: Lists the contents of the specified directory.

Files 
speech.py: Python script
