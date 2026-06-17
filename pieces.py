class Move:
    def __init__(self, move_only: bool, attack_only: bool, first_only: bool, jump: bool, range: int, y: int, x: int) -> object:
        self.move_only = move_only
        self.attack_only = attack_only
        self.first_only = first_only
        self.jump = jump
        self.range = range
        self.x = x
        self.y = y


class Piece:
    def __init__(self, color, name, value):
        self.color = color
        self.name = name
        self.value = value
        self.has_moved = False
        self.selectable = False
        self.can_be_checked = False
        self.blocks_movement = True
        self.direction = 1 if color == "white" else -1

    def moves(self):
        return []


class Empty(Piece):
    def __init__(self, color=None):
        super().__init__(None, None, 0)
        self.blocks_movement = False

    def __str__(self):
        if self.selectable:
            return '*'
        return '_'


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn", 1)

    def __str__(self):
        if self.color == "white":
            return '♟'
        return '♙'

    def moves(self):
        moves = [
            Move(True, False, True, False, 1, 2 * self.direction, 0),
            Move(True, False, False, False, 1, 1 * self.direction, 0),
            Move(False, True, False, False, 1, 1 * self.direction, 1),
            Move(False, True, False, False, 1, 1 * self.direction, -1)
        ]
        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "rook", 5)

    def __str__(self):
        if self.color == "white":
            return '♜'
        return '♖'

    def moves(self):
        moves = [
            Move(False, False, False, False, 7, 1, 0),
            Move(False, False, False, False, 7, -1, 0),
            Move(False, False, False, False, 7, 0, 1),
            Move(False, False, False, False, 7, 0, -1)
        ]
        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "knight", 3)

    def __str__(self):
        if self.color == "white":
            return '♞'
        return '♘'

    def moves(self):
        moves = [
            Move(False, False, False, True, 1, 2, 1),
            Move(False, False, False, True, 1, 2, -1),
            Move(False, False, False, True, 1, -2, 1),
            Move(False, False, False, True, 1, -2, -1),
            Move(False, False, False, True, 1, 1, 2),
            Move(False, False, False, True, 1, 1, -2),
            Move(False, False, False, True, 1, -1, 2),
            Move(False, False, False, True, 1, -1, -2)
        ]
        return moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "bishop", 3)

    def __str__(self):
        if self.color == "white":
            return '♝'
        return '♗'

    def moves(self):
        moves = [
            Move(False, False, False, False, 7, 1, 1),
            Move(False, False, False, False, 7, 1, -1),
            Move(False, False, False, False, 7, -1, 1),
            Move(False, False, False, False, 7, -1, -1)
        ]
        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "queen", 9)

    def __str__(self):
        if self.color == "white":
            return '♛'
        return '♕'

    def moves(self):
        moves = [
            Move(False, False, False, False, 7, 1, 0),
            Move(False, False, False, False, 7, -1, 0),
            Move(False, False, False, False, 7, 0, 1),
            Move(False, False, False, False, 7, 0, -1),
            Move(False, False, False, False, 7, 1, 1),
            Move(False, False, False, False, 7, 1, -1),
            Move(False, False, False, False, 7, -1, 1),
            Move(False, False, False, False, 7, -1, -1)
        ]
        return moves

    pass


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "king", None)
        self.can_be_checked = True

    def __str__(self):
        if self.color == "white":
            return '♚'
        return '♔'

    def moves(self):
        moves = [
            Move(False, False, False, False, 1, 1, 0),
            Move(False, False, False, False, 1, -1, 0),
            Move(False, False, False, False, 1, 0, 1),
            Move(False, False, False, False, 1, 0, -1),
            Move(False, False, False, False, 1, 1, 1),
            Move(False, False, False, False, 1, 1, -1),
            Move(False, False, False, False, 1, -1, 1),
            Move(False, False, False, False, 1, -1, -1)
        ]
        return moves
