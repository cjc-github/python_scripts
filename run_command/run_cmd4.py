import os
import time
import psutil
import subprocess
from datetime import datetime


def execute_command(command, timeout=60, output_file='command_output.txt'):
    """
    执行命令并记录相关信息。

    参数:
    command (str): 要执行的命令
    timeout (int): 命令超时时间(秒)
    output_file (str): 输出文件路径

    返回:
    (bool, float, float, float): 是否超时, CPU使用率, 内存使用率, 执行时间
    """
    start_time = time.time()

    # 打开输出文件
    with open(output_file, "a") as output_file:
        # 执行命令并重定向输出到文件
        try:
            process = subprocess.Popen(command, stdout=output_file, stderr=output_file, universal_newlines=True,
                                       shell=True)
            process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # 如果命令执行超时,则杀掉进程树
            try:
                max_cpu_percent = 0
                max_mem_percent = 0
                for child in psutil.Process(process.pid).children(recursive=True):
                    try:
                        cpu_percent = child.cpu_percent(interval=0.1)
                        mem_percent = child.memory_percent()
                        max_cpu_percent = max(max_cpu_percent, cpu_percent)
                        max_mem_percent = max(max_mem_percent, mem_percent)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                for child in psutil.Process(process.pid).children(recursive=True):
                    child.kill()
                process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                max_cpu_percent = 0
                max_mem_percent = 0
            output_file.write(f"命令执行超时, 已杀掉进程树!\n")
            return True, max_cpu_percent, max_mem_percent, timeout
        except Exception as e:
            output_file.write(f"命令执行出错: {e}\n")
            return False, 0, 0, time.time() - start_time

        # 监控进程及其子进程的CPU和内存使用情况
        max_cpu_percent = 0
        max_mem_percent = 0
        for p in psutil.Process(process.pid).children(recursive=True):
            try:
                if p.is_running():
                    cpu_percent = p.cpu_percent(interval=0.1)
                    mem_percent = p.memory_percent()
                    max_cpu_percent = max(max_cpu_percent, cpu_percent)
                    max_mem_percent = max(max_mem_percent, mem_percent)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # 如果进程已经结束或没有访问权限,则跳过
                pass

        output_file.write(f"命令: {command}\n")
        output_file.write(f"执行时间: {time.time() - start_time:.2f}秒\n")
        output_file.write(f"CPU使用率: {max_cpu_percent:.2f}%\n")
        output_file.write(f"内存使用率: {max_mem_percent:.2f}%\n")

    return False, max_cpu_percent, max_mem_percent, time.time() - start_time


if __name__ == "__main__":
    # 示例用法
    # command = "python -c 'import time; print(\"Hello, World!\"); time.sleep(10)'"
    command = "ping -t 127.0.0.1"
    is_timeout, cpu_percent, mem_percent, exec_time = execute_command(command, timeout=5)
    print(
        f"是否超时: {is_timeout}, CPU使用率: {cpu_percent:.2f}%, 内存使用率: {mem_percent:.2f}%, 执行时间: {exec_time:.2f}秒")
