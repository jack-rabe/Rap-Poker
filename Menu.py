from Game import window, Game, Player, ComputerPlayer
from Constants import rules_txt, is_over, NAMES
from Constants import again_rect, again_msg, quit_rect, quit_msg, rules_rect, rules_msg, play_rect, title_msg, play_msg
from Constants import LIGHT_GRAY, BLACK, GRAY, GREEN
import ctypes  # creates the rules message box
import pygame

def draw_final_screen():
    while True:
        window.fill(GREEN)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # draw play again button
        again_color = LIGHT_GRAY if is_over(again_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, again_color, again_rect)
        pygame.draw.rect(window, BLACK, again_rect, 2)
        window.blit(again_msg, (270, 346))
        # draw quit button
        quit_color = LIGHT_GRAY if is_over(quit_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, quit_color, quit_rect)
        pygame.draw.rect(window, BLACK, quit_rect, 2)
        window.blit(quit_msg, (327, 412))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN and is_over(quit_rect, mouse_x, mouse_y):
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_over(again_rect, mouse_x, mouse_y):
                   start_game()  # restart another game


def draw_menu():
    def draw_bg():
        window.fill(GREEN)
        window.blit(title_msg, (230, 100))

    def draw_play_btn(x, y):
        color = LIGHT_GRAY if is_over(play_rect, x, y) else GRAY
        pygame.draw.rect(window, color, play_rect)
        pygame.draw.rect(window, BLACK, play_rect, 2)
        window.blit(play_msg, (330, 420))

    def draw_rules_btn(x, y):
        color = LIGHT_GRAY if is_over(rules_rect, x, y) else GRAY
        pygame.draw.rect(window, color, rules_rect)
        pygame.draw.rect(window, BLACK, rules_rect, 2)
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

    start_game()

def start_game():
    game = Game()  # start game and initialize all players
    player = Player("You", game)
    game.players.append(player)
    for i in range(1, 4):
        new_name = NAMES.pop()
        game.players.append(ComputerPlayer(new_name, game, i))

    while game.play_hand(): # continues until one player remains
        pass

    draw_final_screen()  # allow players to quit or start new game


draw_menu()
