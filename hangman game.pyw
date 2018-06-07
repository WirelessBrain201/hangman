import random
from tkinter import *
import tkinter.messagebox

class hangman:
    def __init__(self, master):
        file = open("wordbank.txt", "r")
        self.word_bank = file.readlines()
        file.close()
        for i in range(999):
            self.word_bank[i] = self.word_bank[i][:-1]
        self.master = master
        self.master.title("Hangman")
        self.master.iconbitmap("logo.ico")
        self.word = self.word_bank[random.randint(0, 999)].lower()
        self.word_letters = list(self.word)
        self.incorrect_count = 0
        self.guessed_letters = []
        self.incorrect_guesses = []
        self.display_word = ["_" for i in range(len(self.word))]

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu.add_command(label="New game", command=self.new_game)

        self.canvas = Canvas(self.master, height=400, width=400)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.main_word = Label(self.master, text="{}".format("".join(self.display_word)))
        self.main_word.grid(row=1, column=0, columnspan=3, sticky=N) 
        
        self.prompt = Label(self.master, text="Pick a letter to guess")
        self.prompt.grid(row=2, column=0)
        
        self.userletter = Entry(self.master)
        self.userletter.grid(row=2, column=1)

        self.button = Button(self.master, text="Guess letter", command=self.guess)
        self.button.grid(row=2, column=2)

        self.history = Label(self.master, text="Incorrect guesses: ")
        self.history.grid(row=3, column=0, columnspan=3,  sticky=W)

    def guess(self):
        self.user_guess = self.userletter.get().lower()
        if len(self.user_guess) > 1:
            self.userletter.delete(0, len(self.user_guess))
            tkinter.messagebox.showinfo("Message", "Please only enter one letter")
        elif len(self.user_guess) == 0:
            pass
        elif not self.user_guess.isalpha():
            self.userletter.delete(0, len(self.user_guess))
            tkinter.messagebox.showinfo("Message", "Please enter a letter")
        elif self.user_guess in self.guessed_letters:
            self.userletter.delete(0, len(self.user_guess))
            tkinter.messagebox.showinfo("Message", "You've already guessed this letter!")
        elif self.user_guess in self.word:
            self.guessed_letters.append(self.user_guess)
            for i in range(self.word.count(self.user_guess)):
                self.guess_index = self.word_letters.index(self.user_guess)
                self.word_letters[self.guess_index] = "*"
                self.display_word.pop(self.guess_index)
                self.display_word.insert(self.guess_index, self.user_guess)
                self.main_word.config(text="{}".format("".join(self.display_word)))
            self.userletter.delete(0, len(self.user_guess))
            if "_" not in self.display_word:
                self.victory()
        else:
            self.guessed_letters.append(self.user_guess)
            self.incorrect_guesses.append(self.user_guess)
            self.display_str = "Incorrect guesses: {}".format(", ".join(self.incorrect_guesses))
            self.history.config(text=self.display_str)
            self.userletter.delete(0, len(self.user_guess))
            self.incorrect_count += 1
            self.draw()

    def draw(self):
        if self.incorrect_count == 1:
            self.canvas.create_line(200, 0, 200, 50)
        if self.incorrect_count == 2:
            self.canvas.create_oval(165, 50, 235, 120)
        if self.incorrect_count == 3:
            self.canvas.create_line(200, 120, 200, 245)
        if self.incorrect_count == 4:
            self.canvas.create_line(200, 150, 120, 200)
        if self.incorrect_count == 5:
            self.canvas.create_line(200, 150, 280, 200)
        if self.incorrect_count == 6:
            self.canvas.create_line(200, 245, 120, 340)
        if self.incorrect_count == 7:
            self.canvas.create_line(200, 245, 280, 340)
            self.loss()

    def new_game(self):
        self.answer = tkinter.messagebox.askquestion("Start a new game?", "Are you sure you want to start a new game? Your current progress will be lost!")
        if self.answer == "yes":
            self.reset()
        else:
            return

    def victory(self):
        self.answer = tkinter.messagebox.askquestion("Congatulations!", "Congratulations, you've guessed the word! It was \"{}\" Do you want to play again?".format(self.word))
        if self.answer == "yes":
            self.reset()
        else:
            self.quit()

    def loss(self):
        self.main_word.config(text=self.word)
        self.answer = tkinter.messagebox.askquestion("Again?", "Looks like you weren't able to guess the word! It was \"{}\" Do you want to play again?".format(self.word))
        if self.answer == "yes":
            self.reset()
        else:
            self.quit()

    def quit(self):
        self.master.destroy()

    def reset(self):
        self.word = self.word_bank[random.randint(0, 999)].lower()
        self.word_letters = list(self.word)
        self.incorrect_count = 0
        self.guessed_letters = []
        self.incorrect_guesses = []
        self.display_word = ["_" for i in range(len(self.word))]
        self.answer = None

        self.canvas = Canvas(self.master, height=400, width=400)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.history.config(text="Incorrect guesses: ")

        self.userletter.delete(0, len(self.userletter.get()))

        self.main_word.config(text="{}".format("".join(self.display_word)))


top = Tk()
h = hangman(top)
mainloop()
        
