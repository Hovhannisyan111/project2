"""
This file is for speech recognition
Created by: Arman Hovhannisyan
Date: 5 June
"""
import subprocess
import os
#import sys
import webbrowser
import speech_recognition as sr

def open_firefox():
    """
    Function: open_firefox
    Brief: opening firefox browser
    """
    try:
        subprocess.run(["firefox"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen(["firefox"])
    except FileNotFoundError:
        print("There is no firefox or not in path")
        exit()

def search_firefox(search_term):
    """
    Function: search_firefox
    Brief: searching what I say in firefox
    Params: search_term: what I said
    """
    try:
        url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
        webbrowser.open(url)
    except webbrowser.Error as error:
        print(f"An error occurred with the web browser: {error}")

def create_file(file_name):
    """
    Function: create_file
    Brief: creates a file
    Params: file_name: name of the file
    """
    try:
        with open(file_name, "w") as file:
            file.write("")
        print(f"File {file_name} created")
    except FileExistsError:
        print(f"File {file_name} already exists")
        exit()

def open_file(file_name):
    """
    Function: open_file
    Brief: opening file
    Params: file_name: name of the file
    """
    try:
        subprocess.Popen(["xdg-open", file_name])
    except FileNotFoundError:
        print(f"Can't open {file_name}")
        exit()

def read_file(file_name):
    """
    Function: read_file
    Brief: reads a file and prints its contents
    Params: file_name: name of the file to read
    """
    try:
        with open(file_name) as file:
            content = file.read()
            print(f"Contents of {file_name}")
            print(content)
    except FileNotFoundError:
        print(f"File {file_name} doesn't exist")
        exit()

def delete_file(file_name):
    """
    Function: delete_file
    Brief: deletes a file
    Params: file_name: the name of the file to delete
    """
    try:
        os.remove(file_name)
        print(f"File {file_name} deleted")
    except FileNotFoundError:
        print(f"File {file_name} doesn't exist")
        exit()

def create_dir(directory):
    """
    Function: create_dir
    Brief: creates a directory
    Params: directory: the path of the directory to create
    """
    try:
        os.makedirs(directory)
        print(f"Directory {directory} created")
    except FileExistsError:
        print(f"Directory {directory} already exists")
        exit()

def list_dir(directory):
    """
    Function: list_dir
    Brief: lists directory content
    Params: directory: what directory I said
    """
    try:
        files = os.listdir(directory)
        if files:
            print("Content of directory:")
            for file in files:
                print(file)
        else:
            print("Directory is empty")
    except FileNotFoundError:
        print(f"There is no {directory} directory")
        exit()

def main():
    """
    Function: main
    Brief: entry point
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        command = recognizer.recognize_google(audio).lower()
        print("You said: ", command)
        if "open firefox" in command:
            open_firefox()
        elif "search for" in command:
            search_term = command.split("search for ")[-1]
            search_firefox(search_term)
        elif "create file" in command:
            file_name = command.split("create file ")[-1]
            create_file(file_name)
        elif "open file" in command:
            file_name = command.split("open file ")[-1]
            open_file(file_name)
        elif "read file" in command:
            file_name = command.split("read file ")[-1]
            read_file(file_name)
        elif "delete file" in command:
            file_name = command.split("delete file ")[-1]
            delete_file(file_name)
        elif "create directory" in command:
            directory = command.split("create directory ")[-1]
            create_dir(directory)
        elif "list directory" in command:
            directory = command.split("list directory ")[-1]
            list_dir(directory)
        else:
            print("I don't understand the command")
    except sr.RequestError:
        print("Couldn't request results for speech recognition")
    except sr.UnknownValueError:
        print("Could not understand the audio")

if __name__ == "__main__":
    main()
