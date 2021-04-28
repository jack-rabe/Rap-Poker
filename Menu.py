from Game import *
import ctypes  # creates the rules message box

rules_txt = "Rap Poker is a card game played by four players. At the beginning of each game, the dealer \
sets the ante and deals five cards to each player. One card is flipped over to form the discard pile. \
The player to the left of the dealer is then given the opportunity to draw one card from the discard pile or \
draw pile. The player then discards a single card and has the opportunity to place a bet or rap before ending \
their turn. Play proceeds clockwise until someone raps. When a player raps, every other player gets one more turn \
before the final betting round. The winner takes the entire pot and is determined by standard poker scoring."

def draw_final_screen():
    while True:
        window.fill(GREEN)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # play again button
        again_color = LIGHT_GRAY if is_over(again_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, again_color, again_rect)
        pygame.draw.rect(window, BLACK, again_rect, 2)
        window.blit(again_msg, (270, 346))
        # quit button
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

    while game.play_hand():
        pass

    draw_final_screen()


draw_menu()
