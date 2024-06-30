import time
import calendar
from datetime import datetime

# 1s = 10^3ms = 10^6μs = 10^9ns = 10^12ps
if __name__ == "__main__":
    a = time.time()
    print(a)
    # 结果展示，秒（秒后7位数）：1719723242.7938051

    a = int(time.time() * 1000)
    print(a)
    # 结果展示，毫秒：1719726989863

    a = time.time_ns()
    print(a)
    # 结果展示，纳秒：1719723277149794200

    a = time.time_ns() // (1000)
    print(a)
    # 结果展示，微妙：1719727020422290

    a = time.time_ns() // (1000 * 1000)
    print(a)
    # 结果展示，毫秒：1719726989863

    a = time.localtime()
    print(a)
    # time.struct_time(tm_year=2024, tm_mon=6, tm_mday=30, tm_hour=12, tm_min=57, tm_sec=43, tm_wday=6, tm_yday=182, tm_isdst=0)

    a = datetime.now()
    print(a)
    # 纳秒级别的时间：2024-06-30 13:50:04.223765

    a = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(a)
    # 毫秒级别的时间：2024-06-30 13:55:15:437

    a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(a)
    # 2024-06-30 13:22:37

    a = time.ctime(time.time())
    print(a)
    # Sun Jun 30 13:22:37 2024

    a = time.asctime()
    print(a)
    # Sun Jun 30 13:28:42 2024

    today = datetime.today()
    a = calendar.calendar(today.year)  # 记录一年
    # print(a)

    a = calendar.month(today.year, today.month)  # 当前月
    print(a)
