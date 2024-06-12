# coding=utf-8
import subprocess
import psutil
import time


# 返回类型，对执行命令行进行封装
class CommandResult:
    def __init__(self, returncode, stdout, stderr, mem_usage, cpu_usage, execution_time):
        self.returncode = returncode  # 命令返回值
        self.stdout = stdout  # 正常输出
        self.stderr = stderr  # 错误输出
        self.mem_usage = mem_usage  # 内存使用量
        self.cpu_usage = cpu_usage  # cpu使用量
        self.execution_time = execution_time  # 执行时间


def run_cmd(args, mem=False, cpu=False, timeout=5, interval_time=1):
    start_time = time.time()
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    memory_info_list, cpu_percent_list = [], []

    while p.poll() is None:
        if mem:
            # 每秒获取内存量
            mem_usage = psutil.Process(p.pid).memory_info().rss
            memory_info_list.append(mem_usage)
            print(f"mem_usage:{mem_usage}", end=" ")
        if cpu:
            # 每秒获取cpu
            cpu_usage = psutil.Process(p.pid).cpu_percent(interval=interval_time)
            cpu_percent_list.append(cpu_usage)
            print(f"cpu_usage:{cpu_usage}", end=" ")
        print(f"time_usage:{time.time() - start_time}")
        if time.time() - start_time > timeout:
            p.terminate()
            break
        # time.sleep(interval_time)

    stdout, stderr = p.communicate()
    execution_time = time.time() - start_time

    return CommandResult(
        p.returncode,
        stdout.decode(encoding='gbk', errors='ignore').strip(),
        stderr.decode(encoding='gbk', errors='ignore').strip(),
        sum(memory_info_list) / 1024 / 1024 / len(memory_info_list),  # 内存单位为MB
        sum(cpu_percent_list) / len(cpu_percent_list),  # cpu使用情况
        execution_time
    )


if __name__ == "__main__":
    cmd = "ping -t 127.0.0.1"
    # cmd = "ping 127.0.0.1"
    timeout = 5
    interval_time = 1
    run_info = run_cmd(cmd, mem=True, cpu=True, timeout=timeout, interval_time=interval_time)
    print("output:", run_info.stdout)
    print("errput:", run_info.stderr)
    print("cpu:", run_info.cpu_usage)
    print("mem:", run_info.mem_usage)
    print("time:", run_info.execution_time)
