
class Symbol:

    def __init__(self, symbol, series, t) -> None:

        # Symbol properties
        self.symbol = symbol
        self.series = series
        self.t = t

        # Generate dictionary that converts input subrule 'op' parameter
        # into an actual operator
        self._operator = {
            '=': self.__eq__,
            '<=': self.__leq__,
            '>=': self.__geq__,
            '<': self.__lt__,
            '>': self.__gt__,
        }

    def __repr__(self) -> str:
        return f'{self.symbol}: ({self.t[0]}, {self.t[1]})'

    def __eq__(self, other) -> bool:
        """
        Equality operator.
        """

        # Check if self.symbol is a nan
        if self.symbol != self.symbol:
            return False

        if isinstance(other, Symbol):
            return self.symbol == other.symbol

        if isinstance(other, str):
            return self.symbol == other

        else:
            raise RuntimeError("Failure in '=' operator.")

    def __leq__(self, other) -> bool:
        """
        Less or equal operator.
        """

        # Check if self.symbol is a nan
        if self.symbol != self.symbol:
            return False

        if isinstance(other, Symbol):
            return self.symbol <= other.symbol

        if isinstance(other, str):
            return self.symbol <= other

        else:
            raise RuntimeError("Failure in '<=' operator.")

    def __geq__(self, other) -> bool:
        """
        Greater or equal operator.
        """

        # Check if self.symbol is a nan
        if self.symbol != self.symbol:
            return False

        if isinstance(other, Symbol):
            return self.symbol >= other.symbol

        if isinstance(other, str):
            return self.symbol >= other

        else:
            raise RuntimeError("Failure in '>=' operator.")

    def __lt__(self, other) -> bool:
        """
        Less than operator.
        """

        # Check if self.symbol is a nan
        if self.symbol != self.symbol:
            return False

        if isinstance(other, Symbol):
            return self.symbol < other.symbol

        if isinstance(other, str):
            return self.symbol < other

        else:
            raise RuntimeError("Failure in '<' operator.")

    def __gt__(self, other) -> bool:
        """
        Greater than operator.
        """

        # Check if self.symbol is a nan
        if self.symbol != self.symbol:
            return False

        if isinstance(other, Symbol):
            return self.symbol > other.symbol

        if isinstance(other, str):
            return self.symbol > other

        else:
            raise RuntimeError("Failure in '>' operator.")
