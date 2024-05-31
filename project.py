"""
Name of the project: "WordGuesser"

Made by: Kateryna Ivanchuk

City and country: Heimstetten, 85551, Germany

Github: https://github.com/katerynaivanchuk
EdX: https://profile.edx.org/u/kateryna_ivanchuk

Date of recording: 29.03.2024
"""

import sys
import random
import requests
import re
from bs4 import BeautifulSoup


def main():
    print()
    print("Welcome to WordGuesser!")
    correct_word, guess_tires = choose_difficulty_level()
    print("Game begins! Guess the word: ")
    result = game_begins(correct_word,guess_tires)
    print(result)
    word = correct_word.lower()
    meaning = get_word_meaning(word)
    print(f"\033[1m{correct_word}\033[0m is {meaning}")
    sys.exit()


def game_begins(correct_word, guess_tries):
    guess_tries = guess_tries
    guess_word = ["_ " for _ in correct_word]

    while guess_tries != 0:
        print()
        print(f"You have {guess_tries} tries!")

        print(' '.join(guess_word))

        word = get_valid_word_input(correct_word)

        if word == correct_word:
            guess_word = word
        else:
            correct_letters_count = {letter: correct_word.count(letter) for letter in set(correct_word)}
            incorrect_letters = set()
            for i in range(len(word)):
                if word[i] in correct_word:
                    if word[i] == correct_word[i]:
                        guess_word[i] = word[i]
                    elif word[i] in correct_word and guess_word[i] == '_ ':
                        if word.count(word[i]) > correct_letters_count[word[i]]:
                            if word[i] not in incorrect_letters:
                                print(f"You have too many {word[i]}'s!")
                                incorrect_letters.add(word[i])
                        else:
                            print(f"{word[i]} is in incorrect position!")

        # check if user guessed the word
        if ''.join(guess_word).replace(' ', '') == correct_word:
            message = "Congratulations!" + "\n" + "The word is: " + guess_word
            return message

        guess_tries -= 1

        if guess_tries == 0:
            message = "Game over! The word was: " + correct_word
            return message


def get_word(word_length):
    words = sort_words()
    words_of_desired_length = words[word_length]
    random_word = random.choice(words_of_desired_length)
    return random_word.upper()


def get_valid_word_input(correct_word):
    while True:
        word = input("Guess a word: ").upper()
        if len(word) != len(correct_word):
            print("Invalid word length! Try again:")
        else:
            return word


def sort_words():
    words_by_length = {}
    with open("game_words.txt", "r") as file:
        for word in file:
            word = word.strip()
            word_length = len(word)

            if word_length not in words_by_length:
                words_by_length[word_length] = [word]
            else:
                words_by_length[word_length].append(word)
    return words_by_length


def get_word_meaning(word):
    url = f"https://www.dictionary.com/browse/{word}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        div_elements = soup.find("div", {"data-type": "word-definition-content"})

        meaning_element = div_elements.find("p")

        if meaning_element:
            meaning_text = meaning_element.text
            match = re.search(r'[^(:.;,\n]*', meaning_text)
            if match:
                return match.group(0).rstrip()
            else:
                return Exception("Meaning not found")
        else:
            return Exception("Meaning not found")
    else:
        return Exception("Failed to retrieve page")


def choose_difficulty_level():
    level = int(input("Choose level of difficulty:\n"
          "1 - easy\n"
          "2 - moderate\n"
          "3 - challenging: "))

    match level:
        case 1:
            random_length = random.randint(1,4)
            correct_word = get_word(random_length)
            guess_tries = 10
            return correct_word, guess_tries
        case 2:
            random_length = random.randint(5, 8)
            correct_word = get_word(random_length)
            guess_tries = 15
            return correct_word, guess_tries
        case 3:
            random_length = random.randint(9, 14)
            correct_word = get_word(random_length)
            guess_tries = 20
            return correct_word, guess_tries




if __name__ == "__main__":
    main()