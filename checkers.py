class Checker:
    """The checkers piece."""

    # constants (Checker._____)
    PLAYER_ONE = 0
    PLAYER_TWO = 1

    # constructor
    def __init__(self, player):
        """Constructs a new checkers piece."""
        self.player = player

class Board:
    """The board on which the checkers lie."""

    # constructor
    def __init__(self):
        """Constructs a new, normal set up board."""
        self.data = []
        self.data.append(Board.start_rows(Checker.PLAYER_ONE))
        self.data.append(Board.empty_rows(2))
        self.data.append(Board.start_rows(Checker.PLAYER_TWO))

    @staticmethod
    def start_rows(player):
        """The configuration of pieces that the game starts with."""
        r1, r2, r3 = [], [], []
        for _ in range(4):
            r1.append([None, Checker(player)])
            r2.append([Checker(player), None])
            r3.append([None, Checker(player)])
        return [r1, r2, r3]

    @staticmethod
    def empty_rows(count):
        """Returns an amount of empty rows."""
        return [[None] * 8 for _ in range(count)]

if __name__ == '__main__':
    board = Board()
    print(board.data)