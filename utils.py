


def norm(v1, v2):
    size = len(v1)
    n = 0
    temp = 0
    while n < size:
        temp += (abs(v1[n] - v2[n]))**2
        n += 1
    return temp**(1/2)
