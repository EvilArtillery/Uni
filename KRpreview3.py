def LongestWord(line):
    lmax = 0
    imax = 0
    lst = list(line.split())
    for i in range(len(lst)):
        if len(lst[i]) > lmax:
            imax = i
            lmax = len(lst[i])
    return lst[imax]

print(LongestWord(input()))