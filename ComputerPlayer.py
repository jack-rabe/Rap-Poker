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
        # if :
        #     dis_pile = self.game.discard_pile
        #     self.hand.append(dis_pile.pop())  # it should never be empty when this is called
        # else:  # draw from the unknown pile
        self.hand.append(self.game.draw_card())
        print(f"{self.name} drew from the draw pile.")


    def handle_discard(self):
        pop_index = 0
        self.game.discard_pile.append(self.hand.pop(pop_index))
        print(f"{self.name} discarded a card.")

    def set_bet(self, final=False):  # returns a boolean (placed a bet), final is unused just to overload the method
        amount = 10
        if self.player_num == 2:
            self.transfer_money(amount)
            print(f"{self.name} placed a bet of ${amount}.")
            self.game.current_bet = amount
            return amount
            
        return 0

    def handle_bet(self):
        raise_amount = 5
        self.transfer_money(self.game.current_bet + raise_amount)
        print(f"{self.name} raised the amount by ${raise_amount}")
        return (False, raise_amount)  # this is a stub

    def handle_already_bet(self):  # returns a boolean, will they fold
        self.transfer_money(self.game.raise_amount)
        print(f"{self.name} has matched the bet")
        return False  

    def set_ante(self):
        amount= self.set_amount()
        self.transfer_money(amount)
        print(f"{self.name} set the ante to ${amount}.")
        return amount

    def set_amount(self):  # doesn't need to be overloaded
        amount = 10
        return amount