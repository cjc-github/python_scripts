# 一、 实现场景

## 1.1 针对于popen函数的readable()函数的实现场景

代码如下：

```python
import os
import time
import select


def monitor_pipe_output():
    try:
        # 打开管道
        proc = os.popen('some_command', 'r')

        # 读取管道输出
        while True:
            if proc.readable():
                output = proc.read()
                if output:
                    print(output.strip())
            else:
                # 如果没有数据可读,等待一段时间再检查
                time.sleep(0.1)

            # 检查进程是否已经结束
            if proc.close() is not None:
                break
    except OSError as e:
        print(f"Error executing command: {e}")


# may be use linux
# def monitor_pipe_output():
#     # 打开管道
#     pipe = os.popen('some_command', 'r')
#
#     while True:
#         # 检查管道是否可读
#         if pipe.readable():
#             # 从管道读取数据
#             output = pipe.read()
#             if output:
#                 # 处理读取到的数据
#                 print(output)
#         else:
#             # 如果没有数据可读,等待一段时间再检查
#             time.sleep(0.1)
#
#         # 等待管道可读
#         ready, _, _ = select.select([pipe], [], [], 1)
#         if not ready:
#             # 超时,继续下一轮循环
#             continue


if __name__ == '__main__':
    monitor_pipe_output()

```

## 1.2 针对subprocess.Popen函数中的超时以及打印

```python
import subprocess


def run_cmd3(cmd, timeout):
    try:
        _p = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True
                              )
        try:
            output, error = _p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            _p.terminate()
            output, error = _p.communicate()
            print(f"Command timed out after {timeout} seconds")

        print("output: %s\n" % output)
        print("error: %s\n" % error)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


# def run_cmd3(cmd, timeout):
#     try:
#         _p = subprocess.Popen(cmd,
#                               stdout=subprocess.PIPE,
#                               stderr=subprocess.PIPE,
#                               )
#         try:
#             _p.wait(timeout=timeout)
#         except subprocess.TimeoutExpired:
#             # 如果超时,终止进程
#             _p.terminate()
#             print(f"Command timed out after {timeout} seconds")
#             # 读取命令输出
#             output, error = _p.communicate()
#             print("output: %s\n" % output)
#             print("error: %s\n" % error)
#             return
#
#         # 读取命令输出
#         output, error = _p.communicate()
#         print("output: %s\n" % output)
#         print("error: %s\n" % error)
#     except subprocess.CalledProcessError as e:
#         print(f"Error executing command: {e}")


if __name__ == '__main__':
    cmd = "ping -t 120.0.0.1"
    timeout = 3
    run_cmd3(cmd, timeout)

```


test:
```
cur_dir = os.getcwd()
    dir = os.path.join(cur_dir, "test")
    os.makedirs(dir, exist_ok=True)

    file = os.path.join(dir, 'test.txt')
    with open(file, 'w') as f:
        f.write("This is a test file.")
    print("successfuly crated file and dir.")

```