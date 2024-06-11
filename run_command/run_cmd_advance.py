# coding=utf-8

import os
import signal
import subprocess
import time
import shlex

import psutil

"""
1???????????
2????????????????????????
3?????????????
4?????????cpu??????
5??????????????kill?
5?????????????????kill?
"""

# ?????????
# p=run_cmd(cpu=True,mem=True,time=True,timtout=True,interval_time=True,)
# ????p.cpu,p.out,p.error,p.mem???

# ??? log ??????
def write2file(out_file, line):
    if os.path.exists(out_file):
        with open(out_file, "a") as f:
            f.write(line)


# ?? cpu ??????
def decord(p, timeout, interval_time):
    start_time = time.time()
    memory_info_list, cpu_percent_list = [], []
    avg_cpu_percent, avg_memory_info, max_memory_info, min_memory_info = 0, 0, 0, 0

    while True:
        # ????????????
        if p.returncode is not None:
            break

        try:
            # ??1?????
            memory_info = psutil.Process(p.pid).memory_info()
            memory_info_list.append(memory_info.rss / 1024 / 1024)
            print("memory:", memory_info.rss / 1024 / 1024)

            # ??1???cpu
            cpu_percent = psutil.Process(p.pid).cpu_percent(interval=interval_time)
            cpu_percent_list.append(cpu_percent / psutil.cpu_count())
            print("cpu:", cpu_percent / psutil.cpu_count())
        except:
            pass
        finally:
            time.sleep(interval_time)

        # ????
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

    # ????????
    if len(cpu_percent_list) != 0:
        avg_cpu_percent = sum(cpu_percent_list) / len(cpu_percent_list)
    if len(memory_info_list) != 0:
        avg_memory_info = sum(memory_info_list) / len(memory_info_list)
        max_memory_info = max(memory_info_list)
        min_memory_info = min(memory_info_list)

    return [avg_cpu_percent, avg_memory_info, max_memory_info, min_memory_info, p.stdout]


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
        # ????output?stderr?stdout??none
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
