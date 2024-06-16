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

    # 执行命令并获取输出
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                   shell=True)

        # 监控进程及其子进程的CPU和内存使用情况
        max_cpu_percent = 0
        max_mem_percent = 0
        while process.poll() is None:
            try:
                cpu_percent = sum(
                    p.cpu_percent(interval=0.1) for p in psutil.Process(process.pid).children(recursive=True))
                mem_percent = psutil.Process(process.pid).memory_percent()
                max_cpu_percent = max(max_cpu_percent, cpu_percent)
                max_mem_percent = max(max_mem_percent, mem_percent)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # 如果进程已经结束或没有访问权限,则跳过
                pass

            # 实时输出到终端
            print(f"CPU使用率: {max_cpu_percent:.2f}%, 内存使用率: {max_mem_percent:.2f}%", end="\r")

            # 检查是否超时
            if time.time() - start_time > timeout:
                # 如果超时, 杀掉进程树
                try:
                    for child in psutil.Process(process.pid).children(recursive=True):
                        child.kill()
                    process.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # 如果进程已经结束或没有访问权限,则跳过
                    pass
                print(f"命令执行超时, 已杀掉进程树!")
                with open(output_file, "a") as f:
                    f.write(f"命令执行超时, 已杀掉进程树!\n")
                return True, max_cpu_percent, max_mem_percent, timeout

        stdout, stderr = process.communicate()

    except Exception as e:
        print(f"命令执行出错: {e}")
        with open(output_file, "a") as f:
            f.write(f"命令执行出错: {e}\n")
        return False, 0, 0, time.time() - start_time

    # 将输出写入文件
    with open(output_file, "a") as f:
        f.write(f"命令: {command}\n")
        f.write(f"执行时间: {time.time() - start_time:.2f}秒\n")
        f.write(f"CPU使用率: {max_cpu_percent:.2f}%\n")
        f.write(f"内存使用率: {max_mem_percent:.2f}%\n")
        f.write(f"标准输出:\n{stdout}\n")
        f.write(f"标准错误:\n{stderr}\n")
        f.write("-" * 80 + "\n")

    return False, max_cpu_percent, max_mem_percent, time.time() - start_time


if __name__ == "__main__":
    # 示例用法
    # command = "python -c 'import time; print(\"Hello, World!\"); time.sleep(120)'"
    command = "ping -t 127.0.0.1"
    is_timeout, cpu_percent, mem_percent, exec_time = execute_command(command, timeout=5)
    print(
        f"是否超时: {is_timeout}, CPU使用率: {cpu_percent:.2f}%, 内存使用率: {mem_percent:.2f}%, 执行时间: {exec_time:.2f}秒")
