import os
import subprocess
import sys
import time


def process_directory(base_path):
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    log_entries = []
    for entry in os.listdir(base_path):
        entry_path = os.path.join(base_path, entry)

        # 检查是否为文件夹且以 .m3u8 结尾
        if os.path.isdir(entry_path) and entry.endswith('.m3u8'):
            print("entry:", entry_path)

            output_file = os.path.join(entry_path, 'output.mp4')
            index_file = os.path.join(entry_path, 'index.m3u8')
            video_dir = os.path.join(entry_path, 'video')

            # 如果存在output.mp4文件
            if os.path.exists(output_file):
                log_entries.append(f"{entry}: 已存在")
                continue

            if os.path.exists(index_file):
                # if os.path.exists(video_dir):
                #     # 没有下载完成
                #     log_entries.append(f"{entry}: 未下载完成")
                # else:
                # 存在video视频并不是没有下载完成
                try:
                    # 进入目标目录
                    os.chdir(entry_path)

                    # 下载完成，且未处理执行 ffmpeg 命令
                    # ffmpeg_command = f"ffmpeg.exe -i index.m3u8 -c copy {output_file}"
                    ffmpeg_command = f"ffmpeg.exe -i index.m3u8 -c copy \"{output_file}\""
                    subprocess.run(ffmpeg_command, shell=True)
                    # subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.DEVNULL)

                    log_entries.append(f"{entry}: 转换成功")
                except Exception as e:
                    print("[!]", entry, "执行异常", e)
            else:
                log_entries.append(f"{entry}: 文件异常")

    print("finish.")

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
    process_directory(directory_path)
