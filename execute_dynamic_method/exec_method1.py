# coding=utf-8
import importlib


def call_method(module_name, class_name, method_name):
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)
    instance = class_obj()
    method_obj = getattr(instance, method_name)
    return method_obj()


if __name__ == "__main__":
    class_name = "demo1"
    method_name = "hello1"
    module_name = "execute_dynamic_method.scripts." + class_name
    # 使用示例
    result = call_method(module_name, class_name, method_name)
    print(result)
