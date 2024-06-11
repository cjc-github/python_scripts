# coding=utf-8
import subprocess
import psutil
import time


# 返回类型
class CommandResult:
    def __init__(self, returncode, stdout, stderr, mem_usage, cpu_usage, execution_time):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.mem_usage = mem_usage
        self.cpu_usage = cpu_usage
        self.execution_time = execution_time


def run_cmd(args, mem=False, cpu=False, timeout=5, interval_time=1):
    start_time = time.time()
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    mem_usage = None
    cpu_usage = None

    while p.poll() is None:
        if mem:
            mem_usage = psutil.Process(p.pid).memory_info().rss
        if cpu:
            cpu_usage = psutil.Process(p.pid).cpu_percent(interval=interval_time)
        if time.time() - start_time > timeout:
            p.terminate()
            break
        time.sleep(interval_time)

    stdout, stderr = p.communicate()
    execution_time = time.time() - start_time

    return CommandResult(
        p.returncode,
        stdout.decode(encoding='gbk', errors='ignore').strip(),
        stderr.decode(encoding='gbk', errors='ignore').strip(),
        mem_usage,
        cpu_usage,
        execution_time
    )


if __name__ == "__main__":
    # cmd = "ping -t 127.0.0.1"
    cmd = "ping 127.0.0.1"
    timeout = 5
    interval_time = 1
    run_info = run_cmd(cmd, mem=True, cpu=True, timeout=timeout, interval_time=interval_time)
    print("output:", run_info.stdout)
    print("errput:", run_info.stderr)
    print("cpu:", run_info.cpu_usage)
    print("mem:", run_info.mem_usage)
    print("time:", run_info.execution_time)
