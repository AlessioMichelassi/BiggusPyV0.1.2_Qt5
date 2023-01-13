import types


def create_function_from_string(function_string):
    exec(function_string)
    return locals()["my_function"]


def create_function_from_string2(name, function_string):
    function_code = f"{function_string}"
    function_globals = {}
    exec(function_code, function_globals)
    return function_globals[name]


function_string = "def my_function(arg1, arg2): return arg1 + arg2"
my_function = create_function_from_string(function_string)
print(my_function(1, 2))  # Output: 3

a = create_function_from_string2("my_function", function_string)
print(f"returnValue = {a(1, 2)}")  # Output: 3
