# coding=utf-8
# 多个pdf合并
import easygui
import sys
import os
from PyPDF2 import PdfReader, PdfMerger, PdfWriter
import logging
import json
import threading
import tkinter as tk
from tkinter import ttk

from mergepdf.tool.tools_for_pdf import create_title_page

'''
复杂模式：根据文件夹进行pdf合并，同一文件夹下的pdf合并到一起，文件名为文件夹名，统一放到根目录OUT文件夹里
'''

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='merger_pdf.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def traverse_pdf(pdf_obj, root_dir_path):


    for root, dirs, files in os.walk(root_dir_path):
        dir_name = os.path.basename(root)  # 获取当前目录名
        # 更新状态标签
        status_label1.config(text="整理<"+dir_name+">文件夹开始...")
        progress_var.set(0.00)

        # 完成数统计
        finish_file_num = 0
        total_num = len(files)

        for file in files:
            file_full_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            # 后缀pdf的插入字典，key为dir，value为文件名
            if file_ext == '.pdf':
                if dir_name not in pdf_obj:
                    pdf_obj[dir_name] = []  # 如果目录名不在字典中，初始化为空列表
                pdf_obj[dir_name].append(file_full_path)

            finish_file_num = finish_file_num + 1
            progress_var.set(finish_file_num / total_num * 100)  # 更新进度条值
            # 刷新界面
            progress_gui.update_idletasks()

    return pdf_obj


def format_pdf_list(root_dir_path):
    """
    逻辑出所有的pdf文件
    :param root_dir_path:
    :return:
    """
    pdf_obj = {}
    return traverse_pdf(pdf_obj, root_dir_path)


def merge_pdf(pdf_list, root_dir_path, is_need_title_page):
    logging.info('开始遍历单元数据%s', json.dumps(pdf_list, ensure_ascii=False))



    for key in pdf_list:

        # 更新状态标签
        status_label2.pack_forget()
        status_label1.config(text="合并<"+key+">文件夹开始...")
        progress_var.set(0.00)

        merger = PdfMerger()
        # 进度条
        print("正在读取", key + ":")

        # 完成数统计
        done = 0
        total = len(pdf_list[key])

        if total == 0:
            print("文件夹" + key + "为空！")
            continue

        for file_path in pdf_list[key]:

            f = open(file_path, 'rb')
            file_rd = PdfReader(f)
            # 尝试读取文件的页数，如果文件有效，将返回页数
            if len(file_rd.pages) <= 0:
                easygui.msgbox("文件读取失败")
                logging.warning('文件读取失败：', file_path)
                continue
            if file_rd.is_encrypted:
                logging.warning('不支持加密后的文件: %s', file_path)
                continue

            if is_need_title_page:
                # 新增文件标题页
                # 创建标题页
                title_page = create_title_page(os.path.splitext(os.path.basename(file_path))[0])

                # 作为一个单独的pdf merge进去
                merger.append(title_page)

            merger.append(file_rd)
            logging.info('开始合并文件：%s', file_path)
            f.close()

            # 更新进度条
            done = done + 1
            print(done / total * 100)

            progress_var.set(done / total * 100)  # 更新进度条值
            # 刷新界面
            progress_gui.update_idletasks()

        filename = key + ".pdf"
        # 文件夹名做合并后文件名
        out_file_path = str(os.path.join(os.path.abspath(root_dir_path), filename))

        merger.write(out_file_path)
        # logging.info('合并后输出文件：%s', out_file_path)
        merger.close()
        # 更新状态标签
        status_label1.config(text="合并<"+key+">文件夹完成！")
        print("完成合并：", key)


    status_label1.config(text="合并文件夹完成！")
    # easygui.msgbox('恭喜合并成功，成功合并')


def start_combine(root_dir_path):

    # 隐藏按钮
    start_button.pack_forget()
    progress_bar.pack(padx=10,pady=20)

    """
    遍历及整理名字类似的PDF文件
    """
    logging.info('开始整理PDF文件')
    pdf_list = format_pdf_list(root_dir_path)
    if pdf_list is None:
        easygui.msgbox('警告', '未找到符合条件的PDF')
        sys.exit()
    logging.info('整理之后的PDF文件是 %s ', json.dumps(pdf_list, ensure_ascii=False))

    out_path_str = root_dir_path + '\\out'
    if not os.path.exists(out_path_str):
        os.makedirs(out_path_str)

    '''
    遍历组织好的拼接一下
    '''
    merge_pdf(pdf_list, root_dir_path + '\\out', True)


def start_task():
    thread = threading.Thread(target=start_combine, args=(root_dir_path,))
    thread.daemon = True  # 设置为守护线程，主程序退出时子线程会自动退出
    thread.start()


if __name__ == '__main__':

    '''
    选择所有pdf所在的文件的根目录，历史遗留懒得改了
    '''
    root_dir_path = easygui.diropenbox(msg='选择根文件夹', title='浏览文件夹')

    if root_dir_path is None:
        easygui.msgbox('未选择根目录没法处理哦', title='提示')
        sys.exit()

    logging.info('选择的根目录是 %s ', root_dir_path)

    '''
    1.渲染可视化窗口
    '''

    # 创建进度条窗口
    progress_gui = tk.Tk()

    # 窗口的宽度和高度
    window_width = 600
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
    status_label1 = tk.Label(progress_gui, text="等待任务开始...", font=("Arial", 12))
    status_label1.pack(padx=10, pady=20)

    # 创建状态标签，用于显示任务状态
    status_label2 = tk.Label(progress_gui, text="已选文件夹：" + root_dir_path, font=("Arial", 12))
    status_label2.pack(padx=2, pady=20)

    # 创建按钮，点击后开始更新进度条
    start_button = tk.Button(progress_gui, text="开始任务", command=start_task, width=30, height=2)
    start_button.pack(padx=10, pady=20)

    progress_gui.mainloop()
