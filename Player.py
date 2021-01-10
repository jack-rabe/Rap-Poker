import pygame
import io
import requests

pygame.init()

NAMES = ["Jim", "Tim", "Jenny", "Jorge", "Tyrone", "Kate", "Jerry", "Francis", "Riley", "Todd",
         "Lucy", "Frank", "Kylie", "Camila", "Alexa", "Alayna", "Carter", "Ankit", "Mark",
         "Nathan", "Lauren", "Dylan", "Ava", "Matt", "Jacob"]
START_MONEY = 500

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

session = requests.Session()


check_msg = BTN_FONT.render('Check', True, BLACK)
raise_msg = BTN_FONT.render('Raise', True, BLACK)
fold_msg = BTN_FONT.render('Fold', True, BLACK)
title_msg = TITLE_FONT.render('Rap Poker', False, BLACK)
rules_msg = MENU_FONT.render('Rules', True, BLACK)
play_msg = MENU_FONT.render('Play', True, BLACK)  # draw the play button


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

    def handle_draw(self):  # handles the pre-rap moves
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # draw from the discard pile
                if is_over(dp_rect, mouse_x, mouse_y) and len(self.hand) == 5:
                    dis_pile = self.game.discard_pile
                    self.hand.append(dis_pile.pop())  # it should never be empty when this is called

                # draw from the unknown pile
                elif is_over(draw_pile_rect, mouse_x, mouse_y) and len(self.hand) == 5:
                    self.hand.append(self.game.draw_card())

                # discard a card
                elif is_over(hand_rect, mouse_x, mouse_y) and len(self.hand) == 6:
                    pop_index = (mouse_x - 180) // 75  # offset by the x position of the far left card
                    pop_index = 5 if pop_index > 5 else pop_index  # keep index in range
                    self.game.discard_pile.append(self.hand.pop(pop_index))
                    return True

        return False

    def set_bet(self):  # handles the end of the turn
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over(check_rect, mouse_x, mouse_y):
                    pass  # nothing needs to be done
                elif is_over(raise_rect, mouse_x, mouse_y):
                    pass  # add code here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # elif is_over(fold_rect, mouse_x, mouse_y):
                #     pass
                else:
                    return False

                return True

def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]
