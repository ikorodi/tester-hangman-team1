import random
import os


def count_end(level):
    f = open("Countries-Continents.txt")
    text = (f.read())
    lst = text.split("\n")
    levels = {1: ["Europe", "Asia"], 2: ["Europe", "Asia", "America"],
              3: ["Europe", "Asia", "America", "Africa", "Oceania"]}
    countries = []
    for item in lst:
        if " | " in item:
            cnc = item.split(" | ")
            if cnc[2] in levels.get(level):
                countries.append(cnc[0])
    return countries


def random_country(countries):
    country = countries[int(len(countries) * random.random())]
    return country


def changechar(word: str, mask: str, ch: str, wrong_answer: set):
    origin = list(word)
    underscores = list(mask)
    good_guess = False
    for index in range(len(origin)):
        if origin[index].lower() == ch.lower():
            underscores[index] = origin[index]
            good_guess = True
    if not good_guess:
        wrong_answer.add(ch)
    return "".join(underscores)


def draw_hangman(attempts):
    stages = [
        # Stage 0: Empty hangman
        """
         +---+
         |   |
             |
             |
             |
             |
        =========
        """,
        # Stage 1: Head
        """
         +---+
         |   |
         O   |
             |
             |
             |
        =========
        """,
        # Stage 2: Body
        """
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========
        """,
        # Stage 3: One arm
        """
         +---+
         |   |
         O   |
        /|   |
             |
             |
        =========
        """,
        # Stage 4: Two arms
        """
         +---+
         |   |
         O   |
        /|\  |
             |
             |
        =========
        """,
        # Stage 5: One leg
        """
         +---+
         |   |
         O   |
        /|\  |
        /    |
             |
        =========
        """,
        # Stage 6: Two legs (game over)
        """
         +---+
         |   |
         O   |
        /|\  |
        / \  |
             |
        =========
        """
    ]
    stage = int(attempts / max_lives * 6)
    print(stages[stage])


# game_start
os.system({"nt": "cls", "posix": "clear"}[os.name])
name = input("What is your name? ")
if name == "":
    name = "Anonymous"

print("Hello, " + name + "!\nLet's play hangman!")

difficulty = 0
while difficulty not in ["1", "2", "3"]:
    difficulty = input("Choose difficulty level: 1-3!")
difficulty = int(difficulty)

max_lives = lives = 9 - difficulty * 2
word = (random_country(count_end(difficulty)))
mask = "_" * len(word)
mask = changechar(word, mask, " ", set())
wrong_answer = set()

while (lives > 0):
    os.system({"nt": "cls", "posix": "clear"}[os.name])
    print(name + "'s lives: " + " ❤ " * lives)
    draw_hangman(len(wrong_answer))
    if len(wrong_answer) >= 1:
        print("wrong: " + str(wrong_answer))
    print(mask)
    if (mask == word):
        break
    input_char = input("Press a key: ")
    if input_char.lower() == "quit":
        break
    elif len(input_char) == 1:
        mask = changechar(word, mask, input_char, wrong_answer)
        lives = 9 - difficulty * 2 - len(wrong_answer)

if lives == 0:
    os.system({"nt": "cls", "posix": "clear"}[os.name])
    print("Game Over " + name)
    draw_hangman(max_lives)
elif input_char.lower() == "quit":
    print("You Coward!")
else:
    print("Congratulation!")
