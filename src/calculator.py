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

    def add_print_operation(self, register: str):
        """Adds a print operation of the given register to the stack"""
        self.add_operation(register, "print", "0")

    def evaluate_register(self, register: str, list_of_operations, register_value=None, seen_registers=None,
                          root_element: ExecutionTree = None):
        """Evaluates the given register"""
        seen_registers.add(register.lower())
        for operation in list_of_operations:
            child = ExecutionTree(operation)
            root_element.add_child(child)
            if not isinstance(operation, Operation): # case A
                return self.evaluate_register(register, self[register][1:], operation, seen_registers=seen_registers)
            value = operation.value
            operation = operation.operation
            if value_is_numeric(value): # case B
                register_value = update_register_value(operation, register_value, value)
                continue
            another_register = value  # if it is not numeric-> has to be another register
            if another_register not in self: # case C
                raise CalculatorException(f"The value of register {another_register} cannot be resolved.")
            if another_register in seen_registers: # case D
                if isinstance(self[another_register][0], (int, float)):  # has it been determined intermediately
                    if isinstance(self[register][0], (int, float)):
                        register_value = update_register_value(operation, self[register][0],
                                                                    self[another_register][0])
                    else:
                        register_value = update_register_value(operation, register_value,
                                                                    self[another_register][0])
                    self[register] = [register_value]
                    continue
                if not register_value: # case E
                    skipped_operation = self[register].pop(0)
                    try:
                        root_element.add_parent_info(child, "No values found.")
                        root_element.delete_child(child)
                        self.evaluate_register(register, self[register], seen_registers=seen_registers,
                                               root_element=root_element)
                        self.evaluate_register(register, [skipped_operation], self[register][0],
                                               seen_registers=seen_registers,
                                               root_element=root_element)
                        root_element.add_info("Re-evaluated.")
                        return
                    except CalculatorException as e:
                        seen_registers.remove(another_register)
                        self[register] = [skipped_operation] + self[register]
                        child.mark_as_dead_end()
                        continue
            if another_register == register and register_value: # case F
                register_value = update_register_value(operation, register_value, register_value)
                continue
            try:
                self.evaluate_register(another_register, self[another_register], seen_registers=seen_registers,
                                       root_element=child) # case G
                register_value = update_register_value(operation, register_value, self[another_register][0])
            except CalculatorException as e:
                child.mark_as_dead_end()
                return self.evaluate_register(register, self[register], register_value, seen_registers=seen_registers,
                                              root_element=root_element) # case H
        if register_value is None:
            raise CalculatorException(f"The value of register {register} cannot be resolved.")
        self[register] = [register_value]

    def evaluate_stack(self, root_element):
        """Evaluates all the operations in the stuck this far, updates the registers and resets the stack"""
        for operation in self.stack:
            if operation.operation == "print":
                try:
                    register = operation.register
                    if register not in self:
                        raise CalculatorException(f"The value of register {register} cannot be resolved.")
                    self.evaluate_register(register, self[register], seen_registers=set(), root_element=root_element)
                    print(self[register][0])
                    print(self.registers)
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
