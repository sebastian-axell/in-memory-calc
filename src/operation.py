"""Class to represent the operations inputted"""
class Operation():
    def __init__(self, register, operation: str, value):
        self.register=register.lower()
        self.operation=operation.lower()
        self.value=value.lower()
    def __str__(self):
        return f"{self.register} {self.operation} {self.value}"
