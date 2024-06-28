import xfuzz
# 可以直接放在site-package，但是不能有xfuzz目录等。

if __name__ == "__main__":
    result = xfuzz.add(5, 3)
    print(result)  # Output: 8

    result = xfuzz.subtract(10, 4)
    print(result)  # Output: 6

    result = xfuzz.multiply(2, 7)
    print(result)  # Output: 14

    result = xfuzz.divide(15, 3)
    print(result)  # Output: 5.0
