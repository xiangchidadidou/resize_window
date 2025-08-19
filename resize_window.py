import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import win32con

class WindowResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("窗口大小调整器")
        self.root.geometry("400x300")

        self.create_widgets()
        self.populate_windows()

    def create_widgets(self):
        # 窗口选择
        ttk.Label(self.root, text="选择窗口:").pack(pady=5)
        self.window_combobox = ttk.Combobox(self.root, state="readonly", width=50)
        self.window_combobox.pack(pady=5)
        self.window_combobox.bind("<<ComboboxSelected>>", self.on_window_selected)

        # 刷新按钮
        ttk.Button(self.root, text="刷新窗口列表", command=self.populate_windows).pack(pady=5)

        # 尺寸输入
        ttk.Label(self.root, text="新宽度:").pack(pady=5)
        self.width_entry = ttk.Entry(self.root)
        self.width_entry.pack(pady=5)

        ttk.Label(self.root, text="新高度:").pack(pady=5)
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.pack(pady=5)

        # 调整按钮
        ttk.Button(self.root, text="调整窗口大小", command=self.resize_selected_window).pack(pady=10)

    def populate_windows(self):
        # 获取所有可见窗口
        self.windows = {}
        win32gui.EnumWindows(self.enum_windows_callback, None)
        
        # 过滤掉没有标题的窗口和自身窗口
        display_names = [name for name in self.windows.keys() if name and name != self.root.title()]
        self.window_combobox['values'] = sorted(display_names)
        if display_names:
            self.window_combobox.set(display_names[0])
            self.selected_hwnd = self.windows[display_names[0]]
        else:
            self.window_combobox.set("")
            self.selected_hwnd = None

    def enum_windows_callback(self, hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
            self.windows[win32gui.GetWindowText(hwnd)] = hwnd

    def on_window_selected(self, event):
        selected_name = self.window_combobox.get()
        self.selected_hwnd = self.windows.get(selected_name)

    def resize_selected_window(self):
        if not self.selected_hwnd:
            messagebox.showwarning("警告", "请先选择一个窗口！")
            return

        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
        except ValueError:
            messagebox.showerror("错误", "宽度和高度必须是整数！")
            return

        if new_width <= 0 or new_height <= 0:
            messagebox.showwarning("警告", "宽度和高度必须大于0！")
            return

        # 获取当前窗口位置和大小
        x, y, w, h = win32gui.GetWindowRect(self.selected_hwnd)

        # 尝试调整窗口大小
        try:
            win32gui.MoveWindow(self.selected_hwnd, x, y, new_width, new_height, True)
            messagebox.showinfo("成功", f"窗口已调整为 {new_width}x{new_height}")
        except Exception as e:
            messagebox.showerror("错误", f"调整窗口大小失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowResizerApp(root)
    root.mainloop()