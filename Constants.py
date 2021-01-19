import requests
import pygame

pygame.init()

def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]

side_board_rect = (510, 10, 230, 180)
check_rect = (25, 585, 125, 40)  # button rectangles
raise_rect = (25, 630, 125, 40)
rap_rect = raise_rect
fold_rect = (25, 675, 125, 40)
bet_rect = fold_rect
place_rect = (10, 675, 150, 40)
ante_rect = (10, 675, 150, 40)
minus_rect = (170, 703, 25, 25)
plus_rect = (170, 663, 25, 25)
play_rect = (300, 414, 150, 50)  # menu button rectangles
rules_rect = (300, 480, 150, 50)
draw_pile_rect = (270, 300, 90, 125)  # location of the hand and piles
dp_rect = (375, 300, 93, 127)
hand_rect = (180, 525, 465, 125)

GREEN = (0, 200, 0)  # background color
BLUE = (0, 0, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)  # color of the buttons
LIGHT_GRAY = (150, 150, 150)  # color of selected buttons

NAMES = {"Jim", "Tim", "Jenny", "Jorge", "Tyrone", "Kate", "Jerry", "Francis", "Riley", "Todd",
         "Lucy", "Frank", "Kylie", "Camila", "Alexa", "Alayna", "Carter", "Ankit", "Mark",
         "Nathan", "Lauren", "Dylan", "Ava", "Matt", "Jacob", "Jennifer", "Seth", "Bernie", "Klaus",
        "Donna", "Phyllis", "Maddie", "Carly"}
START_MONEY = 500

NAME_FONT = pygame.font.SysFont(None, 30)
MONEY_FONT = pygame.font.SysFont(None, 30)
TITLE_FONT = pygame.font.SysFont(None, 75, True)
MENU_FONT = pygame.font.SysFont(None, 60)
BTN_FONT = pygame.font.SysFont(None, 40)
SIDE_BAR_FONT = pygame.font.SysFont(None, 22)

check_msg = BTN_FONT.render('Check', True, BLACK)  # betting messages
raise_msg = BTN_FONT.render('Raise', True, BLACK)
fold_msg = BTN_FONT.render('Fold', True, BLACK)
bet_msg = BTN_FONT.render('Bet', True, BLACK)  # pre-bet messages
rap_msg = BTN_FONT.render('Rap', True, BLACK)
plus_msg = BTN_FONT.render('+', True, BLACK)  # place bet messages
minus_msg = BTN_FONT.render('-', True, BLACK)
place_msg = BTN_FONT.render("Place Bet", True, BLACK)
ante_msg = BTN_FONT.render("Set Ante", True, BLACK)
title_msg = TITLE_FONT.render('Rap Poker', False, BLACK)  # menu screen messages
rules_msg = MENU_FONT.render('Rules', True, BLACK)
play_msg = MENU_FONT.render('Play', True, BLACK)

# create the game window
WIDTH = 750
HEIGHT = 750
pygame.display.set_caption('Rap Poker')
card_icon = pygame.image.load("mono-package-games-cards.png")  # maybe change this later????????
pygame.display.set_icon(card_icon)
window = pygame.display.set_mode([WIDTH, HEIGHT])

session = requests.Session()