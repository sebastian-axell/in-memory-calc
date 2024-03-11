"""A calculator class."""
import re

from .operation import Operation

class CalculatorException(Exception):
    pass
def value_is_numeric(value):
    return bool(re.match(r'^-?\d+(\.\d*)?$',value)) # either float or an int

def convert_string_value_to_number(value):
    try:
        return int(value)
    except ValueError:
        return float(value)


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
        # we know we only add valid operations from validating at command_parser
        self.stack.append(Operation(register, operation, value))

    def add_print_operation(self, register: str):
        self.add_operation(register, "print", "0")

    def evaluate_register(self, register, list_of_operations, register_value=None):
        for operation in list_of_operations:
            if not isinstance(operation, Operation):
                return self.evaluate_register(register, self[register][1:], operation)
            value = operation.value
            operation = operation.operation
            if value_is_numeric(value):
                register_value = self.update_register_value(operation, register_value, value)
                continue
            another_register = value # if it is not numeric-> has to be another register
            if another_register not in self:
                raise CalculatorException(f"The value of register {another_register} cannot be resolved.")
            self.evaluate_register(another_register, self[another_register])
            register_value = self.update_register_value(operation, register_value, self[another_register][0])
        self[register] = [register_value]

    def update_register_value(self, operation, register_value, value):
        value = convert_string_value_to_number(value)
        operations = {
            "add": lambda x, y: x + y if x is not None else y,
            "subtract": lambda x, y: x - y if x is not None else -y,
            "multiply": lambda x, y: x * y if x is not None else None
        }
        return operations[operation](register_value, value)


    def evaluate_stack(self):
        for operation in self.stack:
            if operation.operation == "print":
                try:
                    register = operation.register
                    if register not in self:
                        raise CalculatorException(f"The value of register {register} cannot be resolved.")
                    self.evaluate_register(operation.register, self[operation.register])
                    print(self[operation.register])
                except CalculatorException as e:
                    print(f"When trying to evaluate the value of register {operation.register} the following error occured: {e.args[0]}")
            else:
                self.add_register_operation(operation)

    def add_register_operation(self, operation):
        if operation.register in self:
            self[operation.register].append(operation)
        else:
            self[operation.register] = list()
            self[operation.register].append(operation)
