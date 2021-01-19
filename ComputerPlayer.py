from Player import Player, window, rotated_card_back, card_back, NAME_FONT, BLACK, WHITE, is_over
import pygame
import time

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
        color = WHITE if self.is_turn else BLACK
        name_str = NAME_FONT.render(f"{self.name}  ${self.money}", True, color)
        x_size = name_str.get_size()[0]  # account for varying string sizes
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
        # if :
        #     dis_pile = self.game.discard_pile
        #     self.hand.append(dis_pile.pop())  # it should never be empty when this is called
        # else:  # draw from the unknown pile
        self.slow_turn()
        self.hand.append(self.game.draw_card())
        print(f"{self.name} drew from the draw pile.")
        self.slow_turn()

    def handle_discard(self):
        self.slow_turn()
        pop_index = 0
        self.game.discard_pile.append(self.hand.pop(pop_index))
        print(f"{self.name} discarded a card.")
        self.slow_turn()

    def set_bet(self, final=False):  # returns a boolean (placed a bet), final is unused just to overload the method
        self.slow_turn()
        amount = 10
        # if self.player_num == 2:  # player 2 always bets, no one else does
        #     self.transfer_money(amount)
        #     self.add_message(f"{self.name} placed a bet of ${amount}.")
        #     self.game.current_bet = amount
        # else:
        #     self.add_message(f"{self.name} did not place a bet.")
        #     amount = 0
        
        self.slow_turn()
        return 0

    def handle_bet(self):
        # self.slow_turn()
        # raise_amount = 5
        # self.transfer_money(self.game.current_bet + raise_amount)
        # self.add_message(f"{self.name} raised the amount by ${raise_amount}.")

        self.slow_turn()
        return (False, 0)  # this is a stub

    def handle_already_bet(self):  # returns a boolean, will they fold
        self.slow_turn()
        self.transfer_money(self.game.raise_amount)
        self.add_message(f"{self.name} has matched the bet.")
        self.slow_turn()
        return False  

    def set_ante(self):
        self.slow_turn()
        amount= self.set_amount()
        self.transfer_money(amount)
        self.add_message(f"{self.name} set the ante to ${amount}.")
        self.slow_turn()
        return amount

    def set_amount(self):  # doesn't need to be overloaded
        amount = 10
        return amount

    def slow_turn(self):
        time.sleep(.25)
        self.game.display_all()