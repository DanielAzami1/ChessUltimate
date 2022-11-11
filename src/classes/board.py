from src.classes import piece
from src.misc.enums import GameType, CellID
from src.misc.exceptions import UnknownGameTypeError, IllegalMoveError
from src.misc.utils import log_debug
from src.misc.constants import DEFAULT_STARTING_CHESS_CONFIG
from loguru import logger
from numpy import array, ndarray, array_equal, flip


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
        self.piece_controller = PieceController(board)  # pass by ref
        logger.info(f"Board Initializing - GameType: {self.game_type}")
        if self.game_type is GameType.Chess:
            cell_identifiers = list(CellID.__members__.values())
            self.initialize_chess_board(cell_identifiers=cell_identifiers)
            self.place_starting_pieces()

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

    def place_starting_pieces(self):
        """
        This method will be invoked when the Board obj is initialized, placing the default set of pieces on the board.
        Modifies the 'occupied_by' attr of specific cells based on the default starting chess config.
        """
        if self.game_type is GameType.Chess:
            cfg = DEFAULT_STARTING_CHESS_CONFIG
            for row_num in cfg:
                for cell, starting_piece in zip(self.board[row_num], cfg[row_num]):
                    cell.occupied_by = starting_piece

    def __str__(self):
        output_string = ""
        for row in self.board:
            output_string += " ".join(map(str, row)) + "\n"
        return f"\n\n{self.game_type.name}\n\n{output_string}"


class Cell:
    """Cell obj to represent the 'squares' on a chess board - positions that pieces can move to and occupy."""

    def __init__(
            self,
            cell_identifier: CellID,
            occupied_by: piece.Piece = None,
            cell_position: ndarray = (0, 0)
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
    def __init__(self, board: list[list[Cell]]):
        self.board = board

    def move_piece(self, current_cell: Cell, target_cell: Cell) -> bool:
        """
        'move' a piece from current_cell to target_cell. Return T if move is successful or raise an error if the move
        is 'illegal', or return F if there is no piece in current_cell.
        """
        if current_cell is target_cell:
            raise IllegalMoveError("Must select a NEW cell to move to.")

        focused_piece = current_cell.occupied_by
        if focused_piece is None:  # if there is no piece in current_cell for some reason
            logger.warning(f"UNABLE to move piece in cell {current_cell.cell_identifier} - Cell is empty")
            return False

        moveset = focused_piece.moveset
        cur_pos, new_pos = array(current_cell.cell_position), array(target_cell.cell_position)
        requested_move = flip(new_pos - cur_pos)  # I messed up my coords logic lol
        moveset_multiplier = focused_piece.moveset_multiplier if hasattr(focused_piece, "moveset_multiplier") else None

        move_valid = self.move_present_in_moveset(requested_move, moveset, moveset_multiplier)
        if not move_valid:
            raise IllegalMoveError(
                f"'{focused_piece}' ({focused_piece.piece_identifier}, {focused_piece.team}) CANNOT"
                f" MOVE from cell {current_cell.cell_identifier} to cell {target_cell.cell_identifier}"
            )

        if type(move_valid) is dict:  # if the piece used multiplier to traverse -> dict returned -> check for blockers
            move_blocked = self.move_blocked_by_piece(cur_pos, **move_valid)
            if move_blocked:
                logger.warning(f"{focused_piece} move BLOCKED by piece")
                return False

        piece_in_target_cell = target_cell.occupied_by
        if piece_in_target_cell is not None:  # if there is a piece already in target_cell
            if piece_in_target_cell.team is focused_piece.team:
                logger.warning(f"{focused_piece} move BLOCKED by friendly piece {piece_in_target_cell}"
                               f" (team {focused_piece.team})")
                return False
            else:
                self.attack_piece(piece_in_target_cell)

        #------------------< move success >-----------------#
        target_cell.occupied_by = current_cell.occupied_by
        current_cell.occupied_by = None
        logger.success(
            f"Piece '{focused_piece}' ({focused_piece.piece_identifier}, {focused_piece.team}) "
            f"MOVED from cell {current_cell.cell_identifier} to cell {target_cell.cell_identifier}"
        )
        return True

    def move_blocked_by_piece(self, cur_pos: ndarray, **multiplier_info):
        """
        Check to see if there is a piece in between the current_cell and the target_cell for piece movement purposes.
        """
        multiplier_used = multiplier_info["multiplier_used"]
        move = multiplier_info["move"] / multiplier_used
        multipliers_to_check = range(1, multiplier_used)
        for multiplier in multipliers_to_check:
            tmp_move = move * multiplier
            tmp_pos = cur_pos + tmp_move
            x, y = int(tmp_pos[0]), int(tmp_pos[1])
            cell = self.board[x][y]
            piece_at_cell = cell.occupied_by
            if piece_at_cell is not None:
                return True
        return False

    @staticmethod
    def move_present_in_moveset(requested_move: ndarray, moveset: ndarray, moveset_multiplier: range):
        """
        Checks to see if requested_move is present in moveset. If the piece has a moveset_multiplier, checks to see
        if there is some multiplier that creates a match.
        """
        if any(array_equal(move, requested_move) for move in moveset):
            return True
        elif moveset_multiplier is not None:
            for multiplier in moveset_multiplier:
                multiplied_moveset = moveset * multiplier
                for move in multiplied_moveset:
                    if array_equal(move, requested_move):
                        return {"move": move, "multiplier_used": multiplier}
        else:
            return False

    @staticmethod
    def attack_piece(enemy_piece: piece.Piece) -> piece.Piece:
        """
        Attack enemy piece. Return the piece that was destroyed/captured.
        """
        enemy_piece.alive = False
        return enemy_piece


if __name__ == "__main__":
    """
    For testing purposes only.
    """
    chess_board = Board(game_type=GameType.Chess)
    logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[0][0], chess_board.board[2][0])  # should be successful
    logger.info(chess_board)
    # chess_board.piece_controller.move_piece(chess_board.board[0][0], chess_board.board[2][2])  # empty cell, should warn
    # logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[1][1], chess_board.board[2][1])
    logger.info(chess_board)
    # try:
    #     chess_board.piece_controller.move_piece(chess_board.board[0][1], chess_board.board[0][2])  # should be illegal
    # except IllegalMoveError:
    #     logger.debug("ILLEGAL MOVE successfully caught")
    # logger.info(chess_board)
    chess_board.piece_controller.move_piece(chess_board.board[1][0], chess_board.board[2][0])
    logger.info(chess_board)

    chess_board.piece_controller.move_piece(chess_board.board[0][0], chess_board.board[1][0])
    logger.info(chess_board)

    chess_board.piece_controller.move_piece(chess_board.board[1][0], chess_board.board[1][0])
    logger.info(chess_board)