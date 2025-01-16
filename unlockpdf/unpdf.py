import threading
import tkinter as tk
from tkinter import ttk
import pikepdf
import os

import easygui


def unlock_pdf(root_dir_path):
    # 隐藏按钮
    start_button.pack_forget()
    # 更新状态标签
    status_label.config(text="任务开始...")
    progress_bar.pack(padx=10,pady=20)

    # 循环读取
    for root, dirs, files in os.walk(root_dir_path):
        dir_name = os.path.basename(root)  # 获取当前目录名

        # progress_var.set(0)  # 更新进度条值

        # 完成数统计
        finish_file_num = 0
        total_num = len(files)

        # 新建输出文件夹
        out_dir_path_str = root_dir_path + '\\unlock\\' + dir_name
        if not os.path.exists(out_dir_path_str):
            os.makedirs(out_dir_path_str)

        for file in files:
            file_full_path = os.path.join(root, file)
            # 用pikepdf破解，并以unlocked.pdf保存在当前程序所在路径下
            pdf = pikepdf.open(file_full_path, allow_overwriting_input=True)
            new_file_name = os.path.join(out_dir_path_str, file)
            pdf.save(new_file_name)

            finish_file_num = finish_file_num + 1
            progress_var.set(finish_file_num / total_num * 100)  # 更新进度条值
            # 刷新界面
            progress_gui.update_idletasks()

    # 任务完成后恢复按钮并更新文本
    status_label.config(text="任务完成！")
    progress_gui.update_idletasks()


def start_task():
    thread = threading.Thread(target=unlock_pdf, args=(root_dir_path,))
    thread.daemon = True  # 设置为守护线程，主程序退出时子线程会自动退出
    thread.start()


if __name__ == '__main__':

    # 选择文件路径 - 历史遗留懒得改了
    root_dir_path = easygui.diropenbox(msg='选择文件夹', title='浏览文件夹')

    # 创建进度条窗口
    progress_gui = tk.Tk()

    # 窗口的宽度和高度
    window_width = 400
    window_height = 200

    # 获取屏幕的宽度和高度
    screen_width = progress_gui.winfo_screenwidth()
    screen_height = progress_gui.winfo_screenheight()

    # 计算窗口在屏幕中心的位置
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    # 设置窗口的大小和位置
    progress_gui.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # 设置窗口标题
    progress_gui.title("开始处理文件夹：")

    # 进度条变量
    progress_var = tk.DoubleVar()

    # 创建进度条
    progress_bar = ttk.Progressbar(progress_gui, orient="horizontal", length=300, mode="determinate",
                                   variable=progress_var)


    # 创建状态标签，用于显示任务状态
    status_label = tk.Label(progress_gui, text="等待任务开始...", font=("Arial", 12))
    status_label.pack(padx=10,pady=20)

    # 创建状态标签，用于显示任务状态
    status_label = tk.Label(progress_gui, text="已选文件夹：" + root_dir_path, font=("Arial", 12))
    status_label.pack(padx=2,pady=20)

    # 创建按钮，点击后开始更新进度条
    start_button = tk.Button(progress_gui, text="开始任务", command=start_task, width=30, height=2)
    start_button.pack(padx=10,pady=20)

    progress_gui.mainloop()
