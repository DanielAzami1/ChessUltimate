"""
Define custom exceptions for clarity in error handling.
"""


class UnknownPieceIDError(Exception):
    """
    Thrown when a Piece child object is instantiated with a non 'PieceID' enum obj.
    """
    pass


class UnknownTeamError(Exception):
    """
    Thrown when a Piece child object is instantiated with a non 'Team' enum obj.
    """
    pass


class UnknownGameTypeError(Exception):
    """
    Thrown when 'game type' arg is passed as a non GameType enum obj.
    """
    pass


class InvalidMovesetError(Exception):
    """
    Thrown when 'moveset' is not properly defined.
    """
    pass


class IllegalMoveError(Exception):
    """
    Thrown when a 'move' is not possible for a given piece.
    """
    pass


class BadMoveError(Exception):
    """
    Thrown when a request to move a piece is junk - i.e. trying to move a non-existent piece, trying to move to the same
    cell, etc.
    """
    pass

