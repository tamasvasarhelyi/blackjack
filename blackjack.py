import random


def create_deck():
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
    rank, suit = card

    BLACK = "\033[30m"
    RED = "\033[31m"
    WHITE_BG = "\033[107m"
    RESET = "\033[0m"

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

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def print_hands(dealer_hand, player_hand, hidden=False):
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
        if i == 2 and not hidden:
            print(f"#{get_hand_value(player_hand)}", end=" ")
        print()

    print()


def play_round(money):
    player_hand = []
    dealer_hand = []

    deck = create_deck()

    game_over = False
    result = None

    while True:
        print(f"\nMoney: {money}")

        try:
            bet = int(input("Bet: "))
        except ValueError:
            print("Invalid input\n")
            continue

        if bet > money:
            print("Not enough money")
        elif bet <= 0:
            print("Bet must be positive")
        else:
            break

    for _ in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())

    print()

    while True:
        if get_hand_value(player_hand) >= 21:
            print_hands(dealer_hand, player_hand)
            if get_hand_value(player_hand) > 21:
                result = "lost"
                game_over = True
            break

        print_hands(dealer_hand, player_hand, hidden=True)

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
            print_hands(dealer_hand, player_hand)
            break

        elif choice == "d":
            if 2 * bet > money:
                print("Not enough money\n")
            else:
                bet *= 2
                player_hand.append(deck.pop())
                if get_hand_value(player_hand) > 21:
                    result = "lost"
                    game_over = True
                print_hands(dealer_hand, player_hand)
                break

    if not game_over:
        while get_hand_value(dealer_hand) < 17:
            input("press any key to continue\n")
            dealer_hand.append(deck.pop())
            print_hands(dealer_hand, player_hand)

            if get_hand_value(dealer_hand) > 21:
                result = "win"
                game_over = True

    if not game_over:
        if get_hand_value(player_hand) > get_hand_value(dealer_hand):
            result = "win"
        elif get_hand_value(player_hand) < get_hand_value(dealer_hand):
            result = "lost"
        else:
            result = "draw"

    if result == "win":
        print("You won!\n")
        money += bet
    elif result == "lost":
        print("You lost!\n")
        money -= bet
    elif result == "draw":
        print("Draw!\n")

    print(f"Money: {money}\n")

    return money


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
