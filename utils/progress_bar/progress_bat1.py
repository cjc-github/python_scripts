import time

if __name__ == "__main__":
    scale = 50

    # 使用center来填充字符串左右
    print("执行开始".center(scale // 2, "-"))
    start = time.perf_counter()
    # 分成50等分
    for i in range(scale + 1):
        a = '*' * i  # *的个数，代表进度
        b = '.' * (scale - i)  # .的个数，代表剩余进度
        c = (i / scale) * 100  # 百分比
        dur = time.perf_counter() - start # 统计时间
        # \r将光标移到行首，以覆盖上一行的输出
        print("\r{:^3.0f}% [{}->{}] {:.2f}s".format(c, a, b, dur), end='')
        time.sleep(0.1)
    print("\n" + "执行结果".center(scale // 2, '-'))
