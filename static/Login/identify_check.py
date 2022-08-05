# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/14
# file:identify_check.py

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random


# 定义随机的颜色
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 确定随机数
def random_pic():
    s = '0123456789abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY'
    size = (130, 30)
    # 创建画布
    img = Image.new('RGB', size, color=random_color())
    # 创建样式
    font = ImageFont.truetype(font="fonts\simhei.ttf", size=35)
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 绘制验证码
    code = ''
    for i in range(4):
        c = random.choice(s)
        code += c
        draw.text((random.randint(5, 7) + 35 * i, random.randint(-8, -3)), text=c, font=font, fill=random_color())
    # 加入六条干扰线

    for i in range(6):
        x = random.randint(0, 100)
        y = random.randint(0, 10)
        x1 = random.randint(30, 100) + 10
        y1 = random.randint(7, 25)
        draw.line(((x, y), (x1, y1)), fill=random_color())
    img.filter(ImageFilter.EDGE_ENHANCE)
    return img, code
