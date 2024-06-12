# 方法1，对应的是developer.py文件
# 将这个文件放到C:\Users\62600\AppData\Local\Programs\Python\Python38\Lib\site-packages目录下

# 方法2，对应的是developed.py文件
# 将这个文件放到C:\Users\62600\AppData\Local\Programs\Python\Python38\Lib\site-packages\xfuzz目录下.
# 此外，xfuzz目录还需要加上一个空的__init__.py文件才行。
# 确保每个目录都包含一个 __init__.py 文件，这样 Python 会将这些目录识别为包。

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b
