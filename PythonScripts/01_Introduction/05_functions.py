# basic function definition
def hello_world():
    print('hello world')
    print('I\'m a print statement inside the hello_world() function')

# calling the function will execute it
hello_world()
hello_world()

# function with inputs and return value
def sum(a, b):
    return a + b

print(sum(3, 7))
print(sum('hello', 'babe'))
# print(sum('hello', 7)) this will throw an error!

# same function with type annotation to increase readability and safety
def sum_of_floats(a: float, b: float) -> float:
    return a + b

print(sum_of_floats(10, 5))
# print(sum_of_floats('3', 5)) # -- this will throw an error