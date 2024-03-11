"""A class to represent a calculator."""
import re

from .operation import Operation


class CalculatorException(Exception):
    """Captures exceptions found during calculator execution"""
    pass


def value_is_numeric(value):
    """Checks if a value is either a float or an int"""
    return bool(re.match(r'^-?\d+(\.\d*)?$', value))


def convert_string_value_to_number(value):
    """Converts the input value to either a float or an int"""
    try:
        return int(value)
    except ValueError:
        return float(value)


class Calculator:
    """A class to represent a calculator"""

    def __init__(self):
        self.stack: list[Operation] = list()
        self.registers: dict[str, list[Operation]] = dict()

    def __contains__(self, register: str):
        """Check whether the given register has been seen before. Enables us to do if REGISTRY in self."""
        return register.lower() in self.registers.keys()

    def __getitem__(self, register: str):
        """Retrieves the register store for a given register. Enables us to do self[REGISTRY]"""
        return self.registers[register.lower()]

    def __setitem__(self, register, value):
        """sets the register store for a given register to value. Enables us to do self[registry]=value"""
        self.registers[register.lower()] = value

    def add_operation(self, register, operation: str, value):
        """Adds an Operation object representing a calculator operation to the stack"""
        self.stack.append(Operation(register, operation, value))

    def add_print_operation(self, register: str):
        """Adds a print operation of the given register to the stack"""
        self.add_operation(register, "print", "0")

    def evaluate_register(self, register, list_of_operations, register_value=None):
        """Evaluates the given register"""
        for operation in list_of_operations:
            if not isinstance(operation, Operation):
                # if the value is not an operation, it is a numeric value which defines the starting value for the
                # subsequent evaluations
                return self.evaluate_register(register, self[register][1:], operation)
            value = operation.value
            operation = operation.operation
            if value_is_numeric(value):
                register_value = self.update_register_value(operation, register_value, value)
                continue
            another_register = value  # if it is not numeric-> has to be another register
            if another_register not in self:
                raise CalculatorException(f"The value of register {another_register} cannot be resolved.")
            self.evaluate_register(another_register, self[another_register])
            register_value = self.update_register_value(operation, register_value, self[another_register][0])
        self[register] = [register_value]

    def update_register_value(self, operation, register_value, value):
        """Updates the given registry value based on the given operation and value"""
        value = convert_string_value_to_number(value)
        operations = {
            "add": lambda x, y: x + y if x is not None else y,
            "subtract": lambda x, y: x - y if x is not None else -y,
            "multiply": lambda x, y: x * y if x is not None else None
        }
        return operations[operation](register_value, value)

    def evaluate_stack(self):
        """Evaluates all the operations in the stuck this far, updates the registers and resets the stack"""
        for operation in self.stack:
            if operation.operation == "print":
                try:
                    register = operation.register
                    if register not in self:
                        raise CalculatorException(f"The value of register {register} cannot be resolved.")
                    self.evaluate_register(register, self[register])
                    print(self[register][0])
                except CalculatorException as e:
                    print(
                        f"When trying to evaluate the value of register {operation.register} the following error occured: {e.args[0]}")
            else:
                self.add_register_operation(operation)
        self.stack = []

    def add_register_operation(self, operation):
        """Adds operations to the register store of a register. If not seen before, it is initialises the store
        and then adds the operation. Else it adds the operation."""
        if operation.register in self:
            self[operation.register].append(operation)
        else:
            self[operation.register] = list()
            self[operation.register].append(operation)
