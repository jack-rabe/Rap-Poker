from Game import *
import random

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

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_bg()
        draw_play_btn(mouse_x, mouse_y)
        draw_rules_btn(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over(rules_rect, mouse_x, mouse_y):
                    print("rules clicked")  # add a rules info slide!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    break
                elif is_over(play_rect, mouse_x, mouse_y):  # start the game
                    print("start playing")  # ask for a name???????????????

                    game = Game()
                    player = Player("Jack", game)  # this is temporary !!!!!!!!!!!!!!!!!!!!!!
                    game.players.append(player)  # the player part is temp!!!!!!!!!!!!!!!!!!!!!!!!!!
                    for i in range(1, 4):
                        new_name = NAMES.pop(random.randint(0, len(NAMES) - 1))
                        game.players.append(ComputerPlayer(new_name, game, i))

                    game.play_hand()  # this temp!!!!!!!!!!!!

        pygame.display.update()


draw_menu()
