from src.classes import piece as _
from src.misc.enums import Team

"""
The default setup for putting pieces on the board at the start of a chess game.
Keys correspond to a row number (0-indexed), values are a list of pieces to assign to them.
"""
DEFAULT_STARTING_CHESS_CONFIG = {
    0: [
        _.Rook(Team.A),
        _.Knight(Team.A),
        _.Bishop(Team.A),
        _.Queen(Team.A),
        _.King(Team.A),
        _.Bishop(Team.A),
        _.Knight(Team.A),
        _.Rook(Team.A)
    ],

    1: [
        _.Pawn(Team.A),
        _.Pawn(Team.A),
        _.Pawn(Team.A),
        _.Pawn(Team.A),
        _.Pawn(Team.A),
        _.Pawn(Team.A),
        _.Pawn(Team.A),
        _.Pawn(Team.A),
    ],

    6: [
        _.Pawn(Team.B),
        _.Pawn(Team.B),
        _.Pawn(Team.B),
        _.Pawn(Team.B),
        _.Pawn(Team.B),
        _.Pawn(Team.B),
        _.Pawn(Team.B),
        _.Pawn(Team.B),
    ],

    7: [
        _.Rook(Team.B),
        _.Knight(Team.B),
        _.Bishop(Team.B),
        _.Queen(Team.B),
        _.King(Team.B),
        _.Bishop(Team.B),
        _.Knight(Team.B),
        _.Rook(Team.B)
    ],
}
