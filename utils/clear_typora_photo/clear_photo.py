import os
from pathlib import Path
import re
import argparse

r"""
清理 Typora 中多余的图片

图片设置：在 Typora 中，插入图像时，图片会被复制到 ./${filename}.assets 文件夹中。
功能：该功能需要识别给定目录中的 Markdown 文件，并根据这些文件的引用情况，删除未被引用的图片。
"""


def list_all_files(file_folder):
    """
    递归列出指定文件夹及其子文件夹下的所有文件。

    参数:
        file_folder (str): 目标文件夹的路径。

    返回:
        list: 包含目标文件夹及其所有子文件夹中所有文件的完整路径列表。
    """
    _files = []
    list_file = os.listdir(file_folder)
    for i in range(0, len(list_file)):
        path = os.path.join(file_folder, list_file[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def parser_argument():
    """
    解析命令行参数。

    如果提供了路径参数，则返回该路径；如果没有提供，则返回当前工作目录。

    返回:
        str: 文件地址，默认为当前工作目录。
    """
    parser = argparse.ArgumentParser(description="处理文件地址参数")
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='文件地址 (默认当前工作目录)')

    args = parser.parse_args()

    print("[+] 输入地址: ", args.path)
    if args.path != os.getcwd() and not os.path.exists(args.path):
        raise FileNotFoundError(f"[1]指定的路径不存在: {args.path}")
    else:
        args.path = os.path.abspath(args.path)
        print("[+] 转换为绝对路径：", args.path)
    return args.path


def extract_image_paths(md_file):
    """
    从 Markdown 文件中提取所有图片路径。

    参数:
        md_file (str): Markdown 文件的路径。

    返回:
        list: 包含所有图片路径的列表。
    """
    image_paths = []
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')  # 正则表达式匹配图片路径

    md_dir = os.path.dirname(md_file)

    try:
        with open(md_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # 查找所有匹配的图片路径
            paths = image_pattern.findall(content)
            for path in paths:
                # absolute_path = os.path.abspath(path)
                absolute_path = Path(os.path.join(md_dir, path))
                # absolute_path = os.path.abspath(Path(path).resolve())  # 转换为绝对路径
                image_paths.append(absolute_path)  # 转换为字符串并添加到列表
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

    return image_paths


def validate_typora_rule(image_list_in_file, image_list_in_dir):
    # 对比 .md 和 .assets 中的图片路径
    md_image_set = set(image_list_in_file)
    asset_image_set = set(image_list_in_dir)

    # 检查 .assets 中存在但 .md 中不存在的图片
    missing_in_md = asset_image_set - md_image_set
    for missing in missing_in_md:
        print(f"[!] Assets 中存在但 MD 中没有的文件: {missing}")

    # 检查 .md 中存在但 .assets 中不存在的图片
    missing_in_assets = md_image_set - asset_image_set
    if missing_in_assets:
        for missing in missing_in_assets:
            print(f"[*] MD 中存在但 Assets 中没有的文件: {missing}")
        print("[!] 规则出错")

    # 检查是否一致
    if not missing_in_md and not missing_in_assets:
        print("[+] Finish: MD 和 Assets 中的图片路径一致")


def get_target_info(dir_path):
    """
    验证 Typora 的文件规则，比较 .md 文件中的图片路径与 .assets 文件夹中的图片路径。

    参数:
        dir_path (str): 要检查的根目录路径。
    """
    file_lists = list_all_files(dir_path)
    for file_list in file_lists:
        # 找到md文件
        if file_list.endswith('.md'):
            print("[+] md文件: ", file_list)
            # md文件中的图片列表
            image_list_in_file = extract_image_paths(file_list)

            # 判断每个md文件
            image_folder = file_list.replace(".md", ".assets")

            # asset文件中的png
            image_list_in_dir = []
            if os.path.isdir(image_folder):
                image_list = os.listdir(image_folder)
                for image_name in image_list:
                    image_path = os.path.join(image_folder, image_name)
                    image_list_in_dir.append(Path(os.path.abspath(image_path)))

            # 验证typora规则
            validate_typora_rule(image_list_in_file, image_list_in_dir)


def main():
    # 解析参数
    dir_path = parser_argument()
    # 获取目标信息
    get_target_info(dir_path)


if __name__ == "__main__":
    main()
    print("done.")
