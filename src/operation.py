"""Class to represent the operations inputted"""

class OperationException(Exception):
    pass

all_operations = ["add", "subtract","multiply", "print"]

class Operation():
    def __init__(self, register, operation: str, value):
        if operation not in all_operations:
            raise OperationException(f"Invalid operation. Valid operations are: {all_operations}")
        self.register=register
        self.operation=operation.lower()
        self.value=value
    def __str__(self):
        return f"{self.register} {self.operation} {self.value}"
