# 使用文档

## 功能描述
clear_photo.py 是一个用于清理 Typora Markdown 文件中未被引用图片的脚本。
在 Typora 编辑器中，插入图片时会自动将图片复制到 ${filename}.assets 文件夹。随着文档编辑，部分图片可能被删除或替换，导致 .assets 文件夹中存在未被 Markdown 文件引用的冗余图片。
本脚本会自动扫描指定目录下所有 Markdown 文件，分析每个 .md 文件实际引用的图片，并删除其 .assets 文件夹中未被引用的图片，保持图片文件夹整洁。

## 使用文档

1. 依赖环境
Python 3.x
需要 basic_logger.py 日志模块（已在脚本中引用）
推荐在 Linux 或 Windows 下运行

2. 命令行参数
path：可选，要扫描的目标目录，默认为当前工作目录。
-s 或 --save-log：可选，保存执行日志到文件。

3. 运行方式

直接运行

```bash
python clear_photo.py [path] [-s]
```


示例1：扫描当前目录

```bash
python clear_photo.py
```

示例2：扫描指定目录并保存日志
```bash
python clear_photo.py /your/markdown/dir -s
```


打包为可执行文件

Windows:

```bash
pyinstaller.exe --onefile --paths ../logging_module clear_photo.py
```

Linux:

```bash
pyinstaller --onefile --paths ../logging_module clear_photo.py
```


4. 日志说明
脚本会输出详细的处理日志，包括每个 Markdown 文件的处理进度、被删除的图片等。
若加 -s 参数，日志会保存到文件。

5. 注意事项
删除操作不可恢复，请提前备份重要数据。
仅会处理 .md 文件及其同名 .assets 文件夹。


pyinstaller --onefile --paths ../logging_module clear_photo.py