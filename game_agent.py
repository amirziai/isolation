"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

INFINITY_POSITIVE = float('+inf')
INFINITY_NEGATIVE = float('-inf')
NO_LEGAL_MOVES = (-1, -1)


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def _is_winner_or_loser(game, player):
    if game.is_loser(player):
        return INFINITY_NEGATIVE
    elif game.is_winner(player):
        return INFINITY_POSITIVE
    else:
        return None


def _get_moves(game, player):
    get_legal_moves = game.get_legal_moves
    moves_player = get_legal_moves(player)
    moves_opponent = get_legal_moves(game.get_opponent(player))
    return moves_player, moves_opponent


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    player_alpha = 0.25
    opponent_alpha = 0.75

    total_squares = game.height * game.width
    filled_squares = total_squares - len(game.get_blank_spaces())
    moves_player, moves_opponent = _get_moves(game, player)
    moves_player_count = len(moves_player)
    moves_opponent_count = len(moves_opponent)

    # Return maximum scores if no moves left by either player
    if player is game.inactive_player and moves_opponent_count == 0:
        return INFINITY_POSITIVE
    elif player is game.active_player and moves_player_count == 0:
        return INFINITY_NEGATIVE

    return -1 * filled_squares * (moves_opponent_count + opponent_alpha) / (
        moves_player_count + player_alpha)


def custom_score_2(game, player):
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

    player_factor = 1
    opponent_factor = 1

    moves_player, moves_opponent = _get_moves(game, player)

    winner_or_loser = _is_winner_or_loser(game, player)
    if winner_or_loser is not None:
        return winner_or_loser

    return float(len(moves_player) * player_factor - (
        len(moves_opponent) * opponent_factor))


def custom_score_3(game, player):
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
    winner_or_loser = _is_winner_or_loser(game, player)
    if winner_or_loser is not None:
        return winner_or_loser

    return (1 / len(game.get_blank_spaces())) * custom_score_2(game, player)


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

    def _check_timer(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def _minimax_main(self, game, depth):
        self._check_timer()

        if depth == 0:
            return self.score(game, self), NO_LEGAL_MOVES

        active = game.active_player == self
        best_score = INFINITY_NEGATIVE if active else INFINITY_POSITIVE
        f = max if active else min
        best_move = NO_LEGAL_MOVES

        for move in game.get_legal_moves():
            forecast = game.forecast_move(move)
            score, _ = self._minimax_main(forecast, depth - 1)
            if score == f(score, best_score):
                best_move = move
                best_score = score

        return best_score, best_move

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
        self._check_timer()
        _, best_move = self._minimax_main(game, depth)
        return best_move


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

        best_move = NO_LEGAL_MOVES
        for depth in range(1, 10000):
            try:
                best_move = self.alphabeta(game, depth)
            except SearchTimeout:
                break

        return best_move

    def _check_timer(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def _alphabeta_main(self, game, depth, alpha, beta):
        self._check_timer()

        if depth == 0:
            return self.score(game, self), NO_LEGAL_MOVES

        active = game.active_player == self
        best_score = INFINITY_NEGATIVE if active else INFINITY_POSITIVE
        f = max if active else min
        best_move = NO_LEGAL_MOVES
        is_alpha = True if active else False

        for move in game.get_legal_moves():
            forecast = game.forecast_move(move)
            score, _ = self._alphabeta_main(forecast, depth - 1, alpha, beta)
            if score == f(score, best_score):
                best_move = move
                best_score = score

            if is_alpha:
                if best_score >= beta:
                    return best_score, best_move
                else:
                    alpha = max(best_score, alpha)
            else:
                if best_score <= alpha:
                    return best_score, best_move
                else:
                    alpha = min(best_score, beta)

        return best_score, best_move

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
        self._check_timer()
        _, best_move = self._alphabeta_main(game, depth, alpha, beta)
        return best_move
