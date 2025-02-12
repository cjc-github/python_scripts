
import subprocess


# 使用gnome-terminal来调用一个新窗口来执行afl-fuzz,前提得是在终端输入，在vscode中会报错：
# Unable to init server: 无法连接： 拒绝连接
# 无法处理参数：无法打开显示：
def main1():
    command = 'gnome-terminal -t AFL-Fuzz -- bash -c "afl-fuzz -i in -o out -- ./fuzzgoat @@ ;exec bash"'
    _ = subprocess.Popen(command, shell=True)



def main2():
    cmd = "afl-fuzz -i in -o out -- ./fuzzgoat @@"
    
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        stdout, stderr = process.communicate()
        print(stdout.decode())
        print(stderr.decode())
    except KeyboardInterrupt:
        process.terminate()


if __name__ == "__main__":
    # main1()
    
    main2()
    

    