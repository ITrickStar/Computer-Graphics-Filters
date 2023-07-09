def reverse(self, x):
    sgn = 1
    if (x < 0):
        sgn = -1
        x *= -1
    s = str(x)[::-1]
    res = int(s)*sgn
    if res < -2**31 or res >= 2**31:
        res = 0
    return res


if __name__ == "__main__":
    print(reverse(10))
