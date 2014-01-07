#!/usr/bin/env python3

class Checker:
    """The checkers piece."""

    # constants (Checker._____)
    PLAYER_ONE = 'one'
    PLAYER_TWO = 'two'

    # constructor
    def __init__(self, player, king = False):
        """Constructs a new checkers piece."""
        self.player = player
        self.king = king

    @staticmethod
    def character(piece):
        """Returns the character for a piece (' ' (a space), x, o, X, or O)."""
        if piece is None: return ' '
        char = 'o' if piece.player == Checker.PLAYER_ONE else 'x'
        return char.upper() if piece.king else char

    @staticmethod
    def deepcopy(piece):
        return Checker(piece.player, piece.king) if piece is not None else None

class Board:
    """The board on which the checkers lie."""

    # constructor
    def __init__(self, blank = False):
        """Constructs a new, normal set up board (if `blank` is False or left out)."""
        self.data = []
        if not blank:
            self.data.extend(Board.start_rows(Checker.PLAYER_ONE))
            self.data.extend(Board.empty_rows(2))
            self.data.extend(Board.start_rows(Checker.PLAYER_TWO))

    @staticmethod
    def start_rows(player):
        """The configuration of pieces that the game starts with."""
        r1, r2, r3 = [], [], []
        for _ in range(4):
            r1.extend([None, Checker(player)] if player == Checker.PLAYER_ONE else [Checker(player), None])
            r2.extend([None, Checker(player)] if player == Checker.PLAYER_TWO else [Checker(player), None])
            r3.extend([None, Checker(player)] if player == Checker.PLAYER_ONE else [Checker(player), None])
        return [r1, r2, r3]

    @staticmethod
    def empty_rows(count):
        """Returns an amount of empty rows."""
        return [[None] * 8 for _ in range(count)]

    def render(self, player):
        """Returns an ASCII representation of the board."""

        if player is Checker.PLAYER_TWO:
            s = '   A B C D E F G H \n'
            for n, row in enumerate(self.data):
                s += '  +-+-+-+-+-+-+-+-+\n'
                s += '%i |%s|\n' % (n, '|'.join([Checker.character(p) for p in row]))
        else:
            s = '   H G F E D C B A \n'
            for n in range(len(self.data)):
                row = self.data[len(self.data)-n-1]
                s += '  +-+-+-+-+-+-+-+-+\n'
                s += ('\n|%s| %i' % ('|'.join([Checker.character(p) for p in row]), len(self.data)-n-1))[::-1]
        s += '  +-+-+-+-+-+-+-+-+'
        return s

    def move(self, player, from_coords, to_coords):
        """
        Given a player that is moving, and A0-style coordinates for from and to, moves the piece.
        Returns a 2-tuple, (move_succeeded, board if move_succeeded else error_message)
        TODO keep count of captured pieces
        """
        from_y, from_x = 'ABCDEFGH'.index(from_coords[0]), int(from_coords[1])
        to_y, to_x = 'ABCDEFGH'.index(to_coords[0]), int(to_coords[1])

        from_piece = self.data[from_x][from_y]
        to_piece = self.data[to_x][to_y]

        # first check to see if there's a piece in `from`
        if from_piece is None: return False, 'There is no piece there!'
        # and check to see if it's that player's
        if from_piece.player != player: return False, 'That\'s not your piece!'
        # check to see if `to` is an open space
        if to_piece is not None: return False, 'There\'s already a piece in that space!'
        # check to see if piece is moving forwards
        dx = to_x - from_x
        forwards = dx > 0 if from_piece.player == Checker.PLAYER_ONE else dx < 0
        if not forwards and not from_piece.king: return False, 'You can\'t move backwards!'

        # check to see if the move is diagonal
        adx, ady = abs(from_x - to_x), abs(from_y - to_y)
        if adx == ady == 1:
            self.data[to_x][to_y], self.data[from_x][from_y] = from_piece, None
            if to_x == 0 or to_x == 7: self.data[to_x][to_y].king = True
            return True, self
        elif adx == ady == 2:
            jumped_x, jumped_y = (from_x + to_x) // 2, (from_y + to_y) // 2
            jumped_piece = self.data[jumped_x][jumped_y]
            if jumped_piece is None:
                return False, 'You can\'t jump over nothing!'
            elif jumped_piece.player == player:
                return False, 'You can\'t jump over yourself!'
            else:
                self.data[to_x][to_y], self.data[from_x][from_y] = from_piece, None
                self.data[jumped_x][jumped_y] = None
                if to_x == 0 or to_x == 7: self.data[to_x][to_y].king = True
                return True, self
        else:
            return False, 'That\'s not a diagonal move!'

    def deepcopy(self):
        copied = Board(True)
        copied.data = [[Checker.deepcopy(piece) for piece in row] for row in self.data]
        return copied

def comp_move(board, player, move):

    message = board.move(player, move[0], move[1])
    
    board = message[1]

    # handle multiple jumps
    for i in range(2, len(move)):
        message = board.move(player, move[i-1], move[i])
        if message[0]:
            board = message[1]
        else:
            print(message[1])
            break

    return board

def is_coord(coord):
    """Is this string a valid coordinate?"""
    return coord[0] in 'ABCDEFGH' and coord[1] in '01234567'

def valid_move(move):
    """Is this a valid move (list of two coordinates)?"""

    # check to see all the list elements are valid coordinates (and there's at least one)
    if len(move) > 1:
        for i in range(0, len(move)):
            if not (len(move[i]) == 2 and len(move[1]) == 2 and is_coord(move[0]) and is_coord(move[1])):
                return False
    else:
        return False

    # make sure they're all jumps
    if len(move) > 2:
        for i in range(1, len(move)):
            if int(move[0][1]) % 2 is not int(move[i][1]) % 2:
                return False

    return True

def ask_for_move(player):
    """The function that requests that the player enter a move."""
    move = []
    while not valid_move(move):
        move = input('Player %s, enter move (ex. A0 B1 to move piece at A0 to B1): ' % player).split(' ')
    return move

def input_and_move(player, board):
    """Ask the player for a move, and move there, given a board."""
    move = ask_for_move(player)

    check_move = get_valid_moves(board, player)
    while is_capture(board, player, check_move[0][0], check_move[0][1]) and not is_capture(board, player, move[0], move[1]):
        print('Invalid move: you must jump')
        move = ask_for_move(player)
    
    message = board.move(player, move[0], move[1])
    while not message[0]:
        print(message[1])
        move = ask_for_move(player)
        message = board.move(player, move[0], move[1])
    board = message[1]

    # handle multiple jumps
    for i in range(2, len(move)):
        message = board.move(player, move[i-1], move[i])
        if message[0]:
            board = message[1]
        else:
            print(message[1])
            break

    return board

def eval_game_state(board):
    has_player1 = False
    has_player2 = False
    totalscore = 0
    for x in range(8):
        for y in range(8):
            piece = board.data[x][y]
            if piece is not None:
                # score the square
                if piece.player == Checker.PLAYER_ONE:
                    has_player1 = True
                    if piece.king:
                        totalscore -= 5
                    else:
                        totalscore -= max(abs(x - 3.5), abs(y - 3.5)) + .5
                else:
                    has_player2 = True
                    if piece.king:
                        totalscore += 5
                    else:
                        totalscore += max(abs(x - 3.5), abs(y - 3.5)) + .5

    # we're assuming player 1 is human and player 2 is AI.
    if not has_player1:
        return 1337 # large value so that victory/defeat outweighs anything
    if not has_player2:
        return -1337

    return totalscore

def is_capture(board, player, from_coords, to_coords):
    from_y, from_x = 'ABCDEFGH'.index(from_coords[0]), int(from_coords[1])
    to_y, to_x = 'ABCDEFGH'.index(to_coords[0]), int(to_coords[1])

    adx, ady = abs(from_x - to_x), abs(from_y - to_y)
    if adx == ady == 2:
        jumped_x, jumped_y = (from_x + to_x) // 2, (from_y + to_y) // 2
        jumped_piece = board.data[jumped_x][jumped_y]
        if jumped_piece is None or jumped_piece.player == player:
            return False
        else:
            return True

def get_no_capture_moves(board, player):
    moves = []

    for x in range(8):
        for y in range(8):
            if board.data[x][y] is not None and board.data[x][y].player == player:

                # moves
                # standard pieces
                if not board.data[x][y].king:
                    direction = 1 if player == Checker.PLAYER_ONE else -1
                    can_move_forwards = x < 7 if player == Checker.PLAYER_ONE else x > 0

                    # moves
                    if can_move_forwards and y > 0 and board.data[x + direction][y - 1] is None:
                        moves.append([xy_to_coords(x, y), xy_to_coords(x + direction, y - 1)])
                    if can_move_forwards and y < 7 and board.data[x + direction][y + 1] is None:
                        moves.append([xy_to_coords(x, y), xy_to_coords(x + direction, y + 1)])

                # kings
                else:

                    # moves
                    if y > 0 and x > 0 and board.data[x - 1][y - 1] is None:
                        moves.append([xy_to_coords(x, y), xy_to_coords(x - 1, y - 1)])
                    if y < 7 and x < 7 and board.data[x + 1][y + 1] is None:
                        moves.append([xy_to_coords(x, y), xy_to_coords(x + 1, y + 1)])
                    if y > 0 and x < 7 and board.data[x + 1][y - 1] is None:
                        moves.append([xy_to_coords(x, y), xy_to_coords(x + 1, y - 1)])
                    if y < 7 and x > 0 and board.data[x - 1][y + 1] is None:
                        moves.append([xy_to_coords(x, y), xy_to_coords(x - 1, y + 1)])

    return moves

def get_valid_moves(board, player):
    moves = []

    for x in range(8):
        for y in range(8):
            if board.data[x][y] is not None and board.data[x][y].player == player:
                capture = 2 if player == Checker.PLAYER_ONE else -2

                # captures
                # standard pieces
                if not board.data[x][y].king:
                    # use nested ifs for readability
                    can_move_forwards = x < 6 if player == Checker.PLAYER_ONE else x > 1
                    if can_move_forwards and y > 1 and board.data[x + capture][y - 2] is None:
                        if is_capture(board, player, xy_to_coords(x, y), xy_to_coords(x + capture, y - 2)):
                            moves.append([xy_to_coords(x, y), xy_to_coords(x + capture, y - 2)])
                    if can_move_forwards and y < 6 and board.data[x + capture][y + 2] is None:
                        if is_capture(board, player, xy_to_coords(x, y), xy_to_coords(x + capture, y + 2)):
                            moves.append([xy_to_coords(x, y), xy_to_coords(x + capture, y + 2)])

                # kings
                else:
                    if y > 1 and x > 1 and board.data[x - 2][y - 2] is None:
                        if is_capture(board, player, xy_to_coords(x, y), xy_to_coords(x - 2, y - 2)):
                            moves.append([xy_to_coords(x, y), xy_to_coords(x - 2, y - 2)])
                    if y < 6 and x < 6 and board.data[x + 2][y + 2] is None:
                        if is_capture(board, player, xy_to_coords(x, y), xy_to_coords(x + 2, y + 2)):
                            moves.append([xy_to_coords(x, y), xy_to_coords(x + 2, y + 2)])
                    if y > 1 and x < 6 and board.data[x + 2][y - 2] is None:
                        if is_capture(board, player, xy_to_coords(x, y), xy_to_coords(x + 2, y - 2)):
                            moves.append([xy_to_coords(x, y), xy_to_coords(x + 2, y - 2)])
                    if y < 6 and x > 1 and board.data[x - 2][y + 2] is None:
                        if is_capture(board, player, xy_to_coords(x, y), xy_to_coords(x - 2, y + 2)):
                            moves.append([xy_to_coords(x, y), xy_to_coords(x - 2, y + 2)])

    # force jumping
    if len(moves) > 0: return moves
    else: moves = get_no_capture_moves(board, player)

    return moves

def xy_to_coords(x, y):
    return 'ABCDEFGH'[y] + str(x)

def get_best_move(board, recurse_depth = 0, moves_so_far = [], maximum = 1337):
    # first we need to get a list of valid moves.
    moves = get_valid_moves(board, Checker.PLAYER_TWO)
    copy_moves_so_far = moves_so_far[:]
    # now we should loop through them, and use recursion to keep getting moves.
    boards = []
    #print('a',moves) #debug
    minimum = -1337
    for m in moves:
        AI_moved_board = board.deepcopy()
        if is_capture(AI_moved_board, Checker.PLAYER_TWO, m[0], m[1]):
            AI_moved_board = AI_moved_board.move(Checker.PLAYER_TWO, m[0], m[1])[1]
            jump = get_best_jump(AI_moved_board, Checker.PLAYER_TWO, m[1])
            
            AI_moved_board = jump[1]
            if jump[0] != []:
                for i in jump[0]:
                    m.append(i)
        else:
            opponent_moved_board = AI_moved_board.move(Checker.PLAYER_TWO, m[0], m[1])[1]
        # we've done a full move.
        # now call `get_o_best_move` on the new board.
        if recurse_depth >= 5: # make this bigger for more look-ahead
            state_score = eval_game_state(AI_moved_board)
            if state_score >= maximum: return [AI_moved_board, state_score] + moves_so_far
            boards.append([AI_moved_board, state_score])
        else:
            copy_moves_so_far = moves_so_far[:]
            copy_moves_so_far.append(m)
            next_move = get_o_best_move(AI_moved_board, recurse_depth + 1, copy_moves_so_far, minimum)
            if next_move[1] >= maximum: return next_move + moves_so_far
            if next_move[1] >= minimum:
                minimum = next_move[1]
                boards.append(next_move)
    if boards == []:
        return [0,-1337] + moves_so_far
    best_board = boards[0]
    for b in boards:
        if b[1] > best_board[1]: best_board = b
    return best_board + moves_so_far

def get_o_best_move(board, recurse_depth = 0, moves_so_far = [], minimum = -1337):
    # first we need to get a list of valid moves.
    moves = get_valid_moves(board, Checker.PLAYER_ONE)
    copy_moves_so_far = moves_so_far[:]
    # now we should loop through them, and use recursion to keep getting moves.
    boards = []
    maximum = 1337
    for m in moves:
        opponent_moved_board = board.deepcopy()
        if is_capture(opponent_moved_board, Checker.PLAYER_ONE, m[0], m[1]):
            opponent_moved_board = opponent_moved_board.move(Checker.PLAYER_ONE, m[0], m[1])[1]
            jump = get_best_jump(opponent_moved_board, Checker.PLAYER_TWO, m[1])
            
            opponent_moved_board = jump[1]
            if jump[0] != []:
                for i in jump[0]:
                    m.append(i)
        else:
            opponent_moved_board = opponent_moved_board.move(Checker.PLAYER_ONE, m[0], m[1])[1]
        
        # we've done a full move.
        # now call `get_best_move` on the new board.
        if recurse_depth >= 5: # make this bigger for more look-ahead
            state_score = eval_game_state(opponent_moved_board)
            if state_score <= minimum: return [opponent_moved_board, state_score] + moves_so_far
            boards.append([opponent_moved_board, state_score])
                
        else:
            copy_moves_so_far = moves_so_far[:]
            copy_moves_so_far.append(m)
            next_move = get_best_move(opponent_moved_board, recurse_depth + 1, copy_moves_so_far, maximum)
            if next_move[1] <= minimum: return next_move + moves_so_far
            if next_move[1] <= maximum:
                maximum = next_move[1]
                boards.append(next_move)
    if boards == []:
        return [0,1337] + moves_so_far
    best_board = boards[0]
    for b in boards:
        if b[1] < best_board[1]: best_board = b  #less than sign because human has opposite goal
    return best_board + moves_so_far

def get_best_jump(board, player, from_coord):

    coords = []

    while True:

        moves = get_valid_moves(board, player)
        if from_coord not in moves[0]: break
        
        test_board = board.deepcopy()

        boards = []
        test_moves = []

        from_y, from_x = 'ABCDEFGH'.index(from_coord[0]), int(from_coord[1])

        if test_board.data[from_x][from_y] is None:
            return [coords, board]
        elif test_board.data[from_x][from_y].king:
            if from_x < 6 and from_y > 1 and board.data[from_x + 2][from_y - 2] is None:
                if is_capture(board, player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + 2, from_y - 2)):
                    next_move = test_board.move(player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + 2, from_y - 2))
                    if next_move[0]:
                        boards.append(next_move[1])
                        test_moves.append(xy_to_coords(from_x + 2, from_y - 2))
                        
            if from_x < 6 and from_y < 6 and board.data[from_x + 2][from_y + 2] is None:
                if is_capture(board, player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + 2, from_y + 2)):
                    next_move = test_board.move(player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + 2, from_y + 2))
                    if next_move[0]:
                        boards.append(next_move[1])
                        test_moves.append(xy_to_coords(from_x + 2, from_y + 2))
                        
            if from_x > 1 and from_y < 6 and board.data[from_x - 2][from_y + 2] is None:
                if is_capture(board, player, xy_to_coords(from_x, from_y), xy_to_coords(from_x - 2, from_y + 2)):
                    next_move = test_board.move(player, xy_to_coords(from_x, from_y), xy_to_coords(from_x - 2, from_y + 2))
                    if next_move[0]:
                        boards.append(next_move[1])
                        test_moves.append(xy_to_coords(from_x - 2, from_y + 2))
                        
            if from_x > 1 and from_y > 1 and board.data[from_x - 2][from_y - 2] is None:
                if is_capture(board, player, xy_to_coords(from_x, from_y), xy_to_coords(from_x - 2, from_y - 2)):
                    next_move = test_board.move(player, xy_to_coords(from_x, from_y), xy_to_coords(from_x - 2, from_y - 2))
                    if next_move[0]:
                        boards.append(next_move[1])
                        test_moves.append(xy_to_coords(from_x - 2, from_y - 2))
        else:
            capture = 2 if player is Checker.PLAYER_ONE else -2
            can_move_forwards = from_x < 6 if player == Checker.PLAYER_ONE else from_x > 1
            if can_move_forwards and from_y > 1 and board.data[from_x + capture][from_y - 2] is None:
                if is_capture(board, player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + capture, from_y - 2)):
                    next_move = test_board.move(player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + capture, from_y - 2))
                    if next_move[0]:
                        boards.append(next_move[1])
                        test_moves.append(xy_to_coords(from_x + capture, from_y - 2))
                        
            if can_move_forwards and from_y < 6 and board.data[from_x + capture][from_y + 2] is None:
                if is_capture(board, player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + capture, from_y + 2)):
                    next_move = test_board.move(player, xy_to_coords(from_x, from_y), xy_to_coords(from_x + capture, from_y + 2))
                    if next_move[0]:
                        boards.append(next_move[1])
                        test_moves.append(xy_to_coords(from_x + capture, from_y + 2))

        if len(boards) == 0:
            #if ch: print('true')
            #print(board.render(Checker.PLAYER_ONE))
            return [coords, board]

        move_evals = []
        for b in boards:
            move_evals.append(eval_game_state(b))

        min_max = move_evals[0]
        for e in move_evals:
            if player is Checker.PLAYER_ONE and min_max > e: min_max = e
            if player is Checker.PLAYER_TWO and min_max < e: min_max = e

        board = boards[move_evals.index(min_max)]
        from_coord = test_moves[move_evals.index(min_max)]
        coords.append(from_coord)

    return [coords, board]

if __name__ == '__main__':
    players = input('Enter number of players (0, 1, 2): ')
    while players not in ['0','1', '2']:
        players = input('Invalid number of players. Try again: ')

    if players == '0':
        board = Board()
        while True:
            print(board.render(Checker.PLAYER_ONE))
            if len(get_valid_moves(board, Checker.PLAYER_ONE)) is 0:
                print('Player 2 wins')
                break
            move = get_o_best_move(board)
            board = comp_move(board, Checker.PLAYER_ONE, move[len(move)-1])
            print(board.render(Checker.PLAYER_ONE))  #disabled board rotation
            if len(get_valid_moves(board, Checker.PLAYER_TWO)) is 0:
                print('Player 1 wins')
                break
            move = get_best_move(board)
            board = comp_move(board, Checker.PLAYER_TWO, move[len(move)-1])
    elif players == '1':
        board = Board()
        while True:
            print(board.render(Checker.PLAYER_ONE))
            if len(get_valid_moves(board, Checker.PLAYER_ONE)) is 0:
                print('Player 2 wins')
                break
            board = input_and_move(Checker.PLAYER_ONE, board)
            print(board.render(Checker.PLAYER_ONE))
            if len(get_valid_moves(board, Checker.PLAYER_TWO)) is 0:
                print('Player 1 wins')
                break
            move = get_best_move(board)
            board = comp_move(board, Checker.PLAYER_TWO, move[len(move)-1])
    else:
        board = Board()
        while True:
            print(board.render(Checker.PLAYER_ONE))
            if len(get_valid_moves(board, Checker.PLAYER_ONE)) is 0:
                print('Player 2 wins')
                break
            board = input_and_move(Checker.PLAYER_ONE, board)
            print(board.render(Checker.PLAYER_TWO))
            if len(get_valid_moves(board, Checker.PLAYER_TWO)) is 0:
                print('Player 1 wins')
                break
            board = input_and_move(Checker.PLAYER_TWO, board)
