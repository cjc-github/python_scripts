import os
import distro
import psutil
import platform
import argparse
import subprocess
import unicodedata


# key的长度
key_width = 15
# value的长度
value_width = 40
# 缩进
ident = 2 * " "
# 结果
report_dict = {}

title = "title"


# 格式化字典
def format_unicode_str(dic):
    # 计算最大键的长度
    def adjusted_length(str):
        return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str)
    
    max_key_length = max(adjusted_length(key) for key in dic.keys())
    
    for key, value in dic.items():
        if value == title:
            print("\n" + key)
        else:
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
        "操作系统:": title,
        "操作系统": platform.system(),
        "发行版本": f"{distro.name()} {distro.version()}",
        "计算机名称": platform.node(),
        "操作系统内核": platform.platform(),
        # "Python版本": platform.python_version(),
    }
    
    # 加入
    report_dict.update(os_info)
    


# 获取环境变量
def get_environ_info():
    print("环境变量:")
    format_unicode_str(os.environ)


# 获取系统信息
def get_system_info():
    system_dict = {}
    
    """获取内存并打印。"""
    # 获取内存信息
    memory_info = psutil.virtual_memory()  # 物理内存信息
    total_memory = memory_info.total  # 总内存
    used_memory = memory_info.used  # 已用内存
    memory_percentage = memory_info.percent  # 内存使用百分比

    system_dict["运行内存"] = f"{used_memory / (1024 ** 3):.2f} / {total_memory / (1024 ** 3):.2f} GB"
    system_dict["内存使用率"] = f"{memory_percentage}%"
    
    # 加入
    report_dict.update(system_dict)


    
# 获取磁盘信息
def get_disk_info():
    """打印当前主机上所有磁盘的信息。"""
    partitions = psutil.disk_partitions()
    
    # 用户跟踪已打印的设备, 去掉同一设备, 但挂载点不一样的设备
    seen_devices = set() 
    
    print("磁盘分区信息:")
    for partition in partitions:
        try:
            # 过滤掉 loop 设备, 在 linux 中常见
            if 'loop' in partition.device:
                continue
    
            # cdrom 一般在 windows 中常见
            if partition.opts == "cdrom":
                continue
            
            # 检查是否已经打印过该设备
            if partition.device in seen_devices:
                continue
            
            # 获取磁盘使用情况
            usage = psutil.disk_usage(partition.mountpoint)
            output = (
                f"设备: {partition.device} "
                f"{usage.used / (1024 ** 3):.2f} / {usage.total / (1024 ** 3):.2f} GB "
                f"使用率: {usage.percent}%"
            )
            seen_devices.add(partition.device)
            print(output)
        except Exception as e:
            print("[*] 分析失败", e)
        

# 获取cpu信息
def get_cpu_info():
    cpu_dict = {}
    # cpu_dict["处理器架构"] = platform.architecture()
    cpu_dict["CPU 架构"] = platform.processor()

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
        
        cpu_dict["CPU 型号"] = cpu_model

    except Exception as e:
        print(f"获取 CPU 信息失败: {e}")
        
    # 获取 CPU 信息
    cpu_count = psutil.cpu_count(logical=True)  # 逻辑 CPU 核心数
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU 使用率
    
    cpu_freq = psutil.cpu_freq(percpu=True)

    # 打印每个核心的频率
    for index, freq in enumerate(cpu_freq):
        print(f"核心 {index}: 当前频率: {freq.current} MHz, 最大频率: {freq.max} MHz, 最小频率: {freq.min} MHz")
        
        cpu_dict["逻辑 CPU 核心数"] = cpu_count
        cpu_dict["CPU 使用率"] = cpu_usage
        
    # 获取 CPU 的逻辑核心数量（线程数量）
    logical_cpu_count = psutil.cpu_count(logical=True)

    # 获取 CPU 的物理核心数量
    physical_cpu_count = psutil.cpu_count(logical=False)

    print(f"逻辑核心数量（线程数量）: {logical_cpu_count}")
    print(f"物理核心数量: {physical_cpu_count}")

    
    # 加入cpu信息
    report_dict.update(cpu_dict)
        
# 获取gpu信息
def get_gpu_info():
    gpu_info = {}
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
        
        gpu_info["GPU 型号"] = gpu_model
    except Exception as e:
        print(f"获取 GPU 信息失败: {e}")
    
    # 加入gpu信息
    report_dict.update(gpu_info)
        

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
    args = parse_argument()
    print(args)
    # 获取操作系统信息
    get_os_info()
    
    # 获取cpu信息
    get_cpu_info()
    
    # 获取gpu信息
    get_gpu_info()
    
    get_system_info()
    
    # 获取磁盘信息
    get_disk_info()
    
    # 获取主板信息
    get_motherboard_info()
    
    # 获取内存信息
    # get_memory_info()
    
    format_unicode_str(report_dict)


# 还需要封装输出
if __name__ == "__main__":
    main()