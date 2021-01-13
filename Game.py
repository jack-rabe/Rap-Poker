from Card import Card
from Player import *
from ComputerPlayer import ComputerPlayer
import time

# find an icon for the game!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# rules slide!!!!!!!!!!!!
# handle running out of cards!!!!!!!!!!!!!! in the deck
# handle player doesn't have enough money to make a bet
# handle only one player being able to rap at a time
# what is the order for players to be matching bets?
# add a rules info slide!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# allow negative $ amounts??????? only allow players to make bets that they can if they're setting it?
# limit ante to the amount of money of the lowest player
# make an actual ante button instead of place bet


class Game:
    def __init__(self):
        self.players = []  # list of 4 players
        self.deck = None  # stores the deck ID
        self.discard_pile = []
        self.rapping_player = None
        self.pot = 0
        self.current_bet = 0
        self.raise_amount = 0

    # handles resets and initial setup
    def deal(self):
        self.discard_pile.clear()
        for player in self.players:
            player.reset()
        self.rapping_player = False
        self.pot = 0

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

    # draws a single card from the deck
    def draw_card(self):
        card_request = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1")
        while card_request.status_code != 200:
            card_request = session.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1")
        card_json = card_request.json()

        t = card_json["cards"][0]
        self.deck = card_json["deck_id"]

        new_card = Card(t["image"], t["value"], t["suit"], session)
        return new_card

    # shows the draw and discard piles
    def display_pile(self):
        dp = self.discard_pile

        # display the face-up card
        if len(dp) >= 1:
            top_card = dp[len(dp) - 1].image
            window.blit(top_card, (375, 300))

        # display the drawing pile
        window.blit(dp_card_back, (270, 300))

    # shows the amount of money in the pot
    def display_pot(self):
        text = MONEY_FONT.render(f"Pot: ${self.pot}", True, BLACK)
        x_length, y_height = text.get_size()
        pos = (725 - x_length, 704)
        window.blit(text, pos)

    @staticmethod  # check, raise, and fold
    def display_bet_buttons():
        Game.display_already_bet_buttons()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the raise button
        raise_color = LIGHT_GRAY if is_over(raise_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, raise_color, raise_rect)
        window.blit(raise_msg, (47, 638))

    @staticmethod
    def display_already_bet_buttons():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        window.blit(check_msg, (45, 593))

        # draw the fold button
        fold_color = LIGHT_GRAY if is_over(fold_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, fold_color, fold_rect)
        window.blit(fold_msg, (55, 683))

    @staticmethod  # check, rap, and bet
    def display_prebet_buttons():
        Game.display_final()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the rap button
        rap_color = LIGHT_GRAY if is_over(rap_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, rap_color, rap_rect)
        window.blit(rap_msg, (58, 638))

    @staticmethod # plus, minus, place_bet, and $ amount of bet
    def display_plus_minus(bet_amount, button="place"):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        plus_color = LIGHT_GRAY if is_over(plus_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, plus_color, plus_rect)
        window.blit(plus_msg, (174, 662))

        minus_color = LIGHT_GRAY if is_over(minus_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, minus_color, minus_rect)
        window.blit(minus_msg, (178, 704))
        if button == "place":
            place_color = LIGHT_GRAY if is_over(place_rect, mouse_x, mouse_y) else GRAY
            pygame.draw.rect(window, place_color, place_rect)
            window.blit(place_msg, (22, 683))
            word = "Bet"
        else:
            ante_color = LIGHT_GRAY if is_over(ante_rect, mouse_x, mouse_y) else GRAY
            pygame.draw.rect(window, ante_color, ante_rect)
            window.blit(ante_msg, (28, 683))
            word = "Ante"

        current_bet = MONEY_FONT.render(f"{word}: ${bet_amount}", True, BLACK)
        offset = current_bet.get_size()[0] / 2
        window.blit(current_bet, (90 - offset, 625))

    @staticmethod # check and bet
    def display_final():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # draw the check button
        check_color = LIGHT_GRAY if is_over(check_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, check_color, check_rect)
        window.blit(check_msg, (45, 593))

        # draw the bet button
        bet_color = LIGHT_GRAY if is_over(bet_rect, mouse_x, mouse_y) else GRAY
        pygame.draw.rect(window, bet_color, bet_rect)
        window.blit(bet_msg, (62, 683))

    # only display method that updates display
    def display_all(self, to_display=None, bet_amount=0): #betting=False, has_discarded=False,already_bet=False, placing_bet=False, bet_amount=0, final=False
        window.fill(GREEN)  # update the graphics
        self.display_pile()
        self.display_pot()
        for player in self.players:
            player.display_hand()
            player.display_name_and_money()

        if to_display == "betting":
            Game.display_bet_buttons()
        elif to_display == "already bet":
            Game.display_already_bet_buttons()
        elif to_display == "discarded":
            Game.display_prebet_buttons()
        elif to_display == "final":
            Game.display_final()
        elif to_display == "placing bet":
            Game.display_plus_minus(bet_amount)
        elif to_display == "ante":
            Game.display_plus_minus(bet_amount, button="ante")

        pygame.display.update()

    def handle_all_bets(self, start_index):
        cur_index = start_index + 1 if start_index != 3 else 0
        already_moved = [self.players[start_index]]  # list of players who moved already

        while cur_index != start_index:
            cur_player = self.players[cur_index]

            if cur_player.has_folded:
                cur_index = cur_index + 1 if cur_index != 3 else 0  # next player
                continue
            cur_player.has_folded, raise_amount = (cur_player.handle_bet())

            if cur_player.has_folded:
                continue

            elif raise_amount != 0:  # determine if the other players will stay in
                self.raise_amount = raise_amount
                self.current_bet += raise_amount
                for player in already_moved:
                    player.has_folded = player.handle_already_bet()  # get rid of the raise button for this!!!!!!!!!!!!!!!!!!!!!

                    if player.has_folded:
                        already_moved.remove(player)  # is this part necessary!!!!!!!!!!!!!!!!!!!!!!!!!!!!       

            already_moved.insert(0, cur_player)  # this maybe should be switched to append?
            cur_index = cur_index + 1 if cur_index != 3 else 0  # next player

    def play_hand(self):
        self.players = self.players[1:] + [self.players[0]]  # switch the dealer
        print(f"{self.players[3].name} is dealing ...")
        self.deal()

        ante = self.players[3].set_ante()
        for player in self.players[:3]:
            player.money -= ante
            self.pot += ante

        next_player_index = None
        run = True
        while run:
            self.display_all()

            for player in self.players:
                if player.has_folded:
                    continue
                if next_player_index and self.players.index(player) != next_player_index:
                    continue
                elif player.has_rapped:
                    run = False  # initialize final betting round
                    break

                player.handle_draw()
                player.handle_discard()

                bet = player.set_bet()
                if bet != 0:
                    index = self.players.index(player)
                    next_player_index = index + 1 if index != 3 else 0
                    better_index = self.players.index(player)
                    self.current_bet = bet

                    self.handle_all_bets(better_index)
                    self.current_bet = 0
                    self.raise_amount = 0
                else:
                    next_player_index = None
                print(f'{player.name} has finished their turn')

        # final betting round
        self.current_bet = self.rapping_player.set_bet(final=True)
        # handle bets for the rest of the players
        index = self.players.index(self.rapping_player)
        self.handle_all_bets(index)

        # subtract the cash from the people and add it to the winner's account


        # show everyone's hand and the winner, switch this up later!!!!!!!!!!!!!!!
        for player in self.players:
            player.display_hand(show_front=True)
            pygame.display.update()
        time.sleep(1.5)

        print("Someone won. The hand is finished")

