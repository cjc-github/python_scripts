# from xfuzz.math_utils import add, subtract, multiply, divide
from xfuzz import math_utils

if __name__ == "__main__":
    result = math_utils.add(5, 3)
    print(result)  # Output: 8

    result = math_utils.subtract(10, 4)
    print(result)  # Output: 6

    result = math_utils.multiply(2, 7)
    print(result)  # Output: 14

    result = math_utils.divide(15, 3)
    print(result)  # Output: 5.0
