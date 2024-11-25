import os
import time
import fcntl
import threading

# 时间间隔
time_interval = 1


def ensure_file_exists(filename):
    """确保文件存在，如果不存在则创建一个空文件。"""
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("hello world")  # 创建一个空文件

# 方法1, 大概率失败
def file_access1():
    # 写线程函数
    def write_data(filename):
        while True:
            with open(filename, "w") as f:
                f.write("hello world")

    # 读线程函数
    def read_data(filename):
        ensure_file_exists(filename)
        
        total_num, num, total_min = 0, 0, 0
        start_time = time.time()
        while True:
            with open(filename, "r") as f:
                lines = f.readlines()
                # 如果为0行
                if len(lines) == 0:
                    num += 1
                total_num += 1

            if int(time.time() - start_time) >= time_interval:
                total_min += 1
                percentage = (num / total_num) * 100 if total_num > 0 else 0

                print(
                    f"time: {total_min}, 读失败次数: {num}, 总执行次数: {total_num}, 失败百分比: {percentage:.2f}%"
                )
                start_time = time.time()  # 重置开始时间

    filename = "example.txt"

    write_thread = threading.Thread(target=write_data, args=(filename,))
    read_thread = threading.Thread(target=read_data, args=(filename,))

    write_thread.start()
    read_thread.start()

    write_thread.join()
    read_thread.join()


# 方法2，使用lock来保护文件
def file_access2():
    # 写线程函数
    def write_data(filename):
        while True:
            with lock:  # 加锁
                with open(filename, "w") as f:
                    f.write("hello world")

    # 读线程函数
    def read_data(filename):
        ensure_file_exists(filename)
        
        total_num, num, total_min = 0, 0, 0
        start_time = time.time()
        while True:
            with lock:
                with open(filename, "r") as f:
                    lines = f.readlines()
                    if len(lines) == 0:
                        num = num + 1
                    total_num += 1

                if int(time.time() - start_time) >= time_interval:
                    total_min += 1
                    percentage = (num / total_num) * 100 if total_num > 0 else 0

                    print(
                        f"time: {total_min}, 读失败次数: {num}, 总执行次数: {total_num}, 失败百分比: {percentage:.2f}%"
                    )
                    start_time = time.time()  # 重置开始时间

    # 定义线程锁, 从而实现读失败为0
    lock = threading.Lock()
    filename = "example.txt"

    write_thread = threading.Thread(target=write_data, args=(filename,))
    read_thread = threading.Thread(target=read_data, args=(filename,))

    write_thread.start()
    read_thread.start()

    write_thread.join()
    read_thread.join()


# 使用fcntl来锁文件
def file_access3():
    # 写线程函数
    def write_data(filename):
        while True:
            with open(filename, "w") as f:
                # 锁定文件以进行写入
                fcntl.flock(f, fcntl.LOCK_EX)  # 锁定文件以进行写入

                try:
                    f.write("hello world")
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)  # 解锁文件

    # 读线程函数
    def read_data(filename):
        ensure_file_exists(filename)
        
        total_num, num, total_min = 0, 0, 0
        start_time = time.time()
        while True:
            with open(filename, "r") as f:
                fcntl.flock(f, fcntl.LOCK_SH)  # 加共享锁以进行读取
                lines = f.readlines()
                if len(lines) == 0:
                    num += 1
                total_num += 1
                fcntl.flock(f, fcntl.LOCK_UN)  # 解锁文件

            if int(time.time() - start_time) >= time_interval:
                total_min += 1
                percentage = (num / total_num) * 100 if total_num > 0 else 0

                print(
                    f"time: {total_min}, 读失败次数: {num}, 总执行次数: {total_num}, 失败百分比: {percentage:.2f}%"
                )
                start_time = time.time()  # 重置开始时间

    filename = "example.txt"

    write_thread = threading.Thread(target=write_data, args=(filename,))
    read_thread = threading.Thread(target=read_data, args=(filename,))

    write_thread.start()
    read_thread.start()

    write_thread.join()
    read_thread.join()


# 使用临时文件来保存数据
def file_access4():
    # 写线程函数
    def write_data(filename):
        while True:
            with open("tmp.txt", "w") as f:
                f.write("hello world")
            os.rename("tmp.txt", filename)
            # os.replace("tmp.txt", filename)

    # 读线程函数
    def read_data(filename):
        ensure_file_exists(filename)
        
        total_num, num, total_min = 0, 0, 0
        start_time = time.time()
        while True:
            with open(filename, "r") as f:
                lines = f.readlines()
                if len(lines) == 0:
                    num += 1
                total_num += 1

            if int(time.time() - start_time) >= time_interval:
                total_min += 1
                percentage = (num / total_num) * 100 if total_num > 0 else 0

                print(
                    f"time: {total_min}, 读失败次数: {num}, 总执行次数: {total_num}, 失败百分比: {percentage:.2f}%"
                )
                start_time = time.time()  # 重置开始时间

    filename = "example.txt"

    write_thread = threading.Thread(target=write_data, args=(filename,))
    read_thread = threading.Thread(target=read_data, args=(filename,))

    write_thread.start()
    read_thread.start()

    write_thread.join()
    read_thread.join()


def main():
    print("[+] 方法一, 不进行任何处理")  # 失败78%
    # file_access1()

    print("[+] 方法二, 使用lock来防止")  # 失败0%
    # file_access2()

    print("[+] 方法三, 使用fcntl来防止")  # 失败78%
    file_access3()

    print("[+] 方法四, 使用临时文件来防止")  # 失败0%
    # file_access4()

    """
    file_access1() 最简单的读和写分开 读的时候会存在为空的情况
    file_access2() 使用threading.lock来实现互斥 读的时候不会为空
    file_access3() 使用fcntl来在写的时候加锁 读的时候会存在为空的情况
    file_access4() 使用临时文件来保存数据 读的时候不会为空
    
    在实际应用场景中, 更推荐使用临时文件来保存数据
    """


if __name__ == "__main__":
    main()
