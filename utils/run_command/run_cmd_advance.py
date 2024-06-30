# coding=utf-8
import os
import time
import shlex
import signal
import psutil
import subprocess

r"""
1、命令执行的信息保存到文件中，超时时需要将超时信息保存到文件中
2、记录命令执行时的cpu和内存量（进程以及子进程）
3、记录命令执行的时间（如果是超时的话，就是超时的时间）
4、超时时，需要kill掉进程树（进程以及子进程）
5、最好可以将命令执行的信息实时展示到终端

要求：
我想构建下面这个函数。
p=run_cmd(args, Mem=False, CPU=False, Timeout=5, interval_time=1,)
这个函数可以通过p.mem,p.cpu,p.time来获取具体的信息
"""


# 将log信息添加到文件中
def write2file(out_file, line):
    if os.path.exists(out_file):
        with open(out_file, "a") as f:
            f.write(line)


# 记录cpu、内存信息
def decord(p, timeout, interval_time):
    start_time = time.time()
    memory_info_list, cpu_percent_list = [], []
    avg_cpu_percent, avg_memory_info, max_memory_info, min_memory_info = 0, 0, 0, 0

    while True:
        # 如果返回值为0，则表示命令执行完毕
        if p.returncode is not None:
            break

        try:
            # 每隔1秒获取内存量
            memory_info = psutil.Process(p.pid).memory_info()
            memory_info_list.append(memory_info.rss / 1024 / 1024)
            print("memory:", memory_info.rss / 1024 / 1024)

            # 每隔1秒获取cpu
            cpu_percent = psutil.Process(p.pid).cpu_percent(interval=interval_time)
            cpu_percent_list.append(cpu_percent / psutil.cpu_count())
            print("cpu:", cpu_percent / psutil.cpu_count())
        except:
            pass
        finally:
            time.sleep(interval_time)

        # 一旦发生超时的cpu和内存信息
        if timeout and time.time() - start_time > timeout:
            avg_cpu_percent = sum(cpu_percent_list) / len(cpu_percent_list)
            avg_memory_info = sum(memory_info_list) / len(memory_info_list)
            max_memory_info = max(memory_info_list)
            min_memory_info = min(memory_info_list)

            if psutil.pid_exists(p.pid):
                try:
                    os.kill(p.pid, signal.SIGTERM)
                    raise
                except:
                    raise TimeoutError(cmd, timeout, avg_cpu_percent, avg_memory_info, max_memory_info, min_memory_info)
        time.sleep(0.1)

    # 正常运行的cpu和内存信息
    if len(cpu_percent_list) != 0:
        avg_cpu_percent = sum(cpu_percent_list) / len(cpu_percent_list)
    if len(memory_info_list) != 0:
        avg_memory_info = sum(memory_info_list) / len(memory_info_list)
        max_memory_info = max(memory_info_list)
        min_memory_info = min(memory_info_list)

    return [avg_cpu_percent, avg_memory_info, max_memory_info, min_memory_info, p.stdout]


# 具体执行命令
def run_cmd1(cmd, timeout=5, interval_time=1):
    cwd = os.path.dirname(__file__)
    out_put = os.path.join(cwd, "out_put.txt")
    err_put = os.path.join(cwd, "err_put.txt")

    _fout = open(out_put, "w")
    _ferr = open(err_put, "w")

    try:
        args = shlex.split(cmd)
        _p = subprocess.Popen(args,
                              text=True,
                              shell=False,
                              stdout=_fout,
                              stderr=_ferr,
                              cwd=cwd,
                              )
        info = decord(_p, timeout, interval_time)
        print("return info: ", info)
    except subprocess.TimeoutExpired as e:
        # 返回值：output、stderr、stdout、none
        timeout_log = f"Command timed out after {timeout} seconds"
        print(timeout_log)
        write2file(out_put, timeout_log)
    except subprocess.CalledProcessError as e:
        print(f"return code : {e.returncode}")
    except Exception as e:
        print(f"Error running command: {e.args}")


if __name__ == "__main__":
    cmd = "ping -t 127.0.0.1"
    # cmd = "ping 127.0.0.1"
    timeout = 5
    interval_time = 1
    run_info = run_cmd1(cmd, timeout, interval_time)
    print(run_info)
