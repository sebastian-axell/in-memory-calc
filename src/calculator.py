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

    def evaluate_register(self, register: str, list_of_operations, register_value=None, seen_registers=None, root_element: ExecutionTree=None):
        """Evaluates the given register"""
        seen_registers.add(register.lower())
        print("evaluting", register)
        print(seen_registers)
        for operation in list_of_operations:
            print(operation)
            if not isinstance(operation, Operation):
                # if the value is not an operation, it is a numeric value which defines the starting value for the
                # subsequent evaluations
                return self.evaluate_register(register, self[register][1:], operation, seen_registers=seen_registers)
            value = operation.value
            operation = operation.operation
            if value_is_numeric(value):
                register_value = self.update_register_value(operation, register_value, value)
                continue
            another_register = value  # if it is not numeric-> has to be another register
            if another_register not in self:
                raise CalculatorException(f"The value of register {another_register} cannot be resolved.")
            if another_register in seen_registers:
                print("seen_registers", seen_registers)
                if isinstance(self[another_register][0], (int,float)): # has it been determined intermediately
                    print("should bepk")
                    if isinstance(self[register][0], (int,float)): # and the current register as well
                        register_value = self.update_register_value(operation, self[register][0], self[another_register][0])
                    else:
                        register_value = self.update_register_value(operation, register_value, self[another_register][0])
                    self[register] = [register_value]
                    return
                print("made it here")
                if not register_value:
                    print("and here")
                    skipped_operation = self[register].pop(0)
                    try:
                        self.evaluate_register(register, self[register], seen_registers=seen_registers)
                        print("switch ->", skipped_operation)
                        self.evaluate_register(register,[skipped_operation], self[register][0], seen_registers=seen_registers)
                        return
                    except CalculatorException as e:
                        seen_registers.remove(another_register)
                        self[register] = [skipped_operation] + self[register]
                        print(self[register])
                        continue
            if another_register == register and register_value:
                print("Ok", register,  register_value)
                register_value = self.update_register_value(operation, register_value, register_value)
                continue
            try:
                print("here", register)
                self.evaluate_register(another_register, self[another_register], seen_registers=seen_registers)
                # if self[register][0] == register_value:
                print("updating", register, register_value, "with", another_register, self[another_register][0])
                register_value = self.update_register_value(operation, register_value, self[another_register][0])
            except CalculatorException as e:
                print("could not find", another_register)
                return self.evaluate_register(register, self[register],register_value, seen_registers=seen_registers)
        print("end of")
        if register_value is None:
            raise CalculatorException(f"The value of register {register} cannot be resolved.")
        self[register] = [register_value]
        print(register, self[register])

    def update_register_value(self, operation, register_value, value):
        """Updates the given registry value based on the given operation and value"""
        if isinstance(value, str):
            value = convert_string_value_to_number(value)
        operations = {
            "add": lambda x, y: x + y if x is not None else y,
            "subtract": lambda x, y: x - y if x is not None else -y,
            "multiply": lambda x, y: x * y if x is not None else None
        }
        return operations[operation](register_value, value)

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
