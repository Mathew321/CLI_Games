import os, random

class Hangman():
    def __init__(self):
        self.clear = lambda: os.system("clear")
        self.hangman = [
            "_____\n|   |\n|   0\n|  /|\\\n|  / \\\n|\n|_________",
            "_____\n|   |\n|   0\n|  /|\\\n|  /\n|\n|_________",
            "_____\n|   |\n|   0\n|  /|\\\n|\n|\n|_________",
            "_____\n|   |\n|   0\n|   |\\\n|\n|\n|_________",
            "_____\n|   |\n|   0\n|   |\n|\n|\n|_________",
            "_____\n|   |\n|   0\n|\n|\n|\n|_________",
            "_____\n|\n|\n|\n|\n|\n|_________",
            "\n|\n|\n|\n|\n|\n|_________",
            "|_________",
            ""]
        self.words = [
            "apple", "book", "car", "dog", "elephant", "flower", "game", "house",
            "ice", "juice", "kite", "lamp", "mountain", "notebook", "orange",
            "pencil", "queen", "rain", "shoe", "tree", "umbrella", "vase", "window",
            "xylophone", "yarn", "zebra", "airplane", "bicycle", "computer",
            "door", "furniture", "guitar", "hat", "island", "jacket", "key",
            "leaf", "mirror", "necklace", "ocean", "pillow", "quilt", "river",
            "sun", "table", "umbrella", "violin", "watch", "yacht", "zoo",
            "cloud", "love", "joy", "happiness", "friendship", "freedom", "peace",
            "knowledge", "power", "strength", "beauty", "patience", "kindness"]
        self.lives = len(self.hangman)-1
        self.guessedLetters = []
        self.word = self.words[random.randrange(0,len(self.words))]
        self.guessedWord = "_" * len(self.word)
        self.guessed = False

    def triedLet(self):
        self.guessedLetters.sort()
        gl = ""

        for letter in self.guessedLetters:
            if letter == self.guessedLetters[0]:
                gl += letter
            else:
                gl += ', ' + letter
        return gl

    def startup(self):
        self.clear()

        while not self.guessed:
            self.guess = input("Guess: ")
            self.clear()

            if len(self.guess) == 1:
                if self.guess in self.word:
                    for i in range(0,len(self.word)):
                        if self.guess == self.word[i]:
                            self.guessedWord = list(self.guessedWord)
                            self.guessedWord[i] = self.guess
                            self.guessedWord = "".join(self.guessedWord)
                else:
                    self.lives -= 1
                    self.guessedLetters += self.guess
            elif self.guess == self.word:
                self.guessedWord = self.word

            print("Letter you tried: " + self.triedLet())
            print(self.hangman[self.lives])
            print("")
            print("The word you are guessing: " + self.guessedWord)

            if self.guessedWord == self.word:
                self.guessed = True
            elif self.lives == 0:
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
        print("Letter you tried: " + self.triedLet())
        print(self.hangman[self.lives])
        if self.guessed:
            print(f"Lives remaining: {self.lives}")
            print('')
            print(f"You have guessed the correct word!\nThe word was indeed: {self.word}")
            print('')
        else:
            print('')
            print(f"Nice try! The correct word was {self.word}!")
            print('')
        return self.replay()

def main():
    app = Hangman()
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
    except Exception as E:
        print(f"\n[INFO] {E}")
