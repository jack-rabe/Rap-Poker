from Player import Player, window, rotated_card_back, card_back, NAME_FONT, BLACK, is_over
import pygame

class ComputerPlayer(Player):
    def __init__(self, name, game, player_num):
        super(ComputerPlayer, self).__init__(name, game)
        self.player_num = player_num

    def display_hand(self, show_front=False):
        if show_front:
            if self.player_num == 1:  # left player
                for index, card in enumerate(self.hand):
                    rotated_image = pygame.transform.rotozoom(card.image, 90, 1)
                    window.blit(rotated_image, (75, index * 40 + 225))
            elif self.player_num == 2:  # top player
                for index, card in enumerate(self.hand):
                    window.blit(card.image, (index * 40 + 250, 75))
            elif self.player_num == 3:  # right player
                for index, card in enumerate(reversed(self.hand)):
                    rotated_image = pygame.transform.rotozoom(card.image, 270, 1)
                    window.blit(rotated_image, (550, 385 - (index * 40)))
        else:
            if self.player_num == 1:  # left player
                for index, card in enumerate(self.hand):
                    window.blit(rotated_card_back, (75, index * 40 + 225))
            elif self.player_num == 2:  # top player
                for index, card in enumerate(self.hand):
                    window.blit(card_back, (index * 40 + 250, 75))
            elif self.player_num == 3:  # right player
                for index, card in enumerate(self.hand):
                    window.blit(rotated_card_back, (550, 225 + (index * 40)))

    def display_name_and_money(self):
        name_str = NAME_FONT.render(f"{self.name}  ${self.money}", True, BLACK)
        x_size, y_size = name_str.get_size()  # account for varying string sizes
        offset =  x_size / 2

        if self.player_num == 1:
            name_str = pygame.transform.rotozoom(name_str, 90, 1)
            name_loc = (25, 360 - offset)
        elif self.player_num == 2:
            name_loc = (375 - offset, 25)
        else:
            name_str = pygame.transform.rotozoom(name_str, 270, 1)
            name_loc = (700, 360 - offset)

        window.blit(name_str, name_loc)

    def handle_draw(self):
        # method stub!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

    def handle_discard(self):
        pass

    def set_bet(self, final=False):  # returns a boolean (placed a bet), one and two are unused just to overload the method
        if self.player_num == 2:
            print(f"{self.name} placed a bet")
            return True
        return 0# also a stub !!!!!!!!!!!

    def handle_bet(self):
        print(f"{self.name} raised the amount by $5")
        return (False, 5)  # this is a stub

    def handle_already_bet(self):  # returns a boolean, will they fold
        return False  # stub!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def set_ante(self):
        pass