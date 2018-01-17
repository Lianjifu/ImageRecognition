# -*-coding:utf-8-*-

# 进行图片训练
from PIL import Image, ImageEnhance
import os
import shutil


def deal_pic(path):
    file_names = os.listdir(path)
    for name in file_names:
        file_name = os.path.join(path, name)
        img = Image.open(file_name)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = img.convert('L')
        img = ImageEnhance.Contrast(img)
        img = img.enhance(1)
        img = img.point(lambda x: 0 if x < 230 else 255)
        #  left,top,right,bottom
        box = (85, 33, 157, 110)
        img = img.crop(box)
        # img.show()
        img.save(file_name)
        # print(img.size)


def press_key(num):
    file_names = os.listdir('../tu')
    for name in file_names:
        shutil.move('../tu/%s' % name, '../iconset/%s/' % num)
    deal_pic('../iconset/%s/' % num)


def main():
    num = int(input('请输入1-14中的数字\n'))
    if num == 1:
        press_key(num)
    elif num == 2:
        press_key(num)
    elif num == 3:
        press_key(num)
    elif num == 4:
        press_key(num)
    elif num == 5:
        press_key(num)
    elif num == 6:
        press_key(num)
    elif num == 7:
        press_key(num)
    elif num == 8:
        press_key(num)
    elif num == 9:
        press_key(num)
    elif num == 10:
        press_key(num)
    elif num == 11:
        press_key(num)
    elif num == 12:
        press_key(num)
    elif num == 13:
        press_key(num)
    elif num == 14:
        press_key(num)
    else:
        return False

if __name__ == '__main__':
    main()
    # deal_pic('../iconset/4/')
