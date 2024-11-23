import os
import argparse

r"""
在指定文件类型的文件中搜索关键字的功能

功能：
该功能需要识别给定目录中的文本文件，并根据文本文件的内容，来搜索文本文件中是否存在关键字。
"""

# 支持的类型
support_type = [".txt", ".md", ".csv", ".log", ".rtf", ".tex",
                ".py", ".js", ".java", ".rs", ".go", ".c", ".cpp", ".cc", ".h",
                ".smali", ".jawa", ".jimple",
                ".html", ".css",
                ".json", ".yaml", ".yml", ".ini", ".xml",
                ".doc", ".docx"]


def list_all_files(file_folder):
    """
    递归列出指定文件夹及其子文件夹下的所有文件。

    参数:
        file_folder (str): 目标文件夹的路径。

    返回:
        list: 包含目标文件夹及其所有子文件夹中所有文件的完整路径列表。
    """
    _files = []
    for root, _, files in os.walk(file_folder):
        for file in files:
            _files.append(os.path.join(root, file))
    return _files


def search_keyword(file_path, keyword):
    """
    在指定的文件中搜索给定的关键字。

    参数：
    file_path (str): 要搜索的文件的路径。
    keyword (str): 要查找的关键字。

    返回：
    bool: 如果在文件中找到关键字，则返回 True；否则返回 False。

    该函数首先尝试以 UTF-8 编码打开文件并搜索关键字。如果在使用 UTF-8 编码时出现
    UnicodeDecodeError，则会尝试以 GBK 编码重新打开文件进行搜索。如果在打开文件
    时发生其他异常，将打印错误信息并返回 False。
    """
    def read_file_with_encoding(filepath, encoding):
        """
        以指定编码读取文件并检查关键字。

        参数：
        filepath (str): 要读取的文件路径。
        encoding (str): 用于打开文件的编码格式。

        返回：
        bool: 如果在文件中找到关键字，则返回 True；否则返回 False。
        """
        with open(filepath, "r", encoding=encoding) as f:
            lines = f.readlines()
            for line in lines:
                if keyword in line:
                    return True
        return False

    # 尝试使用 UTF-8 编码
    try:
        return read_file_with_encoding(file_path, "utf-8")
    except UnicodeDecodeError:
        # 如果 UTF-8 编码失败，尝试使用 GBK 编码
        return read_file_with_encoding(file_path, "gbk")
    except Exception as e:
        print(f"[*] 打开文件失败 {e}")
        return False


def get_target_file(args):
    """
    获取目标文件

    参数:
        args : 命令行参数。
    """
    num = 0
    file_lists = list_all_files(args.path)
    for file_list in file_lists:
        for i in args.filetype:
            if file_list.lower().endswith(i):
                # 符合条件的文件
                num += 1
                # print(f"[+] num: {num} md文件: {file_list}")
                if search_keyword(file_list, args.keyword):
                    print(f"[+] 满足的md文件: {file_list}")


def parser_argument():
    """
    解析命令行参数。

    如果提供了路径参数，则返回该路径；如果没有提供，则返回当前工作目录。

    返回:
        str: 文件地址，默认为当前工作目录。
    """

    parser = argparse.ArgumentParser(description="处理文件地址参数")
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='文件地址 (默认当前工作目录)')
    parser.add_argument('-f', '--filetype', type=str, help='文件类型 (例如: .txt, .py)')
    parser.add_argument('-k', '--keyword', type=str, help='查找的关键字')
    args = parser.parse_args()

    # 待处理地址
    print("[+] 输入地址:", args.path)
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"[*] 指定的路径不存在: {args.path}")

    args.path = os.path.abspath(args.path)
    print("[+] 转换为绝对路径：", args.path)

    # 待处理的文件类型
    if not args.filetype or args.filetype not in support_type:
        print("[+] 采用所有的文件类型")
        args.filetype = support_type
    else:
        args.filetype = [args.filetype]

    # 待查找的关键字
    if not args.keyword:
        raise FileNotFoundError(f"[*] 待查找的关键字不存在: {args.keyword}")

    print("[+] args: ", args)
    return args


def main():
    # 解析命令行参数
    args = parser_argument()
    get_target_file(args)


if __name__ == "__main__":
    main()
    print("done.")
