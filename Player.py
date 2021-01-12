import pygame
import io
# import requests

from Constants import *

pygame.init()

NAME_FONT = pygame.font.SysFont(None, 30)
TITLE_FONT = pygame.font.SysFont(None, 75, True)
MENU_FONT = pygame.font.SysFont(None, 60)
BTN_FONT = pygame.font.SysFont(None, 40)

# create the game window
WIDTH = 750
HEIGHT = 750
window = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Rap Poker')
#pygame.display.set_icon(card_back) decide on this later!!!!!!!!!!!

check_msg = BTN_FONT.render('Check', True, BLACK)
raise_msg = BTN_FONT.render('Raise', True, BLACK)
fold_msg = BTN_FONT.render('Fold', True, BLACK)
bet_msg = BTN_FONT.render('Bet', True, BLACK)
rap_msg = BTN_FONT.render('Rap', True, BLACK)
plus_msg = BTN_FONT.render('+', True, BLACK)
minus_msg = BTN_FONT.render('-', True, BLACK)

title_msg = TITLE_FONT.render('Rap Poker', False, BLACK)
rules_msg = MENU_FONT.render('Rules', True, BLACK)
play_msg = MENU_FONT.render('Play', True, BLACK)


def raw_card_back():  # load the image of the back of card
    card_image_url = session.get("http://res.freestockphotos.biz/originals/15/15686-illustration-of-a-play-card-"
                                 "back-or.png")
    img = io.BytesIO(card_image_url.content)
    return pygame.image.load(img)

card_back = pygame.transform.rotozoom(raw_card_back(), 0, 0.04)  # scale the image for the players
dp_card_back = pygame.transform.rotozoom(raw_card_back(), 0, 0.0425)  # scale the image for the draw pile !!!!!!!!!
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


    def display_hand(self):
        for index, card in enumerate(self.hand):
            pos = (index * 75 + 180, 525)
            window.blit(card.image, pos)

    def display_name_and_money(self):
        name_str = NAME_FONT.render(f"{self.name}  ${self.money}", True, BLACK)
        window.blit(name_str, (330, 690))  # this is overridden for the computer players

    def handle_draw(self, mouse_x, mouse_y):
        if is_over(dp_rect, mouse_x, mouse_y) and len(self.hand) == 5:  # draw from the discard pile
            dis_pile = self.game.discard_pile
            self.hand.append(dis_pile.pop())  # it should never be empty when this is called
        else:  # draw from the unknown pile
            self.hand.append(self.game.draw_card())

    def handle_discard(self, mouse_x, mouse_y):
        pop_index = (mouse_x - 180) // 75  # offset by the x position of the far left card
        pop_index = 5 if pop_index > 5 else pop_index  # keep index in range
        self.game.discard_pile.append(self.hand.pop(pop_index))


    def set_bet(self, mouse_x, mouse_y):  # handles the end of the turn, returns a boolean (made a bet)
            if is_over(check_rect, mouse_x, mouse_y):
                return False
            elif is_over(rap_rect, mouse_x, mouse_y):  # handle betting and wrapping at the same time?????????????????
                self.has_rapped = True
                self.game.rapping_player = self
                return False
            elif is_over(bet_rect, mouse_x, mouse_y):
                return True

    def handle_input(self, betting, has_discarded, *args):
        while True:
            self.game.display_all(betting=betting, has_discarded=has_discarded)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for rect in args:
                        if is_over(rect, mouse_x, mouse_y):
                            return (mouse_x, mouse_y)  # the position of a mouse click that does something

    def handle_bet(self, mouse_x, mouse_y):  # returns a tuple (True if they fold, value amount of raise)
        if is_over(fold_rect, mouse_x, mouse_y):
            return (True, 0)
        elif is_over(check_rect, mouse_x, mouse_y):
            #self.money -= cur_bet
            return (False, 0)
        elif is_over(check_rect, mouse_x, mouse_y):
            num = 5  # change this later!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return (False, num)

    def handle_already_bet(self, mouse_x, mouse_y):  # returns a boolean, will they fold
        if is_over(check_rect, mouse_x, mouse_y):
            return False
        elif is_over(fold_rect, mouse_x, mouse_y):
            return True


def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]
