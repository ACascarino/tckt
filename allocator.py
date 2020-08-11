from dataclasses import dataclass
from typing import List, Tuple


@dataclass(order=True)
class SeatingBank:
    """Dataclass to hold properties of a seating bank.

    Arguments:
    row_pitch: Distance between rows, in metres
    column_pitch: Distance between seats in a row, in metres
    max_columns: Number of seats in a row
    row_labels: List of strings detailing the labels for each row
    """

    row_pitch: float
    column_pitch: float
    max_columns: int
    row_labels: List[str]


class Seat:
    """Class defining a particular seat within a seating bank.

    Arguments:
    bank: The SeatingBank of which the Seat is a member
    row: The row label of the Seat
    column: The seat number of the Seat within the row
    """
    def __init__(self, bank: SeatingBank, row: str, column: int):
        if column > bank.max_columns:
            raise ValueError("Column cannot be beyond the limits of the SeatingBank!")
        if row not in bank.row_labels:
            raise ValueError("Row not in SeatingBank row labels!")

        self.bank = bank
        self.row = bank.row_labels.index(row)
        self.column = column
        self.width = bank.column_pitch
        self.depth = bank.row_pitch

    def get_x(self) -> float:
        """Get the X offset from the edge of the SeatingBank, in metres"""

        return self.width * self.column

    def get_y(self) -> float:
        """Get the Y offset from the edge of the SeatingBank, in metres"""

        return self.depth * self.row

    def distance_from(self, other: 'Seat') -> Tuple[float, float]:
        """Get the X and Y distance between this seat and another, in metres"""

        x_diff = abs(self.get_x() - other.get_x())
        y_diff = abs(self.get_y() - other.get_y())

        return x_diff, y_diff

    def is_socially_distant_from(self, other: 'Seat', x_thresh: float, y_thresh: float) -> bool:
        """Determine if the provided seat is distanced from this one given X and Y thresholds.

        Arguments:
        other: the target seat
        x_thresh: horizontal (along-row) social distancing threshold (in metres)
        y_thresh: lateral (across-row) social distancing threshold (in metres)

        Returns:
        A bool describing if the provided seat is distanced from this one.
        """

        x, y = self.distance_from(other)

        # Draw an ellipse around myself; if the other seat is contained within, we are not distanced.
        if (x ** 2 / x_thresh ** 2) + (y ** 2 / y_thresh ** 2) >= 1:
            return True
        else:
            return False

