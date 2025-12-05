from random import randint


def Task1(lst):
    s = lst[0] + lst[1]
    j = 0
    for index in range(len(lst) - 1):
        if lst[index + 1] + lst[index] <= s:
            s = lst[index + 1] + lst[index]
            j = index
    return j, j + 1


def test_Task1():
    if Task1([4, 3, 2, 1]) == (2, 3):
        print('+')
    else:
        print("\033[91mERROR\033[0m", f"Answer is {Task1([4, 3, 2, 1])} instead of (2, 3).")
    if Task1([0, 0, 1, 1, 2, 2, -1, 3, -3, 4]) == (7, 8):
        print('+')
    else:
        print("\033[91mERROR\033[0m", f"Answer is {Task1([0, 0, 1, 1, 2, 2, -1, 3, -3, 4])} instead of (7, 8).")
    if Task1([0, 0, 0, 0, 0]) == (3, 4):
        print('+')
    else:
        print("\033[91mERROR\033[0m", f"Answer is {Task1([0, 0, 0, 0, 0])} instead of (3, 4).")
    if Task1([0, 0, 1, 2, 3, 4, 5]) == (0, 1):
        print('+')
    else:
        print("\033[91mERROR\033[0m", f"Answer is {Task1([0, 0, 1, 2, 3, 4, 5])} instead of (0, 1).")
    if Task1([1, 2]) == (0, 1):
        print('+')
    else:
        print("\033[91mERROR\033[0m", f"Answer is {Task1([1, 2])} instead of (0, 1).")


n = int(input())
A = [0] * n
a, b = map(int, input().split())
for i in range(n):
    A[i] = randint(a, b)

x = Task1(A)
print(x)
print(A)
print(Task1([0, 1, 2, -2]))
test_Task1()
