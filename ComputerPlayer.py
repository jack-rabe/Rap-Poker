from Player import Player, window, rotated_card_back, card_back, NAME_FONT, BLACK, WHITE, RED, is_over
import pygame
import time
import random

class ComputerPlayer(Player):
    def __init__(self, name, game, player_num):
        super(ComputerPlayer, self).__init__(name, game)
        self.player_num = player_num

    def display_hand(self, show_front=False):
        if show_front:
            self.hand.sort()
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
        if self.has_folded:
            color = RED
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
        def possible_hands():
            possible = []
            for i in range(4):
                copy = self.hand[:]
                copy.insert(i, new_card)
                copy.pop(i + 1)
                possible.append(copy)
            return possible

        self.slow_turn()
        new_card = self.game.discard_pile[len(self.game.discard_pile) - 1]
        current_strength = self.determine_value(self.hand)
        draw_strength = max([self.determine_value(hand) for hand in possible_hands()])
        difference = draw_strength - current_strength

        if difference > random.randint(2, 3):  # play with this number!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.hand.append(self.game.discard_pile.pop())
            print(f"{self.name} drew from the discard pile.")
        else:
            self.hand.append(self.game.draw_card())
            print(f"{self.name} drew from the draw pile.")
        self.slow_turn()

    def handle_discard(self):
        def possible_hands():
            possible = []
            for i in range(6):
                copy = self.hand[:]
                copy.pop(i)
                possible.append(copy)
            return possible
        
        self.slow_turn()
        max_strength = 0
        pop_index = 0
        for index, hand in enumerate(possible_hands()):
            current_strength = self.determine_value(hand)
            if current_strength > max_strength:
                max_strength = current_strength
                pop_index = index

        self.game.discard_pile.append(self.hand.pop(pop_index))
        print(f"{self.name} discarded a card.")
        self.slow_turn()

    def set_bet(self, can_rap=True):  # returns a number (amount of bet)
        self.slow_turn()
        if self.money <= 0:  # skip turn if out of money!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.add_message(f"{self.name} did not place a bet.")
            return 0

        if can_rap:
            current_hand_val = self.game.hand_val(self.hand)[0] # number from 0-9
            if current_hand_val >= 4: # rap if hand is good, sometimes randomly, increase with num_turns!!!!!!!!!!!!!!!! add random chance
                self.has_rapped = True
                self.game.rapping_player = self
                self.add_message(f"{self.name} rapped.")
                self.slow_turn()
                return 0

        if self.determine_value(self.hand) >= (15 + self.game.turn_num * 5) and random.randint(0, 1) == 1: # choose to bet, adjust!!!!!!!!!!!!!!!!!!!!!
            amount = random.randrange(5, 30, 5)  # account for hand value here!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.game.current_bet = amount
            self.transfer_money(amount)
            self.add_message(f"{self.name} bet ${amount}.")
            self.slow_turn()
            return amount

        else:  # choose not to bet
            self.add_message(f"{self.name} did not place a bet.")
            self.slow_turn()
            return 0

    def handle_bet(self):
        self.slow_turn()
        random_num = random.randint(0, 100)# make this actually mean something!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if random_num < 10:  # raise
            raise_amount = random.randrange(5, 20, 5)  # account for hand value here!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.game.raise_amount = raise_amount
            self.transfer_money(self.game.current_bet + raise_amount)
            self.add_message(f"{self.name} raised the amount by ${raise_amount}.")
            return (False, raise_amount)

        elif 10 <= random_num <= 90:  # match bet
            self.transfer_money(self.game.current_bet)
            self.add_message(f"{self.name} has matched the bet.")
            self.slow_turn()
            return (False, 0)

        else:  # fold
            self.add_message(f"{self.name} has folded.")
            self.slow_turn()
            return (True, 0)

    def handle_already_bet(self):  # returns a boolean, will they fold
        self.slow_turn()
        random_num  = random.randint(0, 9)

        if random_num != 0:  # stay in
            self.transfer_money(self.game.raise_amount)
            self.add_message(f"{self.name} has matched the bet.")
            self.slow_turn()
            return False

        else:  # fold
            self.add_message(f"{self.name} has folded.")
            self.slow_turn()
            return True

    def set_ante(self):
        self.slow_turn()
        amount= 10
        self.transfer_money(amount)
        self.add_message(f"{self.name} set the ante to ${amount}.")
        self.slow_turn()
        return amount

    def slow_turn(self):
        time.sleep(.5)
        self.game.display_all()

    def determine_value(self, hand):
        total = 0
        royals = "JQKA"
        suits = []
        values = []
        values_dict = {}
        suits_dict = {}

        # rearrange hand to make it easier to evaluate
        for card in hand:
            suit, val = card.suit, card.value
            if val.isalpha():
                val = val[0]
            if val in royals:
                val = 11 + royals.index(val)
            values.append(int(val))
            suits.append(suit[0])
        values.sort()

        for val in values:
            if val not in values_dict:
                values_dict[val] = 1
            else:
                values_dict[val] += 1
        for suit in suits:
            if suit not in suits_dict:
                suits_dict[suit] = 1
            else:
                suits_dict[suit] += 1

        # check for flushes and near flushes
        if len(suits_dict) == 1:
            total += 40
        elif 4 in suits_dict.values():
            total += 20
        elif 3 in suits_dict.values():
            total += 8

        # check for straights and near straights
        max_straight = 1
        cur_straight = 1
        for i in range(4):
            difference = values[i + 1] - values[i]
            if difference == 1:
                cur_straight += 1
            elif difference == 2 and i == 3 and cur_straight != 4:
                cur_straight += 1
            elif difference != 2:  # don't reset if the gap is only 1 card
                cur_straight = 1
            max_straight = max(max_straight, cur_straight)
        if max_straight == 3:
            total += 5
        elif max_straight == 4:
            total += 15
        elif max_straight == 5:
            total += 35
        
        # check for pairs/full houses
        if len(values_dict) == 4:
            total += 10
        elif len(values_dict) == 3:
            if 3 in values_dict.values():
                total += 15  # three of a kind
            else:
                total += 25 # two pair
        elif len(values_dict) == 2:
            if 4 in values_dict.values():
                total += 60  # four of a kind
            else:
                total += 50  # full house
        
        if values[4] > 11: # add 2-3 for high cards
            total += (values[4] - 10)

        return total

    