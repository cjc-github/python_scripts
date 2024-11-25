import re


"""
替换文件中的中文标点符号

功能：
1、发现存在中文标点符号的文件
2、替换
3、针对没有获取的中文标点符号, 需要进行修改
"""

def replace_punctuation(text):
    # 定义中文标点和对应的英文标点
    punctuation_mapping = {
        '，': ', ',  # 逗号
        '。': '.',  # 句号
        '！': '!',  # 感叹号
        '？': '?',  # 问号
        '；': ';',  # 分号
        '：': ':',  # 冒号
        '“': '"',   # 左双引号
        '”': '"',   # 右双引号
        '‘': "'",   # 左单引号
        '’': "'",   # 右单引号
        '（': '(',   # 左圆括号
        '）': ')',   # 右圆括号
        '【': '[',   # 左方括号
        '】': ']',   # 右方括号
        '《': '<',   # 左书名号
        '》': '>',   # 右书名号
        '…': '...'  # 省略号
    }

    # 替换中文标点为英文标点
    for chinese_punctuation, english_punctuation in punctuation_mapping.items():
        text = text.replace(chinese_punctuation, english_punctuation)

    return text


if __name__ == "__main__":
    # 示例文本
    document_text = "这是一个示例文本，包含中文标点：例如“引号”、（括号）和其他内容！"

    # 替换标点
    result_text = replace_punctuation(document_text)

    print(result_text)