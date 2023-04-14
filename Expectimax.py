# from monopoly import Monopoly

Probabilities = {
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}

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


def min_node(main_player: int, state, depth: int) -> tuple:
    min_eval = float('inf')
    possible_actions = state.get_possible_actions()
    for action in possible_actions:
        # Take the action in a copy of the state
        new_state = state.take_action(action)
        # We should also switch the player
        new_state.switch_player()
        # Recursively call expectiminimax on the new state with depth reduced by 1
        eval, _ = expectiminimax(main_player, new_state, depth - 1, True)
        if eval < min_eval:
            min_eval = eval
            best_action = action
    return min_eval, best_action


def max_node(main_player: int, state, depth: int) -> tuple:
    max_eval = float('-inf')
    possible_actions = state.get_possible_actions()
    for action in possible_actions:
        # Take the action in a copy of the state
        new_state = state.take_action(action)
        # We should also switch the player
        new_state.switch_player()
        # Recursively call expectiminimax on the new state with depth reduced by 1
        eval, _ = expectiminimax(main_player, new_state, depth - 1, True)
        if eval > max_eval:
            max_eval = eval
            best_action = action
    return max_eval, best_action


def chance_node(main_player: int, state, depth: int) -> tuple:
    expected_utility = 0
    # Account for the all possible dice outcomes
    for dice in range(2, 13):
        state.move_player(dice)
        new_state = state
        # Recursively call expectiminimax on the new state with depth reduced by 1
        eval, _ = expectiminimax(main_player, new_state, depth - 1, False)
        expected_utility += eval * Probabilities[dice]
    return expected_utility, None


def expectiminimax(main_player: int, state, depth: int = 4, chance: bool = False) -> tuple:
    # Expectiminimax algorithm to search for the best action
    if state.is_terminal() or depth == 0:
        return state.evaluate_utility(), None
    # Determining which node we're on
    if chance:
        node = chance_node
    elif state.current_player == main_player:
        node = max_node
    else:
        node = min_node
    return node(main_player, state, depth)

