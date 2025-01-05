def paginator(lst_numbers, n):
    lst = []
    for i in range(0, len(lst_numbers), n):
        lst.append(lst_numbers[i: i + n])
    return lst


lts = (paginator([1, 2, 3, 4, 5, 6, 7, 8, 9, ], 2))
print(len(lts))
while True:
    a = input('Enter a number: ')
    print(lts[int(a) - 1])
