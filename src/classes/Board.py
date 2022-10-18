from src.classes.Piece import Piece
from src.misc.enums import GameType, CellID
from src.misc.exceptions import UnknownGameTypeError
from src.misc.constants import DEFAULT_STARTING_CHESS_CONFIG
from loguru import logger
import numpy as np


class Board:
    """Board obj will represent the chess board, a series of individual 'cells' organized in a matrix."""

    def __init__(
            self,
            game_type: GameType = GameType.Chess,
            board: list = []
    ):
        if not isinstance(game_type, GameType):
            raise UnknownGameTypeError(
                f"Chosen game type '{game_type}' is not recognized as a valid game type."
            )
        self.game_type = game_type
        self.board = board
        self.piece_controller = PieceController()
        logger.info(f"Board Initializing - GameType: {self.game_type}")
        if self.game_type is GameType.Chess:
            cell_identifiers = list(CellID.__members__.values())
            self.initialize_chess_board(cell_identifiers=cell_identifiers)

    def initialize_chess_board(self, cell_identifiers: list):
        """Initialize the chess board object by creating 'rows' (list[Cell]) and combining them in a single list."""
        nrow, ncol = 8, 8
        cell_counter = 0  # used to pass in the correct CellID enum to each cell obj instantiated below
        for i in range(nrow):
            row = []
            for j in range(ncol):
                row.append(
                    Cell(
                        cell_identifier=cell_identifiers[cell_counter],
                        cell_position=(i, j),
                    )
                )
                cell_counter += 1
            self.board.append(row)
        self.board = self.piece_controller.chess_place_starting_pieces(self.board)

    def __str__(self):
        output_string = ""
        for row in self.board:
            output_string += " ".join(map(str, row)) + "\n"
        return f"\n\n{self.game_type.name}\n\n" + output_string


class Cell:
    """Cell obj to represent the 'squares' on a chess board - positions that pieces can move to and occupy."""

    def __init__(
            self, cell_identifier: CellID, occupied_by: Piece = None, cell_position: tuple = (0, 0)
    ):
        self.cell_identifier = cell_identifier
        self.occupied_by = occupied_by
        self.cell_position = cell_position

    def __str__(self):
        if self.occupied_by is not None:
            return f"[{self.occupied_by}]"
        else:
            return f"[{self.cell_identifier.value}]"


class PieceController:
    """
    Handler for movement of pieces around the board as I couldn't reconcile how to handle movement functionality
    in either the Piece or Board class.
    """

    @staticmethod
    def chess_place_starting_pieces(board: list[list[Cell]]) -> list[list[Cell]]:
        """
        This method will be invoked when the Board obj is initialized, placing the default set of pieces on the board.
        Takes in the 'board' (list[list[Cell]]), modifies the 'occupied_by' attr of specific cells, and returns
        the updated board.
        """
        cfg = DEFAULT_STARTING_CHESS_CONFIG
        for row_num in cfg:
            for cell, piece in zip(board[row_num], cfg[row_num]):
                cell.occupied_by = piece
        return board

    @staticmethod
    def move_is_valid(current_cell: Cell, target_cell: Cell) -> bool:
        """
        Checks to see if the piece occupying current_cell can move to target_cell based on the piece currently
        occupying current_cell. Returns T/F as expected.

        TODO // This function is a mess need to refactor
        """
        piece = current_cell.occupied_by
        if piece is None:  # if there is no piece in current_cell for some reason
            return False
        moveset = piece.moveset
        cur_pos = np.array(current_cell.cell_position)
        new_pos = np.array(target_cell.cell_position)
        requested_move = new_pos - cur_pos
        blocked_by_piece = False  # i think when a piece is in your path, you can't move past it without attacking it
        # TODO // implement some logic for this
        if requested_move in moveset:
            return True
        else:
            if hasattr(piece, "moveset_multiplier"):
                for multiplier in piece.moveset_multiplier:
                    if requested_move in multiplier * moveset:
                        return True  # TODO // this is just wrong
        return False

    @staticmethod
    def move_piece(current_cell: Cell, target_cell: Cell):
        """
        TODO
        """
        pass

    @staticmethod
    def attack_piece(current_cell: Cell, target_cell: Cell):
        """
        TODO
        """
        pass


if __name__ == "__main__":
    chess_board = Board()
    logger.info(chess_board)
