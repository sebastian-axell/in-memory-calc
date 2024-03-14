"""A class that parses incoming commands."""

import textwrap
import logging
import re

from .ExecutionTree import ExecutionTree
from .calculator import Calculator, CalculatorException, value_is_numeric

logging.basicConfig(level=logging.INFO)
from typing import Sequence


class CommandException(Exception):
    """A class used to represent a wrong command exception."""
    pass

def valid_register_name(input_string):
    """Checks if the register name is alphanumeric"""
    return bool(re.match(r'^[a-zA-Z0-9]+$', input_string))

class CommandParser:
    """A class used to parse and execute user commands."""

    def __init__(self, calculator: Calculator):
        self.calculator = calculator
        self.allowed_operations = ["add", "subtract","multiply", "print"]
        self.root_execution_tree = ExecutionTree("Root")

    def parse_and_validate_command(self, command):
        """Validates and parses a given command"""
        try:
            register, operation, value = command
            if not valid_register_name(register):
                raise CommandException("A register name can only consist of alphanumeric characters.")
            if not (value_is_numeric(value) or valid_register_name(value)):
                raise CommandException(f"{value} is an invalid value: has to be alphanumeric or a numeric")
            if operation.lower() not in self.allowed_operations:
                raise CommandException(f"Invalid operation. Valid operations are: {self.allowed_operations}")
            self.calculator.add_operation(register, operation, value)
        except ValueError as e:
            raise CommandException("Please enter a valid command, type HELP for a list of "
            "available commands")
        except CalculatorException as e:
            raise CommandException(e.args[0])

    def execute_command(self, command: Sequence[str]):
        """Parses and executes command if valid"""
        if not command:
            raise CommandException(
                "Please enter a valid command, "
                "type HELP for a list of available commands.")
        operation = command[0].lower()
        if operation == "print":
            if len(command) != 2:
                raise CommandException("Please enter print command followed by a register.")
            try:
                self.calculator.add_print_operation(command[1])
                self.root_execution_tree = ExecutionTree("Root")
                self.calculator.evaluate_stack(self.root_execution_tree)
            except CalculatorException as e:
                raise CommandException(e.args[0])
        elif operation == "show":
            if len(command) != 2:
                raise CommandException("Please enter show followed by a register")
            if not valid_register_name(command[1]):
                raise CommandException("Please enter show followed by a valid register name")
            self.calculator.show_register(command[1])
        elif operation == "list":
            self.calculator.show_all_registers()
        elif operation == "reset":
            if len(command) != 2:
                raise CommandException("Please enter clear followed by a register")
            self.calculator.reset_register_value(command[1])
        elif operation == "restart":
            self.calculator.reset()
        elif operation == "clear":
            if len(command) != 2:
                raise CommandException("Please enter clear followed by a register")
            self.calculator.clear_register_operations(command[1])
            print("Cleared register", command[1])
        elif operation == "display":
            if len(self.root_execution_tree.children) > 0:
                self.root_execution_tree.display()
            else:
                raise CommandException("No execution to show.")
        elif operation == "help":
            self._get_help()
        else:
            self.parse_and_validate_command(command)

    def _get_help(self):
        """Displays all the implemented commands."""
        help_text = textwrap.dedent("""
        Calculator commands need to be in <register> <operation> <value> format. Available commands:
            <register> <add> <value> - Adds specified value to the given register.
            <register> <subtract> <value> - Subtract the specified value from the given register.
            <register> <multiply> <value> - Multiplies the specified register value with the given value.
        Other commands:
            print <register> - Prints the given registers value.
            show <register> - Shows added operations for a given registry
            list - Shows all the registry values or their store of operations
            clear <register> - Removes all operations for that register
            restart - Resets the calculator.
            reset <register> - Removes the current evaluated value of a given register, if any
            HELP - Displays help.
            QUIT - Terminates the program execution.
        """)
        print(help_text)