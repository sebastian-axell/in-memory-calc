"""A calculator in the terminal."""
from .calculator import Calculator
from .command_parser import CommandException
from .command_parser import CommandParser


if __name__ == "__main__":
    print("""Hello and welcome to this Sectra Calculator.
    Enter HELP for list of available commands or quit to terminate.""")
    calculator = Calculator()
    parser = CommandParser(calculator)
    while True:
        command = input("SectraCalc> ")
        try:
            return_code = parser.execute_command(command.split())
            if return_code == 0:
                break
        except CommandException as e:
            print(e)
    print("The Sectra Calculator has now terminated its execution. "
          "Thank you and goodbye!")