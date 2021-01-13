from Game import *
from Constants import rules_txt
import ctypes  # creates the rules message box

def draw_menu():
    def draw_bg():
        window.fill(GREEN)
        window.blit(title_msg, (230, 100))

    def draw_play_btn(x, y):
        color = LIGHT_GRAY if is_over(play_rect, x, y) else GRAY
        pygame.draw.rect(window, color, play_rect)
        window.blit(play_msg, (330, 420))

    def draw_rules_btn(x, y):
        color = LIGHT_GRAY if is_over(rules_rect, x, y) else GRAY
        pygame.draw.rect(window, color, rules_rect)
        window.blit(rules_msg, (320, 487))

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_bg()
        draw_play_btn(mouse_x, mouse_y)
        draw_rules_btn(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over(rules_rect, mouse_x, mouse_y):
                    ctypes.windll.user32.MessageBoxW(0, rules_txt, "Rap Poker Rules", 1)
                    break
                elif is_over(play_rect, mouse_x, mouse_y):  # start the game
                    running = False

        pygame.display.update()

    game = Game()  # start game and initialize all players
    player = Player("You", game)
    game.players.append(player)
    for i in range(1, 4):
        new_name = NAMES.pop()
        game.players.append(ComputerPlayer(new_name, game, i))

    while True:  # this temp!!!!!!!!!!!!
        game.play_hand()

draw_menu()
