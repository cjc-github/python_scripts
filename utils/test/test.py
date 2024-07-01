import time
import threading

class Test:
    def __init__(self):
        self.count = 0
        self.stop_flag = False

    def run(self):
        while not self.stop_flag:
            self.count += 1
            time.sleep(0.5)

    def print_count(self):
        while not self.stop_flag:
            print(f"Count: {self.count}")
            time.sleep(1)

if __name__ == "__main__":
    test = Test()

    # 创建并启动两个线程,不要加括号
    t1 = threading.Thread(target=test.run)
    t2 = threading.Thread(target=test.print_count)

    t1.start()
    t2.start()

    # 等待两个线程结束
    t1.join()
    t2.join()