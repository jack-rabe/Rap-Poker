import requests
import pygame
import os

pygame.init()
START_MONEY = 20
WIDTH = 750
HEIGHT = 750
pygame.display.set_caption('Rap Poker')
# set the icon in top left corner
dir_name = os.path.dirname(__file__)
file_name = os.path.join(dir_name, "./images/mono-package-games-cards.png")
card_icon = pygame.image.load(file_name)
pygame.display.set_icon(card_icon)

# determines whether a point at (x, y) is on top of a rectangle
def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]

side_board_rect = (510, 10, 230, 180)
# button rectangles
check_rect = (25, 585, 125, 40)
raise_rect = (25, 630, 125, 40)
rap_rect = raise_rect
fold_rect = (25, 675, 125, 40)
bet_rect = fold_rect
place_rect = (10, 675, 150, 40)
ante_rect = (10, 675, 150, 40)
minus_rect = (170, 703, 25, 25)
plus_rect = (170, 663, 25, 25)
 # menu button rectangles
play_rect = (300, 414, 150, 50)
rules_rect = (300, 480, 150, 50)
# location of the hand and piles
draw_pile_rect = (270, 300, 90, 125)
dp_rect = (375, 300, 93, 127)
hand_rect = (180, 525, 465, 125)
# final screen buttons
again_rect = (250, 340, 250, 50)
quit_rect = (301, 405, 150, 50)

GREEN = (0, 200, 0)  # background color
BLUE = (0, 0, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)  # color of unselected buttons
LIGHT_GRAY = (150, 150, 150)  # color of selected buttons

NAMES = {"Jim", "Tim", "Jenny", "Jorge", "Tyrone", "Kate", "Jerry", "Francis", "Riley", "Todd",
         "Lucy", "Frank", "Kylie", "Camila", "Alexa", "Alayna", "Carter", "Ankit", "Mark",
         "Nathan", "Lauren", "Dylan", "Ava", "Matt", "Jacob", "Jennifer", "Seth", "Bernie", "Klaus",
        "Donna", "Phyllis", "Maddie", "Carly", "Brian", "Amanda"}

rules_txt = "Rap Poker is a card game played by four players. At the beginning of each game, the dealer \
sets the ante and deals five cards to each player. One card is flipped over to form the discard pile. \
The player to the left of the dealer is then given the opportunity to draw one card from the discard pile or \
draw pile. The player then discards a single card and has the opportunity to place a bet or rap before ending \
their turn. Play proceeds clockwise until someone raps. When a player raps, every other player gets one more turn \
before the final betting round. The winner takes the entire pot and is determined by standard poker scoring."

NAME_FONT = pygame.font.SysFont(None, 30)
MONEY_FONT = pygame.font.SysFont(None, 30)
TITLE_FONT = pygame.font.SysFont(None, 75, True)
MENU_FONT = pygame.font.SysFont(None, 60)
BTN_FONT = pygame.font.SysFont(None, 40)
SIDE_BAR_FONT = pygame.font.SysFont(None, 22)

# betting messages
check_msg = BTN_FONT.render('Check', True, BLACK)
raise_msg = BTN_FONT.render('Raise', True, BLACK)
fold_msg = BTN_FONT.render('Fold', True, BLACK)
# pre-bet messages
bet_msg = BTN_FONT.render('Bet', True, BLACK)
rap_msg = BTN_FONT.render('Rap', True, BLACK)
# place bet messages
plus_msg = BTN_FONT.render('+', True, BLACK)
minus_msg = BTN_FONT.render('-', True, BLACK)
place_msg = BTN_FONT.render("Place Bet", True, BLACK)
ante_msg = BTN_FONT.render("Set Ante", True, BLACK)
# menu screen messages
title_msg = TITLE_FONT.render('Rap Poker', False, BLACK)
rules_msg = MENU_FONT.render('Rules', True, BLACK)
play_msg = MENU_FONT.render('Play', True, BLACK)
# final screen messages
again_msg = MENU_FONT.render("Play Again", True, BLACK)
quit_msg = MENU_FONT.render("Quit", True, BLACK)

window = pygame.display.set_mode([WIDTH, HEIGHT])  # display screen
session = requests.Session()