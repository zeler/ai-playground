"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from math import inf

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
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


def custom_score_2(game, player):
    return score_mc_with_walls_corners(game, player)


def custom_score_3(game, player):
    return score_blank_spaces_in_squares(game, player)


def combined_heuristics(game, player):
    """
    Combined heuristics using wall and corner detection in early stages and number
    of clear spaces around landing move in later stages of the game.
    """

    if len(game.get_blank_spaces()) > 0.5  *  game.width * game.height:
        return score_mc_with_walls_corners(game, player)

    return score_blank_spaces_in_squares(game, player)


def score_blank_spaces_in_squares(game, player):
    """ 
    This heuristics is based o count of blank spaces around possible landing moves of this move. The motivation for this
    is, the less blank spaces are around landing moves overall, the more (less) possibilities for next move will player 
    (opponent) have. The priority for minimizing opponent moves is slightly higher.
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


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # count legal moves - if there are not any, quickly end
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1)

        x_pos = int(game.width / 2)
        y_pos = int(game.height / 2)

        # Opening move - try to place player in the middle
        if not game.get_player_location(game.active_player) and game.move_is_legal((x_pos, y_pos)):  # noqa
            return x_pos, y_pos

        best_score = -inf
        best_position = None

        for move in legal_moves:
            score = self.minimax_impl(game.forecast_move(move), depth - 1, False)

            if best_position is None or score > best_score:
                best_score = score
                best_position = move
        # Return the best move from the last completed search iteration
        return best_position

    def minimax_impl(self, game, depth, maximizing_player):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # decide whether this move is terminal
        utility = game.utility(game.active_player)
        if utility != 0:
            return utility

        # quick return if depth is 0
        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()

        # minimax implementation
        if maximizing_player:
            best_score = -inf

            for move in legal_moves:
                future = self.minimax_impl(game.forecast_move(move), depth - 1, maximizing_player=False)  # noqa
                best_score = max(best_score, future)

        # minimizing player
        else:
            best_score = inf

            for move in legal_moves:
                future = self.minimax_impl(game.forecast_move(move), depth - 1, maximizing_player=True)  # noqa
                best_score = min(best_score, future)

        return best_score

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        x_pos = int(game.width / 2)
        y_pos = int(game.height / 2)

        # Opening move - try to place player in the middle
        if not game.get_player_location(game.active_player) and game.move_is_legal((x_pos, y_pos)):  # noqa
            return x_pos, y_pos

        best_position = None

        try:
            depth = 1
            # Iteratively increase search depth
            while True:
                best_position = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_position

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = -inf
        best_position = None

        for move in game.get_legal_moves():
            score = self.alphabeta_impl(game.forecast_move(move), depth - 1, alpha, beta, False)

            if best_position is None or score > best_score:
                best_score = score
                best_position = move

        # Return the best move from the last completed search iteration
        return best_position

    def alphabeta_impl(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):  # noqa

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # quick return if depth is 0
        if depth == 0:
            return self.score(game, self)

        # decide whether this move is terminal
        utility = game.utility(game.active_player)
        if utility != 0:
            return utility

        legal_moves = game.get_legal_moves()

        # alphabeta prunning implementation
        if maximizing_player:
            best_score = -inf

            for move in legal_moves:
                future = self.alphabeta_impl(game.forecast_move(move), depth - 1, alpha, beta, maximizing_player=False)  # noqa
                best_score = max(best_score, future)
                alpha = max(alpha, future)

                if beta <= alpha:
                    # beta cut-off
                    break
        # minimizing player
        else:
            best_score = inf

            for move in legal_moves:
                future = self.alphabeta_impl(game.forecast_move(move), depth - 1, alpha, beta, maximizing_player=True)  # noqa
                best_score = min(best_score, future)
                beta = min(beta, future)

                if beta <= alpha:
                    # alpha cut-off
                    break

        return best_score