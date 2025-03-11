# WillDaru22
#
# Acknowledgements
# Diagonal Movement Calculations
# https://stackoverflow.com/questions/20547400/why-allowing-diagonal-movement-would-make-the-a-and-manhattan-distance-inadmiss
# Getting max value in dictionaries - may not use
# https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
# Python mean
# https://www.geeksforgeeks.org/python-statistics-mean-function/

import random
import copy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    firstMove = 0

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        nempty = 0  # used to detect # of elements not empty
        for col in range(5):  # detect drop phase
            for i in range(5):
                if state[i][col] != ' ':
                    nempty += 1
        if nempty < 8:
            drop_phase = True
        else:
            drop_phase = False
        # print("not empty", nempty)  # debug
        if state[2][2] != ' ' and self.firstMove != 2:  # check if the space we want to move to is already full
            self.firstMove = 1
        if self.firstMove == 0:  # make this first move if space is free
            move = []
            (row, col) = (2, 2)
            move.insert(0, (row, col))
            self.firstMove = 2
            return move
        if self.firstMove == 1:  # backup in case our first move is taken
            move = []
            (row, col) = (1, 1)
            move.insert(0, (row, col))
            self.firstMove = 2
            return move
        # drop_phase = True   # detect drop phase
        current_turn = self.my_piece
        move = []  # calculate the next move
        if not drop_phase:
            new_state = self.find_next_state(state, drop_phase, current_turn)  # get state to move to
            # choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            # new_state = self.best_State(state, 0, drop_phase)  # get state to move to
            if not new_state:
                # print("ERROR: New state is null")
                # exit(1)
                new_state = self.find_next_state(state, drop_phase, current_turn)  # let's try that again here
            if state != new_state:  # check to make sure we made a move
                for col in range(5):
                    for i in range(5):
                        if new_state[i][col] != state[i][col] and new_state[i][col] == ' ':  # find place we moved from
                            # found space we moved FROM.  This is our piece to remove
                            state[i][col] = ' '  # remove piece from board
                            (oldrow, oldcol) = (i, col)  # previous position
                            move.insert(0, (oldrow, oldcol))
                (row, col) = self.get_move_row(new_state, state)
                if (row, col) == (-1, -1):  # uh oh didnt pass in a proper state
                    move.insert(0, (0, 0))
                    return move
                move.insert(0, (row, col))
                return move
            else:  # shouldnt get here but oh man are we in trouble if we do
                # print("ERROR: AI did not make a move during the move phase")
                # exit(1)
                pass
        # TODO: implement a minimax algorithm to play better
        # Minimax sort of works... kind of.  It tries to win if it can but it is pretty easy to stump
        else:
            new_state = self.find_next_state(state, drop_phase, current_turn)
            if state != new_state:  # check out here to make sure we made a move
                (row, col) = self.get_move_row(new_state, state)
                move.insert(0, (row, col))
                return move
            else:  # didnt make a move
                # print("ERROR: AI failed to make a move")
                # exit(1)
                pass
                # Old code from prior to minimax algorithm
                # select an unoccupied space randomly
                # move = []
                # (row, col) = (random.randint(0, 4), random.randint(0, 4))
                # while not state[row][col] == ' ':
                #     (row, col) = (random.randint(0, 4), random.randint(0, 4))
                #
                # # ensure the destination (row,col) tuple is at the beginning of the move list
                # move.insert(0, (row, col))
                # return move

    # helper to find the row of our move
    def get_move_row(self, new_state, old_state):
        if not new_state:
            # print("ERROR: new state is null")
            # exit(1)
            return -1, -1
        if not old_state:
            # print("ERROR: old state is null")
            # exit(1)
            return -1, -1
        for col in range(5):
            for i in range(5):
                if new_state[i][col] != old_state[i][col] and new_state[i][col] != ' ':  # get our next move
                    return i, col

    def find_next_state(self, current_state, drop_phase, turn):
        best_value, best_state = -2, None
        for s in self.succ(current_state, drop_phase, turn):
            if self.heuristic_game_value(s) == 1:
                return s
            current_value = self.Min_value(current_state, 0, drop_phase)
            if current_value > best_value:
                best_value - current_value
                best_state = s
        return best_state

    # minimax algorithm helpers
    def Max_value(self, state, depth, drop):  # return best-score available from state for Max
        if depth == 2:
            return self.heuristic_game_value(state)
        if self.heuristic_game_value(state) == 1:
            return 1
        else:
            a = -2  # anything less than -1 works here
            depth += 1
            # print("depth", depth)  # debug
            for item in self.succ(state, drop, self.my_piece):  # for max it is the AI turn
                a = max(a, self.Min_value(item, depth, drop))
        return a

    def Min_value(self, state, depth, drop):  # return best-score available from state for min
        if depth == 2:
            return self.heuristic_game_value(state)
        if self.heuristic_game_value(state) == -1:
            return -1
        else:
            b = 2  # anything more than 1 works here
            depth += 1
            # print("depth", depth)  # debug
            for item in self.succ(state, drop, self.opp):  # for min it is the opponent turn
                b = min(b, self.Max_value(item, depth, drop))
        return b

    # take board state and return list of legal successors
    def succ(self, state, drop_phase, current_player):
        successors = []
        if drop_phase:  # if code is in drop phase, add pieces
            for col in range(5):  # go through all spaces and successor is a piece placed in that space
                for i in range(5):
                    if state[i][col] == ' ':
                        copy_state = copy.deepcopy(state)
                        copy_state[i][col] = current_player
                        successors.append(copy_state)
        else:  # if code is not in drop phase, move pieces.  Get ready for a lot of conditionals
            for col in range(5):  # doesnt really matter if we use state or copy_state here
                for i in range(5):
                    if state[i][col] == current_player:  # if not current player's piece, do nothing
                        if col == 0:  # dont check left column
                            if i == 0:  # dont check top row
                                if state[i][col + 1] == ' ':
                                    # make copy of state, change the point, add to list
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                            elif i == 4:  # dont check bottom row
                                # do something
                                if state[i][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                            else:
                                # do something
                                if state[i][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                        elif col == 4:  # dont check right column
                            if i == 0:  # dont check top row
                                # do something
                                if state[i][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                            elif i == 4:  # dont check bottom row
                                # do something
                                if state[i][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                            else:
                                # do something
                                if state[i + 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                        else:  # not far left or right columns, good to check left right
                            if i == 0:  # dont check top row
                                # do something
                                if state[i][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                            elif i == 4:  # dont check bottom row
                                # do something
                                if state[i][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i-1][col+1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i-1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i-1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                            else:  # check all 8 directions
                                # do something
                                if state[i][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i + 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i + 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col - 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col - 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
                                if state[i - 1][col + 1] == ' ':
                                    # do something
                                    copy_state = copy.deepcopy(state)
                                    copy_state[i - 1][col + 1] = current_player
                                    copy_state[i][col] = ' '
                                    successors.append(copy_state)
        return successors

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        # complete checks for diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for col in range(2):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col+1] == state[i+2][col+2] == \
                        state[i+3][col+3]:
                    return 1 if state[i][col] == self.my_piece else -1
        # check / diagonal wins
        for col in range(2):
            for i in range(2):
                if state[i][col + 3] != ' ' and state[i][col + 3] == state[i + 1][col + 2] == state[i + 2][col + 1] == \
                        state[i + 3][col]:
                    return 1 if state[i][col + 3] == self.my_piece else -1
        # check diamond wins
        for col in range(3):
            for i in range(3):
                if state[i][col + 1] != ' ' and state[i][col + 1] == state[i + 1][col] == state[i + 2][col + 1] == \
                        state[i + 1][col + 2] and state[i+1][col+1] == ' ':
                    return 1 if state[i][col + 1] == self.my_piece else -1
        return 0  # no winner yet

    # assigns a score based on partial wins.  Number of pieces in winning config - number of opposing pieces in win
    def heuristic_game_value(self, state):  # hopefully better heuristic.  Still not great but hopefully better
        if self.game_value(state) != 0:
            return self.game_value(state)  # return if it is a terminal state

        # storage for scores
        row_scores = []
        row_score = 0
        vertical_scores = []
        vert_score = 0
        left_diag_scores = []
        left_diag_score = 0
        right_diag_scores = []
        right_diag_score = 0
        diamond_scores = []
        diamond_score = 0
        heuristic_scores = []

        # check partial horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ':  # dont evaluate empty rows
                    if row[i] == self.my_piece:
                        row_score += 1
                    else:
                        row_score -= 1
                if row[i+1] != ' ':  # dont evaluate empty rows
                    if row[i+1] == self.my_piece:
                        row_score +=1
                    else:
                        row_score -= 1
                if row[i+2] != ' ':  # dont evaluate empty rows
                    if row[i+2] == self.my_piece:
                        row_score += 1
                    else:
                        row_score -= 1
                if row[i+3] != ' ':  # dont evaluate empty rows
                    if row[i+3] == self.my_piece:
                        row_score += 1
                    else:
                        row_score -= 1
                row_scores.append(row_score/4)
                row_score = 0

        # check partial vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ':
                    if state[i][col] == self.my_piece:
                        vert_score += 1
                    else:
                        vert_score -= 1
                if state[i+1][col] != ' ':
                    if state[i+1][col] == self.my_piece:
                        vert_score += 1
                    else:
                        vert_score -= 1
                if state[i+2][col] != ' ':
                    if state[i+2][col] == self.my_piece:
                        vert_score += 1
                    else:
                        vert_score -= 1
                if state[i+3][col] != ' ':
                    if state[i+3][col] == self.my_piece:
                        vert_score += 1
                    else:
                        vert_score -= 1
                vertical_scores.append(vert_score/4)
                vert_score = 0

        # check parital \ diagonal wins
        for col in range(2):
            for i in range(2):
                if state[i][col] != ' ':
                    if state[i][col] == self.my_piece:
                        left_diag_score += 1
                    else:
                        left_diag_score -= 1
                if state[i+1][col+1] != ' ':
                    if state[i+1][col+1] == self.my_piece:
                        left_diag_score += 1
                    else:
                        left_diag_score -= 1
                if state[i+2][col+2] != ' ':
                    if state[i+2][col+2] == self.my_piece:
                        left_diag_score += 1
                    else:
                        left_diag_score -= 1
                if state[i+3][col+3] != ' ':
                    if state[i+3][col+3] == self.my_piece:
                        left_diag_score += 1
                    else:
                        left_diag_score -= 1
                left_diag_scores.append(left_diag_score/4)
                left_diag_score = 0

        # check partial / diagonal wins
        for col in range(2):
            for i in range(2):
                if state[i][col+3] != ' ':
                    if state[i][col+3] == self.my_piece:
                        right_diag_score += 1
                    else:
                        right_diag_score -= 1
                if state[i+1][col+2] != ' ':
                    if state[i+1][col+2] == self.my_piece:
                        right_diag_score += 1
                    else:
                        right_diag_score -= 1
                if state[i+2][col+1] != ' ':
                    if state[i+2][col+1] == self.my_piece:
                        right_diag_score += 1
                    else:
                        right_diag_score -= 1
                if state[i+3][col] != ' ':
                    if state[i+3][col] == self.my_piece:
                        right_diag_score += 1
                    else:
                        right_diag_score -= 1
                right_diag_scores.append(right_diag_score/4)
                right_diag_score = 0

        # check partial diamond wins
        for col in range(3):
            for i in range(3):
                if state[i][col+1] != ' ':
                    if state[i][col+1] == self.my_piece:
                        diamond_score += 1
                    else:
                        diamond_score -= 1
                if state[i+1][col] != ' ':
                    if state[i+1][col] == self.my_piece:
                        diamond_score += 1
                    else:
                        diamond_score -= 1
                if state[i+2][col+1] != ' ':
                    if state[i+2][col+1] == self.my_piece:
                        diamond_score += 1
                    else:
                        diamond_score -= 1
                if state[i+1][col+2] != ' ':
                    if state[i+1][col+2] == self.my_piece:
                        diamond_score += 1
                    else:
                        diamond_score -= 1
                if state[i+2][col+1] != ' ':
                    diamond_score -= 1
            diamond_scores.append(diamond_score/4)
            diamond_score = 0

        # add max of all the scores for each configuration we calculated
        heuristic_scores.append(max(row_scores))
        heuristic_scores.append(max(vertical_scores))
        heuristic_scores.append(max(left_diag_scores))
        heuristic_scores.append(max(right_diag_scores))
        heuristic_scores.append(max(diamond_scores))

        return max(heuristic_scores)  # return the highest score of all the scores as the heuristic score

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
