import time
from io import StringIO
from io import BytesIO


# 字符串的内存io和文件io的性能对比
class StringClass():
    def __init__(self, num):
        self.number = num

    def save_file(self):
        start_time = time.time()
        with open("file_string.txt", "w") as f:
            for i in range(self.number):
                f.write(f"id:{i} Hello world\n")
        end_time = time.time() - start_time
        print(end_time)

    def save_file_with_memory_io(self):
        start_time = time.time()
        s = StringIO()
        for i in range(self.number):
            s.write(f"id:{i} Hello world\n")
        end_time = time.time() - start_time
        print(end_time)


# 二进制数据的内存io和文件io的性能对比
class BytesClass():
    def __init__(self, num):
        self.number = num

    def save_file(self):
        start_time = time.time()
        with open("file_bytes.txt", "wb") as f:
            for i in range(self.number):
                f.write(f"id:{i} hello world\n".encode())
        end_time = time.time() - start_time
        print(end_time)

    def save_file_with_memory_io(self):
        start_time = time.time()
        s = BytesIO()
        for i in range(self.number):
            s.write(f"id:{i} hello world\n".encode())
        end_time = time.time() - start_time
        print(end_time)


if __name__ == "__main__":
    num = 1000
    stringio = StringClass(num)
    stringio.save_file_with_memory_io()
    stringio.save_file()

    bytesio = BytesClass(num)
    bytesio.save_file_with_memory_io()
    bytesio.save_file()
