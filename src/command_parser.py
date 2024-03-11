"""A class that parses incoming commands."""

import textwrap
import logging
import re

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
                self.calculator.evaluate_stack()
            except CalculatorException as e:
                raise CommandException(e.args[0])
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
            HELP - Displays help.
            QUIT - Terminates the program execution.
        """)
        print(help_text)