# Sectra Programming Assignment
#### By Sebastian Axell

## Overview
Care has been made to make methods, variables and classes as mnemonic as possible.
The code has also been commented throughout.

Exception handling is added throughout.

The test cases given in the assignments are used in testing but
no further tests has been written.

No non-standard libraries are used.

### Modes

This calculator application can run in two ways: 
- with file input
- without file input

### Implemented commands

When run with no input, an interactive commandline application is run. 
The following commands are implemented:
* _register_ _add_ _value_ - Adds specified value to the given register.
* _register_ _subtract_ _value_ - Subtract the specified value from the given register.
* _register_ _multiply_ _value_ - Multiplies the specified register value with the given value.
* print _register_ - Prints the given registers value.
* HELP - Displays help.
* QUIT - Terminates the program execution

The inputs are validated according to these rules:
- Has to be of this form: _register_ _operation_ _value_
- A _register_ name can only consist of alphanumeric characters.")
- A _value_: has to be alphanumeric or a numeric 
- Valid operations are: "add", "subtract","multiply", "print"

Invalid inputs are not evaluated but printed to the console.

**Note:** circular referencing is enabled meaning a given register can be used
in operation with itself like so : _a_ add _a_. If the value of _a_
cannot be resolved an error message will be displayed. 
### Assumptions
If the value of a register cannot be resolved, an error message is displayed.
However, the operations for that register is not cleared. This is in case
the user adds the required inputs later on. If you want to clear a register of
the list of operations that will be carried out on it, you need to use the 
clear _register_ command
\

No assumptions regarding number type is made:
both floats and integers are acceptable (mixed input will result in float result).

When there is file input, it is assumed it is in the same directory as that containing
the src module.

All inputs are case-insensitive.


## How to run
Navigate to the directory containing the src module.

### With file input
`python -m src.run FILE_NAME`

Examples
`python -m src.run FILE_NAME`

`python -m src.run FILE_NAME`

`python -m src.run FILE_NAME`

Note the file is assumed to be in the same directory as that containing 
the src module.

### Without file input

`python -m src.run`