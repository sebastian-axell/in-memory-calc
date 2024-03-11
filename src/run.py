"""A calculator in the terminal."""
import sys

from .calculator import Calculator
from .command_parser import CommandException
from .command_parser import CommandParser

def command_line_application():
    print("""Hello and welcome to this commandline Sectra Calculator.
    Enter HELP for list of available commands or quit to terminate.""")
    calculator = Calculator()
    parser = CommandParser(calculator)
    while True:
        command = input("SectraCalc> ")
        if command.lower() == "quit":
            break
        try:
            parser.execute_command(command.split())
        except CommandException as e:
            print(e)
    print("The Sectra Calculator has now terminated its execution. "
          "Thank you and goodbye!")

def file_based_application(file):
    calculator = Calculator()
    parser = CommandParser(calculator)
    for command in f.readlines():
        command = command.strip()
        if command.lower() == "quit":
            break
        parser.execute_command(command.split())

if __name__ == "__main__":
    if len(sys.argv) == 1:
        command_line_application()
    elif len(sys.argv) == 2:
        file = sys.argv[1]
        try:
            f = open("./" + file, 'r')
            file_based_application(f)
            f.close()
        except FileNotFoundError as e:
            print(f"Unable to read {file}: ", e.args[1])
    else:
        print("Sorry this application can only take 1 or no arguments. Please try again.")
