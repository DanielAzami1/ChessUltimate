"""
Define custom exceptions for clarity in error handling.
"""


class UnknownPieceIDError(Exception):
    """
    Thrown when a Piece child object is instantiated with a non 'PieceID' instance arg.
    """
    pass


class UnknownTeamError(Exception):
    """
    Thrown when a Piece child object is instantiated with a non 'Team' enum arg.
    """
    pass

