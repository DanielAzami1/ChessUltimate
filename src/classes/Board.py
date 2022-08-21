from src.misc.enums import GameType, CellID
from loguru import logger


class Board:
    """Board obj will represent the chess board, a series of individual 'cells' organized in a matrix."""

    def __init__(self, game_type: GameType = GameType.Chess, board: list = []):
        self.game_type = game_type
        self.board = board
        logger.info(f"Board Initializing - GameType: {self.game_type}")

        if self.game_type is GameType.Chess:
            self.initialize_chess_board(cell_identifiers=list(CellID.__members__.values()))

    def initialize_chess_board(self, cell_identifiers: list):
        """Initialize the chess board object by creating 'rows' (list[Cell]) and combining them in a single list."""
        nrow, ncol = 8, 8
        cell_counter = 0  # used to pass in the correct CellID enum to each cell obj instantiated below.
        for i in range(nrow):
            row = []
            for j in range(ncol):
                row.append(
                    Cell(cell_identifier=cell_identifiers[cell_counter], cell_position=(i, j))
                )
                cell_counter += 1
            self.board.append(row)

    def __str__(self):
        output_string = ""
        for row in self.board:
            output_string += " ".join(map(str, row)) + "\n"
        return f"\n{self.game_type.name}\n" + output_string


class Cell:
    """Cell obj to represent the 'squares' on a chess board - positions that pieces can move to and occupy."""

    def __init__(self, cell_identifier: CellID, occupied_by=None, cell_position: tuple(int) = (0, 0)):
        self.cell_identifier = cell_identifier
        self.occupied_by = occupied_by
        self.cell_position = cell_position

    def __str__(self):
        if self.occupied_by is not None:
            return f"[{self.occupied_by}]"
        else:
            return f"[{self.cell_identifier.value}]"


if __name__ == "__main__":
    chess_board = Board()
    logger.info(chess_board)
