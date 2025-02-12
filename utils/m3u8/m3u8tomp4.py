import os
import sys
import time
import shutil
import subprocess


# 删除m3u8
def remove_m3u8(base_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    count = 0

    log_entries = []
    for entry in os.listdir(base_path):
        entry_path = os.path.join(base_path, entry)

        # 检查是否为文件夹且以 .m3u8 结尾
        if os.path.isdir(entry_path) and entry.endswith('.m3u8'):
            print("entry:", entry_path)
            # 删除 index 文件夹及其内容
            index_dir = os.path.join(entry_path, 'index')
            if os.path.isdir(index_dir):
                print(f"Deleting directory: {index_dir}")
                shutil.rmtree(index_dir)  # 删除文件夹及其所有内容

            # 删除 hls.cfg 文件
            hls_cfg = os.path.join(entry_path, 'hls.cfg')
            if os.path.isfile(hls_cfg):
                print(f"Deleting file: {hls_cfg}")
                os.remove(hls_cfg)  # 删除文件

            # 删除 index.m3u8 文件
            index_m3u8 = os.path.join(entry_path, 'index.m3u8')
            if os.path.isfile(index_m3u8):
                print(f"Deleting file: {index_m3u8}")
                os.remove(index_m3u8)  # 删除文件
                
                
def process_directory(base_path):
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    count = 0

    log_entries = []
    for entry in os.listdir(base_path):
        entry_path = os.path.join(base_path, entry)

        # 检查是否为文件夹且以 .m3u8 结尾
        if os.path.isdir(entry_path) and entry.endswith('.m3u8'):
            # print("entry:", entry_path)
            count += 1

            output_file = os.path.join(entry_path, 'output.mp4')
            index_file = os.path.join(entry_path, 'index.m3u8')
            video_dir = os.path.join(entry_path, 'video')
            index = os.path.join(entry_path, 'index')

            # 如果存在output.mp4文件
            if os.path.exists(output_file):
                log_entries.append(f"{entry}: 已存在")

                continue

            if os.path.exists(index_file):
                # if not (os.path.exists(video_dir) and os.path.exists(index)):
                # 存在video视频并不是没有下载完成
                try:
                    # 进入目标目录
                    os.chdir(entry_path)

                    # 下载完成，且未处理执行 ffmpeg 命令
                    # ffmpeg_command = f"ffmpeg.exe -i index.m3u8 -c copy {output_file}"
                    # ffmpeg_command = f"ffmpeg.exe -i index.m3u8 -c copy \"{output_file}\""
                    ffmpeg_command = f"ffmpeg.exe -allowed_extensions ALL -i index.m3u8 -c copy \"{output_file}\""
                    subprocess.run(ffmpeg_command, shell=True)

                    log_entries.append(f"{entry}: 转换成功")
                except Exception as e:
                    print("[!]", entry, "执行异常", e)
            else:
                log_entries.append(f"{entry}: 文件异常")

    print("finish.", count)

    # 写入日志文件
    timestamp = int(time.time())
    log_file = os.path.join(script_dir, f"report_{timestamp}.log")  # 使用当前脚本目录
    # log_file = f"report_{timestamp}.log"
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            for log in log_entries:
                f.write(log + '\n')
    except Exception as e:
        print(f"Failed to write log file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    # 转换
    process_directory(directory_path)
    # 删除m3u8等文件
    remove_m3u8(directory_path)
