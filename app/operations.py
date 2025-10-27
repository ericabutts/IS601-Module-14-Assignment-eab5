from decimal import Decimal
from app.exceptions import OperationError

class Operation:
    """Base class for all operations."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__.replace("Operation", "").lower()


class AddOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b


class SubtractOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b


class MultiplyOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b


class DivideOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Division by zero")
        return a / b


class PowerOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b < 0:
            raise OperationError("Negative exponents not supported")
        return Decimal(pow(float(a), float(b)))


class RootOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if a < 0:
            raise OperationError("Cannot calculate root of negative number")
        if b == 0:
            raise OperationError("Zero root is undefined")
        return Decimal(pow(float(a), 1 / float(b)))

class ModulusOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Division by zero")
        return a % b
    
class IntegerDivisionOperation(Operation):
    """Perform division that results in an integer quotient, discarding any fractional part."""
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Division by zero")
        return a // b
    
class PercentageOperation(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Division by zero")
        return (a / b) * 100
    
class AbsoluteDifferenceOperation(Operation):
    def execute(self, a: Decimal, b: Decimal):
        diff = a - b
        if diff < 0:
            diff = -diff
        return diff

class OperationFactory:
    """Factory for creating operation instances by name."""
    _operations = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'integerdivision': IntegerDivisionOperation,
        'percentage': PercentageOperation,
        'absolutedifference': AbsoluteDifferenceOperation
    }

    @classmethod
    def create_operation(cls, name: str) -> Operation:
        op_class = cls._operations.get(name.lower())
        if not op_class:
            raise ValueError(f"Unknown operation: {name}")
        return op_class()
