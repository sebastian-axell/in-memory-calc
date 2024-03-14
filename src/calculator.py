"""A class to represent a calculator."""
import re

from .ExecutionTree import ExecutionTree
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


def update_register_value(operation, register_value, value):
    """Updates the given registry value based on the given operation and value"""
    if isinstance(value, str):
        value = convert_string_value_to_number(value)
    operations = {
        "add": lambda x, y: x + y if x is not None else y,
        "subtract": lambda x, y: x - y if x is not None else -y,
        "multiply": lambda x, y: x * y if x is not None else None
    }
    return operations[operation](register_value, value)


class Calculator:
    """A class to represent a calculator"""

    def __init__(self):
        self.stack: list[Operation] = list()
        self.registers: dict[str, list[Operation]] = dict()
        self.evaluated_registers = dict()
        self.seen_registers=set()

    def __contains__(self, register: str):
        """Checks whether the given register has been seen before. Enables us to do if REGISTRY in self."""
        return register.lower() in self.registers.keys()

    def __getitem__(self, register: str):
        """Retrieves the register store for a given register. Enables us to do self[REGISTRY]"""
        return self.registers[register.lower()]

    def __setitem__(self, register, value):
        """Sets the register store for a given register to value. Enables us to do self[registry]=valuea"""
        self.registers[register.lower()] = value

    def add_operation(self, register, operation: str, value):
        """Adds an Operation object representing a calculator operation to the stack"""
        self.stack.append(Operation(register, operation, value))

    def reset_register_value(self, register):
        """Removes the evaluated value for a given register"""
        self.evaluated_registers.pop(register.lower(), None)

    def clear_register_operations(self, register):
        """Clears all operations for the given register"""
        if register in self:
            self[register] = []
        else:
            self.stack = [operation for operation in self.stack if operation.register!=register.lower()]

    def show_register(self, register):
        """Shows all the operations for the given register"""
        all_operations = [str(operation) for operation in self.stack if operation.register==register.lower()]
        if len(all_operations) == 0:
            print(f"Register {register} has no operations added.")
        else:
            register_operations = [str(operation) for operation in self.stack if operation.register==register.lower()]
            print(f"Register {register} has the following operations: {', '.join(register_operations)}")

    def show_all_registers(self):
        """Shows all the operations for all the registers"""
        all_registers = [operation.register for operation in self.stack]
        if len(all_registers) == 0:
            print("No operations for any registered register.")
        else:
            for register in all_registers:
                self.show_register(register)

    def reset(self):
        """Resets the calculator"""
        self.evaluated_registers={}
        self.registers={}
        self.stack = []
        self.seen_registers=set()

    def add_print_operation(self, register: str):
        """Adds a print operation of the given register to the stack"""
        self.add_operation(register, "print", "0")

    def evaluate_register(self, register, list_of_operations, register_value=None, root_element: ExecutionTree=None):
        """Evaluates the given register"""
        self.seen_registers.add(register.lower())
        for operation in list_of_operations:
            child = ExecutionTree(operation)
            root_element.add_child(child)
            value = operation.value
            operation = operation.operation
            if value_is_numeric(value):
                register_value = update_register_value(operation, register_value, value)
                continue
            another_register = value  # if it is not numeric-> has to be another register
            if another_register not in self:
                raise CalculatorException(f"The value of register {another_register} cannot be resolved.")
            if another_register in self.seen_registers and another_register not in self.evaluated_registers:
                child.mark_as_dead_end()
                raise CalculatorException(f"{register} references register {another_register} but register {another_register} has not previously been determined.")
            if not another_register in self.evaluated_registers:
                self.evaluate_register(another_register, self[another_register], root_element=child)
            register_value = update_register_value(operation, register_value, self.evaluated_registers[another_register])
        if register_value is None:
            raise CalculatorException(f"The value of register {register} cannot be resolved.")
        self.evaluated_registers[register] = register_value
        self.clear_register_operations(register)

    def evaluate_stack(self, root_element):
        """Evaluates all the operations in the stuck this far, updates the registers and resets the stack"""
        for operation in self.stack:
            if operation.operation == "print":
                try:
                    register = operation.register
                    if register not in self:
                        raise CalculatorException(f"The value of register {register} cannot be resolved.")
                    if register in self.evaluated_registers:
                        self.evaluate_register(register, self[register], self.evaluated_registers[register], root_element=root_element)
                    else:
                        self.evaluate_register(register, self[register], root_element=root_element)
                    print(self.evaluated_registers[register])
                    self.seen_registers=set()
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
