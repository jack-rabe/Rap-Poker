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

    def reset(self):
        self.hand = []
        self.has_folded = False
        self.has_rapped = False

    def display_hand(self, show_front=True):  # show front is only for overloading
        for index, card in enumerate(self.hand):
            pos = (index * 75 + 180, 525)
            window.blit(card.image, pos)

    def display_name_and_money(self):
        name_str = NAME_FONT.render(f"{self.name}  ${self.money}", True, BLACK)
        window.blit(name_str, (330, 690))

    def handle_draw(self):
        mouse_x, mouse_y = self.handle_input(dp_rect, draw_pile_rect)

        if is_over(dp_rect, mouse_x, mouse_y) and len(self.hand) == 5:  # draw from the discard pile
            dis_pile = self.game.discard_pile
            self.hand.append(dis_pile.pop())  # it should never be empty when this is called
        else:  # draw from the unknown pile
            self.hand.append(self.game.draw_card())

    def handle_discard(self):
        mouse_x, mouse_y = self.handle_input(hand_rect)

        pop_index = (mouse_x - 180) // 75  # offset by the x position of the far left card
        pop_index = 5 if pop_index > 5 else pop_index  # keep index in range
        self.game.discard_pile.append(self.hand.pop(pop_index))

    def set_bet(self, final=False):  # returns 0 if no bet is made (or is wrapping) else returns the amount of the bet
        discarded = False if final else True
        mouse_x, mouse_y = self.handle_input(check_rect, rap_rect, bet_rect, discarded=discarded, final=final)

        if is_over(check_rect, mouse_x, mouse_y):
            return False

        elif is_over(rap_rect, mouse_x, mouse_y):  # handle betting and wrapping at the same time?????????????????
            self.has_rapped = True
            self.game.rapping_player = self
            return False

        elif is_over(bet_rect, mouse_x, mouse_y):  # set a bet amount
            amount = self.set_amount()
            return amount

    def handle_input(self, *btns, betting=False, discarded=False, already_bet=False, placing_bet=False, bet_amount=0, final=False):
        while True:
            self.game.display_all(betting=betting, has_discarded=discarded, already_bet=already_bet, placing_bet=placing_bet, bet_amount=bet_amount, final=final)
            button_list = list(btns)

            if final and rap_rect in button_list:  # handle the case where the player has already rapped and is placing a bet
                button_list.remove(rap_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for rect in btns:
                        if is_over(rect, mouse_x, mouse_y):
                            return (mouse_x, mouse_y)  # the position of a mouse click that does something

    def handle_bet(self):  # returns a tuple (True if they fold, value amount of raise)
        mouse_x, mouse_y = self.handle_input(fold_rect, check_rect, raise_rect, betting=True)

        if is_over(fold_rect, mouse_x, mouse_y):
            return (True, 0)
        elif is_over(check_rect, mouse_x, mouse_y):
            #self.money -= cur_bet
            return (False, 0)
        elif is_over(raise_rect, mouse_x, mouse_y):
            num = self.set_amount()  # change this later!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print(f"You have raised by ${num}.")
            return (False, num)

    def handle_already_bet(self):  # returns a boolean, will they fold
        mouse_x, mouse_y = self.handle_input(check_rect, fold_rect, already_bet=True)

        if is_over(check_rect, mouse_x, mouse_y):
            return False
        elif is_over(fold_rect, mouse_x, mouse_y):
            return True

    def set_amount(self):
        amount = 5
        input_x, input_y = self.handle_input(plus_rect, minus_rect, place_rect, placing_bet=True, bet_amount=amount)
        while not is_over(place_rect, input_x, input_y) or self.money <= amount:
            if is_over(plus_rect, input_x, input_y):
                amount += 5
            elif amount > 5:
                amount -= 5
            elif self.money <= amount:
                print(f"You don't have ${amount}.")
            input_x, input_y = self.handle_input(plus_rect, minus_rect, place_rect, placing_bet=True, bet_amount=amount)

        self.money -= amount
        self.game.pot += amount
        return amount

    def set_ante(self):
        pass

def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]
