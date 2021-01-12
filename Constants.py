import requests

# button rectangles
check_rect = (25, 585, 125, 40)
raise_rect = (25, 630, 125, 40)
rap_rect = raise_rect
fold_rect = (25, 675, 125, 40)
bet_rect = fold_rect

# menu button rectangeles
play_rect = (300, 414, 150, 50)
rules_rect = (300, 480, 150, 50)

# location of the hand and piles
draw_pile_rect = (270, 300, 90, 125)
dp_rect = (375, 300, 93, 127)
hand_rect = (180, 525, 465, 125)

GREEN = (0, 200, 0)  # background color
BLUE = (0, 0, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)  # color of the buttons
LIGHT_GRAY = (150, 150, 150)  # color of selected buttons

NAMES = ["Jim", "Tim", "Jenny", "Jorge", "Tyrone", "Kate", "Jerry", "Francis", "Riley", "Todd",
         "Lucy", "Frank", "Kylie", "Camila", "Alexa", "Alayna", "Carter", "Ankit", "Mark",
         "Nathan", "Lauren", "Dylan", "Ava", "Matt", "Jacob"]
rules_txt = "Rap Poker is a card game played by four players ..."
START_MONEY = 500

session = requests.Session()