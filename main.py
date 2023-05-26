import csv
import random
from tkinter import *
from random import choice
import pandas as pd
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = "Ariel", 40, "italic"
WORD_FONT = "Ariel", 60, "bold"

# --------------------- GET WORD -------------------- #


def get_word():
    global timer, random_pair
    window.after_cancel(timer)
    random_pair = choice(word_pairs)
    card.itemconfig(img, image=front_image)
    card.itemconfig(lang, text="French", fill="#000000")
    card.itemconfig(word, text=f'{random_pair[0]}', fill="#000000")
    timer = window.after(3000, flip)


# --------------------- FLIP CARD -------------------- #


def flip():
    card.itemconfig(img, image=back_image)
    card.itemconfig(lang, text="English", fill="#ffffff")
    card.itemconfig(word, text=f'{random_pair[1]}', fill="#ffffff")


# --------------------- REMOVE CARD -------------------- #


def remove_card():
    word_pairs.remove(random_pair)
    with open("data/french_words.csv", "w", newline='', encoding='utf-8') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(["English", "French"])
        writer.writerows(word_pairs)
    get_word()


window = Tk()
window.title("Flashcards")
timer = window.after(3000, flip)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
card = Canvas()
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

card.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card.grid(column=0, row=0, columnspan=2)

vocab_list = pd.read_csv("data/french_words.csv")
word_pairs = [tuple(x) for x in vocab_list[["French", "English"]].values]
random_pair = choice(word_pairs)

img = card.create_image(400, 263, image=front_image)
lang = card.create_text(400, 150, text="French", font=(TITLE_FONT))
word = card.create_text(400, 263, text=f'{random_pair[0]}', font=(WORD_FONT))

image_correct = PhotoImage(file="images/right.png")
button_correct = Button(image=image_correct, highlightthickness=0, borderwidth=0, command=get_word)
button_correct.grid(column=1, row=1)

image_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=image_wrong, highlightthickness=0, borderwidth=0, command=get_word)
button_wrong.grid(column=0, row=1)

remove_button = Button(text="Remove Word", highlightthickness=0, borderwidth=0, command=remove_card,
                       font=("Ariel", 24, "bold"), fg="red", bg=BACKGROUND_COLOR)
remove_button.grid(column=0, row=2, columnspan=2)

get_word()
window.mainloop()


