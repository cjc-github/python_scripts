# coding=utf-8
import importlib
from execute_dynamic_method.scripts.demo1 import Demo1Class
from execute_dynamic_method.scripts.demo1 import hello2

"""
调用外部函数，即execute_dynamic_method/scripts/demo1文件中的 Demo1Class 类中的 hello1() 函数
module_name: execute_dynamic_method.scripts.demo1
class_name: Demo1Class
method_name: hello1
"""


# 方法1，调用某个文件中的类的函数
def run_execute_method1():
    class_name = "Demo1Class"
    method_name = "hello1"
    module_name = "execute_dynamic_method.scripts.demo1"

    # 方法1：
    result = execute_method(module_name, class_name, method_name)
    print(result)
    # 方法2：
    result = call_method(module_name, class_name, method_name)
    print(result)


# 模块名称，类名，函数名称
def call_method(module_name, class_name, method_name):
    # 使用import动态导入模块
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)
    # 创建类的实力
    instance = class_obj()
    # 获取方法对象并调用
    method_obj = getattr(instance, method_name)
    return method_obj()


# 模块名称，类名，函数名称
def execute_method(module_name, class_name, method_name):
    # 使用 __import__() 动态导入模块
    module = __import__(module_name, fromlist=[class_name])
    # 获取类对象
    class_obj = getattr(module, class_name)
    # 创建类实例
    instance = class_obj()
    # 获取方法对象并调用
    method_obj = getattr(instance, method_name)
    return method_obj()


"""
调用外部函数，即execute_dynamic_method/scripts/demo1文件中的 hello2() 函数
module_name: execute_dynamic_method.scripts.demo1
method_name: hello2
"""


# 方法2，调用某个文件中的类的函数
def run_execute_method2():
    method_name = "hello2"
    module_name = "execute_dynamic_method.scripts.demo1"

    result = call_dynamic_function(module_name, method_name)
    print(result)


# 模块名称，函数名称
def call_dynamic_function(module_name, function_name):
    module = importlib.import_module(module_name)
    function_obj = getattr(module, function_name)
    return function_obj()


if __name__ == "__main__":
    print("===== way 1: ======")
    run_execute_method1()
    print("\n\n===== way 2: ======")
    run_execute_method2()
    print("\n\n=====  直接执行 =====")
    print("===== way 3: ======")
    print(Demo1Class().hello1())
    print("\n\n===== way 4: ======")
    print(hello2())

