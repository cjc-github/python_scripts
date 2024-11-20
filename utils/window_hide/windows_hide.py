import tkinter as tk
from tkinter import ttk

import win32gui
import win32process
import win32con
import psutil
import keyboard
# pip install keyboard

class WindowController:
    def __init__(self, root):
        self.root = root
        self.root.title("窗口隐藏工具v1.3")
        self.root.geometry("300x150")

        self.original_styles = {}  # 存储窗口原始样式的字典
        self.is_visible = True  # 主窗口可见性标志

        self.create_widgets()  # 创建图形界面组件

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # 绑定窗口关闭事件

        self.root.bind("<Unmap>", self.on_minimize)  # 覆盖默认的最小化行为

        self.update_process_list()  # 更新进程列表

        # 设置全局热键
        keyboard.add_hotkey('ctrl+alt+h', self.toggle_window)

    def create_widgets(self):
        # 创建进程选择标签
        self.process_label = tk.Label(self.root, text="选择进程:")
        self.process_label.pack()

        # 创建进程选择下拉列表
        self.process_dropdown = ttk.Combobox(self.root, state='readonly')
        self.process_dropdown.pack()

        # 创建隐藏按钮
        self.hide_button = tk.Button(self.root, text="隐藏", command=self.hide_process)
        self.hide_button.pack()

        # 创建恢复按钮
        self.restore_button = tk.Button(self.root, text="恢复", command=self.restore_process)
        self.restore_button.pack()

        # 创建刷新进程列表按钮
        self.refresh_button = tk.Button(self.root, text="刷新进程列表", command=self.update_process_list)
        self.refresh_button.pack()

        # 设置快捷键
        keyboard.add_hotkey('ctrl+z', self.hide_process)
        keyboard.add_hotkey('ctrl+x', self.restore_process)

    def toggle_window(self):
        # 切换主窗口可见性
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
        else:
            self.root.deiconify()
            self.root.focus_force()
            self.is_visible = True

    def on_close(self):
        # 处理窗口关闭事件
        self.root.withdraw()
        self.is_visible = False

    def on_minimize(self, event):
        # 处理窗口最小化事件
        self.root.withdraw()
        self.is_visible = False

    def update_process_list(self):
        # 更新进程列表
        processes = [proc.name() for proc in psutil.process_iter(['pid', 'name'])]
        self.process_dropdown['values'] = list(set(processes))

    def hide_windows(self, process_name):
        # 隐藏指定进程的所有窗口
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.name() == process_name:
                pid = proc.info['pid']
                self.hide_windows_by_pid(pid)

    def hide_windows_by_pid(self, pid):
        # 隐藏指定进程ID的所有窗口
        def callback(hwnd, whdls):
            if win32gui.IsWindowVisible(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    whdls.append(hwnd)
                    self.original_styles[hwnd] = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    win32gui.ShowWindow(hwnd, 0)
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, self.original_styles[hwnd] & ~win32con.WS_VISIBLE)

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)

    def restore_windows(self, process_name):
        # 恢复指定进程的所有窗口
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.name() == process_name:
                pid = proc.info['pid']
                self.restore_windows_by_pid(pid)

    def restore_windows_by_pid(self, pid):
        # 恢复指定进程ID的所有窗口
        def callback(hwnd, _):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                original_style = self.original_styles.get(hwnd, None)
                if original_style is not None:
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, original_style)
                    # 强制窗口显示并获得焦点
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    win32gui.SetForegroundWindow(hwnd)
                    # 更新窗口状态
                    win32gui.RedrawWindow(hwnd, None, None,
                                          win32con.RDW_INVALIDATE | win32con.RDW_UPDATENOW | win32con.RDW_ALLCHILDREN)

        win32gui.EnumWindows(callback, None)

        win32gui.EnumWindows(callback, None)

    def hide_process(self):
        # 隐藏选定进程的窗口
        process_name = self.process_dropdown.get()
        if process_name:
            self.hide_windows(process_name)

    def restore_process(self):
        # 恢复选定进程的窗口
        process_name = self.process_dropdown.get()
        if process_name:
            self.restore_windows(process_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = WindowController(root)
    root.mainloop()
