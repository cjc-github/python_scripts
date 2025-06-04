# pyscripts

some python scripts


## 依赖:

python版本：

python 3.8.10 - python 3.10.12


```shell
pip install psutil==5.9.8

# 安装pyinstaller
pip install pyinstaller

```


pyinstaller可能遇见的问题

```bash
# 直接运行pyinstaller命令，可能会出现下面错误：
pyinstaller: command not found

# 方法1、使用python来间接调用pyinstaller模块
python3 -m PyInstaller

# 方法2、确定pyinstaller安装目录，然后将路径添加到PATH环境变量中
/home/test/.local/bin/pyinstaller

sudo gedit ~/.bashrc
export PATH=$PATH:/home/test/.local/bin

source ~/.bashrc

# 使用
pyinstaller -F xx.py

```


<br/>

```python
# 安装时间相关的库
pip insall -U arrow

```


## main执行

具体执行命令：

```shell
python main.py -h
python main.py find -h
python main.py find -f .py -k main ./utils/clear_typora_photo/

```