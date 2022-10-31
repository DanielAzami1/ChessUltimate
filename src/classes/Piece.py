from src.misc.enums import PieceID, Team, PieceStatus
from src.misc.exceptions import UnknownPieceIDError, UnknownTeamError, InvalidMovesetError
from abc import ABC
import numpy as np


class Piece(ABC):
    """Abstract Base Class for Piece objects (pieces on the chess board)"""

    def __init__(
        self,
        *args,
        **kwargs
    ):
        piece_identifier = kwargs["piece_identifier"]
        team = kwargs["team"]
        moveset = np.atleast_2d(np.array(kwargs["moveset"]))  # moves piece is able to make, cast to np.array for vector arithmetic
        try:
            moveset_multiplier = kwargs["moveset_multiplier"]
            if not isinstance(moveset_multiplier, range) or not moveset_multiplier:
                raise InvalidMovesetError(
                    f"Moveset multiplier '{moveset_multiplier}' improperly defined."
                )
            self.moveset_multiplier = moveset_multiplier  # many pieces can move multiple cells, this just saves LOC
        except KeyError:
            pass  # some pieces won't have a multiplier (e.g. Pawn, King)

        if not isinstance(piece_identifier, PieceID):
            raise UnknownPieceIDError(
                f"Piece '{piece_identifier}' is not a valid piece for this gamemode."
            )
        if not isinstance(team, Team):
            raise UnknownTeamError(
                f"Team '{team}' is not a valid team for this gamemode."
            )
        if not isinstance(moveset, np.ndarray) or not np.any(moveset):
            raise InvalidMovesetError(
                f"Moveset \n'{moveset}'\n improperly defined."
            )

        if team is Team.B:  # team A moves 'down' the board, so the move values are inverse
            moveset *= -1

        self.piece_identifier = piece_identifier
        self.team = team
        self.alive = PieceStatus.ALIVE  # whether this piece is still in play / on the board
        """
        Moveset Logic:
            
            Cells organized in a matrix, therefore possess some arbitrary (x, y) position in the 'board'. To 'move' a
            piece, we can take the piece's current cell's position, and increment (for team A :: 'down' the board) 
            or decrement (team B :: 'up' the board) to find the position of the new cell, and make the attribute swap.
            
            The 'moveset' variable will be assigned a tuple(tuple(int)). Each sub-tuple will hold two ints, an 'x' and
            a 'y' value that will be used to increment or decrement the current x/y value. 
            These values represent the amount of cells a particular move can traverse, i.e. for a Rook, we would have 
            something like self.moveset = ((1, 0), (0, 1)...), with the addition of a 'multiplier' to allow the piece
            to move additional cells without having to hard-code those tuples for each permutation. 
        """
        self.moveset = moveset

    def __str__(self):
        return self.piece_identifier.value[self.team]

    def __repr__(self):
        return f"\nName: {self.piece_identifier}\n" \
               f"Team: {self.team}\n" \
               f"Moveset: {self.moveset}\n" \
               f"Has Multiplier: {hasattr(self, 'moveset_multiplier')}"


class Pawn(Piece):
    """
    Pawn object.
    """
    def __init__(self, team: Team = Team.B):
        super().__init__(
            piece_identifier=PieceID.Pawn,
            team=team,
            moveset=(
                (0, 1)
            )  # moves one square 'up' the board
        )


class Bishop(Piece):
    """
    Bishop object.
    """
    def __init__(self, team: Team = Team.B):
        super().__init__(
            piece_identifier=PieceID.Bishop,
            team=team,
            moveset=(
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            ),
            moveset_multiplier=range(1, 8)  # Bishop can move up to 7 cells diagonally
        )


class Knight(Piece):
    """
    Knight object.
    """
    def __init__(self, team: Team = Team.B):
        super().__init__(
            piece_identifier=PieceID.Knight,
            team=team,
            moveset=(
                (2, 1),
                (1, 2),
                (-2, 1),
                (2, -1),
                (-2, -1),
                (-1, 2),
                (-1, -2)
            )
        )


class Rook(Piece):
    """
    Rook object.
    """
    def __init__(self, team: Team = Team.B):
        super().__init__(
            piece_identifier=PieceID.Rook,
            team=team,
            moveset=(
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1)
            ),
            moveset_multiplier=range(1, 8)
        )


class Queen(Piece):
    """
    Queen object.
    """
    def __init__(self, team: Team = Team.B):
        super().__init__(
            piece_identifier=PieceID.Queen,
            team=team,
            moveset=(
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
                (1, 1),
                (-1, -1),
                (1, -1),
                (-1, 1)
            ),
            moveset_multiplier=range(1, 8)
        )


class King(Piece):
    """
    King object.
    """
    def __init__(self, team: Team = Team.B):
        super().__init__(
            piece_identifier=PieceID.King,
            team=team,
            moveset=(
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            )
        )


if __name__ == "__main__":
    pawn = Pawn(Team.B)
    print(pawn.piece_identifier)
    print(pawn.team)
    print(pawn)
    print(pawn.moveset)
