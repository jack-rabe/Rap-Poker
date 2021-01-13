import pygame
import io
from Constants import *

def raw_card_back():  # load the image of the back of card
    card_image_url = session.get("http://res.freestockphotos.biz/originals/15/15686-illustration-of-a-play-card-"
                                 "back-or.png")
    img = io.BytesIO(card_image_url.content)
    return pygame.image.load(img)

raw_card_back = raw_card_back()
card_back = pygame.transform.rotozoom(raw_card_back, 0, 0.04)  # scale the image for the players
dp_card_back = pygame.transform.rotozoom(raw_card_back, 0, 0.0425)  # scale the image for the draw pile !!!!!!!!!
rotated_card_back = pygame.transform.rotate(card_back, 90)


class Player:
    def __init__(self, name, game):
        self.name = name  # set during the main menu
        self.game = game
        self.hand = []  # list of 5 cards
        self.money = START_MONEY
        self.has_folded = False
        self.has_rapped = False

    # resets all of the necessary instance variables
    def reset(self):
        self.hand = []
        self.has_folded = False
        self.has_rapped = False

    # shows the cards of the human player
    def display_hand(self, show_front=True):  # show front is only for overloading
        for index, card in enumerate(self.hand):
            pos = (index * 75 + 180, 525)
            window.blit(card.image, pos)

    # shows the human player's name and amount of money
    def display_name_and_money(self):
        name_str = NAME_FONT.render(f"{self.name}  ${self.money}", True, BLACK)
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
    def set_bet(self, final=False):  # returns 0 if no bet is made (or is wrapping) else returns the amount of the bet
        buttons = "final" if final else "discarded"
        mouse_x, mouse_y = self.handle_input(check_rect, rap_rect, bet_rect, to_display=buttons)

        if is_over(check_rect, mouse_x, mouse_y):
            return False

        elif is_over(rap_rect, mouse_x, mouse_y):  # handle betting and wrapping at the same time?????????????????
            self.has_rapped = True
            self.game.rapping_player = self
            print("You rapped.")
            return False

        elif is_over(bet_rect, mouse_x, mouse_y):  # set a bet amount
            amount = self.set_amount()
            print(f"You placed a bet of ${amount}.")
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
        mouse_x, mouse_y = self.handle_input(fold_rect, check_rect, raise_rect, to_display="betting")

        if is_over(fold_rect, mouse_x, mouse_y):
            print("You have folded.")
            return (True, 0)
        elif is_over(check_rect, mouse_x, mouse_y):
            self.money -= self.game.current_bet
            print("You have matched the bet")
            return (False, 0)
        elif is_over(raise_rect, mouse_x, mouse_y):
            num = self.set_amount() + self.game.current_bet
            print("You have raised the bet.")
            return (False, num)

    # choose whether to fold if someone raises after you
    def handle_already_bet(self):  # returns a boolean, will they fold
        mouse_x, mouse_y = self.handle_input(check_rect, fold_rect, to_display="already bet")

        if is_over(check_rect, mouse_x, mouse_y):
            self.money -= self.game.raise_amount
            print("You have matched the bet.")
            return False
        elif is_over(fold_rect, mouse_x, mouse_y):
            print("You have folded.")
            return True

    # helper method for player to select how much to bet
    def set_amount(self, button="placing bet"):
        rect = place_rect if button == "placing bet" else ante_rect  # choose the message to display
        amount = 5
        input_x, input_y = self.handle_input(plus_rect, minus_rect, rect, to_display=button, bet_amount=amount)
        while not is_over(place_rect, input_x, input_y) or self.money <= amount:
            if is_over(plus_rect, input_x, input_y):
                amount += 5
            elif amount > 5:
                amount -= 5
            elif self.money <= amount:
                print(f"You don't have ${amount}.")
            input_x, input_y = self.handle_input(plus_rect, minus_rect, rect, to_display=button, bet_amount=amount)

        self.money -= amount
        self.game.pot += amount
        return amount

    # set the ante when the player is the dealer
    def set_ante(self):  # return the amount of the ante
        ante = self.set_amount(button="ante")
        print(f"You set the ante to ${ante}.")
        return ante
