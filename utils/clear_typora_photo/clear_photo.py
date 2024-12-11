import os
import re
import sys
import logging
import argparse

from pathlib import Path

# 将 logging_module 的路径添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../logging_module')))

from basic_logger import setup_logging


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
    for root, _, files in os.walk(file_folder):
        for file in files:
            _files.append(os.path.join(root, file))
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
    # add the save log
    parser.add_argument('-s', '--save-log', type=str, choices=['true', 'false'], default='false', help='保存执行日志 (默认: true)')
    args = parser.parse_args()
    
    # 增加日志模块
    import logging
    logging = setup_logging(save_log=args.save_log, log_level=logging.INFO)


    logging.info(f"[+] args:{args}")

    logging.info(f"[+] 输入地址:{args.path}")
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"[*] 指定的路径不存在: {args.path}")
    args.path = os.path.abspath(args.path)
    logging.info(f"[+] 转换为绝对路径：{args.path}")
    return args


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
                absolute_path = Path(os.path.join(md_dir, path)).resolve()  # 转换为绝对路径
                image_paths.append(absolute_path)
    except Exception as e:
        logging.error(f"[!] 读取文件时发生错误: {e}")

    return image_paths


def validate_typora_rule(image_list_in_file, image_list_in_dir):
    """
    验证 Typora 的文件规则，比较 .md 文件中的图片路径与 .assets 文件夹中的图片路径。

    参数:
        image_list_in_file (list): .md 文件中提取的图片路径列表。
        image_list_in_dir (list): .assets 文件夹中的图片路径列表。
    """
    md_image_set = set(image_list_in_file)
    asset_image_set = set(image_list_in_dir)

    # 检查 .assets 中存在但 .md 中不存在的图片
    missing_in_md = asset_image_set - md_image_set
    for missing in missing_in_md:
        logging.error(f"[!] Assets 中存在但 MD 中没有的文件: {missing}")
        os.remove(missing)
        logging.info("[+] 删除: ", missing)

    # 检查 .md 中存在但 .assets 中不存在的图片
    missing_in_assets = md_image_set - asset_image_set
    if missing_in_assets:
        for missing in missing_in_assets:
            logging.warning(f"[*] MD 中存在但 Assets 中没有的文件: {missing}")
        logging.error("[!] typora 规则出错")

    # 检查是否一致
    if not missing_in_md and not missing_in_assets and len(md_image_set) > 0:
        logging.info("[+] Finish: MD 和 Assets 中的图片路径一致")


# 获取md文件中的图片列表和assets中的图片列表
def obtain_tuple(md_file_path):
    # md文件中的图片列表
    image_list_in_file = extract_image_paths(md_file_path)

    # 生成对应的 .assets 文件夹路径
    image_folder = md_file_path.replace(".md", ".assets")

    # asset文件中的图片列表
    image_list_in_dir = []
    if os.path.isdir(image_folder):
        image_list = os.listdir(image_folder)
        for image_name in image_list:
            image_path = os.path.join(image_folder, image_name)
            image_list_in_dir.append(Path(os.path.abspath(image_path)))

    return image_list_in_file, image_list_in_dir


def get_target_info(dir_path):
    """
    验证 Typora 的文件规则，比较 .md 文件中的图片路径与 .assets 文件夹中的图片路径。

    参数:
        dir_path (str): 要检查的根目录路径。
    """
    num = 0
    file_lists = list_all_files(dir_path)
    for file_list in file_lists:
        # 找到 .md 文件
        if file_list.endswith('.md'):
            num += 1
            logging.info(f"[+] num: {num} md文件: {file_list}")
            image_list_in_file, image_list_in_dir = obtain_tuple(file_list)
            # 验证 Typora 规则
            validate_typora_rule(image_list_in_file, image_list_in_dir)


def main():
    # 解析命令行参数
    args = parser_argument()
    # 获取目标信息
    get_target_info(args.path)


if __name__ == "__main__":
    # windows
    # C:\Users\62600\AppData\Local\Programs\Python\Python39\Scripts\pyinstaller.exe - F clear_photo.py
    # 需要将C:\Users\62600\AppData\Local\Programs\Python\Python39\Scripts目录加入到path中
    # linux
    # pyinstaller -F clear_photo.py
    main()
    logging.info("done.")
