# here's a print statement
print('hello world')

# printing variables
a = 1
b = 'some text'
print(a)
print(b)

# print multiple variables in one print statement
print(a, b)

# use f-strings to print
print(f'a: {a}, b: {b}')

# unreal logging
import unreal # import the unreal module before you call unreal.log(...)

unreal.log(f'unreal log: {b}')
unreal.log_warning(f'unreal log warning: {b}')
unreal.log_error(f'unreal log error: {b}')