# 创建包含标题的新页面 PDF
import os
from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab import pdfbase
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfbase import pdfmetrics

def create_title_page(title):
    # 创建一个内存中的 PDF 文件
    packet = BytesIO()
    c = canvas.Canvas(packet,page_size=A4)

    font_path = 'SimHei.ttf'  # Specify the path to a Chinese font
    if not os.path.exists(font_path):
        print(f"字体文件不存在：{font_path}")

    pdfmetrics.registerFont(TTFont('SimHei', font_path))


    # print("Registered fonts:", pdfmetrics.getRegisteredFontNames())

    c.setFont('SimHei', 20)
    c.drawString(50, 750, title)  # 将标题绘制到页面上
    c.save()

    # 将生成的 PDF 数据从内存中读取到 PdfReader
    packet.seek(0)
    new_pdf = PdfReader(packet)
    return new_pdf