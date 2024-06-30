import subprocess
import multiprocessing

"""
python执行命令的高级用法1：
python创建一个子进程来执行外部命令。主进程会正常退出，但是子进程会持续运行
"""


def run_backgroud_command():
    cmd = "ping -t 127.0.0.1 > advance1.txt"
    subprocess.Popen(cmd,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     shell=True)


def main():
    p = multiprocessing.Process(target=run_backgroud_command)
    p.start()
    print("python script started the background process and exited.")


if __name__ == "__main__":
    main()
    # 其他的任务
    print("done.")
