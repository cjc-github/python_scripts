import unicodedata

ident = " " * 2
key_width = 20

# 列表
dic = [
    'apple', 'banana', 'orange', 'grape', 'kiwi',
    'mango', 'pineapple', 'strawberry', 'blueberry',
    'watermelon', 'peach', 'plum', 'cherry', 'papaya', 'pomegranate'
]

# 带中文的列表
fruits = [
    'apple (苹果)', 'banana (香蕉)', 'orange (橙子)', 'grape (葡萄)',
    'kiwi (猕猴桃)', 'mango (芒果)', 'pineapple (菠萝)', 'strawberry (草莓)',
    'blueberry (蓝莓)', 'watermelon (西瓜)', 'peach (桃子)', 'plum (李子)',
    'cherry (樱桃)', 'papaya (木瓜)', 'pomegranate (石榴)'
]


# 对英文字符串的格式化
def format_str():
    # 使用<: 字符串居左
    def format1():
        for i in dic:
            print(f"{ident} {i:<{key_width}} :")

    # 计算最大值 + 使用<: 字符串居左
    def format2():
        for i in dic:
            print(f"{ident} {i:<{max_key_length}} :")

    # 计算最大值 + 使用^: 字符串居中
    def format3():
        for i in dic:
            print(f"{ident} {i:^{max_key_length}} :")

    # 计算最大值 + 使用center: 字符串居中
    def format4():
        for i in dic:
            print(f"{ident} {i.center(max_key_length, ' ')} :")

    # 计算最大值 + 使用ljust: 字符串居左
    def format5():
        for i in dic:
            print(f"{ident} {i.ljust(max_key_length, ' ')} : ")

    # 计算最大值 + 使用>: 字符串居右
    def format6():
        for i in dic:
            print(f"{ident} {i:>{max_key_length}} :")

    max_key_length = max(len(i) for i in dic)

    formats = [("format1", format1),
               ("format2", format2),
               ("format3", format3),
               ("format4", format4),
               ("format5", format5),
               ("format6", format6)]

    for name, func in formats:
        print(name)
        func()


# 对于format_str的简化
def format_str_simple():
    max_key_length = max(len(i) for i in dic)

    # 定义一个格式化函数
    def format_fruits(fmt):
        for i in dic:
            print(f"{ident} {fmt(i, max_key_length)} :")

    # 映射格式化方法
    format_methods = {
        'format1': lambda x, width: f"{x:<{width}}",
        'format2': lambda x, width: f"{x:<{max_key_length}}",
        'format3': lambda x, width: f"{x:^{width}}",
        'format4': lambda x, width: x.center(width, ' '),
        'format5': lambda x, width: x.ljust(width, ' '),
        'format6': lambda x, width: f"{x:>{width}}"
    }

    # 输出各种格式
    for name, method in format_methods.items():
        print(name)
        format_fruits(method)


# 格式化带中文的字符串
def format_unicode_str():
    """计算字符串的实际显示宽度，包括中文字符"""

    def adjusted_length(s):
        # sum = 0
        # for c in s:
        #     if unicodedata.east_asian_width(c) in 'WF':
        #         sum += 2
        #     else:
        #         sum += 1
        # return sum
        return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)

    """使用空格来填充"""

    def format1():
        for s in fruits:
            # 使用空格填充
            print(s, " " * (max_length - adjusted_length(s)), ":")  # 使用空格填充

    max_length = max(adjusted_length(s) for s in fruits)
    format1()


# main()
if __name__ == "__main__":
    # 格式化字符串
    # format_str()
    # format_str_simple()

    # 格式化带中文的字符串
    format_unicode_str()
