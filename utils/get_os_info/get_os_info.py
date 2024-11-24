import os
import psutil
import platform
import argparse
import subprocess
import unicodedata


key_width = 15
value_width = 40
ident = 2 * " "


# 格式化字典
def format_unicode_str(dic):
    # 计算最大键的长度
    def adjusted_length(str):
        return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str)
    
    max_key_length = max(adjusted_length(key) for key in dic.keys())
    
    for key, value in dic.items():
        print(ident, key, " " * (max_key_length - adjusted_length(key)), " : ", value)


# 判断当前操作系统
def get_os_identifier():
    os_name = platform.system()
    
    if os_name == "Windows":
        return 0
    elif os_name == "Linux":
        return 1
    elif os_name == "Darwin":
        return 2
    else:
        return -1


# 获取操作信息信息
def get_os_info():
    os_info = {
        "系统名称": platform.system(),
        "系统版本": platform.version(),
        "系统版本号": platform.release(),
        "平台信息": platform.platform(),
        "计算机名称": platform.node(),
        "Python版本": platform.python_version(),
    }

    print("操作系统信息:")
    format_unicode_str(os_info)

    print("环境变量:")
    format_unicode_str(os.environ)


# 获取系统信息
def get_system_info():
    """获取 CPU、内存和磁盘信息并打印。"""

    # 获取 CPU 信息
    cpu_count = psutil.cpu_count(logical=True)  # 逻辑 CPU 核心数
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU 使用率

    # 获取内存信息
    memory_info = psutil.virtual_memory()  # 物理内存信息
    total_memory = memory_info.total  # 总内存
    used_memory = memory_info.used  # 已用内存
    memory_percentage = memory_info.percent  # 内存使用百分比

    # # 获取磁盘信息
    # disk_usage = psutil.disk_usage('/')  # 磁盘使用情况
    # total_disk = disk_usage.total  # 总磁盘空间
    # used_disk = disk_usage.used  # 已用磁盘空间
    # disk_percentage = disk_usage.percent  # 磁盘使用百分比

    # 打印信息
    print("系统信息:")
    print(f"逻辑 CPU 核心数: {cpu_count}")
    print(f"CPU 使用率: {cpu_usage}%")
    # print(f"总内存: {total_memory / (1024 ** 3):.2f} GB")
    # print(f"已用内存: {used_memory / (1024 ** 3):.2f} GB")
    # print(f"内存使用率: {memory_percentage}%")
    
    # print(f"总磁盘空间: {total_disk / (1024 ** 3):.2f} GB")
    # print(f"已用磁盘空间: {used_disk / (1024 ** 3):.2f} GB")
    # print(f"磁盘使用率: {disk_percentage}%")
    
    output = (
        f"运行内存: {used_memory / (1024 ** 3):.2f} / {total_memory / (1024 ** 3):.2f} GB "
        f"内存使用率: {memory_percentage}%"
    )
    print(output)
    
    
# 获取磁盘信息
def get_disk_info():
    """打印当前主机上所有磁盘的信息。"""
    partitions = psutil.disk_partitions()
    
    print("磁盘分区信息:")
    for partition in partitions:
        try:
            if partition.opts != "cdrom":
                # 获取磁盘使用情况
                usage = psutil.disk_usage(partition.mountpoint)
                output = (
                    f"设备: {partition.device} "
                    f"{usage.used / (1024 ** 3):.2f} / {usage.total / (1024 ** 3):.2f} GB "
                    f"使用率: {usage.percent}%"
                )
                print(output)
            
            # print(f"设备: {partition.device}")
            # print(f"挂载点: {partition.mountpoint}")
            # print(f"文件系统类型: {partition.fstype}")
            # print(f"选项: {partition.opts}")
            # if partition.opts != "cdrom":
            #     # 获取磁盘使用情况
            #     usage = psutil.disk_usage(partition.mountpoint)
            #     print(f"  总空间: {usage.total / (1024 ** 3):.2f} GB")
            #     print(f"  已用空间: {usage.used / (1024 ** 3):.2f} GB")
            #     print(f"  可用空间: {usage.free / (1024 ** 3):.2f} GB")
            #     print(f"  使用率: {usage.percent}%\n")
        except Exception as e:
            print("[*] 分析失败", e)
        

# 获取cpu信息
def get_cpu_info():
    cpu_arch = platform.architecture()
    print(f"处理器架构: {platform.architecture()}")
    cpu_info = platform.processor()  # 获取 CPU 处理器信息
    print(f"CPU 型号: {cpu_info}")
    
    # 使用 subprocess 获取更详细的 CPU 信息
    try:
        if platform.system() == "Windows":
            # Windows
            command = "wmic cpu get name"
            cpu_model = subprocess.check_output(command, shell=True).decode().strip().split('\n')[1]
        elif platform.system() == "Linux":
            # Linux
            command = "cat /proc/cpuinfo | grep 'model name' | uniq"
            cpu_model = subprocess.check_output(command, shell=True).decode().strip().split(': ')[1]
        elif platform.system() == "Darwin":
            # macOS
            command = "sysctl -n machdep.cpu.brand_string"
            cpu_model = subprocess.check_output(command, shell=True).decode().strip()
        else:
            cpu_model = "不支持的操作系统"
        
        print(f"CPU 型号 (subprocess): {cpu_model}")
    except Exception as e:
        print(f"获取 CPU 信息失败: {e}")
        
        
# 获取gpu信息
def get_gpu_info():
    try:
        if platform.system() == "Windows":
            # Windows
            command = "wmic path win32_VideoController get name"
            gpu_model = subprocess.check_output(command, shell=True).decode().strip().split('\n')[1]
        elif platform.system() == "Linux":
            # Linux
            command = "lspci | grep -i vga"
            gpu_model = subprocess.check_output(command, shell=True).decode().strip()
        elif platform.system() == "Darwin":
            # macOS
            command = "system_profiler SPDisplaysDataType | grep 'Chipset Model'"
            gpu_model = subprocess.check_output(command, shell=True).decode().strip().split(': ')[1]
        else:
            gpu_model = "不支持的操作系统"
        
        print(f"GPU 型号: {gpu_model}")
    except Exception as e:
        print(f"获取 GPU 信息失败: {e}")
        

# 获取主板信息
def get_motherboard_info():
    """获取主板信息，支持 Windows 和 Linux。"""
    os_type = platform.system()

    if os_type == "Windows":
        try:
            command = "wmic baseboard get product, manufacturer, version, serialnumber"
            output = subprocess.check_output(command, shell=True).decode().strip().split('\n')[1:]
            for line in output:
                if line.strip():
                    print(f"主板信息: {line.strip()}")
        except Exception as e:
            print(f"获取主板信息失败: {e}")
    elif os_type == "Linux":
        try:
            command = "sudo dmidecode -t baseboard"
            output = subprocess.check_output(command, shell=True).decode().strip().split('\n')
            print(f"主板信息: {output}")
        except Exception as e:
            print(f"获取主板信息失败: {e}")
    else:
        print("[*]不支持的操作系统，无法获取主板信息。")
    
    
# 获取内存信息
def get_memory_info():
    os_type = platform.system()

    if os_type == "Windows":
        try:
            command = "wmic memorychip get manufacturer, capacity, speed, memorytype, partnumber"
            output = subprocess.check_output(command, shell=True).decode().strip().split('\n')[1:]
            memory_info = [line.strip() for line in output if line.strip()]
            print(f"内存信息: {memory_info}")
        except Exception as e:
            print(f"获取内存信息失败: {e}")
    elif os_type == "Linux":
        try:
            command = "sudo dmidecode -t memory"
            output = subprocess.check_output(command, shell=True).decode().strip().split('\n')
            print(f"内存信息: {output}")
        except Exception as e:
            print(f"获取内存信息失败: {e}")
    else:
        print("[*] 不支持的操作系统，无法获取内存信息。")


# 创建命令行解析器
def parse_argument():
    parser = argparse.ArgumentParser(description='处理数据的程序')
    
    # 添加命令行参数
    parser.add_argument('-d', '--detailed', action='store_true', help='开启详细模式')
    parser.add_argument('-s', '--save', action='store_true', help='保存到文件')

    # 解析参数
    args = parser.parse_args()
    return args


# main()函数
def main():
    # args = parse_argument()
    # print(args)
    get_os_info()
    
    


r"""
简短的电脑环境
设备名称：
操作信息：
处理器:
主板：
内存：型号+内存大小
显卡：
显示器：
磁盘:型号+磁盘大小

声卡:

网卡:

"""

r"""

完整的电脑环境:
简短的电脑环境
设备名称：
操作信息：
处理器:型号+使用占比
主板：
内存:型号+内存大小+使用占比
显卡：
显示器：

磁盘:型号+磁盘大小+使用占比

声卡:

网卡:

环境变量：
"""

# 还需要封装输出

if __name__ == "__main__":
    main()
    
    # # get_os_info()
    # # # 获取cpu信息
    # # get_cpu_info()
    # # # 获取gpu信息
    # # get_gpu_info()
    # # get_system_info()
    # # # 获取磁盘信息
    # # get_disk_info()
    # # 获取主板信息
    # # get_motherboard_info()
    # # 获取内存信息
    # get_memory_info()
    
    
    
r"""
# 保存时间：

计算机
    操作系统：
    操作系统版本：
    计算机名称：

处理器

主板
    主板名称

内存


显卡


磁盘


显示屏


声卡


网卡：


"""