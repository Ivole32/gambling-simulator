from rich import print
import random

print("[green]Gambeling Simulator[/green]")

money = 1000
inventory = {"house": 275000}

while True:
    print(f"[green]Money: {str(money)}$\n")
    if money <= 0:
        if not inventory["house"] is None:
            print("[red]Game Over! But wait you cann sell your house (Y/N): [/red]", end="")
            if input("") == "Y":
                money += inventory["house"]
                inventory["house"] = None
                continue
            else:
                pass
        print("[red bold]Game Over![/red bold]")
        exit(0)
    print("[green]Game Mode: [/green]\n1. Coin flip")
    game = int(input("Mode: "))
    if game == 1:
        print("\n[red]Coin Flip:[/red]")
        amount = int(input("Bet amount: "))
        if amount <= money:
            money -= amount
            while True:
                print("Coinflip: ")
                random_flip = random.randint(1, 2)
                if random_flip == 1:
                    amount *= 2
                    print("\n[green]You won![/green]")
                    if input("Flip again? (Y/N): ") == "Y":
                        continue
                    else:
                        money += amount
                        break
                else:
                    print("[red]You lost[/red]")
                    break