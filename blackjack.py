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
    print("Dealer:", end=" ")
    for i, card in enumerate(dealer_hand):
        if i == 0 and hidden:
            print("??", end=" ")
        else:
            print(f"{card[0]}{card[1]}", end=" ")

    if not hidden:
        print(f"  #{get_hand_value(dealer_hand)}", end=" ")

    print()

    print("Player:", end=" ")
    for card in player_hand:
        print(f"{card[0]}{card[1]}", end=" ")

    if not hidden:
        print(f"  #{get_hand_value(player_hand)}", end=" ")

    print()

player_hand = []
dealer_hand = []

deck = create_deck()

game_over = False
result = None

for _ in range(2):
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())


while True:
    if get_hand_value(player_hand) >= 21:
        print_hands(dealer_hand, player_hand)
        if get_hand_value(player_hand) > 21:
            result = "lost"
            game_over = True
        break

    print_hands(dealer_hand, player_hand, hidden=True)

    choice = input("Hit or Stand? (h/s): ")

    print()

    if choice == "h":
        player_hand.append(deck.pop())

    if choice == "s":
        print_hands(dealer_hand, player_hand)
        break


if not game_over:
    while get_hand_value(dealer_hand) < 17:
        input("press any key to continue")
        print()
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
    print("You won!")
elif result == "lost":
    print("You lost!")
elif result == "draw":
    print("Draw!")
