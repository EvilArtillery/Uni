def recursive_summ(a, b):
    if b > 0:
        return recursive_summ(a + 1, b - 1)
    elif b < 0:
        return recursive_summ(a - 1, b + 1)
    else:
        return a


a = int(input())
b = int(input())
print(recursive_summ(a, b))
