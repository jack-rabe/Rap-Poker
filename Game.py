from Card import Card
from Player import *
from ComputerPlayer import ComputerPlayer

# display names and money  (correct position for the number of letters
# fix pygame.display.update() to update the correct area!!!!!!!!!!!!!!!!!!!!
# find an icon for the game!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# add a way for the ante
# rules slide!!!!!!!!!!!!
# handle running out of cards!!!!!!!!!!!!!! in the deck
# handle player doesn't have enough money to make a bet
# handle only one player being able to rap at a time
# what is the order for players to be matching bets?


class Game:
    def __init__(self):
        self.players = []  # list of 4 players
        self.dealer = 0  # index of the dealer in players
        self.deck = None  # stores the deck ID
        self.discard_pile = []
        self.rapping_player = None

    def deal(self):
        self.discard_pile.clear()
        for player in self.players:
            player.reset()
        self.rapping_player = False
        new_deck = session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        while new_deck.status_code != 200:
            new_deck = session.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        deck_id = new_deck.json()["deck_id"]

        for i in range(4):
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

    def draw_card(self):
        card_request = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1")
        while card_request.status_code != 200:
            card_request = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1")
        card_json = card_request.json()

        t = card_json["cards"][0]
        self.deck = card_json["deck_id"]

        new_card = Card(t["image"], t["value"], t["suit"], session)
        return new_card

    def display_pile(self):
        dp = self.discard_pile

        # display the face-up card
        if len(dp) >= 1:
            top_card = dp[len(dp) - 1].image
            window.blit(top_card, (375, 300))

        # display the drawing pile
        window.blit(dp_card_back, (270, 300))

    @staticmethod
    def display_bet_buttons():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        window.blit(check_msg, (45, 593))

        # draw the raise button
        raise_color = LIGHT_GRAY if is_over(raise_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, raise_color, raise_rect)
        window.blit(raise_msg, (47, 638))

        # draw the fold button
        fold_color = LIGHT_GRAY if is_over(fold_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, fold_color, fold_rect)
        window.blit(fold_msg, (55, 683))

    @staticmethod
    def display_prebet_buttons():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        window.blit(check_msg, (45, 593))

        # draw the rap button
        rap_color = LIGHT_GRAY if is_over(rap_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, rap_color, rap_rect)
        window.blit(rap_msg, (58, 638))

        # draw the bet button
        bet_color = LIGHT_GRAY if is_over(bet_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, bet_color, bet_rect)
        window.blit(bet_msg, (62, 683))

        # move from here probably!!!!!!!!!!!!!!!!!!!!11
        plus_rect = (170, 663, 25, 25)
        plus_color = LIGHT_GRAY if is_over(plus_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, plus_color, plus_rect)
        window.blit(plus_msg, (174, 662))

        minus_rect = (170, 703, 25, 25)
        minus_color = LIGHT_GRAY if is_over(minus_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, minus_color, minus_rect)
        window.blit(minus_msg, (178, 704))

    def display_all(self, betting, has_discarded):
        window.fill(GREEN)  # update the graphics
        self.display_pile()
        for player in self.players:
            player.display_hand()
            player.display_name_and_money()

        if betting:
            Game.display_bet_buttons()
        elif has_discarded:
            Game.display_prebet_buttons()

        pygame.display.update()

    def handle_all_bets(self, start_index):
        cur_index = start_index + 1 if start_index != 3 else 0
        already_moved = [self.players[start_index]]  # list of players who moved already

        while cur_index != start_index:
            cur_player = self.players[cur_index]

            if type(cur_player) != ComputerPlayer:
                bet_x, bet_y = cur_player.handle_input(True, False, check_rect, fold_rect, raise_rect)
                cur_player.has_folded, raise_amount = (cur_player.handle_bet(bet_x, bet_y))
            else:
                cur_player.has_folded, raise_amount = (cur_player.handle_bet())

            if cur_player.has_folded:
                print(f"{cur_player.name} has folded")
                continue

            elif raise_amount != 0:  # determine if the other players will stay in
                for player in already_moved:
                    if type(player) != ComputerPlayer:
                        stay_x, stay_y = player.handle_input(True, False, check_rect, fold_rect)  # get rid of the raise button for this!!!!!!!!!!!!!!!!!!!!!
                        player.has_folded = player.handle_already_bet(stay_x, stay_y)
                        if player.has_folded:
                            already_moved.remove(player)
                            print(f"{player.name} has folded")
                            continue

                    else:
                        player.has_folded = player.handle_already_bet()
                    print(f"{player.name} has matched {cur_player.name}'s bet")

            already_moved.insert(0, cur_player)  # this maybe should be switched to append?
            cur_index = cur_index + 1 if cur_index != 3 else 0  # next player


    def play_hand(self):
        self.deal()
        run = True
        next_player_index = None

        while run:
            self.display_all(False, False)

            for player in self.players:
                if player.has_folded:
                    continue
                if next_player_index and self.players.index(player) != next_player_index:
                    continue
                elif player.has_rapped:
                    run = False  # initialize final betting round
                    break

                if type(player) == ComputerPlayer:
                    player.handle_draw()
                    if player.set_bet(0, 0):
                        index = self.players.index(player)
                        next_player_index = index + 1 if index != 3 else 0
                        better_index = self.players.index(player)

                        self.handle_all_bets(better_index)
                    else:
                        next_player_index = None
                    print(f'{player.name} has finished their turn')

                else:  # handle normal players
                    draw_x, draw_y = player.handle_input(False, False, dp_rect, draw_pile_rect)  # draw a card
                    player.handle_draw(draw_x, draw_y)

                    discard_x, discard_y = player.handle_input(False, False, hand_rect)  # discard a card
                    player.handle_discard(discard_x, discard_y)

                    bet_x, bet_y = player.handle_input(False, True, check_rect, rap_rect, bet_rect)
                    if player.set_bet(bet_x, bet_y):
                        index = self.players.index(player)
                        next_player_index = index + 1 if index != 3 else 0
                        better_index = self.players.index(player)

                        self.handle_all_bets(better_index)
                    else:
                        next_player_index = None  # reset the next player if no betting occurred

        # final betting round
        final_x, final_y = 0, 0  # set the initial bet
        if type(self.rapping_player) != ComputerPlayer:
            final_x, final_y = self.rapping_player.handle_input(False, True, check_rect, bet_rect)############## don't show fold_rect
        self.rapping_player.set_bet(final_x, final_y)

        # handle bets for the rest of the players
        index = self.players.index(self.rapping_player)
        self.handle_all_bets(index)

        print("finished")



def is_over(rect, x, y):
    left = rect[0]
    top = rect[1]
    return left < x < left + rect[2] and top < y < top + rect[3]
