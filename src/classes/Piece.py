from Board import Board, Cell
from src.misc.enums import PieceID, Team, PieceStatus
from src.misc.exceptions import UnknownPieceIDError, UnknownTeamError
from abc import ABC, abstractmethod


class Piece(ABC):
    """Abstract Base Class for Piece objects (pieces on the chess board)"""
    @abstractmethod  # don't want to instantiate Piece
    def __init__(self, piece_identifier: PieceID = None, team: Team = Team.A, cell: Cell = None):
        assert piece_identifier is None or isinstance(piece_identifier, PieceID)
        if not isinstance(team, Team):
            raise TypeError(f"Team {team} is not a valid team for this gamemode.")
        self.piece_identifier = piece_identifier
        self.team = team
        self.alive = None  # whether this piece is still in play / on the board
        assert cell.occupied_by is None
        self.cell = cell
        cell.occupied_by = self
        '''
        Moveset Logic:
            
            Cells organized in a matrix, therefore possess some arbitrary (x, y) position in the 'board'. To 'move' a
            piece, we can take the piece's current cell's position, and increment (for team A :: 'down' the board) 
            or decrement (team B :: 'up' the board) to find the position of the new cell, and make the attribute swap.
            
            The 'moveset' variable will be assigned a tuple(tuple(int)). Each sub-tuple will hold two ints, an 'x' and
            a 'y' value that will be used to increment or decrement the current x/y value. 
            These values represent the amount of cells a particular move can traverse, i.e. for a Rook, we would have 
            something like self.moveset = ((1, 0), (2, 0), (3, 0) ... (n-1, 0), (0, 1), (0, 2) ... (0, n-1)), where 'n' 
            is the number of cells in a particular row or column. 
        '''
        self.moveset = None  # moves this piece is able to make

    def move_is_valid(self, requested_move: tuple[int]) -> bool:
        """
        TODO // Check if the requested_move is a valid move for caller piece.
        :param requested_move: increment/decrement of (x, y) coords that will land the piece in a new cell.
        :return: T/F based on whether the requested_move is possible
        """
        pass

    def move(self, requested_move: tuple[int]) -> bool:
        """
        TODO // First Check to see if the requested_move is valid, if it is, execute the move by changing the cell.
        :param requested_move: increment/decrement of (x, y) coords that will land the piece in a new cell.
        :return: T/F based on whether the requested_move was successful or not.
        """
        pass

    def __str__(self):
        return self.piece_identifier.value[self.team]


class Pawn(Piece):
    def __init__(self, piece_identifier: PieceID = None, team: Team = Team.A, cell: Cell = None):
        if not isinstance(piece_identifier, PieceID):
            raise UnknownPieceIDError(f"Invalid piece ID for Pawn: '{piece_identifier}'")
        if not isinstance(team, Team):
            raise UnknownTeamError(f"Piece {piece_identifier} cannot belong to team '{team}'.")
        self.piece_identifier = PieceID.Pawn
        self.team = team
        self.alive = PieceStatus.ALIVE
        self.moveset = ((1, 0), (-1, 0), (0, 1), (0, -1))  # ((1 right), (1 left), (1 up), (1 down))




if __name__ == "__main__":
    pawn = Pawn(PieceID.Pawn, Team.B)
    print(pawn.piece_identifier)
    print(pawn.team)
    print(pawn)






