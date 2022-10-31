from src.classes.Piece import Piece
from src.misc.enums import GameType, CellID
from src.misc.exceptions import UnknownGameTypeError, IllegalMoveError
from src.misc.utils import log_debug
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
            self,
            cell_identifier: CellID,
            occupied_by: Piece = None,
            cell_position: tuple = (0, 0)
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
    def move_is_valid(requested_move: np.ndarray, piece: Piece) -> bool:
        """
        Checks to see if the piece occupying current_cell can move to target_cell based on the piece currently
        occupying current_cell. Returns T/F as expected.

        TODO // This function is a mess need to refactor
        """
        blocked_by_piece = False  # i think when a piece is in your path, you can't move past it without attacking it
        # TODO // implement some logic for this
        moveset = piece.moveset
        
        if any(np.array_equal(move, requested_move) for move in moveset):
            log_debug(
                piece=piece,
                moveset=moveset,
                requested_move=requested_move,
                match_found=True
            )
            return True
        elif hasattr(piece, "moveset_multiplier"):
            for multiplier in piece.moveset_multiplier:
                if any(np.array_equal(move, requested_move) for move in multiplier * moveset):
                    return True
        return False

    @staticmethod
    def move_piece(current_cell: Cell, target_cell: Cell) -> bool:
        """
        'move' a piece from current_cell to target_cell. Return T if move is successful or raise an error if the move
        is 'illegal', or return F if there is no piece in current_cell.

        TODO // need to implement some logic for attacks
        """
        piece = current_cell.occupied_by
        if piece is None:  # if there is no piece in current_cell for some reason
            logger.warning(
                f"UNABLE to move piece in cell {current_cell.cell_identifier} - Cell is empty"
            )
            return False
        cur_pos = np.array(current_cell.cell_position)
        new_pos = np.array(target_cell.cell_position)
        requested_move = np.flip(new_pos - cur_pos)
        if not PieceController.move_is_valid(requested_move, piece):
            log_debug(
                requested_move=requested_move,
                piece=repr(piece)
            )
            raise IllegalMoveError(
                f"'{piece}' ({piece.piece_identifier}, {piece.team}) CANNOT"
                f" MOVE from cell {current_cell.cell_identifier} to cell {target_cell.cell_identifier}"
            )
        target_cell.occupied_by = current_cell.occupied_by
        current_cell.occupied_by = None
        logger.success(
            f"Piece '{piece}' ({piece.piece_identifier}, {piece.team}) "
            f"MOVED from cell {current_cell.cell_identifier} to cell {target_cell.cell_identifier}"
        )
        return True

    @staticmethod
    def attack_piece(current_cell: Cell, target_cell: Cell):
        """
        TODO
        """
        pass


if __name__ == "__main__":
    """
    For testing purposes only.
    """
    chess_board = Board(game_type=GameType.Chess)
    logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[0][0], chess_board.board[2][0])  # should be successful
    logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[0][0], chess_board.board[2][2])  # empty cell, should warn
    logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[1][1], chess_board.board[2][1])
    logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[0][1], chess_board.board[0][2])  # should be illegal
    logger.info(chess_board)