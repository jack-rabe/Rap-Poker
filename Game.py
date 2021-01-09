import requests
from Card import Card
from Player import *
from ComputerPlayer import ComputerPlayer

# display names and money  (correct position for the number of letters
# fix pygame.display.update() to update the correct area!!!!!!!!!!!!!!!!!!!!
# find an icon for the game!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# add a way for the ante
# check for errors when making api calls
# rules slide!!!!!!!!!!!!
# handle running out of cards!!!!!!!!!!!!!!


class Game:
    def __init__(self):
        self.players = []  # list of 4 players
        self.dealer = 0  # index of the dealer in players
        self.deck = None  # stores the deck ID
        self.discard_pile = []

    def deal(self):
        self.discard_pile.clear()
        for player in self.players:
            player.reset()
        new_deck = session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        deck_id = new_deck.json()["deck_id"]

        for i in range(4):
            # draw 5 cards
            draw_hands = session.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=5").json()
            self.deck = draw_hands["deck_id"]
            cards = draw_hands["cards"]
            hand = []

            for card in cards:  # add the cards to the player's hand
                new_card = Card(card["image"], card["value"], card["suit"], session)
                hand.append(new_card)
            self.players[i].hand = hand

        # discard a single card before the game starts
        self.discard_pile.append(self.draw_card())

    def draw_card(self):
        card_json = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json()
        t = card_json["cards"][0]
        self.deck = card_json["deck_id"]

        new_card = Card(t["image"], t["value"], t["suit"], session)
        return new_card

    def display_pile(self):
        dp = self.discard_pile

        # display the face-up card
        if len(dp) >= 1:
            top_card = dp[len(dp) - 1].image
            window.blit(top_card, (375, 300))

        # display the drawing pile
        window.blit(dp_card_back, (270, 300))

    @staticmethod
    def display_buttons():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        window.blit(check_msg, (45, 593))

        # draw the fold button
        fold_color = LIGHT_GRAY if is_over(fold_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, fold_color, fold_rect)
        window.blit(fold_msg, (55, 683))

        # draw the raise button
        raise_color = LIGHT_GRAY if is_over(raise_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, raise_color, raise_rect)
        window.blit(raise_msg, (47, 638))

    def play_hand(self):
        self.deal()
        has_discarded = False
        run = True

        while run:
            window.fill(GREEN)  # update the graphics
            self.display_pile()
            Game.display_buttons()
            for player in self.players:
                player.display_hand()
                player.display_name_and_money()

            pygame.display.update()

            for player in self.players:
                if player.has_folded:
                    continue
                elif player.has_rapped:
                    run = False  # initialize final betting round
                    break
                if not has_discarded:
                    if player.handle_draw():  # wait for a move (from human player)
                        has_discarded = True
                    else:
                        break

                if has_discarded and run:
                    if not player.set_bet():  # wait for a move (from human player)
                        # the actual betting is called within the set_bet method!!!!!!!!!!!!!!!!!!!
                        # !! create a rap and bet for the main loop button!!!!! and money increment buttons + and -
                        #
                        break
                    else:
                        has_discarded = False
        # handle the final betting round here!!!!!!!!!!!!!!!!!!!, create handle bet method used for set bet and this

        #sfdfdkl


def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]
