from execute_dynamic_method.scripts.demo2 import hello2
import importlib


def call_dynamic_function(module_name, function_name):
    module = importlib.import_module(module_name)
    function_obj = getattr(module, function_name)
    return function_obj()


if __name__ == "__main__":
    module_name = "execute_dynamic_method.scripts.demo2"
    function_name = "hello2"

    result = call_dynamic_function(module_name, function_name)
    print("way 1:", result)

    print("way 2:", hello2())
