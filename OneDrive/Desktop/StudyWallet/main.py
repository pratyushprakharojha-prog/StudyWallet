import os
from colorama import Fore, Style, init
from tracker import (
    setup_budget,
    add_expense,
    add_stock,
    check_stocks,
    monthly_report
)

# activates colorama for Windows
init(autoreset=True)

def clear():
    # clears the terminal screen for a clean look
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear()
    print(Fore.CYAN + "\n╔══════════════════════════════════╗")
    print(Fore.CYAN + "║       💰 STUDYWALLET 💰          ║")
    print(Fore.CYAN + "║  College Student Finance Tracker ║")
    print(Fore.CYAN + "╚══════════════════════════════════╝")
    print(Fore.YELLOW + "\n  1. 💰 Set Monthly Budget")
    print(Fore.YELLOW + "  2. ➕ Add Expense")
    print(Fore.YELLOW + "  3. 📈 Add Stock Investment")
    print(Fore.YELLOW + "  4. 📊 Check Stock Profit/Loss")
    print(Fore.YELLOW + "  5. 📋 View Monthly Report")
    print(Fore.YELLOW + "  6. 🚪 Exit")
    print(Fore.CYAN + "\n══════════════════════════════════")

def main():
    clear()
    print(Fore.GREEN + "\nWelcome to StudyWallet!")
    print(Fore.WHITE + "Your personal college finance tracker.")

    while True:
        show_menu()
        choice = input(Fore.GREEN + "\nChoose an option (1-6): ").strip()

        if choice == "1":
            setup_budget()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            add_stock()
        elif choice == "4":
            check_stocks()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            clear()
            print(Fore.CYAN + "\nGoodbye! Stay broke-proof. 💪\n")
            break
        else:
            print(Fore.RED + "Invalid option — please choose between 1 and 6.")

if __name__ == "__main__":
    main()