"""
This file is for Tkinter game: Who wants to ba a millinoare
Created by: Arman Hovhannisyan
Date: 17.06.2024
"""
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

class Millionaire:
    def __init__(self, master, questions_file, top_players_file, num_questions=10):
        """
        Function: __init__
        Brief: initializes the Millionaire game
        Params: master: root window
                questions_file: file containing questions
                top_players_file: file to store top players scores
                num_questions: number of questions in the game
        """
        self.master = master
        self.questions_file = questions_file
        self.top_players_file = top_players_file
        self.num_questions = num_questions
        self.questions = self.get_content(self.questions_file)
        self.quest = self.select_questions(self.questions, self.num_questions)
        self.questions_dict = self.define_questions(self.quest)
        self.score = 0
        self.current_index = 0
        self.money = [500, 1000, 5000, 10000, 50000, 100000, 300000, 500000, 800000, 1000000]

        self.help_50_used = False
        self.help_audience_used = False
        self.help_friend_used = False
        self.used_help = False

        self.player_name = self.get_name()
        self.setup_window()
        self.ask_question()

    def setup_window(self):
        """
        Function: setup_window
        Brief: sets up the main game window and other elements.
        """
        self.master.title("Who Wants to Be a Millionaire")
        self.master.geometry("600x500")

        self.question_frame = tk.Frame(self.master)
        self.question_frame.pack(pady=20)

        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 20))
        self.question_label.pack()

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=20)

        self.answer_buttons = []
        button_width = 20
        button_height = 2
        for i in range(4):
            button = tk.Button(self.buttons_frame, text="",
                    command=lambda ind=i: self.check_answer(ind),
                    bg="blue", font=("Arial", 12, "bold"), width=button_width, height=button_height)
            button.pack(side=tk.TOP, pady=5)
            self.answer_buttons.append(button)

        self.help_frame = tk.Frame(self.master)
        self.help_frame.pack(pady=20)

        self.help_50_button = tk.Button(self.help_frame, text="50/50",
                command=self.use_50, font=("Arial", 10),
                width=button_width, height=button_height, bg="green")
        self.help_50_button.pack(side=tk.LEFT, padx=10)

        self.help_audience_button = tk.Button(self.help_frame, text="Audience",
                command=self.use_audience, font=("Arial", 10),
                width=button_width, height=button_height, bg="green")
        self.help_audience_button.pack(side=tk.LEFT, padx=10)

        self.help_friend_button = tk.Button(self.help_frame, text="Call a Friend",
                command=self.use_friend, font=("Arial", 10),
                width=button_width, height=button_height, bg="green")
        self.help_friend_button.pack(side=tk.LEFT, padx=10)

    def get_name(self):
        """
        Function: get_name
        Brief: asks the player to enter your name
        Return: player's name
        """
        name = simpledialog.askstring("Player Name", "Enter your name")
        if name:
            return name
        else:
            return "Player"

    def get_content(self, fname):
        """
        Function: get_content
        Brief: reads the content of a file
        Params: the name of file to read
        Return: a list of lines from the file
        """
        with open(fname) as file:
            return file.readlines()

    def select_questions(self, questions, num_questions):
        """
        Function: select_questions
        Brief: selects random questions
        Params: questions: the list of all questions
                num_questions: the number of questions to select
        Return: a list of selected questions
        """
        ind = random.sample(range(len(questions)), num_questions)
        quest = [questions[i].strip() for i in ind]
        return quest

    def define_questions(self, quest):
        """
        Function: define_questions
        Brief: defines the questions and answers dictionary
        Params: quest: the list of selected questions
        Return: dictionary of questions with their answers
        """
        questions_dict = {}
        for question in quest:
            q, a = question.split("?")
            answers = [answer.strip() for answer in a.split(",")]
            questions_dict[q.strip()] = {"correct": answers[0], "all_answers": answers}
        return questions_dict

    def ask_question(self):
        """
        Function: ask_question
        Brief: displays the current question and possible answers
        """
        self.used_help = False
        if self.current_index < self.num_questions:
            question = list(self.questions_dict.keys())[self.current_index]
            answers = self.questions_dict[question]["all_answers"]
            if self.question_label.winfo_exists():
                self.question_label.config(text=question)
            random.shuffle(answers)
            for i in range(len(answers)):
                if self.answer_buttons[i].winfo_exists():
                    self.answer_buttons[i].config(text=answers[i], state=tk.NORMAL, bg="lightblue")
        else:
            self.end_game()

    def check_answer(self, selected_index):
        """
        Function: check_answer
        Brief: checks if the selected answer is correct and updates the score
        Params: selected_index: the index of the selected answer button
        """
        if self.current_index < self.num_questions:
            question = list(self.questions_dict.keys())[self.current_index]
            correct_answer = self.questions_dict[question]["correct"]
            selected_answer = self.answer_buttons[selected_index].cget("text")
            if selected_answer == correct_answer:
                self.score += 1
            else:
                self.end_game()
            self.next_question()

    def next_question(self):
        """
        Function: next_question
        Brief: moves to the next question or ends the game
        """
        self.current_index += 1
        if self.current_index < self.num_questions:
            self.ask_question()
        else:
            self.end_game()

    def use_50(self):
        """
        Function: use_50
        Brief: uses the 50/50 help to disable two incorrect answer buttons
        """
        if self.used_help:
            messagebox.showinfo("Help used", "You already used help for this question")
            return

        if not self.help_50_used:
            self.help_50_used = True
            self.used_help = True
            self.help_50_button.config(state=tk.DISABLED, bg="gray")
            if self.current_index < self.num_questions:
                question = list(self.questions_dict.keys())[self.current_index]
                correct_answer = self.questions_dict[question]["correct"]
                all_answers = self.questions_dict[question]["all_answers"]
                wrong_answers = [i for i in all_answers if i != correct_answer]
                if len(wrong_answers) >= 2:
                    remove_answers = random.sample(wrong_answers, 2)
                    for button in self.answer_buttons:
                        if button.cget("text") in remove_answers:
                            button.config(state=tk.DISABLED, bg="gray")
        else:
            messagebox.showinfo("Help used", "You already used 50/50")

    def use_audience(self):
        """
        Function: use_audience
        Brief: uses the audience help to show a poll result
        """
        if self.used_help:
            messagebox.showinfo("Help Used", "You already used help for this question")
            return

        if not self.help_audience_used:
            self.help_audience_used = True
            self.used_help = True
            self.help_audience_button.config(state=tk.DISABLED, bg="gray")
            if self.current_index < self.num_questions:
                question = list(self.questions_dict.keys())[self.current_index]
                all_answers = self.questions_dict[question]["all_answers"]
                percentages = [random.randint(0, 100) for _ in range(len(all_answers))]
                total = sum(percentages)
                percents = [int(i * 100 / total) for i in percentages]
                while sum(percents) != 100:
                    difference = 100 - sum(percents)
                    percents[random.choice(range(len(percents)))] += difference
                poll_result = {all_answers[i]: percents[i] for i in range(len(all_answers))}
                audience_poll = "\n".join([f"{i}: {poll_result[i]}%" for i in poll_result])
                messagebox.showinfo("Audience Poll", f"Audience poll: \n{audience_poll}")
        else:
            messagebox.showinfo("No help left", "You already used Audience help")

    def use_friend(self):
        """
        Function: use_friend
        Brief: sses the call a friend help to show the correct answer
        """
        if self.used_help:
            messagebox.showinfo("Help Used", "You already used help for this question")
            return

        if not self.help_friend_used:
            self.help_friend_used = True
            self.used_help = True
            self.help_friend_button.config(state=tk.DISABLED, bg="gray")
            if self.current_index < self.num_questions:
                question = list(self.questions_dict.keys())[self.current_index]
                correct_answer = self.questions_dict[question]["correct"]
                messagebox.showinfo("Call a Friend", f"Friend: '{correct_answer}'")
        else:
            messagebox.showinfo("No help left", "You already used Call a Friend help")

    def end_game(self):
        """
        Function: end_game
        Brief: ends the game, saves the score, and shows the top players
        """
        self.save_score()
        self.show_players()
        final_score = self.money[self.score - 1] if self.score > 0 else 0
        messagebox.showinfo("Your score", f"{self.player_name}: ${final_score}")
        self.master.destroy()

    def save_score(self):
        """
        Function: save_score
        Brief: saves the player's score to the top players file
        """
        final_score = self.money[self.score - 1] if self.score > 0 else 0

        with open(self.top_players_file, "a") as file:
            file.write(f"{self.player_name}: ${final_score}\n")

    def show_players(self):
        """
        Function: show_players
        Brief: displays the top players scores
        """
        try:
            with open(self.top_players_file) as file:
                scores = file.readlines()

            scores_list = []
            for score in scores:
                try:
                    name, earn = score.strip().split(": $")
                    scores_list.append((name, int(earn)))
                except ValueError:
                    continue

            top_scores = sorted(scores_list, key=lambda x: x[1], reverse=True)[:5]
            top_scores_str = "\n".join([f"{name}: ${earn}" for name, earn in top_scores])
            messagebox.showinfo("Top Players", f"\n{top_scores_str}")
        except FileNotFoundError:
            messagebox.showinfo("No scores", "Nothing to show")

def main():
    """
    Function: main
    Brief: entery point
    """
    root = tk.Tk()
    millionare = Millionaire(root, "questions.txt", "top.txt")
    root.mainloop()

if __name__ == "__main__":
    main()
