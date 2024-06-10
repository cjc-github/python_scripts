import subprocess


if __name__ =="__main__":
    # 使用字符串作为标准输入
    p = subprocess.Popen(['python', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    p.stdin.write('print("Hello, World!")\n')
    p.stdin.flush()
    output, error = p.communicate()
    print(output)

    # 使用文件作为标准输入
    with open('input.txt', 'r') as f:
        p = subprocess.Popen(['wc', '-l'], stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        print(output.decode().strip())