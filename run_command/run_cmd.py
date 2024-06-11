import codecs
import io
import os
import shlex
import signal
import time
import psutil
import asyncio
import subprocess


# 关闭pid进程树
def terminate_process_tree(pid):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    # 关闭子进程
    for child in children:
        try:
            child.terminate()
        except psutil.NoSuchProcess:
            pass
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    for p in still_alive:
        p.kill()

    # 关闭父进程
    try:
        parent.terminate()
    except psutil.NoSuchProcess:
        pass
    gone, still_alive = psutil.wait_procs([parent], timeout=5)
    for p in still_alive:
        p.kill()


# RunCmd类保存了一些执行命令的函数
class RunCmd:
    def __init__(self):
        self.cmd = "ping -t 127.0.0.1"
        # self.cmd = "ping 127.0.0.1"
        self.time = 100
        # self.cmd = "echo '1111'"

    # 直接使用 os.system 函数来执行
    r"""
    官网链接：
    https://docs.python.org/3/library/os.html#os.system
    
    参数原型：
    os.system(*args, **kwargs)：
    返回值：命令的退出状态码， 0表示指令执行成功，1表示失败，256表示没有返回结果。
    
    运用场景：适用于哪些不需要输出内容的场景,但是会将命令执行的内容展示到终端上面。
    
    缺点: 无法实现超时停止
    """

    def run_cmd1(self):
        _p = os.system(self.cmd)
        print("return: ", _p)

    # 使用 os.popen 函数来执行,实际上也是调用了 subprocess.Popen 函数，但是输出默认是subprorcess.PIPE，且shell为true
    r"""
    官网链接：
    https://docs.python.org/3/library/os.html#os.popen
    
    参数原型：
    popen(cmd, mode="r", buffering=-1)
    cmd：命令行
    mode：可选r或w，其中r模式可从返回的文件对象中读取子进程的输出，w模式可向返回的文件对象写入数据，作为子进程的输入
    buffering：默认-1，即采用系统默认的缓冲模式,大小为8192（io.DEFAULT_BUFFER_SIZE）
    
    其他参数（均不可修改）：shell为True，text为True，输出为管道
    
    返回值：命令执行过程中的输出内容，可以使用read()、readlines()、readline()、readable()
    
    缺点: 无法实现超时停止，无法将输出保存到文件
    """

    def run_cmd2(self):
        _p = os.popen(self.cmd,
                      mode="r",
                      buffering=-1
                      )
        print("return: ", _p.read())

    # 使用 subprocess.Popen 函数来执行
    r"""
    官网链接：
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen
    
    参数原型：
    def __init__(self, args, bufsize=-1, executable=None,
                 stdin=None, stdout=None, stderr=None,
                 preexec_fn=None, close_fds=True,
                 shell=False, cwd=None, env=None, universal_newlines=None,
                 startupinfo=None, creationflags=0,
                 restore_signals=True, start_new_session=False,
                 pass_fds=(), *, user=None, group=None, extra_groups=None,
                 encoding=None, errors=None, text=None, umask=-1, pipesize=-1)
    args: 可以是列表，可以使用shlex.split(cmd)函数来对参数进行切割
    buffering：默认-1，即采用系统默认的缓冲模式,大小为8192（io.DEFAULT_BUFFER_SIZE）
    executable: 替换程序，再次启动当前的python解释器的推荐方法，并使用-m命令行格式来启动已经安装的模块
    stdin,stdout,stderr：输入、正常输出、错误输出
    shell：是否启动shell或者cmd，默认关闭，这意味着如果一些命令不符合要求的话，可能会报错.
        默认的话，可以使用grep、sed、awk等命令行工具
        shell = True, echo "000"
        shell = False, 对应的则是cmd.exe echo "000"
    cwd：设置工作目录
    env：设置环境变量，一般为PATH
    universal_newlines:各种换行符统一处理成"\n"
    text: 是否以字符串形式返回stdout和stderr，默认是字节形式
    
    Popen类中有几个允许与进程交互的方法
    返回值: poll、wait、communicate、send_signal、terminate、kill、stdin、stdout、stderr、pid、returncode
    
    运行场景：在新进程中执行子程序，这个可以作为监听程序，一旦主程序结束，这个子程序也会结束
    注意：一定要加上communicate啥的，不然只有popen函数会直接结束的。
    """

    def run_cmd3(self):
        timeout = 5
        try:
            _p = subprocess.Popen(self.cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True
                                  )
            try:
                # output, error = _p.communicate(timeout=timeout) 与进程交互
                # _p.wait(timeout=timeout) 等待子进程终止
                # 超时处理，在使用PIPE时，使用wait函数来等待子进程终止，会造成死锁，因此使用communicate函数更好
                output, error = _p.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                # _p.terminate() 尝试优雅地终止子进程，也可以两个都使用
                # _p.kill() 直接强制终止子进程
                _p.terminate()
                output, error = _p.communicate()
                print(f"Command timed out after {timeout} seconds")

            print("output: %s\n" % output)
            print("error: %s\n" % error)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    # 输入输出使用文件的形式
    r"""
    官网链接：
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen
    
    stdin、stderr、stdout可以为None、subprocess.PIPE、STDOUT、DEVNULL、以及文件描述符
    这里的stdout和stderr使用文件描述符来保存这些信息
    
    使用场景：保存到文件中，方便后期查看和信息提取
    """

    def run_cmd3_new(self):
        timeout = 5
        cwd = os.path.dirname(__file__)
        out_put = open(os.path.join(cwd, "out_put.txt"), "w")
        err_put = open(os.path.join(cwd, "err_put.txt"), "w")

        try:
            args = shlex.split(self.cmd)
            _p = subprocess.Popen(args,
                                  shell=False,
                                  stdout=out_put,
                                  stderr=err_put,
                                  text=True,
                                  cwd=cwd,
                                  )
            try:
                # output, error = _p.communicate(timeout=timeout) 与进程交互
                # _p.wait(timeout=timeout) 等待子进程终止
                # 超时处理，在使用PIPE时，使用wait函数来等待子进程终止，会造成死锁，因此使用communicate函数更好
                return_code = _p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # _p.terminate() 尝试优雅地终止子进程，也可以两个都使用
                # _p.kill() 直接强制终止子进程
                _p.terminate()
                return_code = _p.wait()
                print(f"Command timed out after {timeout} seconds")

            print("return code: %s\n" % return_code)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    # 使用 subprocess.call 函数来执行，实际也是调用了 subprocess.Popen 函数来执行
    r"""
    官网链接：
    https://docs.python.org/3/library/subprocess.html#subprocess.call
    
    参数原型：
    call(*popenargs, timeout=None, **kwargs)
    timeout:这里是超时时间
    其他参数均与subprocess.Popen函数一致
    
    返回值：
    0表示命令执行成功，其他的返回值则表示执行失败
    """

    def run_cmd4(self):
        timeout = 5
        try:
            _p = subprocess.call(self.cmd,
                                 timeout=timeout,
                                 text=True
                                 )
            print("return: ", _p)
        except subprocess.TimeoutExpired as e:
            # 超时时，output、stderr、stdout均为none
            print(f"Command timed out after {timeout} seconds: {e}")

    # 使用 exec 函数来执行python代码
    r"""
    官网链接：
    https://docs.python.org/3/library/functions.html#exec
    
    使用场景，exec函数可以间接执行命令行，但是无法直接执行.
    不推荐使用exec
    
    eval的返回值是计算结果
    官网链接：
    https://docs.python.org/3/library/functions.html#eval
    
    缺点: 无法实现超时停止
    """

    def run_cmd5(self):
        exec(f"os.system('{self.cmd}')")

        # exec的用法
        # exec("print('Hello, World!')")
        # exec("import os; os.system('ping 127.0.0.1')")

        # eval的用法
        # _p = eval(f"os.system('{self.cmd}')")
        # _p = eval("print('Hello, World!')")
        # result = eval("42")
        # print("result:", result)

    # 使用 subprocess.run 函数来执行，实际上也是 subprocess.Popen 函数来执行
    r"""
    官网链接：
    https://docs.python.org/3/library/subprocess.html#subprocess.run
    
    函数原型：
    run(*popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs)
    capture_output:为true时，则将普惠stdout，stderr。此时，stdout和stderr为PIPE
    其他参数均与subprocess.Popen函数一致
    
    返回参数：stdout、stderr、args、returncode
    """

    def run_cmd6(self):
        timeout = 5
        try:
            _p = subprocess.run(self.cmd,
                                capture_output=True,
                                timeout=timeout,
                                check=True,
                                text=True)

            print("output: %s\n" % _p.stdout)
            print("error: %s\n" % _p.stderr)
        except subprocess.TimeoutExpired as e:
            print(f"Command timed out after {timeout} seconds")
            if e.stdout:
                print("output: %s\n" % e.stdout)
                print("error: %s\n" % e.stderr)
        except subprocess.CalledProcessError as e:
            print("return code: ", e.returncode)
        except Exception as e:
            print(f"Error running command: {e.args}")

    # 使用 subprocess.check_call 函数来执行，调用了call函数，即调用了 subprocess.Popen 函数来执行
    # 会主动检查退出码，如果不为0，则抛出异常，不需要调用者手动检查退出码
    r"""
    函数原型：
    check_call(*popenargs, **kwargs)
    参数与call一致
    其他参数均与subprocess.Popen函数一致
    
    对应subprocess.call的封装，如果返回码不为0，则弹出CalledProcessError
    
    返回值：正常0或者CalledProcessError
    """

    def run_cmd7(self):
        timeout = 5
        try:
            _p = subprocess.check_call(self.cmd,
                                       timeout=timeout,
                                       text=True)
            print("return code：", _p)
        except subprocess.TimeoutExpired as e:
            # 超时时，output、stderr、stdout均为none
            print(f"Command timed out after {timeout} seconds")
            # 这个参数只有cmd和args
            print(e.cmd, e.args)
        except subprocess.CalledProcessError as e:
            print(f"return code :{e.returncode}")
        except Exception as e:
            print(f"Error running command: {e.args}")

    # 使用 subprocess.check_output 函数来执行，调用了run函数，即调用了 subprocess.Popen 函数来执行
    r"""
    网络链接：
    https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    
    函数原型：
    check_output(*popenargs, timeout=None, **kwargs)
    其他参数均与subprocess.Popen函数一致
    
    内容与subprocess.run一致，但是对返回的是stdout
    
    """

    def run_cmd8(self):
        timeout = 5
        try:
            _p = subprocess.check_output(self.cmd,
                                         timeout=timeout,
                                         text=True
                                         )
            print("output:", _p)
        except subprocess.TimeoutExpired as e:
            print(f"Command timed out after {timeout} seconds")
            print("output: ", e.output)
            # if e.stdout:
            #     print("output: %s\n" % e.stdout)
            #     print("error: %s\n" % e.stderr)
        except Exception as e:
            print(f"Error running command: {e.args}")

    # 使用 os.execv 函数来执行
    r"""
    函数原型：
    os.execv(path, args)
    
    函数功能：
    在python中执行一个新的程序，并且会替换当前的进程
    
    类似的函数还有
    os.execv, execve, execl, execle, execlp, execlpe, execvp, execvpe
    """

    def run_cmd9(self):
        os.execv('C:\\Windows\\System32\\cmd.exe', self.cmd.split(" "))

    # 使用 create_subprocess_shell 函数来执行命令
    """
    网络链接：
    https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.create_subprocess_shell
    
    函数原型：
    asyncio.create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None, limit=None, **kwds)
    limit: 设置stdout和stderr的缓冲区限制,默认是64k
    
    
    缺点：一旦发生超时时，无法保存stderr和stdout信息
    """

    def run_cmd10(self):
        try:
            loop = asyncio.get_event_loop()
            stdout, stderr = loop.run_until_complete(self.start_cmd10())
            print("output: %s\n" % stdout.decode('gbk', errors="ignore"))
            print("error: %s\n" % stderr.decode('gbk', errors="ignore"))
        except TimeoutError as e:
            print(f"Command '{e.args[0]}' timed out after {e.args[1]} seconds")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    async def start_cmd10(self):
        timeout = 5
        _p = await asyncio.create_subprocess_shell(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(_p.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            if _p.returncode is None:
                # os.killpg(_p.pid, signal.SIGTERM)
                terminate_process_tree(_p.pid)
            #     _p.terminate()
            #     await _p.wait()
            #     _p.kill()
            raise TimeoutError(self.cmd, timeout)
        return stdout, stderr

    # 使用 create_subprocess_shell 函数来执行命令，并使用文件来保存
    """
    网络链接：
    https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.create_subprocess_shell

    函数原型：
    asyncio.create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None, limit=None, **kwds)
    limit: 设置stdout和stderr的缓冲区限制,默认是64k


    缺点：一旦发生超时时，可以保存到文件中.
    注意：对于create_subprocess_shell函数创建的进程，pid属性是生成的shell的pid
    """

    def run_cmd11(self):
        try:
            loop = asyncio.get_event_loop()
            return_code = loop.run_until_complete(self.start_cmd11())
            print("return code: %s\n" % return_code)
            loop.close()
        except TimeoutError as e:
            print(f"Command '{e.args[0]}' timed out after {e.args[1]} seconds")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    # 关闭进程树
    async def start_cmd11(self):
        timeout = 5
        cwd = os.path.dirname(__file__)
        out_put = open(os.path.join(cwd, "out_put.txt"), "w")
        err_put = open(os.path.join(cwd, "err_put.txt"), "w")
        _p = await asyncio.create_subprocess_shell(
            self.cmd,
            stdout=out_put,
            stderr=err_put,
        )

        try:
            return_code = await asyncio.wait_for(_p.wait(), timeout=timeout)
            return return_code
        except asyncio.TimeoutError:
            if _p.returncode is None:
                terminate_process_tree(_p.pid)
            raise TimeoutError(self.cmd, timeout)

    # 使用 create_subprocess_exec 函数来执行命令
    """
    网络链接：
    https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.create_subprocess_exec
    
    函数原型：
    create_subprocess_exec(program, *args, stdin=None, stdout=None,
                                 stderr=None, loop=None,
                                 limit=streams._DEFAULT_LIMIT, **kwds)
    参数，cmd命令是*cmd.split(" ")
    limit: 设置stdout和stderr的缓冲区限制,默认是64k    
    
    
    """

    def run_cmd12(self):
        try:
            loop = asyncio.get_event_loop()
            stdout, stderr = loop.run_until_complete(self.start_cmd12())
            print("output: %s\n" % stdout)
            print("error: %s\n" % stderr)
        except TimeoutError as e:
            print(f"Command '{e.args[0]}' timed out after {e.args[1]} seconds")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    async def start_cmd12(self):
        timeout = 5
        _p = await asyncio.create_subprocess_exec(
            *self.cmd.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(_p.communicate(), timeout=timeout)
            # 使用replace或ignore来处理 UnicodeDecodeError 异常
            return stdout.decode("gbk", errors='replace'), stderr.decode("gbk", errors='replace')
        except asyncio.TimeoutError:
            if _p.returncode is None:
                # os.killpg(_p.pid, signal.SIGTERM)
                terminate_process_tree(_p.pid)

            raise TimeoutError(self.cmd, timeout)

    # 使用 create_subprocess_exec 函数来执行命令，并保存到文件中
    def run_cmd13(self):
        try:
            loop = asyncio.get_event_loop()
            return_code = loop.run_until_complete(self.start_cmd13())
            print("return code: %s\n" % return_code)
        except TimeoutError as e:
            print(f"Command '{e.args[0]}' timed out after {e.args[1]} seconds")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    async def start_cmd13(self):
        timeout = 5
        cwd = os.path.dirname(__file__)
        out_put = open(os.path.join(cwd, "out_put.txt"), "w")
        err_put = open(os.path.join(cwd, "err_put.txt"), "w")
        _p = await asyncio.create_subprocess_exec(
            *self.cmd.split(" "),
            stdout=out_put,
            stderr=err_put,
        )
        try:
            return_code = await asyncio.wait_for(_p.wait(), timeout=timeout)
            return return_code
        except asyncio.TimeoutError:
            if _p.returncode is None:
                # os.killpg(_p.pid, signal.SIGTERM)
                terminate_process_tree(_p.pid)
            raise TimeoutError(self.cmd, timeout)


r"""
实际上python执行命令的方法就以下几种：
1、subprocess.popen() 推荐
2、os.system() 推荐用于简单场景
3、exec()、eval() 但是不推荐
4、os.execv() 不推荐
5、create_subprocess_shell()
"""

if __name__ == "__main__":
    start_time = time.time()
    rc = RunCmd()
    # rc.run_cmd1() # os.system
    # rc.run_cmd2()  # os.popen
    # rc.run_cmd3()  # subprocess.Popen
    # rc.run_cmd3_new()  # subprocess.Popen
    # rc.run_cmd4()  # subprocess.call
    # rc.run_cmd5()  # exec
    # rc.run_cmd6()  # subprocess.run
    rc.run_cmd7()  # subprocess.check_call
    # rc.run_cmd8()  # subprocess.check_output
    # execv没啥用
    # rc.run_cmd9()  # os.execv
    # rc.run_cmd10()  # asyncio.create_subprocess_shell函数
    # rc.run_cmd11()  # asyncio.create_subprocess_shell函数，保存到文件
    # rc.run_cmd12()  # asyncio.create_subprocess_exec函数
    # rc.run_cmd13()  # asyncio.create_subprocess_exec函数，保存到文件

    print("exec time: %s" % str(time.time() - start_time))
    print("done.")

# 说明：

# os.popen 简单调用 subprocess.Popen

# subprocess.call 封装 subprocess.Popen
# subprocess.check_call 对 subprocess.call 进行检查

# subprocess.run 高级封装 subprocess.Popen （推荐）
# subprocess.check_output 对 subprocess.run 进行检查
