import functools

def create_function_from_string(function_string):
    exec(function_string)
    return locals()['my_function']

my_function_string = "def my_function(arg1, arg2): return arg1 + arg2"
my_function = create_function_from_string(my_function_string)
print(my_function(1, 2)) # output: 3

