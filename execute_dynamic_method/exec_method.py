# coding=utf-8
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


if __name__ == "__main__":
    class_name = "demo1"
    method_name = "hello1"
    module_name = "execute_dynamic_method.scripts." + class_name

    result = execute_method(module_name, class_name, method_name)
    print(result)
