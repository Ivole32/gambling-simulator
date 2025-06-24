from rich import print
import random

print("[green]Gambeling Simulator[/green]")

money = 1000

while True:
    print(f"[green]Money: {str(money)}$\n")
    print("[red]Coin Flip:[/red]")
    print("Bet amount: ", end="")
    amount = int(input(""))
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