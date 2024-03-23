import random, time, os

class Guesser():
    def __init__(self):
        self.clear = lambda:os.system("clear")
        self.min = 1
        self.max = 100
        self.number = 0 
        self.guesses = 8
        self.wins = 0
        self.losses = 0

    def print_slowly(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True) 
            time.sleep(delay)
        print()

    def check(self, guess):
        if guess > self.max or guess < self.min:
            self.dialogue("InvalidRange")
            self.guesses -= 1
            self.dialogue("Guesses")
        elif guess > self.number:
            self.dialogue("Lower")
            self.guesses -= 1
            self.dialogue("Guesses")
        elif guess < self.number:
            self.dialogue("Higher")
            self.guesses -= 1
            self.dialogue("Guesses")

        if self.guesses == 0:
            self.dialogue("Incorrect")
            self.dialogue("Number")
            self.losses += 1
            return False
        elif guess == self.number:
            self.dialogue("Correct")
            self.dialogue("Guesses")
            self.wins += 1
            return False
        else:
            return True

    def game_loop(self):
        num = random.randint(50, 10000)
        random.seed((self.wins+self.losses+127)*num)
        self.number = random.randint(self.min,self.max)
        self.guesses = 8
        running = True
        while running:
            guess = input("Guess: ")
            self.clear()
            try:
                running = self.check(int(guess))
            except Exception:
                self.dialogue("InvalidGuess")
        
        play = "no"
        while True:
            play = input("Would you like to play again: ")
            if play.lower() == "no":
                self.dialogue("Games")
                self.dialogue("Goodbye")
                break
            elif play.lower() == "yes":
                break
            else:
                self.dialogue("InvalidAnswer")
        
        if play.lower() == "yes":
            self.clear()
            self.dialogue("Range")
            self.game_loop()

    def run(self):
        self.clear()
        self.dialogue("Welcome")
        self.dialogue("Range")
        self.game_loop()
        

    def dialogue(self, d):
        match d:
            case "Welcome":
                self.print_slowly("(⌐■_■) : Welcome to a little game of mine\n" +
                                  "The game is pretty simple just guess the number\n" +
                                  "that I thought of! Pretty simple right?\n") 
            case "Range":
                self.print_slowly(f"Try to guess the number between {self.min} and {self.max}")
            case "InvalidRange":
                self.print_slowly("(⌐■_■) : Number out of range, try again!")
            case "InvalidGuess":
                self.print_slowly("( °□°) ︵ ┻━┻ : Hey, that's illegal! That's not a valid number.\n" + 
                                  "You won't lose any guesses for this though ¯\\_(ツ)_/¯")
            case "InvalidAnswer":
                self.print_slowly("( °□°) ︵ ┻━┻ : Hey, that's illegal! That's not a valid answer.\n" + 
                                  "Please answer with yes or no ¯\\_(ツ)_/¯")
            case "Higher":
                self.print_slowly("(⌐■_■) : The number is higher!")
            case "Lower":
                self.print_slowly("(⌐■_■) : The number is lower!")
            case "Correct":
                self.print_slowly("\n\\(─‿‿─)/ : YeY!! You guessed the correct number!")
            case "Incorrect":
                self.print_slowly("\nAah man, you lost, you were so close!\n" +
                                  "Better luck next time ¯\\_(⊙︿⊙)_/¯")
            case "Guesses":
                self.print_slowly(f"Guesses left: {self.guesses}\n")
            case "Number":
                self.print_slowly(f"I chose {self.number} as the number you had to guess!\n")
            case "Games":
                self.print_slowly(f"Wins: {self.wins}\nLosses: {self.losses}")
            case "Exit":
                self.print_slowly("\n(⌐■_■) : You need to go, I understand.\n" +
                                  "Have a nice day (─‿‿─)\n")
            case "Goodbye":
                self.print_slowly("\n(⌐■_■) : Thank you for playing!\n" +
                                  "Have a nice day (─‿‿─)\n")
            case _:
                self.print_slowly("(⌐■_■) : Imposible what did you do!\n" +
                                  "You shouldn't have gotten the default dialogue!")

def main():
    app = Guesser()
    try:
        app.run()
    except KeyboardInterrupt:
        app.clear()
        app.dialogue("Games")
        app.dialogue("Exit")

if __name__ == "__main__":
    main()
