def signum_partition(lst):
    for i in range(len(lst)):
        if lst[i] > 0:
            mem = lst[i]
            j = i-1
            while j >= 0 >= lst[j]:
                lst[j+1] = lst[j]
                j -= 1
            lst[j+1] = mem
        elif lst[i] < 0:
            j = i+1
            mem = lst[i]
            while j <= len(lst) and lst[j] >= 0:
                lst[j-1] = lst[j]
                j += 1
            lst[j-1] = mem