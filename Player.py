import pygame
import io
import time
from Constants import *


class Player:
    def __init__(self, name, game):
        self.name = name  # set during the main menu
        self.game = game
        self.hand = []  # list of 5 cards
        self.money = START_MONEY
        self.has_folded = False
        self.has_rapped = False
        self.is_turn = False

    # resets all of the necessary instance variables
    def reset(self):
        self.hand = []
        self.has_folded = False
        self.has_rapped = False
        self.is_turn = False

    # shows the cards of the human player
    def display_hand(self, show_front=True):  # show front is only for overloading
        for index, card in enumerate(self.hand):
            pos = (index * 75 + 180, 525)
            window.blit(card.image, pos)

    # shows the human player's name and amount of money
    def display_name_and_money(self):
        color = WHITE if self.is_turn else BLACK
        if self.has_folded:
            color = RED
        name_str = NAME_FONT.render(f"{self.name}  ${self.money}", True, color)
        window.blit(name_str, (330, 690))

    # draw a card from either the discard or draw pile
    def handle_draw(self):
        mouse_x, mouse_y = self.handle_input(dp_rect, draw_pile_rect)

        if is_over(dp_rect, mouse_x, mouse_y) and len(self.hand) == 5:  # draw from the discard pile
            dis_pile = self.game.discard_pile
            self.hand.append(dis_pile.pop())  # it should never be empty when this is called
        else:  # draw from the unknown pile
            self.hand.append(self.game.draw_card())

    # discard one of the cards in a six-card hand
    def handle_discard(self):
        mouse_x, mouse_y = self.handle_input(hand_rect)

        pop_index = (mouse_x - 180) // 75  # offset by the x position of the far left card
        pop_index = 5 if pop_index > 5 else pop_index  # keep index in range
        self.game.discard_pile.append(self.hand.pop(pop_index))

    # choose whether to set a bet and how much to set it for
    def set_bet(self, can_rap = True):  # returns 0 if no bet is made (or is wrapping) else returns the amount of the bet
        # if self.money <= 0:  # skip turn if out of money
        #     self.add_message(f"{self.name} did not place a bet.")
        #     return 0
            

        buttons = "discarded" if can_rap else "final"
        if can_rap:
            mouse_x, mouse_y = self.handle_input(check_rect, rap_rect, bet_rect, to_display=buttons)
        else:
            mouse_x, mouse_y = self.handle_input(check_rect, bet_rect, to_display=buttons)

        if is_over(check_rect, mouse_x, mouse_y):
            self.add_message("You did not place a bet.")
            return 0

        elif is_over(rap_rect, mouse_x, mouse_y):
            self.has_rapped = True
            self.game.rapping_player = self
            self.add_message("You rapped.")
            return 0

        elif is_over(bet_rect, mouse_x, mouse_y):  # set a bet amount
            amount = self.set_amount()
            self.game.current_bet = amount
            self.transfer_money(amount)
            self.add_message(f"You placed a bet of ${amount}.")
            return amount

    # display the appropriate buttons and piles for the player to make their decision 
    def handle_input(self, *btns, to_display=None, bet_amount=0):
        while True:
            self.game.display_all(to_display=to_display, bet_amount=bet_amount)
            button_list = list(btns)

            if to_display == "final" and rap_rect in button_list:  # handle the case where the player has already rapped and is placing a bet
                button_list.remove(rap_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for rect in btns:
                        if is_over(rect, mouse_x, mouse_y):
                            return (mouse_x, mouse_y)  # the position of a mouse click that does something

    # choose whether they want to raise or fold if a bet has already been made
    def handle_bet(self):  # returns a tuple (True if they fold, value amount of raise)
        if self.money <= 0:
            return (self.handle_already_bet, 0)
        mouse_x, mouse_y = self.handle_input(fold_rect, check_rect, raise_rect, to_display="betting")

        if is_over(fold_rect, mouse_x, mouse_y):
            msg = "You have folded."
            to_return  = (True, 0)
        elif is_over(check_rect, mouse_x, mouse_y):
            self.transfer_money(self.game.current_bet)
            msg = "You have matched the bet."
            to_return = (False, 0)
        elif is_over(raise_rect, mouse_x, mouse_y):
            raise_amount = self.set_amount()
            total = self.game.current_bet + raise_amount
            self.transfer_money(total)
            msg = f"You have raised the bet by ${raise_amount}."
            to_return = (False, raise_amount)
        
        self.add_message(msg)
        return to_return

    # choose whether to fold if someone raises after you
    def handle_already_bet(self):  # returns a boolean, will they fold
        mouse_x, mouse_y = self.handle_input(check_rect, fold_rect, to_display="already bet")
        if is_over(check_rect, mouse_x, mouse_y):
            self.transfer_money(self.game.raise_amount)
            msg = "You have matched the bet."
            to_return = False
        elif is_over(fold_rect, mouse_x, mouse_y):
            msg = "You have folded."
            to_return = True

        self.add_message(msg)
        return to_return

    # helper method for player to select how much to bet, does not handle the money tranfer
    def set_amount(self, button="placing bet", max_bet=2000):
        rect = place_rect if button == "placing bet" else ante_rect  # choose the message to display
        max_bet = min(self.money, max_bet)
        amount = 5

        input_x, input_y = self.handle_input(plus_rect, minus_rect, rect, to_display=button, bet_amount=amount)
        while not is_over(place_rect, input_x, input_y) or max_bet < amount:
            if is_over(plus_rect, input_x, input_y):
                amount += 5
            elif is_over(minus_rect, input_x, input_y) and amount > 5:
                amount -= 5
            elif amount >= max_bet:
                amount = max_bet
            input_x, input_y = self.handle_input(plus_rect, minus_rect, rect, to_display=button, bet_amount=amount)

        return amount

    # set the ante when the player is the dealer
    def set_ante(self):  # return the amount of the ante
        least_money = 2000
        for player in self.game.players:
            least_money = min(least_money, player.money)  # limit the ante to the lowest amount any player has

        ante = self.set_amount(button="ante", max_bet=least_money)
        self.transfer_money(ante)
        self.add_message(f"You set the ante to ${ante}.")
        return ante

    # helper method to move money from this player to the pot
    def transfer_money(self, amount):
        self.money -= amount
        self.game.pot += amount
    
    def add_message(self, msg):
        messages = self.game.msgs
        messages.append(msg)
