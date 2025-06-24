from rich import print
import random

def print_rich(message:str, style:str, end="\n") -> None:
    """
    Prints a formated message with a given style

    Arguments:
        message: str (The message you want to print)
        style: str (The style you want to add)
        end: str (The end parameter you want to add at the end of the message)
    """
    if style == "":
        print(f"{message}{end}")
        return
    print(f"[{style}]{message}[/{style}]{end}")

class game:
    """
    The main class for the game
    """
    def __init__(self, start_money:int, start_inventory:dict) -> None:
        """
        All variables will be inited here

        Arguments:
            start_money: int (The money the player should start with)
            start_inventory: dict (The inventory with things the player can sell)
        """
        self.money = start_money
        self.inventory = start_inventory

    def main_loop(self) -> None:
        """
        The main loop for the game
        """
        print_rich("Gambeling Simulator", "green")

        while True:
            print_rich(f"Money: {str(self.money)}$\n", "green")
            if self.money <= 0:
                if not self.inventory["house"] is None:
                    print_rich("Game Over! But wait you could still sell your house (Y/N): ", "red", end="")
                    if input("") == "Y":
                        self.money += self.inventory["house"]
                        self.inventory["house"] = None
                        continue
                    else:
                        pass
                print_rich("Game Over!", "red bold")
                exit(0)
            print_rich("Game Mode:\n1. Coin flip\n2. Number Guessr", "green")
            game = int(input("Mode: "))

            if game == 1:
                print_rich("\nCoin Flip:", "red")
                amount = int(input("Bet amount: "))
                if amount <= self.money:
                    self.money -= amount
                    while True:
                        print_rich("Coinflip: ", "")
                        random_flip = random.randint(1, 2)
                        if random_flip == 1:
                            amount *= 2
                            print_rich("\nYou won!", "green")
                            if input("Flip again? (Y/N): ") == "Y":
                                continue
                            else:
                                self.money += amount
                                break
                        else:
                            print_rich("You lost", "red")
                            break

            if game == 2:
                print_rich("\nNumber Guessr:", "red")
                amount = int(input("Bet amount: "))
                number = int(input("Number guess (1-49): "))
                if amount <= self.money:
                    if number >= 0 and number <=49:
                        if random.randint(1,49) == number:
                            print_rich("\nYou won!", "green")
                            self.money += amount * 49
                        else:
                            print_rich("You lost", "red")
                            self.money -= amount


if __name__ == "__main__":
    start_money = 1000
    start_inventory = {"house": 275000}

    game = game(start_money, start_inventory)
    game.main_loop()