import random
import time
from copy import deepcopy
from typing import List

import Utils
from Enums import PropertyTypeEnum
from Board import Board
from ConsoleLog import ConsoleLog
from Expectimax import expectiminimax
from Player import Player
from Property import Property

ACTIONS = {
    0: "does nothing",
    1: "buys property",
    2: "pays rent",
    3: "upgrades property",
    4: "downgrades property",
    5: "goes to jail",
    6: "stays in jail",
    7: "bails out of jail",
    8: "is freed from jail",
}


class Monopoly:
    def __init__(self, board: Board.board, players: List, current_player: int = 0, game_over: bool = False):
        self.game_over = game_over
        self.board = board
        self.players = players
        self.player_1 = players[0]
        self.player_2 = players[1]
        self.current_player = current_player

        self.chest_list = [
            {'money': 100, 'message': "Your friend owed you money, now he pays you back!"},
            {'money': -100, 'message': "Your sister wants a new ipad, she needs a $100!"},
            {'money': 50, 'message': "Your grandma gave you money. She tells you to buy candy for yourself!"},
            {'money': 200, 'message': "You received $200 for your birthday! Don't spend it on drugs!"},
            {'money': -200, 'message': "Oops! You lost $200. It maybe fell off your pocket."},
            {'money': 500,
             'message': "You won the national hot dog eating contest and won $500! Hope that'll cover your toilet repairs..."},
            {'money': -50, 'message': "Your phone died. pay $50 to repair it!"},
            {'money': -50, 'message': "Doctor's fee. Pay $50"},
            {'money': 100, 'message': "Holiday fund matures. Receive $100"},
            {'money': 100, 'message': "Life insurance matures. Collect $100"},
            {'money': 25, 'message': "Receive $25 consultancy fee"},
            {'money': 100, 'message': "You inherit $100."},
        ]

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def choose_a_random_chest(self):
        chosen_chest = random.randint(0, 5)
        ConsoleLog.print_chest_found(self.chest_list[chosen_chest])
        self.player_1.add_balance(money=self.chest_list[chosen_chest]['money'])

    def start_game(self):
        input("{}, Click <ENTER> to begin your go... ".format(self.player_1.name))
        player_turn = 1

        while not self.game_over:
            ConsoleLog.print_line()
            player_now = self.players[self.current_player]

            print("It's {} Turn.\n".format(player_now.name))
            time.sleep(0.5)

            rolled_dice = self.roll_dice()
            ConsoleLog.print_rolling_dice(rolled_dice)

            self.move_player(rolled_dice[0] + rolled_dice[1])
            if self.players[self.current_player].name == "Agent":
                _, best_action = expectiminimax(self.current_player, self)
                self.take_action(best_action)
            else:
            # Are you in Prison?!
                if self.player_1.prison_time > 0:
                    ConsoleLog.print_in_prison()

                    rolled_dice = self.roll_dice()
                    ConsoleLog.print_rolling_dice(rolled_dice)

                    if Utils.check_double_dice(dice=rolled_dice):
                        player_now.prison_time = 0
                        player_now.move_player(steps=rolled_dice[0] + rolled_dice[1])
                    else:
                        if player_now.prison_time >= 3:
                            player_now.get_out_of_jail()
                        else:
                            player_now.prison_time += 1
                # todo: make doubles zero when gone to jail
                else:
                    if not player_now.is_visiting:
                        player_now.prison_time = 0

                        # todo: do the logic
                        if self.board[player_now.position].property_type == PropertyTypeEnum.CHEST:
                            self.choose_a_random_chest()
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.INCOME_TAX:
                            player_now.apply_tax(tax_type=PropertyTypeEnum.INCOME_TAX)
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.SUPER_TAX:
                            player_now.apply_tax(tax_type=PropertyTypeEnum.SUPER_TAX)
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.JAIL:
                            player_now.handle_jail()
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.GO_TO_JAIL:
                            player_now.go_to_jail()
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.JUST_VISITING:
                            player_now.just_visiting()
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.LANDMARK:
                            player_now.land_on_property(self.board[player_now.position])
                        elif self.board[player_now.position].property_type == PropertyTypeEnum.AIRPORT:
                            player_now.land_on_airport(self.board[player_now.position])

                        if Utils.check_double_dice(rolled_dice):
                            player_now.set_doubled_dice_times(player_now.doubled_dice_times + 1)
                            player_now.check_doubled_dice_times()
                            print("You diced a double. Your turn again!")
                            player_now.work_with_properties()
                            player_now.check_positive_balance()
                            continue
                        else:
                            player_now.set_doubled_dice_times(0)
                    else:
                        player_now.set_doubled_dice_times(0)
                        player_now.is_visiting = False
                    player_now.work_with_properties()
                    player_now.check_positive_balance()

            if self.is_terminal():
                self.game_over = True
            else:
                self.switch_player()
        print(f"{self.players[0 if self.current_player else 1].name} Won!")


    def take_action(self, action: int):
        # Updating the game state based on the action taken by the current player
        new_players = deepcopy(self.players)
        new_board = deepcopy(self.board)
        curr_player = new_players[self.current_player]
        current_position = curr_player.position
        current_property = new_board[current_position]
        # Do the appropriate changes for the action
        if action == 0:
            pass
        elif action == 1:
            curr_player.buy_property(current_property)
        elif action == 2:
            curr_player.pay_rent(current_property.rent, current_property.owner)
        elif action == 3:
            current_property.upgrade()
        elif action == 4:
            current_property.downgrade()
        elif action == 5:
            curr_player.go_to_jail()
            curr_player.prison_time += 1
            # current_player.position = 10
            # current_player.in_jail = True
            # current_player.turns_in_jail += 1
        elif action == 6:
            curr_player.prison_time += 1
        elif action == 7:
            curr_player.get_out_of_jail_for_money()
        elif action == 8:
            curr_player.prison_time = 0
            # current_player.in_jail = False
            # current_player.turns_in_jail = 0
        return Monopoly(new_board, new_players, self.current_player, self.game_over)

    def get_possible_actions(self) -> list:
        # Get the possible actions available to the current player
        curr_player = self.players[self.current_player]
        curr_position = curr_player.position
        curr_prop: Property = self.board[curr_position]
        if curr_player.prison_time > 0:
            if curr_player.rolled_doubles:
                return [8]
            if curr_player.turns_in_jail >= 3:
                return [7]
            return [6, 7]
        if curr_prop.property_type == PropertyTypeEnum.AIRPORT or curr_prop.property_type == PropertyTypeEnum.LANDMARK:
            if curr_prop.owner == self.players[self.current_player]:
                if curr_prop.buildings_count < 5 and curr_prop.property_type != PropertyTypeEnum.AIRPORT:
                    return [3, 0]
                return [0]
            elif not curr_prop.owner:
                if curr_player.balance > curr_prop.price:
                    return [1, 0]
                return [0]
            else:
                return [2]
        if curr_prop.property_type == PropertyTypeEnum.GO_TO_JAIL:
            return [5]
        return [0]

    def move_player(self, dice_result: int) -> None:
        # Pass if the player is in jail
        if self.players[self.current_player].prison_time > 0:
            return
        curr_player = self.players[self.current_player]
        curr_position = curr_player.position
        # Update the player's position based on the dice roll result
        curr_position = (curr_position + dice_result) % len(self.board)
        curr_player.position = curr_position

    def is_terminal(self) -> bool:
        # Check if the game has reached a terminal state
        curr_player: Player = self.players[self.current_player]
        if curr_player.balance <= 0:
            return True
        return False

    def evaluate_utility(self):
        curr_player = self.players[self.current_player]
        # Evaluate the utility of the current game state for the current player
        return curr_player.net_worth(self.board)

    def switch_player(self):
        # Switch to the next player's turn
        self.current_player += 1
        self.current_player %= 2
