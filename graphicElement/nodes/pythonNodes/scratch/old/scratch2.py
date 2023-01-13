import ast
import types


def create_function_from_string(function_string):
    function_name = "user_defined_function"
    exec(f"{function_name} = {function_string}")
    return locals()[function_name]


def create_function_from_string2(function_string):
    parsed_function = ast.parse(function_string).body[0]
    func_name = parsed_function.name
    func_args = [arg.arg for arg in parsed_function.args.args]
    func_body = parsed_function.body
    function = types.FunctionType(
        ast.Module(body=[parsed_function]).body[0],
        globals(),
        name=func_name,
        argdefs=[],
        closure=None
    )
    return function


# esempio di utilizzo
function_string = "def my_function(arg1, arg2):\n    return arg1 + arg2"
my_function = create_function_from_string(function_string)
print(my_function(1, 2))  # Output: 3


function_string2 = "def my_function(arg1, arg2):\n    return arg1 + arg2"
my_function2 = create_function_from_string2(function_string2)
print(my_function2(1, 2))  # Output: 3