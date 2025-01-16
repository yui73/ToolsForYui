# coding=utf-8
# 多个pdf合并
import easygui
import sys
import os
from PyPDF2 import PdfReader, PdfMerger, PdfWriter
import logging
import    json

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
        for file in files:
            file_full_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            # 后缀pdf的插入字典，key为dir，value为文件名
            if file_ext == '.pdf':
                if dir_name not in pdf_obj:
                    pdf_obj[dir_name] = []  # 如果目录名不在字典中，初始化为空列表
                pdf_obj[dir_name].append(file_full_path)


    return pdf_obj


def format_pdf_list(root_dir_path):
    """
    逻辑出所有的pdf文件
    :param root_dir_path:
    :return:
    """
    pdf_obj = {}
    return traverse_pdf(pdf_obj, root_dir_path)


def merge_pdf(pdf_list, root_dir_path,is_need_title_page):


    logging.info('开始遍历单元数据%s', json.dumps(pdf_list, ensure_ascii=False))

    for key in pdf_list:
        merger = PdfMerger()
        # 进度条
        print("正在读取", key+":")

        done = 0
        total = len(pdf_list[key])

        if total == 0 :
            print("文件夹"+key+"为空！")
            continue


        for file_path in pdf_list[key]:

            f = open(file_path, 'rb')
            file_rd = PdfReader(f)
            # 尝试读取文件的页数，如果文件有效，将返回页数
            if len(file_rd.pages) <= 0:
                print("文件读取失败")
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
            print(done/total * 100)



        filename = key+".pdf"
        # 文件夹名做合并后文件名
        out_file_path = str(os.path.join(os.path.abspath(root_dir_path), filename))

        merger.write(out_file_path)
        # logging.info('合并后输出文件：%s', out_file_path)
        merger.close()
        print("完成合并：", key)

    easygui.msgbox('恭喜合并成功，成功合并')



if __name__ == '__main__':

    '''
    选择所有pdf所在的文件的根目录
    '''
    root_dir_path = easygui.diropenbox(msg='选择根文件夹', title='浏览文件夹')

    if root_dir_path is None:
        easygui.msgbox('未选择根目录没法处理哦', title='提示')
        sys.exit()

    logging.info('选择的根目录是 %s ', root_dir_path)

    '''
    1.遍历及整理名字类似的PDF文件
    '''
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
    merge_pdf(pdf_list, root_dir_path + '\\out',True)
