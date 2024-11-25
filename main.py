# main.py
import subprocess
import argparse


# 可以执行的command命令
command_convert_script = {
    'clear': 'utils/clear_typora_photo/clear_photo.py',
    'find': 'utils/find_files_with_keyword/find_files_with_keyword.py',
    'get_system': 'utils/get_os_info/get_os_info.py',
}

command_list = list(command_convert_script.keys())


# 运行python脚本
def run_script(script_name, args):
    try:
        cmd = ["python", script_name] + list(args)
        print("cmd", cmd)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[*] Error occurred while running {script_name}: {e}")


# 解析命令行参数
def parse_argument():
    parser = argparse.ArgumentParser(description="Run different scripts.")
    parser.add_argument('command', type=str, choices=command_list, nargs="?", help='Python files to run python scirpt')
    parser.add_argument('args', type=str, nargs=argparse.REMAINDER, help='Arguments for the python script')

    args = parser.parse_args()
    if not args.command:
        # raise ValueError("command不存在")
        print("[+] No command provided. Here is the help information:")
        parser.print_help()
        exit(1)
        
    return args


# main函数
if __name__ == "__main__":
    args = parse_argument()
    if args.command in command_convert_script:
        run_script(command_convert_script[args.command], args.args)
    else:
        print("[!] Unknown command. Use '-h' to choice comamnd option")