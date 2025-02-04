import os, random, json
from colorama import Fore, init

class Wordle():
    def __init__(self):
        self.clear = lambda: os.system("clear")
        self.words = [
            "about", "after", "again", "below", "could", "every", "first", "found", "great",
            "house", "large", "never", "other", "place", "point", "right", "small", "sound",
            "still", "table", "these", "thing", "think", "three", "water", "where", "which",
            "world", "would", "years", "apple", "beach", "birth", "black", "brown", "carry",
            "chain", "clean", "clear", "close", "dance", "dream", "drink", "earth", "eight",
            "field", "fight", "floor", "force", "forth", "fresh", "front", "glass", "green",
            "happy", "heart", "horse", "human", "image", "large", "learn", "light", "magic",
            "metal", "music", "north", "ocean", "order", "paper", "party", "plant", "press",
            "queen", "quick", "reach", "river", "round", "sense", "seven", "shall", "shape",
            "share", "sharp", "sheet", "shift", "shoot", "short", "since", "skill", "sleep",
            "smile", "south", "space", "speak", "speed", "spend", "sport", "staff", "stage",
            "stand", "start", "state", "steam", "stone", "story", "table", "taste", "teach",
            "thank", "their", "there", "these", "thick", "thing", "think", "third", "three",
            "throw", "tiger", "title", "today", "topic", "total", "touch", "trade", "train",
            "treat", "trend", "trust", "truth", "twice", "under", "until", "upper", "usual",
            "valid", "value", "video", "visit", "voice", "watch", "water", "where", "which",
            "whole", "world", "worry", "worse", "worth", "would", "write", "wrong", "years",
            "young", "youth"]
        self.word = self.words[random.randrange(0,len(self.words))]
        self.triedWords = ["_ _ _ _ _ " for i in range(0,5)]
        self.guessed = False

    def game(self, loop):
        self.guess = input("Word: ")
        self.guessedWord = ""
        self.allWords = []
        with open("file.json","r") as file:
            self.allWords = json.load(file)['words']

        if len(self.guess) == 5 and self.guess in self.allWords:
            for i in range(0,len(self.guess)):
                if self.guess[i] in self.word:
                    if self.guess[i] == self.word[i]:
                        # Letter should be green if letter in word and in right pos
                        self.guessedWord += Fore.GREEN + self.guess[i] + " "
                    else:
                        # Letter should be yellow if letter is in word but not in the right pos
                        self.guessedWord += Fore.YELLOW + self.guess[i] + " "
                else:
                    # Letter should be grey if letter not in word
                    self.guessedWord += "\033[90m" + self.guess[i] + " "
            self.triedWords[loop] = self.guessedWord
            if self.guess == self.word:
                self.guessed = True
                self.guessedWord = Fore.GREEN + " ".join(self.guess)  # Make entire word green
                self.triedWords[loop] = self.guessedWord
                return True
        else:
            print("\nInvalid word!\nThe word should be 5 characters long!\nAnd has to exist!\n")
            self.game(loop)
        return False

    def startup(self):
        for loop in range(0,5):
            self.clear()
            print(self.word)
            [print(word) for word in self.triedWords]
            if self.game(loop):
                break

    def replay(self):
        r = input("Would you like to play again? ")

        if r[0] == "y":
            return True
        elif r[0] == "n":
            return False
        else:
            return self.replay()

    def exit(self):
        self.clear()
        [print(word) for word in self.triedWords]
        print('')

        if self.guessed:
            print(f"You have guessed the correct word!\nThe word was indeed: {self.word}")
            print('')
        else:
            print('')
            print(f"Nice try! The correct word was {self.word}!")
            print('')
        return self.replay()

def main():
    init(autoreset=True)

    app = Wordle()
    app.startup()
    replay = app.exit()

    if replay:
        main()
    else:
        print("Have a nice day!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSystem exit!")
    #except Exception as E:
        #print(f"\n[INFO] {E}")
