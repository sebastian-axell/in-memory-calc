"""A calculator class."""
import re

from .operation import Operation, OperationException, mathematical_operations


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
        return self.registers.get(register.lower(), [])

    def __setitem__(self, register, value):
        if isinstance(value, int):
            self.registers[register.lower()]=value
        else:
            if register in self:
                self.registers[register].append(value)
            else:
                self.registers[register] = list()
                self.registers[register].append(value)

    # def __setitem__(self, register, value):
    #     self.registers[register.lower()] = value

    def register_register(self, register, operation, value):
        if register in self:
            self[register].append(Operation(register, operation, value))
        else:
            self[register] = list()
            self[register].append(Operation(register, operation, value))

    def add_value_to_register(self, register, value):
        self[register] += value

    def subtract_value_from_register(self, register, value):
        self[register] -= value

    def multiply_register_with_value(self, register,value):
        self[register] *= value


            # if value_is_register(value) and value not in self:
            #     raise CalculatorException(f"{value} is not registered as a register. "
            #                               f"Please add a value to the register before using.")
    def add_operation(self, register, operation: str, value):
        try:
            self.stack.append(Operation(register, operation, value))
        except OperationException as e:
            raise CalculatorException(e.args[0])

    def add_print_operation(self, register: str):
        # if register.lower() not in self:
        #     raise CalculatorException(f"Register {register} is not valid. Please add a value to the register before printing.")
        self.add_operation(register, "print", "0")

    def evaluate_registers(self):
        print(self.registers)
        for register, eval_list in self.registers.items():
            # sorted_evaluations = sorted(eval_list, key=lambda operation: mathematical_operations.index(operation.operation))
            # print(sorted_evaluations)
            val = 0
            for operation in eval_list:
                value = operation.value
                operation = operation.operation
                if operation == "add":
                    val += value
                elif operation == "subtract":
                    val -= value
                elif operation == "multiply":
                    val *= value
            self[register] = val
    def determine_register_value(self, register, list_of_operations, register_value=0):
        print("determining", register)
        for operation in list_of_operations:
            print("operation: ", operation)
            value = operation.value
            if value_is_numeric(value):
                print(f"{register} is {value}")
                if operation.operation == "add":
                    register_value += int(value)
                    if isinstance(self[register], list):
                        self[register] = int(value)
                    else:
                        self[register] += int(value)
                elif operation.operation == "subtract":
                    register_value -= int(value)
                    if isinstance(self[register], list):
                        self[register] = - int(value)
                    else:
                        self[register] -= int(value)
                elif operation.operation == "multiply":
                    if isinstance(self[register], list):
                        print("Cannot multiply undefined register - skipping")
                    if register_value == 0:
                        print("woah, cannot determine that value hermano")
                    else:
                        self[register] *= int(value)
                        register_value *= int(value)
            elif value_is_register(value):
                self.determine_register_value(value, self[value], 0)
                if not self[value]:
                    raise CalculatorException(f"The value of register {value} cannot be resolved.")
                if isinstance(self[register], list):
                    if operation.operation == "add":
                        self[register] = self[value]
                    elif operation.operation == "subtract":
                        self[register] = -self[value]
                else:
                    if operation.operation == "add":
                        self[register] += self[value]
                    elif operation.operation == "subtract":
                        self[register] -= self[value]
                print("register", self[register])

                # if self[value] != "NaN":
                #     print(f"{register} depends on {value} which is {self[value]}")
                #     if list_of_operations[1:]:
                #         print(f"continuing to process remainder of {register}'s ops: ")
                #         self.determine_register_value(register, list_of_operations[1:])
                #         if operation.operation == "add":
                #             self[register] += self[value]
                #         elif operation.operation == "subtract":
                #             self[register] = self[value]
                #         elif operation.operation == "multiply":
                #             self[register] = self[value]
                #         return self[register]
                #     else:
                #         if operation.operation == "add":
                #             self[register] = self[value]
                #         elif operation.operation == "subtract":
                #             self[register] = -self[value]
                #         return self[register]
                # else:
                #  raise CalculatorException(f"The value of register {value} cannot be resolved.")
        print("print regiester alue", register_value)
        print("end of operations for", register)
        return "NaN"


    def evaluate_register(self, register):
        if isinstance(self[register], int):
            return self[register]
        else:
            try:
                print(self.determine_register_value(register, self[register]))
            except CalculatorException as e:
                print(f"When trying to evaluate the value of register {register} the following error occured: {e.args[0]}")
            print(self.registers)
            # self[register]= value_returned

    def evaluate_stack(self):
        # self.evaluate_registers()
        for operation in self.stack:
            if operation.operation == "print":
                try:
                    value = self.evaluate_register(operation.register)
                except CalculatorException as e:
                    print(e.args[0])
            else:
                self[operation.register.lower()]=operation
            # self.run_operation(operation)

    def run_operation(self, operation: Operation):
        register = operation.register
        value = operation.value
        operation = operation.operation
        # here keep a list of each register's operations
        all_operations = dict()
        all_operations[register] = [operation, value]
        # if print() -> evaluate_register(all_operations[register], all_operations)
        value = self[value] if value_is_register(value) else int(value)
        if operation == "add":
            self.add_value_to_register(register, value)
        elif operation == "subtract":
            self.subtract_value_from_register(register, value)
        elif operation == "multiply":
            self.multiply_register_with_value(register, value)
        elif operation == "print":
            print(self[register])
