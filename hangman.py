import random
import os
import time


def create_country_list(level):
    f = open("countries-and-capitals.txt", "r", encoding="utf8")
    file_read = f.read().split("\n")
    f.close()
    levels = {1: ["Europe", "Asia"], 2: ["Europe", "Asia", "America"],
              3: ["Europe", "Asia", "America", "Africa", "Oceania"]}
    countries = []
    for line in file_read:
        if " | " in line:
            cnc = line.split(" | ")
            if cnc[2] in levels.get(level):
                countries.append(cnc[0])
    return countries


def pick_country(countries):
    country = countries[int(len(countries) * random.random())]
    return country


def changechar(word: str, mask: str, ch: str):
    origin = list(word)
    underscores = list(mask)
    for index in range(len(origin)):
        if origin[index].lower() == ch.lower():
            underscores[index] = origin[index]
    return "".join(underscores)


def draw_hangman(attempts):
    stage = int(attempts / max_lives * 6)
    f = open("hangman.txt", "r", encoding="utf8")
    file_read = f.read().split("\n")
    f.close()
    for step in range(7):
        line = stage * 8 + 1 + step
        print("\033[{0};{1}H{2}".format(step + 5, 35, file_read[line]), end='', flush=True)


def get_masked():
    masked = ""
    for char in masked_word:
        masked += char + " "
    return masked


def main_menu():
    f = open("menu.txt", "r", encoding="utf8")
    file_read = f.read().split("\n")
    f.close()
    clear_game_screen()
    name = "Anonymous"
    user_choice = ""
    message1 = "Hello, " + name + "! Let's play hangman!"
    message2 = "Choose an option: "
    while user_choice.lower() not in ["e", "m", "d", "q"]:
        for line in range(len(file_read)):
            if len(file_read[line]) > 0:
                print("\033[{0};{1}H{2}".format(line + 3, 25, file_read[line]), end='', flush=True)
        print("\033[{0};{1}H{2}".format(14, 16, " " * 49), end='', flush=True)
        print("\033[{0};{1}H{2}".format(14, 16, message1), end='', flush=True)
        print("\033[{0};{1}H{2}".format(15, 16, " " * 49), end='', flush=True)
        print("\033[{0};{1}H{2}".format(15, 16, message2), end='', flush=True)
        user_choice = input()
        if message2 == "Enter your name: ":
            name = user_choice[:20].capitalize()
            if len(name) == 0:
                name = "Anonymous"
            message1 = "Hello, " + name + "! Let's play hangman!"
            message2 = "Choose an option: "
        elif user_choice.lower() == "n":
            message1 = " " * 48
            message2 = "Enter your name: "
    return (name, user_choice.lower())


def title():
    title_screen = []
    f = open("title_screen.txt", "r", encoding="utf8")
    file_read = f.read().split("\n")
    f.close()
    for line in file_read:
        title_screen.append(line.replace("\n", ""))
    screen = title_screen.copy()
    for line in range(25):
        print("\033[{0};{1}H{2}".format(line + 1, 1, screen[line]), end='', flush=True)
    title_text = []
    f = open("title.txt", "r", encoding="utf8")
    file_read = f.read().split("\n")
    f.close()
    for line in file_read:
        title_text.append(line.replace("\n", ""))
    for step in range(0, 19):
        screen = title_screen.copy()
        print("\033[{0};{1}H{2}".format(step - 1, 1, screen[step - 1]), end='')
        for row in range(0, 7):
            print("\033[{0};{1}H{2}".format(row + step, 3, title_text[row]), end='', flush=True)
        print("\033[{0};{1}H{2}".format(25, 81, " " * 7), end='')
        time.sleep(0.05)


def clear_game_screen():
    for line in range(3, 17):
        print("\033[{0};{1}H{2}".format(line, 7, " " * 66), end='', flush=True)


# game_start
os.system({"posix": "clear", "nt": "cls"}[os.name])

title()

while True:
    name, user_choice = main_menu()
    game_on = True
    if user_choice != "q":
        difficulty = {"e": 1, "m": 2, "d": 3}[user_choice]
        max_lives = lives = 9 - difficulty * 2
        word_to_guess = pick_country(create_country_list(difficulty))
        masked_word = "_" * len(word_to_guess)
        for char in [" ", "-"]:
            masked_word = changechar(word_to_guess, masked_word, char)
        wrong_answers = set()
        already_tried_letters = set()
        message1 = "Good luck!"
        message2 = ""
        input_char = ""
    else:
        break

    while game_on:
        if len(input_char) == 1:
            if input_char.lower() in already_tried_letters:
                message1 = "You already tried that one!"
                message2 = ""
            elif input_char.lower() in "abcdefghijklmnopqrstuvwxyz":
                already_tried_letters.add(input_char.lower())
                word_check = changechar(word_to_guess, masked_word, input_char)
                if word_check == masked_word:
                    wrong_answers.add(input_char.lower())
                    message1 = "No, there is no '" + input_char + "' in it!"
                    message2 = str(wrong_answers)
                    lives = 9 - difficulty * 2 - len(wrong_answers)
                else:
                    masked_word = word_check
                    message1 = "Yes, it has '" + input_char + "' in it!"
                    message2 = ""
        elif input_char.lower() == word_to_guess.lower():
            message1 = "Wow, you guessed it!"
            masked_word = word_to_guess
        elif len(input_char) > 1 and input_char.lower() != word_to_guess.lower():
            if input_char.lower() == "quit":
                message1 = "You Coward!"
                message2 = ""
                game_on = False
                user_choice = "q"
            elif input_char.lower() == "menu":
                game_on = False
            else:
                lives = 0

        if masked_word == word_to_guess:
            message2 = "Congratulations! You won, " + name + "!"
            game_on = False
        elif lives == 0:
            message1 = "R.I.P. " + name + "!"
            message2 = "It was " + word_to_guess + "!"
            game_on = False

        clear_game_screen()
        print("\033[{0};{1}H{2}".format(4, 16, name + "'s lives: ").replace("s's ", "s' ") +
              "❤ " * lives + "♡ " * (max_lives - lives), end='', flush=True)
        draw_hangman(max_lives - lives)
        print("\033[{0};{1}H{2}".format(12, 16 + (48 - len(get_masked())) // 2,
                                        get_masked()), end='', flush=True)
        print("\033[{0};{1}H{2}".format(13, 16, message1), end='', flush=True)
        print("\033[{0};{1}H{2}".format(14, 16, message2), end='', flush=True)

        if not game_on:
            break
        else:
            print("\033[{0};{1}H{2}".format(15, 16,
                  "Enter a <letter> or a <guess> or <'quit'> or <'menu'>: "), end='', flush=True)
            print("\033[{0};{1}H{2}".format(16, 16, ""), end='', flush=True)
            input_char = input()

    if user_choice != "q":
        print("\033[{0};{1}H{2}".format(15, 16, "Press enter to return to menu..."), end='',
              flush=True)
        input()
    else:
        break

print("\033[{0};{1}H{2}".format(26, 1, ""), end='', flush=True)
