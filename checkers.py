class Checker:
    """The checkers piece."""

    # constants (Checker._____)
    PLAYER_ONE = 'one'
    PLAYER_TWO = 'two'

    # constructor
    def __init__(self, player):
        """Constructs a new checkers piece."""
        self.player = player
        self.king = False

    @staticmethod
    def character(piece):
        if piece is None: return ' '
        char = 'o' if piece.player == Checker.PLAYER_ONE else 'x'
        return char.upper() if piece.king else char

class Board:
    """The board on which the checkers lie."""

    # constructor
    def __init__(self):
        """Constructs a new, normal set up board."""
        self.data = []
        self.data.extend(Board.start_rows(Checker.PLAYER_ONE))
        self.data.extend(Board.empty_rows(2))
        self.data.extend(Board.start_rows(Checker.PLAYER_TWO))

    @staticmethod
    def start_rows(player):
        """The configuration of pieces that the game starts with."""
        r1, r2, r3 = [], [], []
        for _ in range(4):
            r1.extend([None, Checker(player)])
            r2.extend([Checker(player), None])
            r3.extend([None, Checker(player)])
        return [r1, r2, r3]

    @staticmethod
    def empty_rows(count):
        """Returns an amount of empty rows."""
        return [[None] * 8 for _ in range(count)]

    def render(self):
        """Returns an ASCII representation of the board."""
        s = '   A B C D E F G H \n'
        for n, row in enumerate(self.data):
            s += '  +-+-+-+-+-+-+-+-+\n'
            s += '%i |%s|\n' % (n, '|'.join([Checker.character(p) for p in row]))
        s += '  +-+-+-+-+-+-+-+-+'
        return s

    def move(self, player, from_coords, to_coords):
        from_y, from_x = 'ABCDEFGH'.index(from_coords[0]), int(from_coords[1])
        to_y, to_x = 'ABCDEFGH'.index(to_coords[0]), int(to_coords[1])
        if self.data[from_x][from_y] is None:
            return 'There is no piece there!'
        elif self.data[from_x][from_y].player == player:
            if abs(from_x - to_x) == 1 and abs(from_y - to_y) == 1:
                self.data[to_x][to_y], self.data[from_x][from_y] = self.data[from_x][from_y], None
                return 'Moved'
            else:
                return 'That\'s not a diagonal move!'
        else:
            return 'That\'s not your piece!'

def ask_for_move(player, board):
    move = input('Player %s, enter move (for example, A0 B1 to move the piece at A0 to B1): ' % player).split(' ')
    board.move(player, move[0], move[1])

if __name__ == '__main__':
    board = Board()
    print(board.render())
    ask_for_move(Checker.PLAYER_ONE, board)
    print(board.render())
