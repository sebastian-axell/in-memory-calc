"""A calculator class."""
import re

from .operation import Operation, OperationException

class CalculatorException(Exception):
    pass

def value_is_register(value):
    return bool(re.match(r'^[a-zA-Z]+$',value))
def value_is_numeric(value):
    return bool(re.match(r'^[0-9]+$',value))

class Calculator:
    """A class to represent a calculator"""
    def __init__(self):
        self.stack: list[Operation]=list()
        self.registers: dict[str, list[Operation]] =dict()

    def __contains__(self, register: str):
        """Check whether the register has already been added"""
        return register.lower() in self.registers.keys()

    def __getitem__(self, register: str):
        return self.registers[register.lower()]

    def __setitem__(self, register, value):
        self.registers[register.lower()] = value

    def add_operation(self, register, operation: str, value):
        try:
            self.stack.append(Operation(register, operation, value))
        except OperationException as e:
            raise CalculatorException(e.args[0])

    def add_print_operation(self, register: str):
        self.add_operation(register, "print", "0")

    def determine_register_value(self, register, list_of_operations, register_value=None):
        print("determining", register)
        for operation in list_of_operations:
            print("operation: ", operation)
            value = operation.value
            operation = operation.operation
            if value_is_numeric(value):
                print(f"{register} is {value}, regiser value {register_value}")
                register_value = self.update_register_value(operation, register_value, int(value))
            elif value_is_register(value):
                if value not in self:
                    raise CalculatorException(f"The value of register {value} cannot be resolved.")
                self.determine_register_value(value, self[value])
                if not self[value]:
                    raise CalculatorException(f"The value of register {value} cannot be resolved.")
                register_value = self.update_register_value(operation, register_value, self[value][0])
        self[register] = [register_value]
        return "NaN"

    def update_register_value(self, operation, register_value, value):
        if operation == "add":
            if register_value:
                register_value += value
            else:
                register_value = value
        elif operation == "subtract":
            if register_value:
                register_value -= value
            else:
                register_value = value
        elif operation == "multiply":
            if not register_value:
                print("Cannot multiply undefined register - skipping")
            else:
                register_value *= value
        return register_value

    def evaluate_register(self, register):
        if isinstance(self[register][0], int) and len(self[register])==1:
            return self[register][0]
        else:
            try:
                if isinstance(self[register][0], int):
                    self.determine_register_value(register, self[register][1:], self[register][0])
                else:
                    self.determine_register_value(register, self[register])
            except CalculatorException as e:
                print(f"When trying to evaluate the value of register {register} the following error occured: {e.args[0]}")
            print(self.registers)

    def evaluate_stack(self):
        for operation in self.stack:
            if operation.operation == "print":
                self.evaluate_register(operation.register)
            else:
                self.add_register_operation(operation)

    def add_register_operation(self, operation):
        if operation.register in self:
            self[operation.register].append(operation)
        else:
            self[operation.register] = list()
            self[operation.register].append(operation)
