import customtkinter
import subprocess
import random
from typing import Dict, Callable

app = customtkinter.CTk()
app.geometry("1200x700")
app.title("Gambling Simulator")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

current_frame = None
current_title = None
current_bet_frame = None
current_balance_label = None
balance = 1000
current_bet = 0
game_active = False
sidebar_expanded = False

# Shop system
inventory: Dict[str, int] = {}  # Player's inventory
shop_items = {
    "🍎": {"name": "Lucky Apple", "price": 50, "description": "Brings good luck!"},
    "💎": {"name": "Diamond Ring", "price": 500, "description": "Shiny and valuable"},
    "🎩": {"name": "Top Hat", "price": 200, "description": "Classy headwear"},
    "🕶️": {"name": "Cool Sunglasses", "price": 150, "description": "Look cool while gambling"},
    "🎲": {"name": "Lucky Dice", "price": 100, "description": "Roll your way to fortune"},
    "🪙": {"name": "Golden Coin", "price": 75, "description": "A collector's item"},
    "🎯": {"name": "Dart Set", "price": 120, "description": "For precise betting"},
    "🃏": {"name": "Magic Cards", "price": 300, "description": "May help with card games"},
    "🎰": {"name": "Mini Slot Machine", "price": 800, "description": "Your own personal slots"},
    "🏆": {"name": "Trophy", "price": 1000, "description": "Symbol of victory"}
}

def reload() -> None:
    app.quit()
    app.destroy()
    subprocess.run(["python", r".\ui.py"], shell=True)
    exit(0)

def show_casino() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎰 Coin Flip Casino", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame, 
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    coin_label = customtkinter.CTkLabel(master=current_frame, text="🪙", font=("Arial", 100))
    coin_label.pack(pady=60)
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Click 'Bet' to flip!", 
                                        font=("Arial", 26, "italic"),
                                        text_color=("#E0E0E0", "#E0E0E0"))
    result_label.pack(pady=15)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    bet_submit_button = customtkinter.CTkButton(master=button_container, text="🎲 FLIP COIN", 
                                              width=140, height=40,
                                              font=("Arial", 16, "bold"),
                                              fg_color=("#FFD700", "#FFA500"),
                                              hover_color=("#FFB347", "#FF8C00"),
                                              text_color=("#000000", "#000000"),
                                              command=lambda: start_coinflip())
    bet_submit_button.pack(side="left", padx=15)
    
    win_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    
    double_button = customtkinter.CTkButton(master=win_frame, text="🎲 Double or Nothing", 
                                          command=lambda: double_bet(), 
                                          width=180, height=50,
                                          font=("Arial", 16, "bold"),
                                          fg_color=("#FF6B6B", "#FF4757"),
                                          hover_color=("#FF5252", "#FF3742"))
    cash_out_button = customtkinter.CTkButton(master=win_frame, text="💰 Cash Out", 
                                            command=lambda: cash_out(),
                                            width=180, height=50,
                                            font=("Arial", 16, "bold"),
                                            fg_color=("#00FF7F", "#32CD32"),
                                            hover_color=("#00FA54", "#28B428"),
                                            text_color=("#000000", "#000000"))
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_coinflip() -> None:
        global balance, current_bet, game_active
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            game_active = True
            current_balance_label.configure(text=f"Balance: ${balance}")
            bet_submit_button.configure(state="disabled")
            animate_coin(coin_label, result_label, 0)
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_coin(coin_label: customtkinter.CTkLabel, result_label: customtkinter.CTkLabel, count: int) -> None:
        if count < 10:
            symbols = ["🪙", "⚪", "🟡", "🔵"]
            coin_label.configure(text=symbols[count % len(symbols)])
            result_label.configure(text="Flipping...")
            app.after(100, lambda: animate_coin(coin_label, result_label, count + 1))
        else:
            result = random.choice(["Heads", "Tails"])
            coin_symbol = "👑" if result == "Heads" else "🐍"
            coin_label.configure(text=coin_symbol)
            
            if result == "Heads":
                result_label.configure(text=f"You won ${current_bet * 2}!")
                show_win_options()
            else:
                result_label.configure(text=f"You lost ${current_bet}!")
                reset_game()
    
    def show_win_options() -> None:
        win_frame.pack(pady=30)
        double_button.pack(side="left", padx=20)
        cash_out_button.pack(side="left", padx=20)
    
    def double_bet() -> None:
        global current_bet
        current_bet *= 2
        win_frame.pack_forget()
        result_label.configure(text=f"Double or Nothing: ${current_bet}")
        coin_label.configure(text="🪙")
        animate_coin(coin_label, result_label, 0)
    
    def cash_out() -> None:
        global balance, current_bet, game_active
        balance += current_bet * 2
        current_balance_label.configure(text=f"Balance: ${balance}")
        result_label.configure(text=f"Cashed out ${current_bet * 2}!")
        reset_game()
    
    def reset_game() -> None:
        global current_bet, game_active
        current_bet = 0
        game_active = False
        bet_submit_button.configure(state="normal")
        win_frame.pack_forget()
        bet_entry.delete(0, "end")
        bet_entry.insert(0, "0")

def show_number_guesser() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🔢 Number Guesser", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    center_container = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    center_container.pack(expand=True, fill="both")
    center_container.grid_rowconfigure(0, weight=1)
    center_container.grid_columnconfigure(0, weight=1)
    
    content_frame = customtkinter.CTkFrame(master=center_container, 
                                          fg_color="transparent")
    content_frame.grid(row=0, column=0)
    
    instruction_label = customtkinter.CTkLabel(master=content_frame, 
                                             text="🎯 Guess a number between 1-49", 
                                             font=("Arial", 24, "bold"),
                                             text_color=("#E0E0E0", "#E0E0E0"))
    instruction_label.pack(pady=15)
    
    odds_label = customtkinter.CTkLabel(master=content_frame, 
                                       text="💎 Win 49x your bet!", 
                                       font=("Arial", 20, "bold"), 
                                       text_color=("#FFD700", "#FFD700"))
    odds_label.pack(pady=15)
    
    number_entry = customtkinter.CTkEntry(master=content_frame, 
                                        placeholder_text="🔢 Your guess (1-49)", 
                                        width=250, height=50,
                                        font=("Arial", 18, "bold"),
                                        corner_radius=15)
    number_entry.pack(pady=25)
    
    result_label = customtkinter.CTkLabel(master=content_frame, text="", 
                                        font=("Arial", 20, "bold"))
    result_label.pack(pady=15)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    bet_submit_button = customtkinter.CTkButton(master=button_container, text="🔮 GUESS", 
                                              width=140, height=40,
                                              font=("Arial", 16, "bold"),
                                              fg_color=("#9B59B6", "#8E44AD"),
                                              hover_color=("#8E44AD", "#7D3C98"),
                                              command=lambda: start_number_game())
    bet_submit_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_number_game() -> None:
        global balance, current_bet, game_active
        try:
            bet_amount = int(bet_entry.get() or 0)
            guess = int(number_entry.get() or 0)
            
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            if guess < 1 or guess > 49:
                result_label.configure(text="Please guess a number between 1-49!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            current_balance_label.configure(text=f"Balance: ${balance}")
            bet_submit_button.configure(state="disabled")
            
            winning_number = random.randint(1, 49)
            
            if guess == winning_number:
                winnings = current_bet * 49
                balance += winnings
                current_balance_label.configure(text=f"Balance: ${balance}")
                result_label.configure(text=f"🎉 YOU WON! Number was {winning_number}. Won ${winnings}!", text_color="green")
            else:

                result_label.configure(text=f"😞 You lost! Number was {winning_number}. Your guess: {guess}", text_color="red")
            
            bet_submit_button.configure(state="normal")
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            number_entry.delete(0, "end")
            
        except ValueError:
            result_label.configure(text="Please enter valid numbers!")

def show_roulette() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎯 Roulette", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    wheel_label = customtkinter.CTkLabel(master=current_frame, text="🎰", font=("Arial", 100))
    wheel_label.pack(pady=30)
    
    # Betting options frame
    bet_options_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    bet_options_frame.pack(pady=20)
    
    selected_bet_type = customtkinter.StringVar(value="red")
    
    red_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🔴 Red (2x)", 
                                           variable=selected_bet_type, value="red",
                                           font=("Arial", 16, "bold"))
    red_radio.pack(side="left", padx=20)
    
    black_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="⚫ Black (2x)", 
                                             variable=selected_bet_type, value="black",
                                             font=("Arial", 16, "bold"))
    black_radio.pack(side="left", padx=20)
    
    green_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🟢 Green (36x)", 
                                             variable=selected_bet_type, value="green",
                                             font=("Arial", 16, "bold"))
    green_radio.pack(side="left", padx=20)
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Place your bet and spin!", 
                                        font=("Arial", 20, "bold"),
                                        text_color=("#E0E0E0", "#E0E0E0"))
    result_label.pack(pady=20)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    # Bet adjustment buttons
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    spin_button = customtkinter.CTkButton(master=button_container, text="🎯 SPIN", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#E74C3C", "#C0392B"),
                                        hover_color=("#CB4335", "#A93226"),
                                        command=lambda: start_roulette())
    spin_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_roulette() -> None:
        global balance, current_bet, game_active
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            current_balance_label.configure(text=f"Balance: ${balance}")
            spin_button.configure(state="disabled")
            animate_roulette_wheel(wheel_label, result_label, 0, selected_bet_type.get())
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_roulette_wheel(wheel_label: customtkinter.CTkLabel, result_label: customtkinter.CTkLabel, count: int, bet_type: str) -> None:
        global balance
        if count < 15:
            symbols = ["🎰", "🔴", "⚫", "🟢", "🎯", "⭕"]
            wheel_label.configure(text=symbols[count % len(symbols)])
            result_label.configure(text="Spinning...")
            app.after(100, lambda: animate_roulette_wheel(wheel_label, result_label, count + 1, bet_type))
        else:
            # Roulette numbers: 0 (green), 1-36 (red/black alternating roughly)
            number = random.randint(0, 36)
            if number == 0:
                color = "green"
                symbol = "🟢"
            elif number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                color = "red"
                symbol = "🔴"
            else:
                color = "black"
                symbol = "⚫"
            
            wheel_label.configure(text=symbol)
            
            if bet_type == color:
                if color == "green":
                    winnings = current_bet * 36
                else:
                    winnings = current_bet * 2
                balance += winnings
                current_balance_label.configure(text=f"Balance: ${balance}")
                result_label.configure(text=f"🎉 Winner! Number {number} ({color}). Won ${winnings}!", text_color="green")
            else:
                result_label.configure(text=f"😞 Number {number} ({color}). Better luck next time!", text_color="red")
            
            spin_button.configure(state="normal")
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")

def show_blackjack() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🃏 Blackjack", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    # Game state
    player_cards = []
    dealer_cards = []
    game_over = False
    
    dealer_label = customtkinter.CTkLabel(master=current_frame, text="Dealer: 🂠 🂠", 
                                        font=("Arial", 20, "bold"))
    dealer_label.pack(pady=20)
    
    dealer_score_label = customtkinter.CTkLabel(master=current_frame, text="Dealer: ?", 
                                              font=("Arial", 16))
    dealer_score_label.pack()
    
    player_label = customtkinter.CTkLabel(master=current_frame, text="You: 🂠 🂠", 
                                        font=("Arial", 20, "bold"))
    player_label.pack(pady=20)
    
    player_score_label = customtkinter.CTkLabel(master=current_frame, text="You: 0", 
                                               font=("Arial", 16))
    player_score_label.pack()
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Place your bet to start!", 
                                        font=("Arial", 18, "bold"))
    result_label.pack(pady=20)
    
    # Game buttons
    game_buttons_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    game_buttons_frame.pack(pady=20)
    
    hit_button = customtkinter.CTkButton(master=game_buttons_frame, text="🃏 Hit", 
                                       width=100, height=40,
                                       font=("Arial", 14, "bold"),
                                       state="disabled",
                                       command=lambda: hit_card())
    hit_button.pack(side="left", padx=10)
    
    stand_button = customtkinter.CTkButton(master=game_buttons_frame, text="✋ Stand", 
                                         width=100, height=40,
                                         font=("Arial", 14, "bold"),
                                         state="disabled",
                                         command=lambda: stand())
    stand_button.pack(side="left", padx=10)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    # Bet controls
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    deal_button = customtkinter.CTkButton(master=button_container, text="🃏 DEAL", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#2ECC71", "#27AE60"),
                                        hover_color=("#58D68D", "#2ECC71"),
                                        command=lambda: start_blackjack())
    deal_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def get_card_value(card: int) -> int:
        if card > 10:
            return 10
        return card
    
    def calculate_score(cards: list) -> int:
        score = sum(get_card_value(card) for card in cards)
        aces = cards.count(1)
        while score <= 11 and aces > 0:
            score += 10
            aces -= 1
        return score
    
    def start_blackjack() -> None:
        nonlocal player_cards, dealer_cards, game_over
        global balance, current_bet
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            current_balance_label.configure(text=f"Balance: ${balance}")
            
            # Deal initial cards
            player_cards = [random.randint(1, 13), random.randint(1, 13)]
            dealer_cards = [random.randint(1, 13), random.randint(1, 13)]
            game_over = False
            
            update_display()
            
            if calculate_score(player_cards) == 21:
                result_label.configure(text="🎉 Blackjack! You win!", text_color="green")
                balance += int(current_bet * 2.5)
                current_balance_label.configure(text=f"Balance: ${balance}")
                game_over = True
            else:
                hit_button.configure(state="normal")
                stand_button.configure(state="normal")
                deal_button.configure(state="disabled")
                result_label.configure(text="Hit or Stand?")
                
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def update_display() -> None:
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)
        
        # Show player cards
        player_cards_text = " ".join(["🂠"] * len(player_cards))
        player_label.configure(text=f"You: {player_cards_text}")
        player_score_label.configure(text=f"You: {player_score}")
        
        # Show dealer cards (hide second card until stand)
        if game_over:
            dealer_cards_text = " ".join(["🂠"] * len(dealer_cards))
            dealer_label.configure(text=f"Dealer: {dealer_cards_text}")
            dealer_score_label.configure(text=f"Dealer: {dealer_score}")
        else:
            dealer_label.configure(text=f"Dealer: 🂠 🂭")
            dealer_score_label.configure(text="Dealer: ?")
    
    def hit_card() -> None:
        nonlocal player_cards, game_over
        player_cards.append(random.randint(1, 13))
        player_score = calculate_score(player_cards)
        update_display()
        
        if player_score > 21:
            result_label.configure(text=f"😞 Bust! You lose ${current_bet}!", text_color="red")
            game_over = True
            hit_button.configure(state="disabled")
            stand_button.configure(state="disabled")
            deal_button.configure(state="normal")
    
    def stand() -> None:
        nonlocal dealer_cards, game_over
        global balance
        
        # Dealer hits until 17 or higher
        while calculate_score(dealer_cards) < 17:
            dealer_cards.append(random.randint(1, 13))
        
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)
        game_over = True
        update_display()
        
        if dealer_score > 21:
            result_label.configure(text=f"🎉 Dealer busts! You win ${current_bet * 2}!", text_color="green")
            balance += current_bet * 2
        elif player_score > dealer_score:
            result_label.configure(text=f"🎉 You win ${current_bet * 2}!", text_color="green")
            balance += current_bet * 2
        elif player_score == dealer_score:
            result_label.configure(text="🤝 Push! Bet returned.", text_color="yellow")
            balance += current_bet
        else:
            result_label.configure(text=f"😞 Dealer wins! You lose ${current_bet}!", text_color="red")
        
        current_balance_label.configure(text=f"Balance: ${balance}")
        hit_button.configure(state="disabled")
        stand_button.configure(state="disabled")
        deal_button.configure(state="normal")
        bet_entry.delete(0, "end")
        bet_entry.insert(0, "0")

def show_dice_roll() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎲 Dice Roll", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    dice_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    dice_frame.pack(pady=40)
    
    dice1_label = customtkinter.CTkLabel(master=dice_frame, text="🎲", font=("Arial", 80))
    dice1_label.pack(side="left", padx=20)
    
    dice2_label = customtkinter.CTkLabel(master=dice_frame, text="🎲", font=("Arial", 80))
    dice2_label.pack(side="left", padx=20)
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Choose your bet and roll!", 
                                        font=("Arial", 20, "bold"))
    result_label.pack(pady=20)
    
    # Betting options
    bet_options_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    bet_options_frame.pack(pady=20)
    
    selected_bet_type = customtkinter.StringVar(value="over7")
    
    over7_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🔺 Over 7 (2x)", 
                                             variable=selected_bet_type, value="over7",
                                             font=("Arial", 16, "bold"))
    over7_radio.pack(side="left", padx=20)
    
    exactly7_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🎯 Exactly 7 (4x)", 
                                                variable=selected_bet_type, value="exactly7",
                                                font=("Arial", 16, "bold"))
    exactly7_radio.pack(side="left", padx=20)
    
    under7_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🔻 Under 7 (2x)", 
                                              variable=selected_bet_type, value="under7",
                                              font=("Arial", 16, "bold"))
    under7_radio.pack(side="left", padx=20)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    roll_button = customtkinter.CTkButton(master=button_container, text="🎲 ROLL", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#3498DB", "#2980B9"),
                                        hover_color=("#5DADE2", "#3498DB"),
                                        command=lambda: start_dice_roll())
    roll_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_dice_roll() -> None:
        global balance, current_bet
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            current_balance_label.configure(text=f"Balance: ${balance}")
            roll_button.configure(state="disabled")
            animate_dice(dice1_label, dice2_label, result_label, 0, selected_bet_type.get())
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_dice(dice1_label: customtkinter.CTkLabel, dice2_label: customtkinter.CTkLabel, 
                   result_label: customtkinter.CTkLabel, count: int, bet_type: str) -> None:
        global balance
        if count < 10:
            dice_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            dice1_label.configure(text=random.choice(dice_symbols))
            dice2_label.configure(text=random.choice(dice_symbols))
            result_label.configure(text="Rolling...")
            app.after(100, lambda: animate_dice(dice1_label, dice2_label, result_label, count + 1, bet_type))
        else:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            total = dice1 + dice2
            
            dice_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            dice1_label.configure(text=dice_symbols[dice1-1])
            dice2_label.configure(text=dice_symbols[dice2-1])
            
            won = False
            multiplier = 0
            
            if bet_type == "over7" and total > 7:
                won = True
                multiplier = 2
            elif bet_type == "exactly7" and total == 7:
                won = True
                multiplier = 4
            elif bet_type == "under7" and total < 7:
                won = True
                multiplier = 2
            
            if won:
                winnings = current_bet * multiplier
                balance += winnings
                current_balance_label.configure(text=f"Balance: ${balance}")
                result_label.configure(text=f"🎉 Total: {total}! You won ${winnings}!", text_color="green")
            else:
                result_label.configure(text=f"😞 Total: {total}. Better luck next time!", text_color="red")
            
            roll_button.configure(state="normal")
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")

def show_slot_machine() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎰 Slot Machine", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    # Slot machine display
    slot_frame = customtkinter.CTkFrame(master=current_frame, 
                                       corner_radius=15,
                                       fg_color=("#1A1A1A", "#0F0F0F"))
    slot_frame.pack(pady=40)
    
    slots_container = customtkinter.CTkFrame(master=slot_frame, fg_color="transparent")
    slots_container.pack(padx=40, pady=30)
    
    slot1_label = customtkinter.CTkLabel(master=slots_container, text="🍒", 
                                       font=("Arial", 80),
                                       fg_color=("#333333", "#2A2A2A"),
                                       corner_radius=10,
                                       width=100, height=100)
    slot1_label.pack(side="left", padx=10)
    
    slot2_label = customtkinter.CTkLabel(master=slots_container, text="🍒", 
                                       font=("Arial", 80),
                                       fg_color=("#333333", "#2A2A2A"),
                                       corner_radius=10,
                                       width=100, height=100)
    slot2_label.pack(side="left", padx=10)
    
    slot3_label = customtkinter.CTkLabel(master=slots_container, text="🍒", 
                                       font=("Arial", 80),
                                       fg_color=("#333333", "#2A2A2A"),
                                       corner_radius=10,
                                       width=100, height=100)
    slot3_label.pack(side="left", padx=10)
    
    # Paytable
    paytable_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    paytable_frame.pack(pady=20)
    
    paytable_label = customtkinter.CTkLabel(master=paytable_frame, 
                                          text="💎💎💎 = 50x | 🍒🍒🍒 = 10x | 🔔🔔🔔 = 5x | Any 2 = 2x", 
                                          font=("Arial", 14, "bold"),
                                          text_color=("#E0E0E0", "#E0E0E0"))
    paytable_label.pack()
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Pull the lever to play!", 
                                        font=("Arial", 20, "bold"))
    result_label.pack(pady=20)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    spin_button = customtkinter.CTkButton(master=button_container, text="🎰 SPIN", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#F39C12", "#E67E22"),
                                        hover_color=("#F4D03F", "#F39C12"),
                                        command=lambda: start_slot_spin())
    spin_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_slot_spin() -> None:
        global balance, current_bet
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            current_balance_label.configure(text=f"Balance: ${balance}")
            spin_button.configure(state="disabled")
            animate_slots(slot1_label, slot2_label, slot3_label, result_label, 0)
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_slots(slot1_label: customtkinter.CTkLabel, slot2_label: customtkinter.CTkLabel, 
                     slot3_label: customtkinter.CTkLabel, result_label: customtkinter.CTkLabel, count: int) -> None:
        global balance
        if count < 20:
            symbols = ["🍒", "🔔", "🍋", "🍊", "🍇", "💎", "7"]
            slot1_label.configure(text=random.choice(symbols))
            slot2_label.configure(text=random.choice(symbols))
            slot3_label.configure(text=random.choice(symbols))
            result_label.configure(text="Spinning...")
            app.after(100, lambda: animate_slots(slot1_label, slot2_label, slot3_label, result_label, count + 1))
        else:
            # Final result with weighted chances
            symbols = ["🍒", "🍒", "🍒", "🔔", "🔔", "🍋", "🍊", "🍇", "💎", "7"]
            
            final1 = random.choice(symbols)
            final2 = random.choice(symbols)
            final3 = random.choice(symbols)
            
            slot1_label.configure(text=final1)
            slot2_label.configure(text=final2)
            slot3_label.configure(text=final3)
            
            # Check for wins
            if final1 == final2 == final3:
                if final1 == "💎":
                    multiplier = 50
                elif final1 == "🍒":
                    multiplier = 10
                elif final1 == "🔔":
                    multiplier = 5
                else:
                    multiplier = 3
                winnings = current_bet * multiplier
                balance += winnings
                current_balance_label.configure(text=f"Balance: ${balance}")
                result_label.configure(text=f"🎉 JACKPOT! Won ${winnings}!", text_color="green")
            elif final1 == final2 or final2 == final3 or final1 == final3:
                winnings = current_bet * 2
                balance += winnings
                current_balance_label.configure(text=f"Balance: ${balance}")
                result_label.configure(text=f"🎊 Pair! Won ${winnings}!", text_color="green")
            else:
                result_label.configure(text="😞 No match. Try again!", text_color="red")
            
            spin_button.configure(state="normal")
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")

def show_shop() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label, balance
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🛍️ Shop", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    main_container = customtkinter.CTkFrame(master=main_frame,
                                          corner_radius=20,
                                          fg_color=("#2B2B2B", "#1C1C1C"))
    main_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    # Tab frame for Shop and Inventory
    tab_frame = customtkinter.CTkFrame(master=main_container, fg_color="transparent")
    tab_frame.pack(fill="x", padx=20, pady=20)
    
    shop_tab_btn = customtkinter.CTkButton(master=tab_frame, text="🛒 Shop", 
                                         width=150, height=40,
                                         font=("Arial", 16, "bold"),
                                         fg_color=("#4ECDC4", "#26D0CE"),
                                         hover_color=("#45B7B8", "#22A3B8"),
                                         command=lambda: switch_to_shop_tab())
    shop_tab_btn.pack(side="left", padx=10)
    
    inventory_tab_btn = customtkinter.CTkButton(master=tab_frame, text="🎒 Inventory", 
                                              width=150, height=40,
                                              font=("Arial", 16, "bold"),
                                              fg_color=("#9B59B6", "#8E44AD"),
                                              hover_color=("#8E44AD", "#7D3C98"),
                                              command=lambda: switch_to_inventory_tab())
    inventory_tab_btn.pack(side="left", padx=10)
    
    # Scrollable content frame
    content_frame = customtkinter.CTkScrollableFrame(master=main_container,
                                                   corner_radius=15,
                                                   fg_color=("#1A1A1A", "#0F0F0F"))
    content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def switch_to_shop_tab():
        # Clear content frame
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        shop_tab_btn.configure(fg_color=("#4ECDC4", "#26D0CE"))
        inventory_tab_btn.configure(fg_color=("#555555", "#404040"))
        
        # Shop header
        shop_header = customtkinter.CTkLabel(master=content_frame, 
                                           text="🛍️ Welcome to the Shop!", 
                                           font=("Arial", 24, "bold"),
                                           text_color=("#FFD700", "#FFD700"))
        shop_header.pack(pady=20)
        
        # Create shop items
        for emoji, item_data in shop_items.items():
            item_frame = customtkinter.CTkFrame(master=content_frame,
                                              corner_radius=12,
                                              fg_color=("#333333", "#2A2A2A"))
            item_frame.pack(fill="x", padx=20, pady=10)
            
            item_info_frame = customtkinter.CTkFrame(master=item_frame, fg_color="transparent")
            item_info_frame.pack(fill="x", padx=20, pady=15)
            
            # Item icon and name
            icon_name_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
            icon_name_frame.pack(side="left", fill="x", expand=True)
            
            item_icon = customtkinter.CTkLabel(master=icon_name_frame, text=emoji, 
                                             font=("Arial", 40))
            item_icon.pack(side="left", padx=(0, 15))
            
            item_details = customtkinter.CTkFrame(master=icon_name_frame, fg_color="transparent")
            item_details.pack(side="left", fill="x", expand=True)
            
            item_name = customtkinter.CTkLabel(master=item_details, 
                                             text=item_data["name"], 
                                             font=("Arial", 18, "bold"),
                                             anchor="w")
            item_name.pack(anchor="w")
            
            item_desc = customtkinter.CTkLabel(master=item_details, 
                                             text=item_data["description"], 
                                             font=("Arial", 14),
                                             text_color=("#B0B0B0", "#B0B0B0"),
                                             anchor="w")
            item_desc.pack(anchor="w")
            
            # Price and buy button
            price_buy_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
            price_buy_frame.pack(side="right")
            
            price_label = customtkinter.CTkLabel(master=price_buy_frame, 
                                               text=f"${item_data['price']}", 
                                               font=("Arial", 18, "bold"),
                                               text_color=("#00FF7F", "#00FF7F"))
            price_label.pack(pady=(0, 5))
            
            buy_btn = customtkinter.CTkButton(master=price_buy_frame, text="Buy", 
                                            width=80, height=35,
                                            font=("Arial", 14, "bold"),
                                            fg_color=("#4ECDC4", "#26D0CE"),
                                            hover_color=("#45B7B8", "#22A3B8"),
                                            command=lambda e=emoji, data=item_data: buy_item(e, data))
            buy_btn.pack()
    
    def switch_to_inventory_tab():
        # Clear content frame
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        shop_tab_btn.configure(fg_color=("#555555", "#404040"))
        inventory_tab_btn.configure(fg_color=("#9B59B6", "#8E44AD"))
        
        # Inventory header
        inv_header = customtkinter.CTkLabel(master=content_frame, 
                                          text="🎒 Your Inventory", 
                                          font=("Arial", 24, "bold"),
                                          text_color=("#9B59B6", "#8E44AD"))
        inv_header.pack(pady=20)
        
        if not inventory:
            empty_label = customtkinter.CTkLabel(master=content_frame, 
                                               text="Your inventory is empty!\nVisit the shop to buy some items.", 
                                               font=("Arial", 16),
                                               text_color=("#B0B0B0", "#B0B0B0"))
            empty_label.pack(pady=50)
        else:
            # Create inventory items
            for emoji, quantity in inventory.items():
                if quantity > 0:
                    item_data = shop_items[emoji]
                    sell_price = int(item_data["price"] * 0.7)  # Sell for 70% of buy price
                    
                    item_frame = customtkinter.CTkFrame(master=content_frame,
                                                      corner_radius=12,
                                                      fg_color=("#333333", "#2A2A2A"))
                    item_frame.pack(fill="x", padx=20, pady=10)
                    
                    item_info_frame = customtkinter.CTkFrame(master=item_frame, fg_color="transparent")
                    item_info_frame.pack(fill="x", padx=20, pady=15)
                    
                    # Item icon and name
                    icon_name_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
                    icon_name_frame.pack(side="left", fill="x", expand=True)
                    
                    item_icon = customtkinter.CTkLabel(master=icon_name_frame, text=emoji, 
                                                     font=("Arial", 40))
                    item_icon.pack(side="left", padx=(0, 15))
                    
                    item_details = customtkinter.CTkFrame(master=icon_name_frame, fg_color="transparent")
                    item_details.pack(side="left", fill="x", expand=True)
                    
                    item_name = customtkinter.CTkLabel(master=item_details, 
                                                     text=f"{item_data['name']} x{quantity}", 
                                                     font=("Arial", 18, "bold"),
                                                     anchor="w")
                    item_name.pack(anchor="w")
                    
                    item_desc = customtkinter.CTkLabel(master=item_details, 
                                                     text=item_data["description"], 
                                                     font=("Arial", 14),
                                                     text_color=("#B0B0B0", "#B0B0B0"),
                                                     anchor="w")
                    item_desc.pack(anchor="w")
                    
                    # Sell price and button
                    sell_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
                    sell_frame.pack(side="right")
                    
                    sell_price_label = customtkinter.CTkLabel(master=sell_frame, 
                                                            text=f"Sell: ${sell_price}", 
                                                            font=("Arial", 16, "bold"),
                                                            text_color=("#FF6B6B", "#FF4757"))
                    sell_price_label.pack(pady=(0, 5))
                    
                    sell_btn = customtkinter.CTkButton(master=sell_frame, text="Sell", 
                                                     width=80, height=35,
                                                     font=("Arial", 14, "bold"),
                                                     fg_color=("#E74C3C", "#C0392B"),
                                                     hover_color=("#C0392B", "#A93226"),
                                                     command=lambda e=emoji, price=sell_price: sell_item(e, price))
                    sell_btn.pack()
    
    def buy_item(emoji: str, item_data: Dict[str, any]):
        global balance
        price = item_data["price"]
        
        if balance >= price:
            balance -= price
            current_balance_label.configure(text=f"Balance: ${balance}")
            
            # Add to inventory
            if emoji in inventory:
                inventory[emoji] += 1
            else:
                inventory[emoji] = 1
            
            # Show success message
            success_window = customtkinter.CTkToplevel(app)
            success_window.title("Purchase Successful")
            success_window.geometry("400x200")
            success_window.transient(app)
            success_window.grab_set()
            
            success_label = customtkinter.CTkLabel(master=success_window, 
                                                 text=f"✅ Successfully bought {item_data['name']}!\n\n{emoji} Added to inventory", 
                                                 font=("Arial", 16, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
            success_label.pack(pady=50)
            
            ok_btn = customtkinter.CTkButton(master=success_window, text="OK", 
                                           width=100, height=35,
                                           command=success_window.destroy)
            ok_btn.pack(pady=20)
            
        else:
            # Show insufficient funds message
            error_window = customtkinter.CTkToplevel(app)
            error_window.title("Insufficient Funds")
            error_window.geometry("400x200")
            error_window.transient(app)
            error_window.grab_set()
            
            error_label = customtkinter.CTkLabel(master=error_window, 
                                               text=f"❌ Not enough money!\n\nYou need ${price} but only have ${balance}", 
                                               font=("Arial", 16, "bold"),
                                               text_color=("#FF6B6B", "#FF4757"))
            error_label.pack(pady=50)
            
            ok_btn = customtkinter.CTkButton(master=error_window, text="OK", 
                                           width=100, height=35,
                                           command=error_window.destroy)
            ok_btn.pack(pady=20)
    
    def sell_item(emoji: str, sell_price: int):
        global balance
        
        if emoji in inventory and inventory[emoji] > 0:
            balance += sell_price
            current_balance_label.configure(text=f"Balance: ${balance}")
            inventory[emoji] -= 1
            
            # Show success message
            success_window = customtkinter.CTkToplevel(app)
            success_window.title("Sale Successful")
            success_window.geometry("400x200")
            success_window.transient(app)
            success_window.grab_set()
            
            item_name = shop_items[emoji]["name"]
            success_label = customtkinter.CTkLabel(master=success_window, 
                                                 text=f"💰 Successfully sold {item_name}!\n\n+${sell_price} added to balance", 
                                                 font=("Arial", 16, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
            success_label.pack(pady=50)
            
            ok_btn = customtkinter.CTkButton(master=success_window, text="OK", 
                                           width=100, height=35,
                                           command=lambda: [success_window.destroy(), switch_to_inventory_tab()])
            ok_btn.pack(pady=20)
    
    # Start with shop tab
    switch_to_shop_tab()

def show_settings() -> None:
    global current_frame, current_title, current_bet_frame, current_balance_label
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="Settings", font=("Arial", 28, "bold"))
    current_title.pack(pady=(20, 10))
    
    current_frame = customtkinter.CTkFrame(master=main_frame)
    current_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    label = customtkinter.CTkLabel(master=current_frame, text="", font=("Arial", 24))
    label.pack(pady=50)

def create_sidebar(buttons: Dict[str, Callable[[], None]]) -> None:
    global sidebar_expanded
    sidebar = customtkinter.CTkFrame(master=app, 
                                   width=250, 
                                   corner_radius=0,
                                   fg_color=("#1E1E1E", "#0D1117"))
    sidebar.pack(side="left", fill="y")

    casino_frame = customtkinter.CTkFrame(master=sidebar, fg_color="transparent")
    casino_frame.pack(fill="x", padx=15, pady=15)
    
    casino_button = customtkinter.CTkButton(master=casino_frame, text="🎰 Casino Games ▼", 
                                          command=lambda: toggle_casino_menu(),
                                          font=("Arial", 16, "bold"),
                                          height=50,
                                          fg_color=("#FFD700", "#FFA500"),
                                          hover_color=("#FFB347", "#FF8C00"),
                                          text_color=("#000000", "#000000"),
                                          corner_radius=15)
    casino_button.pack(fill="x")
    
    casino_submenu = customtkinter.CTkFrame(master=casino_frame, 
                                          fg_color=("#2B2B2B", "#1C1C1C"),
                                          corner_radius=12)
    
    coinflip_btn = customtkinter.CTkButton(master=casino_submenu, 
                                         text="🪙 Coin Flip", 
                                         command=show_casino,
                                         font=("Arial", 14, "bold"),
                                         height=45,
                                         fg_color="transparent",
                                         hover_color=("#4ECDC4", "#26D0CE"),
                                         corner_radius=10,
                                         anchor="w")
    coinflip_btn.pack(fill="x", padx=12, pady=8)
    
    number_btn = customtkinter.CTkButton(master=casino_submenu, 
                                       text="🔢 Number Guesser", 
                                       command=show_number_guesser,
                                       font=("Arial", 14, "bold"),
                                       height=45,
                                       fg_color="transparent",
                                       hover_color=("#9B59B6", "#8E44AD"),
                                       corner_radius=10,
                                       anchor="w")
    number_btn.pack(fill="x", padx=12, pady=8)
    
    roulette_btn = customtkinter.CTkButton(master=casino_submenu, 
                                         text="🎯 Roulette", 
                                         command=show_roulette,
                                         font=("Arial", 14, "bold"),
                                         height=45,
                                         fg_color="transparent",
                                         hover_color=("#E74C3C", "#C0392B"),
                                         corner_radius=10,
                                         anchor="w")
    roulette_btn.pack(fill="x", padx=12, pady=8)
    
    blackjack_btn = customtkinter.CTkButton(master=casino_submenu, 
                                          text="🃏 Blackjack", 
                                          command=show_blackjack,
                                          font=("Arial", 14, "bold"),
                                          height=45,
                                          fg_color="transparent",
                                          hover_color=("#2ECC71", "#27AE60"),
                                          corner_radius=10,
                                          anchor="w")
    blackjack_btn.pack(fill="x", padx=12, pady=8)
    
    dice_btn = customtkinter.CTkButton(master=casino_submenu, 
                                     text="🎲 Dice Roll", 
                                     command=show_dice_roll,
                                     font=("Arial", 14, "bold"),
                                     height=45,
                                     fg_color="transparent",
                                     hover_color=("#3498DB", "#2980B9"),
                                     corner_radius=10,
                                     anchor="w")
    dice_btn.pack(fill="x", padx=12, pady=8)
    
    slot_btn = customtkinter.CTkButton(master=casino_submenu, 
                                     text="🎰 Slot Machine", 
                                     command=show_slot_machine,
                                     font=("Arial", 14, "bold"),
                                     height=45,
                                     fg_color="transparent",
                                     hover_color=("#F39C12", "#E67E22"),
                                     corner_radius=10,
                                     anchor="w")
    slot_btn.pack(fill="x", padx=12, pady=8)
    
    def toggle_casino_menu():
        global sidebar_expanded
        if sidebar_expanded:
            casino_submenu.pack_forget()
            casino_button.configure(text="🎰 Casino Games ▼")
            sidebar_expanded = False
        else:
            casino_submenu.pack(fill="x", pady=(12, 0))
            casino_button.configure(text="🎰 Casino Games ▲")
            sidebar_expanded = True
    
    separator_line = customtkinter.CTkFrame(master=sidebar, 
                                          height=3, 
                                          fg_color=("#FFD700", "#FFA500"),
                                          corner_radius=2)
    separator_line.pack(fill="x", padx=30, pady=20)
    
    for button in buttons:
        btn = customtkinter.CTkButton(master=sidebar, 
                                    text=f"🛍️ {button}" if button == "Shop" else f"⚙ {button}" if button == "Settings" else f"🔄 {button}", 
                                    command=buttons[button],
                                    height=50,
                                    font=("Arial", 15, "bold"),
                                    fg_color=("#333333", "#2A2A2A"),
                                    hover_color=("#555555", "#404040"),
                                    corner_radius=15)
        btn.pack(pady=12, padx=15, fill="x")

    separator = customtkinter.CTkFrame(master=app, 
                                     width=3, 
                                     fg_color=("#FFD700", "#FFA500"))
    separator.pack(side="left", fill="y")

# Initialize sidebar after all functions are defined
buttons: Dict[str, Callable[[], None]] = {"Shop": show_shop, "Settings": show_settings, "Reload": reload}
create_sidebar(buttons)

main_frame = customtkinter.CTkFrame(master=app,
                                   fg_color=("#F0F0F0", "#1A1A1A"),
                                   corner_radius=0)
main_frame.pack(side="left", fill="both", expand=True)

show_casino()

app.mainloop()
