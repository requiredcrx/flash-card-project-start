from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
to_learn = {}

# _____________________READ FILE________________________________________
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ______________________Random words____________________________________
def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


# ________________FLIP CARD__________________________________________
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_word["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    global to_learn
    to_learn.remove(current_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


# ______________________________UI SETUP_________________________________
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50,  bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="English", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2, sticky="EW")

# Buttons
right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
left_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
left_button.grid(row=1, column=0)

next_card()
window.mainloop()
