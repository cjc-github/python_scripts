import os
import time
from contextlib import closing

file_name = "output.txt"
content = """这是文件的内容,非常非常长长长长长长长长长长长长长长长长长长长长长
长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长。\n"""

"""
方法1：（一般）
使用closing来确保数据会最后一次性完整地写入到文件中
只有with结束的时候，所有的数据才会一次性地完整地写入到文件中。
缺点：只有写入完成的时候，文件才不为空
"""


def save_file1():
    with closing(open(file_name, "w", encoding="utf-8")) as f:
        for _ in range(5):
            f.write(content)
            time.sleep(1)
    print("done.")


"""
方法2：（不推荐）
使用buffering实现将每次write函数写入的信息刷新到缓冲区，确保了每次write的内容完整
缺点：访问该文件时，依然存在为空的情况
"""


def save_file2():
    with open(file_name, "w", encoding="utf-8", buffering=1) as f:
        for _ in range(5):
            f.write(content)
            time.sleep(1)


"""
方法3：可以
先将所有的内容都写入到临时文件，然后改名，确保访问该文件时内容完整
"""


def save_file3():
    with open("tmp.txt", "w", encoding="utf-8", buffering=1) as f:
        for _ in range(5):
            f.write(content)
            # time.sleep(1)
    if os.path.exists(file_name):
        os.remove(file_name)
    os.rename("tmp.txt", file_name)


"""
方法4：可以(推荐)
将所有的内容写入到变量中，最后一次性将内容写入到文件中
缺点：占用内存来存储
"""


def save_file4():
    data = ""
    for _ in range(5):
        data += content
        # time.sleep(1)
    with open(file_name, "w", encoding="utf-8", buffering=1) as f:
        f.write(data)


"""
方法5：可以
先将所有的内容都写入到临时文件，然后替换，确保访问该文件时内容完整
"""


def save_file5():
    with open("tmp.txt", "w", encoding="utf-8", buffering=1) as f:
        for _ in range(5):
            f.write(content)
            # time.sleep(1)
    os.replace("tmp.txt", file_name)


def save_pre():
    if os.path.exists(file_name):
        os.remove(file_name)


if __name__ == "__main__":
    save_pre()
    # save_file1()
    # save_file2()
    # save_file3()

    # start_time = time.time()
    # for _ in range(100000):
    #     save_file3()
    # end_time = time.time()
    # print("time:", end_time - start_time)

    # start_time = time.time()
    # for _ in range(100000):
    #     save_file4()
    # end_time = time.time()
    # print("time:", end_time - start_time)

    start_time = time.time()
    for _ in range(100000):
        save_file5()
    end_time = time.time()
    print("time:", end_time - start_time)
