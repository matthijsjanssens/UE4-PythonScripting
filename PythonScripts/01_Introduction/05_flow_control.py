# if statement example 01
if True:
    print('true')
else:
    print('not true')

# if elif else example
list_of_letters = ['a', 'b', 'c']

if 'd' in list_of_letters:
    print('d was found')
elif 'b' in list_of_letters:
    print('b was found')
else:
    print(list_of_letters)

# for loop examples
print('for loop 01')
for i in [0, 1, 2, 3, 4]:
    print(i)

print('\nfor loop 02')
for i in range(5):
    if i == 0:
        continue
    if i > 2:
        break
    print(i)

# while loop example
print('\nwhile loop')
count = 5
while(count != 0):
    print(count)
    count -= 1