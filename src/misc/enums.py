"""
Various enums because strings are gross.
"""


from enum import Enum, auto


class GameType(Enum):
    Chess = auto()


class Team(Enum):
    A = auto()
    B = auto()


class PieceID(Enum):
    Pawn = {Team.A: "♙", Team.B: "♟"}
    Bishop = {Team.A: "♗", Team.B: "♝"}
    Knight = {Team.A: "♘", Team.B: "♞"}
    Rook = {Team.A: "♖", Team.B: "♜"}
    Queen = {Team.A: "♕", Team.B: "♛"}
    King = {Team.A: "♔", Team.B: "♚"}


class PieceStatus(Enum):
    ALIVE = auto()
    DEAD = auto()


class CellID(Enum):
    """enums for cells on the board"""
    A_ONE = "A1"
    A_TWO = "A2"
    A_THREE = "A3"
    A_FOUR = "A4"
    A_FIVE = "A5"
    A_SIX = "A6"
    A_SEVEN = "A7"
    A_EIGHT = "A8"

    B_ONE = "B1"
    B_TWO = "B2"
    B_THREE = "B3"
    B_FOUR = "B4"
    B_FIVE = "B5"
    B_SIX = "B6"
    B_SEVEN = "B7"
    B_EIGHT = "B8"

    C_ONE = "C1"
    C_TWO = "C2"
    C_THREE = "C3"
    C_FOUR = "C4"
    C_FIVE = "C5"
    C_SIX = "C6"
    C_SEVEN = "C7"
    C_EIGHT = "C8"

    D_ONE = "D1"
    D_TWO = "D2"
    D_THREE = "D3"
    D_FOUR = "D4"
    D_FIVE = "D5"
    D_SIX = "D6"
    D_SEVEN = "D7"
    D_EIGHT = "D8"

    E_ONE = "E1"
    E_TWO = "E2"
    E_THREE = "E3"
    E_FOUR = "E4"
    E_FIVE = "E5"
    E_SIX = "E6"
    E_SEVEN = "E7"
    E_EIGHT = "E8"

    F_ONE = "F1"
    F_TWO = "F2"
    F_THREE = "F3"
    F_FOUR = "F4"
    F_FIVE = "F5"
    F_SIX = "F6"
    F_SEVEN = "F7"
    F_EIGHT = "F8"

    G_ONE = "G1"
    G_TWO = "G2"
    G_THREE = "G3"
    G_FOUR = "G4"
    G_FIVE = "G5"
    G_SIX = "G6"
    G_SEVEN = "G7"
    G_EIGHT = "G8"

    H_ONE = "H1"
    H_TWO = "H2"
    H_THREE = "H3"
    H_FOUR = "H4"
    H_FIVE = "H5"
    H_SIX = "H6"
    H_SEVEN = "H7"
    H_EIGHT = "H8"
 