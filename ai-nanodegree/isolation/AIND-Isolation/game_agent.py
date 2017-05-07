"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from math import inf


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return float(combined_heuristics(game, player))


def combined_heuristics(game, player):
    """
    Combined heuristics using number
    of clear spaces around landing move in early stages of the game and wall and corner detection in later stages.
    """

    if len(game.get_blank_spaces()) < 0.4 * game.width * game.height:
        return score_mc_with_walls_corners(game, player)

    return score_blank_spaces_in_squares(game, player)


def score_blank_spaces_in_squares(game, player):
    """ 
    This heuristics is based o count of blank spaces around possible landing moves of this move. The motivation for this
    is, the less balnk spaces are around landing moves overally, the more (less) posibilities for next move will player 
    (opponent) have. The priority for minimizing opponent moves is slighty higher.
    """

    player_moves = game.get_legal_moves(player=player)
    opponent_moves = game.get_legal_moves(player=game.get_opponent(player))
    player_score = 0
    opponent_score = 0

    for move in player_moves:
        player_score += get_blank_count_on_land(game, move)

    for move in opponent_moves:
        opponent_score += get_blank_count_on_land(game, move)

    return player_score - 1.25 * opponent_score  # noqa


def get_blank_count_on_land(game, move):
    min_height = move[0] - 3 if move[0] - 3 > 0 else 0
    max_height = move[0] + 3 if move[0] + 3 > 0 else game.width
    min_width = move[1] - 3 if move[1] - 3 > 0 else 0
    max_width = move[1] + 3 if move[1] + 3 > 0 else game.width

    positions = [(x, y) for x in range(min_height, max_height) for y in range(min_width, max_width)]
    blank = game.get_blank_spaces()

    count = 0
    for pos in positions:
        if pos in blank:
            count += 1

    return count


def score_mc_with_walls_corners(game, player):
    """
    This is an improved version of 'count legal moves' heuristics. Any position near wall/corner is penalized for player
    as this further reduces valid move possibilities in the future.
    """
    player_moves = game.get_legal_moves(player=player)
    opponent_moves = game.get_legal_moves(player=game.get_opponent(player))
    score = 0

    for move in opponent_moves:
        if is_near_wall(game, move):
            score += 5
        # further penalize corners
        if is_in_corner(game, move):
            score += 2

    return float(len(player_moves) - len(opponent_moves)) + score  # noqa


def is_near_wall(game, move):
    """Calculate if move lies near wall"""
    return True if move[0] in [0, game.height - 1] and move[1] in [0, game.width - 1] else False


def is_in_corner(game, move):
    """Calculate if move lies near wall"""
    return True if move in [(0,0), (game.height - 1, 0), (0, game.width - 1), (game.height - 1, game.width - 1)] \
        else False


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)  This parameter should be ignored when iterative = True

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            DEPRECATED -- This argument will be removed in the next release

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # count legal moves - if there are not any, quickly end
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1)

        x_pos = game.width / 2
        y_pos = game.height / 2

        # Opening move - try to place player in the middle
        if not game.get_player_location(game.active_player) and game.move_is_legal((x_pos, y_pos)):  # noqa
            return x_pos, y_pos

        best_score = -inf
        best_position = (-1, -1)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if self.iterative:
                depth = 1
                # Iteratively increase search depth
                while True:
                    score, position = self.execute_search(game, depth)

                    # If current score is better the best found, update results
                    if score > best_score:
                        best_score = score
                        best_position = position

                    depth += 1
            else:
                best_score, best_position = self.execute_search(game, self.search_depth)  # noqa

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # special case, when we didn't find any valid (not losing) position in next move, but there are still moves left
        # Choose first one. This will usually end in a loss, except for cases, when opponent can't move at all
        if best_position not in legal_moves:
            best_position = legal_moves[0]

        # Return the best move from the last completed search iteration
        return best_position

    def execute_search(self, game, depth):
        if self.method == 'minimax':
            return self.minimax(game.copy(), depth)
        else:
            return self.alphabeta(game.copy(), depth)

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # decide whether this move is terminal
        utility = game.utility(game.active_player)
        if utility != 0:
            return utility, (-1, -1)

        # quick return if depth is 0
        if depth == 0:
            return self.score(game, self), (-1, -1)

        legal_moves = game.get_legal_moves(game.active_player)

        # minimax implementation
        if maximizing_player:
            best_score = -inf
            best_position = (-1, -1)

            for move in legal_moves:
                future = self.minimax(game.forecast_move(move), depth - 1, maximizing_player=False)  # noqa

                if best_score < future[0]:
                    best_score = future[0]
                    best_position = move
        # minimizing player
        else:
            best_score = inf
            best_position = (-1, -1)

            for move in legal_moves:
                future = self.minimax(game.forecast_move(move), depth - 1, maximizing_player=True)  # noqa

                if best_score > future[0]:
                    best_score = future[0]
                    best_position = move

        return best_score, best_position

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):  # noqa
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # decide whether this move is terminal
        utility = game.utility(game.active_player)
        if utility != 0:
            return utility, (-1, -1)

        # quick return if depth is 0
        if depth == 0:
            return self.score(game, self), (-1, -1)

        legal_moves = game.get_legal_moves(game.active_player)

        # alphabeta prunning implementation
        if maximizing_player:
            best_score = -inf
            best_position = (-1, -1)

            for move in legal_moves:
                future = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, maximizing_player=False)  # noqa

                if best_score < future[0]:
                    best_score = future[0]
                    best_position = move

                alpha = max(alpha, future[0])

                if beta <= alpha:
                    # beta cut-off
                    break
        # minimizing player
        else:
            best_score = inf
            best_position = (-1, -1)

            for move in legal_moves:
                future = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, maximizing_player=True)  # noqa

                if best_score > future[0]:
                    best_score = future[0]
                    best_position = move

                beta = min(beta, future[0])

                if beta <= alpha:
                    # alpha cut-off
                    break

        return best_score, best_position
