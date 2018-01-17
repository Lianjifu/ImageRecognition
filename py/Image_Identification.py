#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
__author__ = "lianjifu"
1. 本脚本为图像识别
2. 主要利用原理：向量空间模型(VSM)
3. 使用opencv 调用摄像头拍照并保存
"""

from PIL import Image, ImageEnhance
import math
import os
import time
import cv2

def listfiles(rootdir, prefix='.xml'):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    file.append(rootdir + filename)
            return file
        else:
            pass


# 使用余弦距离
class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                # 计算相乘的和
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


# 定义一个页码数
iconset = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

# 读取样本文件夹里的样本
imageset = []
for letter in iconset:
    for img in os.listdir('..\\iconset\\%s\\' % (letter)):
        temp = []
        if img != "":
            temp.append(buildvector(Image.open("..\\iconset\\%s\\%s" % (letter, img))))
        imageset.append({letter: temp})


# 捕获摄像头图像
def camera():
    path = "..\\tu\\"
    cap = cv2.VideoCapture(0)
    while(True):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        # 对时间字符转换
        time1 = str(int(time.time()))
        time1 = time1 + ".png"
        # 键盘按键处理
        # key = cv2.waitKey(1) & 0xFF
        # 在键盘上按下s键保存图片
            # if key == ord('s'):
        #     cv2.imwrite(os.path.join(path, time1), frame)
        #     break
        time.sleep(0.3)
        cv2.imwrite(os.path.join(path, time1), frame)
        break
        # 在键盘上按下q键退出
        # if key == ord('q'):
        #     break
    cap.release()
    cv2.destroyAllWindows()


# 主函数
def main(item):
    try:
        img = Image.open(item)
        # ANTIALIAS 平滑滤波， resize改变图像大小
        img = img.resize((200, 200), Image.ANTIALIAS)
        # 灰度处理
        img = img.convert('L')
        # 对比度增强
        img = ImageEnhance.Contrast(img)
        # 颜色增强
        img = img.enhance(1)
        img = img.point(lambda x: 0 if x < 220 else 255)
        # 对拍照的图片进行剪贴处理
        box = (85, 33, 157, 110)
        # 图片切割
        im2 = img.crop(box)
        # 图片展示
        # im2.show()

        # 找到切割的起始和结束的横坐标
        inletter = False

        foundletter = False
        start = 0
        end = 0

        letters = []

        for x in range(im2.size[0]):  # h
            for y in range(im2.size[1]):  # w
                pix = im2.getpixel((x, y))
                if pix != 255:
                    inletter = True
            if foundletter == False and inletter == True:
                foundletter = True
                start = x

            if foundletter == True and inletter == False:
                foundletter = False
                end = x
                letters.append((start, end))

            inletter = False
        # 获取训练集
        v = VectorCompare()
        guess = []
        # 将切割得到的小片段与每个训练片段进行比较
        for image in imageset:
            for x, y in image.items():
                if len(y) != 0:
                    guess.append((v.relation(y[0], buildvector(im2)), x))
        # 排序选出即cos值最大的向量，夹角越小则越接近重合，匹配越接近
        guess.sort(reverse=True)
        page = guess[0][1]
        print '=='
        print "", guess[0]
        # return page
        # 当夹角度大于0.81时 输出相应的页码
        if guess[0][0] > 0.81:
            # newjpgname.append(guess[0][1])
            print "此页是第%s页" % page
        else:
            print '请重新放入护照'

    except Exception as err:
        print(err)
        # 如果错误就记录下来
        file = open("..\\error.txt", "a")
        file.write("\n" + item)
        file.close()

if __name__ == '__main__':
    # 单个图测试
    # main('../tu/c1_1.png')
    # 调用摄像头并拍照保存
    camera()
    # 从文件夹中读取图片
    path = "..\\tu\\"
    jpgname = listfiles(path, 'png')
    for item in jpgname:
        main(item)

    # 延时删除图片
    # time.sleep(0.1)
    # os.remove(item)
