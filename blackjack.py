import random


# ANSI escape codes for terminal colors.
BLACK = "\033[30m"
RED = "\033[31m"
WHITE_BG = "\033[107m"
RESET = "\033[0m"
CLEAR_SCREEN = "\033[2J\033[H"


def create_deck():
    """Create and shuffle a standard 52-card deck."""

    suits = ("♠", "♥", "♦", "♣")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
    deck = []

    for suit in suits:
        for rank in ranks:
            card = (rank, suit)
            deck.append(card)

    random.shuffle(deck)

    return deck


def get_card(card):
    """Return a three-line colored ASCII representation of a card."""

    rank, suit = card

    if suit in ("♥", "♦"):
        color = RED
    else:
        color = BLACK

    return [
        f"{WHITE_BG}{color}{rank:<2}   {RESET}",
        f"{WHITE_BG}{color}  {suit}  {RESET}",
        f"{WHITE_BG}{color}   {rank:>2}{RESET}"
    ]


def get_hand_value(hand):
    """Calculate the Blackjack value of a hand."""

    value = 0
    aces = 0

    for card in hand:
        if card[0] in ['J', 'Q', 'K']:
            value += 10
        elif card[0] == 'A':
            aces += 1
            value += 11
        else:
            value += int(card[0])

    # Convert aces from 11 to 1 as needed to avoid busting.
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def print_hands(dealer_hand, player_hand, hidden=False):
    """Display both hands, optionally hiding the dealer's first card."""

    print("Dealer:")

    for i in range(3):
        for j, card in enumerate(dealer_hand):
            if j == 0 and hidden:
                print("?????", end=" ")
            else:
                print(f"{get_card(card)[i]}", end=" ")
        if i == 2 and not hidden:
            print(f"#{get_hand_value(dealer_hand)}", end=" ")
        print()

    print()

    print("Player:")

    for i in range(3):
        for card in player_hand:
            print(f"{get_card(card)[i]}", end=" ")
        if i == 2:
            print(f"#{get_hand_value(player_hand)}", end=" ")
        print()

    print()


def print_table(money, bet, dealer_hand, player_hand, hidden=False):
    """Clear the screen and display the current game table."""

    print(CLEAR_SCREEN, end="")

    print(f"Money: {money}")
    print(f"Bet: {bet}\n")

    print_hands(dealer_hand, player_hand, hidden)


def play_round(money):
    """Play one round of Blackjack and return the updated balance."""

    player_hand = []
    dealer_hand = []

    deck = create_deck()

    game_over = False
    result = None

    while True:
        print(f"{CLEAR_SCREEN}Money: {money}")

        try:
            bet = int(input("Bet: "))
        except ValueError:
            print("Invalid input\n")
            continue

        if bet > money:
            print("Not enough money")
        elif bet <= 0:
            print("Bet must be positive")
        elif bet % 2 != 0:
            print("Bet must be even")
        else:
            break

    for _ in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())

    player_blackjack = len(player_hand) == 2 and get_hand_value(player_hand) == 21
    dealer_blackjack = len(dealer_hand) == 2 and get_hand_value(dealer_hand) == 21

    print()

    # Check for a natural Blackjack before starting the player's turn.
    if player_blackjack:
        print_table(money, bet, dealer_hand, player_hand)

        if dealer_blackjack:
            result = "draw"
        else:
            result = "win"

        game_over = True

    # Player's turn.
    if not game_over:
        while True:
            if get_hand_value(player_hand) == 21:
                print_table(money, bet, dealer_hand, player_hand)
                break
            elif get_hand_value(player_hand) > 21:
                print_table(money, bet, dealer_hand, player_hand, hidden=True)
                result = "lost"
                game_over = True
                break

            print_table(money, bet, dealer_hand, player_hand, hidden=True)

            if len(player_hand) == 2:
                choice = input("Hit, Stand or Double Down? (h/s/d): ").lower()
                while choice not in ["h", "s", "d"]:
                    print("Invalid choice\n")
                    choice = input("Hit, Stand or Double Down? (h/s/d): ").lower()
            else:
                choice = input("Hit or Stand? (h/s): ").lower()
                while choice not in ["h", "s"]:
                    print("Invalid choice\n")
                    choice = input("Hit or Stand? (h/s): ").lower()

            print()

            if choice == "h":
                player_hand.append(deck.pop())

            elif choice == "s":
                print_table(money, bet, dealer_hand, player_hand)
                break

            elif choice == "d":
                if 2 * bet > money:
                    input("Not enough money\nPress any key to continue\n")
                else:
                    bet *= 2
                    player_hand.append(deck.pop())

                    if get_hand_value(player_hand) > 21:
                        result = "lost"
                        game_over = True
                        print_table(money, bet, dealer_hand, player_hand, hidden=True)
                    else:
                        print_table(money, bet, dealer_hand, player_hand)

                    break

    # Dealer's turn.
    if not game_over:
        if dealer_blackjack:
            result = "lost"
            game_over = True
        else:
            while get_hand_value(dealer_hand) < 17:
                input("press any key to continue\n")
                dealer_hand.append(deck.pop())
                print_table(money, bet, dealer_hand, player_hand)

                if get_hand_value(dealer_hand) > 21:
                    result = "win"
                    game_over = True


    # Determine the result if neither player has busted.
    if not game_over:
        if get_hand_value(player_hand) > get_hand_value(dealer_hand):
            result = "win"
        elif get_hand_value(player_hand) < get_hand_value(dealer_hand):
            result = "lost"
        else:
            result = "draw"

    if result == "win":
        if player_blackjack:
            print("Blackjack!\n")
            money += bet * 3 // 2
        else:
            print("You won!\n")
            money += bet
    elif result == "lost":
        print("You lost!\n")
        money -= bet
    elif result == "draw":
        print("Draw!\n")

    print(f"Money: {money}\n")

    return money


def main():
    money = 5000

    while True:
        money = play_round(money)

        if money <= 0:
            print("Out of money!")
            break

        again = input("Play again? (y/n): ").lower()
        while again not in ["y", "n"]:
            print("Invalid choice\n")
            again = input("Play again? (y/n): ").lower()

        if again == "n":
            break


if __name__ == "__main__":
    main()
