from Card import Card
from Player import *
from ComputerPlayer import ComputerPlayer
import time
import pygame


class Game:
    def __init__(self):
        self.players = []  # list of 4 players
        self.deck = None  # stores the deck ID
        self.cards_left = 32
        self.discard_pile = []
        self.rapping_player = None
        self.pot = 0
        self.current_bet = 0
        self.raise_amount = 0
        self.msgs = []
        self.turn_num = 0

    def check_reshuffle(self):  # shuffles the deck when the draw pile has been used up
        if self.cards_left == 0:
            deck_cards = [card.__str__() for card in self.discard_pile]
            self.discard_pile = []
            to_shuffle = ",".join(deck_cards)

            shuffled_deck = session.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?cards={to_shuffle}")
            while shuffled_deck.status_code != 200:
                shuffled_deck = session.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?cards={to_shuffle}")
            self.deck = shuffled_deck.json()["deck_id"]
            self.cards_left = shuffled_deck.json()["remaining"]

            # discard a single card
            self.discard_pile.append(self.draw_card())
            self.players[0].add_message("The deck has been reshuffled.")
            # reset the display
            self.display_all()

    # handles resets and initial setup
    def deal(self):
        self.discard_pile.clear()
        self.cards_left = 52 - len(self.players) * 5
        for player in self.players:
            player.reset()
        self.rapping_player = None
        self.pot = 0
        self.current_bet = 0
        self.raise_amount = 0
        self.turn_num = 0
        self.msgs = []

        new_deck = session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        while new_deck.status_code != 200:
            new_deck = session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        deck_id = new_deck.json()["deck_id"]

        for i in range(len(self.players)):
            # draw 5 cards
            draw_hands = session.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=5")
            while draw_hands.status_code != 200:
                draw_hands = session.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=5")
            draw_hands = draw_hands.json()

            self.deck = draw_hands["deck_id"]
            cards = draw_hands["cards"]
            hand = []

            for card in cards:  # add the cards to the player's hand
                new_card = Card(card["image"], card["value"], card["suit"], session)
                hand.append(new_card)
            self.players[i].hand = hand

        # discard a single card before the game starts
        self.discard_pile.append(self.draw_card())
        # reset the display
        self.display_all()

    # draws a single card from the deck
    def draw_card(self):
        card_request = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1")
        while card_request.status_code != 200:
            card_request = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1")
        card_json = card_request.json()

        t = card_json["cards"][0]
        self.deck = card_json["deck_id"]
        self.cards_left = card_json["remaining"]

        new_card = Card(t["image"], t["value"], t["suit"], session)
        return new_card

    def display_hand_values(self):
        nonfolded_players = [player for player in self.players if not player.has_folded]
        for index, player in enumerate(nonfolded_players):
            def val_to_string(points):
                if points == 0:
                    high_card = max(player.hand).value
                    high_card = high_card[0] + high_card[1:].lower()
                    string = f"{high_card} high"
                elif points == 1:
                    string = "One pair"
                elif points == 2:
                    string = "Two pair"
                elif points == 3:
                    string = "Three of a kind"
                elif points == 4:
                    string = "Straight"
                elif points == 5:
                    string = "Flush"
                elif points == 6:
                    string = "Full house"
                elif points == 7:
                    string = "Four of a kind"
                else:
                    string = "Straight flush" if max(player.hand).value != "KING" else "Royal flush"
                return string
            
            points = self.hand_val(player.hand)[0]
            string = val_to_string(points)
            
            name_str = SIDE_BAR_FONT.render(f"{player.name}:  {string}", True, BLACK)
            pos = (10, 10 + index * 25)
            window.blit(name_str, pos)

    # check, raise, and fold, calls already_bet_buttons()
    def display_bet_buttons(self):
        self.display_already_bet_buttons()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the raise button
        raise_color = LIGHT_GRAY if is_over(raise_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, raise_color, raise_rect)
        pygame.draw.rect(window, BLACK, raise_rect, 2)
        window.blit(raise_msg, (47, 638))

    def display_already_bet_buttons(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.display_current_bet()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        pygame.draw.rect(window, BLACK, check_rect, 2)
        window.blit(check_msg, (45, 593))

        # draw the fold button
        fold_color = LIGHT_GRAY if is_over(fold_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, fold_color, fold_rect)
        pygame.draw.rect(window, BLACK, fold_rect, 2)
        window.blit(fold_msg, (55, 683))

    # check, rap, and bet
    def display_prebet_buttons(self):
        self.display_final()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the rap button
        rap_color = LIGHT_GRAY if is_over(rap_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, rap_color, rap_rect)
        pygame.draw.rect(window, BLACK, rap_rect, 2)
        window.blit(rap_msg, (58, 638))

    # plus, minus, place_bet, and $ amount of bet
    def display_plus_minus(self, bet_amount, button="place"):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        plus_color = LIGHT_GRAY if is_over(plus_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, plus_color, plus_rect)
        pygame.draw.rect(window, BLACK, plus_rect, 2)
        window.blit(plus_msg, (175, 661))

        minus_color = LIGHT_GRAY if is_over(minus_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, minus_color, minus_rect)
        pygame.draw.rect(window, BLACK, minus_rect, 2)
        window.blit(minus_msg, (178, 704))
        if button == "place":
            place_color = LIGHT_GRAY if is_over(place_rect, mouse_x, mouse_y) else GRAY
            pygame.draw.rect(window, place_color, place_rect)
            pygame.draw.rect(window, BLACK, place_rect, 2)
            window.blit(place_msg, (22, 683))
            word = "Bet"
            self.display_current_bet()
        else:
            ante_color = LIGHT_GRAY if is_over(ante_rect, mouse_x, mouse_y) else GRAY
            pygame.draw.rect(window, ante_color, ante_rect)
            pygame.draw.rect(window, BLACK, ante_rect, 2)
            window.blit(ante_msg, (28, 683))
            word = "Ante"

        bet_choice = MONEY_FONT.render(f"{word}: ${bet_amount}", True, BLACK)
        offset = bet_choice.get_size()[0] / 2
        window.blit(bet_choice, (90 - offset, 625))

    # check and bet
    def display_final(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.display_current_bet()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        pygame.draw.rect(window, BLACK, check_rect, 2)
        window.blit(check_msg, (45, 593))

        # draw the bet button
        bet_color = LIGHT_GRAY if is_over(bet_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, bet_color, bet_rect)
        pygame.draw.rect(window, BLACK, bet_rect, 2)
        window.blit(bet_msg, (62, 683))

    def display_current_bet(self):
        bet = MONEY_FONT.render(f"Current Bet: ${self.current_bet}", True, BLACK)
        offset = bet.get_size()[0] / 2
        window.blit(bet, (375 - offset, 450))
            
    # only display method that updates display
    def display_all(self, to_display=None, bet_amount=0):
        def display_pot():  # shows the amount of money in the pot
            text = MONEY_FONT.render(f"Pot: ${self.pot}", True, BLACK)
            x_length, y_height = text.get_size()
            pos = (725 - x_length, 704)
            window.blit(text, pos)

        def display_pile():  # displays the draw and discard piles
                dp = self.discard_pile
                # display the face-up card
                if len(dp) >= 1:
                    top_card = dp[len(dp) - 1].image
                    window.blit(top_card, (375, 300))
                # display the drawing pile
                if self.cards_left >= 1:
                    window.blit(dp_card_back, (270, 300))
    
        def display_msgs():
            def display_msg(msg, line_num):
                line_one = SIDE_BAR_FONT.render(msg, True, BLACK)
                line_two = ""
                words = msg.split()
                x_pos, y_pos = 515, 15 + line_num * 25

                while line_one.get_size()[0] > max_length:  # checks if the message needs to be displayed on a new line
                    line_two += (words[-1] + " ")
                    words = words[:-1]
                    line_one = "".join([word + " " for word in words])
                    line_one = SIDE_BAR_FONT.render(line_one, True, BLACK)

                if len(line_two) == 0:
                    window.blit(line_one, (x_pos, y_pos))
                    return True
                else:  # two lines are needed to display the message
                    reversed_list = []
                    for word in  line_two.split():
                        reversed_list.insert(0, word)
                    line_two = "".join(word + " " for word in reversed_list)     #   reversed(line_two)
                    line_two = SIDE_BAR_FONT.render(line_two, True, BLACK)

                    window.blit(line_one, (x_pos, y_pos))
                    window.blit(line_two, (x_pos, y_pos + 25))
                    return False
            line_num = 0
            max_length = 222
            num_lines = 0
            messages = self.msgs
                    
            pygame.draw.rect(window, WHITE, side_board_rect)
            pygame.draw.rect(window, BLACK, side_board_rect, 2)

            for msg in messages:  # remove old messages
                line_one = SIDE_BAR_FONT.render(msg, True, BLACK)  
                if line_one.get_size()[0] > max_length:
                    num_lines += 1
            extra_lines = -7 + len(messages) + num_lines
            if extra_lines > 0:
                for i in range(extra_lines):
                    messages.pop(0)

            for msg in messages:  # display current messages
                if not display_msg(msg, line_num):  # if it is two lines long, add 2
                    line_num += 1
                line_num += 1

        window.fill(GREEN)
        display_pile()
        display_pot()
        for player in self.players:
            player.display_hand()
            player.display_name_and_money()
        display_msgs()
        
        disp = to_display  # display the amount of the current betting round
        if disp == "betting":
            self.display_bet_buttons()
        elif disp == "already bet":
            self.display_already_bet_buttons()
        elif disp == "discarded":
            self.display_prebet_buttons()
        elif disp == "final":
            self.display_final()
        elif disp == "placing bet":
            self.display_plus_minus(bet_amount)
        elif disp == "ante":
            self.display_plus_minus(bet_amount, button="ante")

        pygame.display.update()

    def hand_finished(self):
        # determine the winner of the hand and transfer money
        winner = self.determine_winner()
        winner.add_message(f"{winner.name} won ${self.pot}.")
        winner.transfer_money(-self.pot)

        # show everyone's hand and the winner
        self.display_all()
        for player in self.players:
            player.display_hand(show_front=True)
            self.display_hand_values()
            pygame.display.update()
        check_for_quit(60, skip=True)  # if player clicks they can skip the wait time, otherwise 15 seconds

        # remove players who don't have enough money
        money_list = [p.money for p in self.players]
        num_removed = 0
        for i in range(len(money_list)):
            if money_list[i] <= 0:
                winner.add_message(f"{self.players[i - num_removed].name} has run out of money.")
                self.players.pop(i - num_removed)
                num_removed += 1
                check_for_quit(4)
    
    def hand_val(self, hand): # returns a tuple representing the value of the hand
        royals = "JQKA"
        suits = set()
        values = []
        values_dict = {}
        def search_dict(value, exclude=0):
            for k, v in values_dict.items():
                if v == value and k != exclude:
                    return k

        for card in hand:
            suit, val = card.suit, card.value
            suits.add(suit)
            if val.isalpha():
                val = val[0]
            if val in royals:
                val = 11 + royals.index(val)
            values.append(int(val))
        values.sort()

        for val in values:
            if val not in values_dict:
                values_dict[val] = 1
            else:
                values_dict[val] += 1

        # check for value of hand
        is_flush = False
        if len(suits) == 1:
            is_flush = True
        
        is_straight = True
        for i in range(4):
            if values[i + 1] - values[i] != 1:
                is_straight = False
                break
        
        one_pair = True if len(values_dict) == 4 else False
        if one_pair:
            pair_val = search_dict(2)

        three_of_kind = False
        two_pair = False
        if len(values_dict) == 3:
            if 3 in values_dict.values():
                three_of_kind = True
                pair_val = search_dict(3)
            else:
                two_pair = True
                first_pair = search_dict(2)
                second_pair = search_dict(2, exclude=first_pair)
                high = max(first_pair, second_pair)
                low = min(first_pair, second_pair)
                pair_val = (high, low)
        
        four_of_kind = False
        full_house = False
        if len(values_dict) == 2:
            if 4 in values_dict.values():
                four_of_kind = True
                pair_val = search_dict(4)
            else:
                full_house = True
                pair_val = (search_dict(3), search_dict(2))

        # add points for type of hand
        if one_pair:
            total_value = 1, pair_val
        elif two_pair:
            total_value = 2, pair_val
        elif three_of_kind:
            total_value = 3, pair_val
        elif is_straight and not is_flush:
            total_value = 4, None
        elif is_flush and not is_straight:
            total_value = 5, None
        elif full_house:
            total_value = 6, pair_val
        elif four_of_kind:
            total_value = 7, pair_val
        elif is_straight and is_flush:
            total_value = 8, None
        else:
            total_value = 0, None

        return total_value # always a tuple

    def determine_winner(self):
        hands = []
        temp_players = []
        for player in self.players:
            if not player.has_folded:
                hands.append(player.hand)
                temp_players.append(player)

        best_hand = hands[0]
        best_hand_val = self.hand_val(hands[0])  # a tuple with score, pair
        best_high = max(hands[0])
        index = 0

        for i in range(1, len(hands)):  # put the winner/tied in a list
            cur_val = self.hand_val(hands[i])
            cur_high = max(hands[i])
            if cur_val > best_hand_val or (cur_val == best_hand_val and best_high < cur_high):
                best_hand = hands[i]
                best_hand_val = cur_val
                best_high = cur_high
                index = i

            elif cur_val == best_hand_val and cur_high == best_high: # still equal
                best_tuple = tuple(sorted(best_hand, reverse=True))
                cur_tuple = tuple(sorted(hands[i], reverse=True))
                if cur_tuple > best_tuple:
                    best_hand = hands[i]
                    index = i

        return temp_players[index]

    def handle_all_bets(self, start_index):
        cur_index = start_index + 1 if start_index != (len(self.players) - 1) else 0
        already_moved = [self.players[start_index]]  # list of players who moved already

        while cur_index != start_index:
            cur_player = self.players[cur_index]

            if cur_player.has_folded:
                cur_index = cur_index + 1 if cur_index != (len(self.players) - 1) else 0  # next player
                continue
            cur_player.has_folded, raise_amount = (cur_player.handle_bet())

            if cur_player.has_folded:
                continue

            elif raise_amount != 0:  # determine if the other players will stay in
                self.raise_amount = raise_amount
                self.current_bet += raise_amount
                for player in already_moved:
                    player.has_folded = player.handle_already_bet()

                    if player.has_folded:
                        already_moved.remove(player)      

            already_moved.insert(0, cur_player)
            cur_index = cur_index + 1 if cur_index != (len(self.players) - 1) else 0  # next player

        self.current_bet = 0
        self.raise_amount = 0
        check_for_quit(1)

    def play_hand(self):
        self.players = self.players[1:] + [self.players[0]]  # switch the dealer
        self.players[len(self.players) - 1].add_message(f"{self.players[len(self.players) - 1].name} is dealing.")
        self.deal()

        dealer = self.players[len(self.players) - 1]
        ante = dealer.set_ante()
        for player in self.players[:len(self.players) - 1]:
            player.transfer_money(ante)

        next_player_index = None
        run = True
        while run:
            self.display_all()
            self.turn_num += 1

            for player in self.players:
                check_for_quit(1)
                if player.has_rapped:
                    run = False  # initialize final betting round
                    break
                elif player.has_folded:
                    if next_player_index == self.players.index(player):
                        next_player_index = next_player_index + 1 if next_player_index != (len(self.players) - 1) else 0
                    continue
                if next_player_index and self.players.index(player) != next_player_index:
                    continue
                if player.has_rapped:
                    run = False  # initialize final betting round
                    break

                player.is_turn = True
                player.handle_draw()
                player.handle_discard()

                can_rap = False if self.rapping_player else True
                bet = player.set_bet(can_rap=can_rap)
                if bet != 0:
                    index = self.players.index(player)
                    next_player_index = index + 1 if index != (len(self.players) - 1) else 0
                    better_index = self.players.index(player)

                    self.handle_all_bets(better_index)
                else:
                    next_player_index = None


                player.is_turn = False
                player.add_message((f'{player.name} has finished their turn.'))
                self.check_reshuffle()

        # final betting round
        for player in self.players:
            self.is_turn = False

        better_index = -1  # wait for one of the players to bet
        cur_index = self.players.index(self.rapping_player)
        for i in range(len(self.players)):
            cur_player = self.players[cur_index]
            if cur_player.has_folded:
                continue
            bet = cur_player.set_bet(can_rap=False)
            if bet != 0:
                self.current_bet = bet
                better_index = cur_index
                break
            else:
                cur_index = cur_index + 1 if cur_index != (len(self.players) - 1) else 0

        # handle bets for the rest of the players
        if better_index != -1:
            self.handle_all_bets(better_index)
        # transfer money, remove players who lost, display results
        self.hand_finished()
        # determine if there is a final winner
        return len(self.players) != 1


def check_for_quit(cycles, skip=False):  # checks for quitting every .25 seconds, if skip is True a click will exit the method
    for i in range(cycles):
        time.sleep(.25)
        outer_break = False  # break out of both loops if clicked
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif i > 1 and skip and event.type == pygame.MOUSEBUTTONDOWN:
                    outer_break = True

        if outer_break:
            break

